"""Éléments dessinés par-dessus les pages : symboles, traits, fils, murs, cotes, textes, images, champs."""
import base64
import math

from PySide6.QtCore import QByteArray, QPointF, QRectF, Qt
from PySide6.QtGui import (QBrush, QColor, QFont, QFontMetricsF, QImage, QPainterPath, QPen,
                           QPolygonF, QTransform)
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QGraphicsItem

from .symbols import BY_ID

MM = 72 / 25.4                 # points par millimètre
GRID_UNIT = 2.5 * MM / 10      # 10 unités de symbole = 2,5 mm
POLY_TYPES = ("line", "wire", "wall", "freehand", "highlight", "dim")
FIELD_TYPES = ("field_text", "field_check", "field_combo", "field_radio", "field_sig", "field_link")
BOX_TYPES = ("rect", "ellipse", "image", "node") + FIELD_TYPES

_svg_cache = {}
_img_cache = {}


def pts_per_cm(denom):
    """Points papier pour 1 cm réel à l'échelle 1/denom."""
    return 10 * MM / denom


def text_font(size, bold=False, family="Helvetica", italic=False, underline=False):
    f = QFont(family or "Helvetica")
    f.setPixelSize(100)
    f.setBold(bold)
    f.setItalic(italic)
    f.setUnderline(underline)
    return f


def rich_segments(line):
    """Découpe une ligne : texte normal et racines √{...} (la barre couvre tout le contenu)."""
    out, i = [], 0
    while True:
        j = line.find("√{", i)
        if j < 0:
            out.append(("n", line[i:]))
            return [x for x in out if x[1]]
        k = line.find("}", j)
        if k < 0:
            out.append(("n", line[i:]))
            return [x for x in out if x[1]]
        out.append(("n", line[i:j]))
        out.append(("s", line[j + 2:k]))
        i = k + 1


def rich_width(fm, line):
    w = 0.0
    for kind, txt in rich_segments(line):
        w += fm.horizontalAdvance(txt) + (fm.height() * 0.62 if kind == "s" else 0)
    return w


def draw_rich(p, fm, x, base, line):
    for kind, txt in rich_segments(line):
        if kind == "n":
            p.drawText(QPointF(x, base), txt)
            x += fm.horizontalAdvance(txt)
        else:
            e = fm.height()
            a = fm.ascent()
            inner = fm.horizontalAdvance(txt)
            top = base - a * 0.95
            path = QPainterPath(QPointF(x, base - a * 0.38))
            path.lineTo(x + e * 0.1, base - a * 0.46)
            path.lineTo(x + e * 0.24, base + fm.descent() * 0.25)
            path.lineTo(x + e * 0.44, top)
            path.lineTo(x + e * 0.5 + inner + e * 0.08, top)
            pen = QPen(p.pen().color(), max(4.0, e * 0.055))
            pen.setJoinStyle(Qt.RoundJoin)
            pen.setCapStyle(Qt.RoundCap)
            p.save()
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            p.drawPath(path)
            p.restore()
            p.drawText(QPointF(x + e * 0.52, base), txt)
            x += inner + e * 0.62
    return x


def item_font(d):
    return text_font(d.get("size", 10), d.get("bold", False), d.get("font", "Helvetica"),
                     d.get("italic", False), d.get("underline", False))


class PItem(QGraphicsItem):
    def __init__(self, d):
        super().__init__()
        self.d = dict(d)
        self.d.setdefault("angle", 0.0)
        self.d.setdefault("fh", False)
        self.d.setdefault("fv", False)
        self.d.setdefault("color", "#000000")
        self.d.setdefault("sw", 1.0)
        if not self.d.get("uid"):
            import uuid
            self.d["uid"] = uuid.uuid4().hex[:10]
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable
                      | QGraphicsItem.ItemSendsGeometryChanges)
        self.setPos(self.d.get("x", 0), self.d.get("y", 0))
        self.setZValue(self.d.get("z", 1))
        self._br = QRectF()
        self.update_geom()

    # ------------------------------------------------------------ géométrie
    @property
    def typ(self):
        return self.d["type"]

    def plan_denom(self):
        s = self.scene()
        return getattr(s, "plan_denom", 50) if s else 50

    def sym(self):
        return BY_ID.get(self.d.get("sym"))

    def sym_unit(self):
        s = self.sym()
        base = pts_per_cm(self.plan_denom()) if s and s.kind == "real" else GRID_UNIT
        return base * self.d.get("scale", 1.0)

    def local_rect(self):
        t = self.typ
        if t == "symbol":
            s = self.sym()
            if not s:
                return QRectF(0, 0, 20, 20)
            w, h, _ = s.geometry(self.d.get("params"))
            u = self.sym_unit()
            return QRectF(0, 0, w * u, h * u)
        if t in BOX_TYPES:
            return QRectF(0, 0, self.d.get("w", 50), self.d.get("h", 30))
        if t == "text":
            return self.text_rect()
        pts = self.points()
        if not pts:
            return QRectF(0, 0, 1, 1)
        xs = [p.x() for p in pts]
        ys = [p.y() for p in pts]
        return QRectF(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

    def points(self):
        return [QPointF(x, y) for x, y in self.d.get("pts", [])]

    def text_rect(self):
        size = self.d.get("size", 10)
        fm = QFontMetricsF(item_font(self.d))
        lines = (self.d.get("text") or " ").split("\n")
        k = size / 100
        w = max(rich_width(fm, l) for l in lines) * k
        h = fm.lineSpacing() * len(lines) * k
        return QRectF(0, 0, max(w, 2), h)

    def apply_transform(self):
        c = self.local_rect().center()
        t = QTransform()
        t.translate(c.x(), c.y())
        t.rotate(-self.d["angle"])   # angle compté dans le sens trigonométrique
        t.scale(-1 if self.d["fh"] else 1, -1 if self.d["fv"] else 1)
        t.translate(-c.x(), -c.y())
        self.setTransform(t)

    def update_geom(self):
        self.prepareGeometryChange()
        r = self.local_rect()
        pad = self.d.get("sw", 1) * 2 + 2 + (10 if self.d.get("plugs") else 0)
        if self.typ == "wall":
            pad += self.d.get("thick", 20) * pts_per_cm(self.plan_denom()) / 2
        if self.typ == "highlight":
            pad += self.d.get("sw", 10) / 2
        if self.typ == "dim":
            pad += 14
        if self.typ == "line" and self.d.get("arrow", "none") != "none":
            pad += 8
        self._br = r.adjusted(-pad, -pad, pad, pad)
        self.apply_transform()
        lab = self.label_rect_local()
        if lab is not None:
            self._br = self._br.united(lab)
        if self.typ == "node":
            self._br = self._br.united(self.node_extra_rect().adjusted(-3, -3, 3, 3))
        self.update()

    def boundingRect(self):
        return self._br

    def shape(self):
        p = QPainterPath()
        if self.typ in POLY_TYPES:
            path = QPainterPath()
            pts = self.points()
            if self.typ == "wire":
                path, _ = self.wire_path()
            elif pts:
                path.moveTo(pts[0])
                for q in pts[1:]:
                    path.lineTo(q)
            from PySide6.QtGui import QPainterPathStroker
            st = QPainterPathStroker()
            w = 8
            if self.typ == "wall":
                w = max(8, self.d.get("thick", 20) * pts_per_cm(self.plan_denom()))
            if self.typ == "highlight":
                w = self.d.get("sw", 10)
            st.setWidth(w)
            return st.createStroke(path)
        p.addRect(self.local_rect().adjusted(-2, -2, 2, 2))
        return p

    # ------------------------------------------------------------ repère (étiquette non tournée)
    def label_frame(self):
        """Repère d'étiquette : coordonnées 'pos' sans rotation."""
        return self.transform().mapRect(self.local_rect())

    def pin_labels(self):
        """Numéros de bornes (A1, A2, 13, 14…) placés près de chaque borne, toujours horizontaux."""
        s = self.sym() if self.typ == "symbol" else None
        names = (self.d.get("pins") or "").split()
        if not s or not s.pins or not names:
            return []
        u = self.sym_unit()
        tr = self.transform()
        fc = tr.map(self.local_rect().center())
        fs = self.d.get("label_size", 7) * 0.8
        fm = QFontMetricsF(text_font(fs))
        out = []
        for (px, py), name in zip(s.pins, names):
            fp = tr.map(QPointF(px * u, py * u))
            dx, dy = fp.x() - fc.x(), fp.y() - fc.y()
            w = fm.horizontalAdvance(name) * fs / 100
            h = fm.height() * fs / 100
            if abs(dx) >= abs(dy):      # borne à gauche / à droite : numéro au-dessus du fil
                x = fp.x() + 1 if dx < 0 else fp.x() - 1 - w
                y = fp.y() - h - 0.3
            else:                       # borne en haut / en bas : numéro à droite du fil
                x = fp.x() + 1.5
                y = fp.y() + 0.3 if dy < 0 else fp.y() - h - 0.3
            out.append((name, QRectF(x, y, w, h), fs))
        return out

    def label_rect_local(self):
        if self.typ != "symbol":
            return None
        inv, _ = self.transform().inverted()
        res = None
        for _, r, _ in self.pin_labels():
            rr = inv.mapRect(r).adjusted(-2, -2, 2, 2)
            res = rr if res is None else res.united(rr)
        lab = self.d.get("label")
        if not lab:
            self._label_rect = None
            return res
        r = self.label_frame()
        fs = self.d.get("label_size", 7)
        fm = QFontMetricsF(text_font(fs, True))
        w = fm.horizontalAdvance(lab) * fs / 100
        h = fm.height() * fs / 100
        pos = self.d.get("label_pos", "auto")
        if pos == "auto":
            # fils horizontaux -> repère au-dessus ; fils verticaux -> repère à gauche
            s = self.sym()
            pos = "haut"
            if s and len(s.pins) >= 2:
                # fils plutôt verticaux (bornes en haut / en bas) -> repère à gauche
                tr = self.transform()
                u = self.sym_unit()
                c = tr.map(self.local_rect().center())
                dx = dy = 0.0
                for (px, py) in s.pins:
                    q = tr.map(QPointF(px * u, py * u))
                    dx += abs(q.x() - c.x())
                    dy += abs(q.y() - c.y())
                if dy > dx:
                    pos = "gauche"
        if pos == "droite":
            lr = QRectF(r.right() + 2, r.center().y() - h / 2, w, h)
        elif pos == "gauche":
            lr = QRectF(r.left() - 2 - w, r.center().y() - h / 2, w, h)
        elif pos == "bas":
            lr = QRectF(r.center().x() - w / 2, r.bottom() + 1, w, h)
        else:
            lr = QRectF(r.center().x() - w / 2, r.top() - 1 - h, w, h)
        self._label_rect = lr
        lr2 = inv.mapRect(lr).adjusted(-2, -2, 2, 2)
        return lr2 if res is None else res.united(lr2)

    # ------------------------------------------------------------ déplacement aimanté
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            s = self.scene()
            if getattr(s, "snap", False) and not getattr(s, "no_snap", False):
                g = s.grid_step
                return QPointF(round(value.x() / g) * g, round(value.y() / g) * g)
        if change == QGraphicsItem.ItemPositionHasChanged and self.scene():
            cb = getattr(self.scene(), "on_moved", None)
            if cb and self.typ in ("symbol", "node") and not getattr(self, "is_temp", False):
                cb(self)
        return super().itemChange(change, value)

    # ------------------------------------------------------------ bornes de connexion
    def pins_scene(self):
        """Points de connexion en coordonnées de scène (centre pour les symboles de plan)."""
        if self.typ == "node":
            return [self.mapToScene(q) for q in self.node_pins()]
        if self.typ != "symbol":
            return []
        s = self.sym()
        if not s:
            return []
        u = self.sym_unit()
        if s.pins:
            return [self.mapToScene(QPointF(x * u, y * u)) for x, y in s.pins]
        return [self.mapToScene(self.local_rect().center())]

    # ------------------------------------------------------------ dessin
    def pen(self, width=None, dash=None):
        p = QPen(QColor(self.d["color"]))
        p.setWidthF(width if width is not None else self.d["sw"])
        p.setCapStyle(Qt.RoundCap)
        p.setJoinStyle(Qt.RoundJoin)
        dash = dash if dash is not None else self.d.get("dash", "solid")
        if dash == "dash":
            p.setDashPattern([4, 3])
        elif dash == "dot":
            p.setDashPattern([0.1, 2.5])
        elif dash == "dashdot":
            p.setDashPattern([6, 2.5, 0.1, 2.5])
        return p

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        exporting = getattr(self.scene(), "exporting", False)
        t = self.typ
        getattr(self, "paint_" + t)(painter, exporting)
        if t == "symbol" and (self.d.get("label") or self.d.get("pins")):
            self.paint_label(painter)
        if self.isSelected() and not exporting:
            painter.save()
            pen = QPen(QColor("#1e88e5"), 0)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.local_rect().adjusted(-2, -2, 2, 2))
            if self.resizable():
                wt = painter.worldTransform()
                k = (wt.m11() ** 2 + wt.m12() ** 2) ** 0.5 or 1
                hs = 7 / k
                c = self.local_rect().bottomRight()
                painter.setPen(QPen(QColor("#ffffff"), 0))
                painter.setBrush(QColor("#1e88e5"))
                painter.drawRect(QRectF(c.x() - hs / 2, c.y() - hs / 2, hs, hs))
            painter.restore()

    def paint_symbol(self, p, exp):
        s = self.sym()
        if not s:
            return
        u = self.sym_unit()
        sw_units = self.d["sw"] / u
        key = (s.id, repr(sorted((self.d.get("params") or {}).items())), self.d["color"], round(sw_units, 3))
        r = _svg_cache.get(key)
        if r is None:
            r = QSvgRenderer(QByteArray(s.svg(self.d["color"], sw_units, self.d.get("params")).encode()))
            _svg_cache[key] = r
        r.render(p, self.local_rect())

    def paint_label(self, p):
        self.label_rect_local()
        inv, _ = self.transform().inverted()
        texts = [(n, r, fs, False) for n, r, fs in self.pin_labels()]
        if self.d.get("label") and self._label_rect is not None:
            texts.append((self.d["label"], self._label_rect, self.d.get("label_size", 7), True))
        base = inv * p.transform()
        for txt, lr, fs, bold in texts:
            p.save()
            p.setTransform(base)
            p.translate(lr.left(), lr.top())
            p.scale(fs / 100, fs / 100)
            p.setFont(text_font(fs, bold))
            p.setPen(QColor(self.d["color"]))
            fm = QFontMetricsF(p.font())
            p.drawText(QPointF(0, fm.ascent()), txt)
            p.restore()

    def _polyline(self, p, pen):
        pts = self.points()
        if len(pts) < 2:
            return pts
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawPolyline(QPolygonF(pts))
        return pts

    def paint_line(self, p, exp):
        pts = self._polyline(p, self.pen())
        if self.d.get("color2") and len(pts) >= 2:
            pen = QPen(QColor(self.d["color2"]), self.d["sw"])
            pen.setCapStyle(Qt.FlatCap)
            pen.setDashPattern([3, 3])
            p.setPen(pen)
            p.drawPolyline(QPolygonF(pts))
        if len(pts) < 2:
            return
        a = self.d.get("arrow", "none")
        if a in ("end", "both"):
            self._arrow_head(p, pts[-2], pts[-1])
        if a in ("start", "both"):
            self._arrow_head(p, pts[1], pts[0])

    def _arrow_head(self, p, a, b):
        ang = math.atan2(b.y() - a.y(), b.x() - a.x())
        L = 3 + self.d["sw"] * 2.5
        pts = [b, QPointF(b.x() - L * math.cos(ang - 0.4), b.y() - L * math.sin(ang - 0.4)),
               QPointF(b.x() - L * math.cos(ang + 0.4), b.y() - L * math.sin(ang + 0.4))]
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(self.d["color"]))
        p.drawPolygon(QPolygonF(pts))

    def wire_path(self):
        pts = self.points()
        path = QPainterPath()
        if len(pts) < 2:
            return path, pts
        if self.d.get("route") == "curve":
            a, b = pts[0], pts[-1]
            dx = (b.x() - a.x()) * 0.5
            dy = (b.y() - a.y()) * 0.5
            horiz = abs(b.x() - a.x()) >= abs(b.y() - a.y())
            c1 = QPointF(a.x() + dx, a.y()) if horiz else QPointF(a.x(), a.y() + dy)
            c2 = QPointF(b.x() - dx, b.y()) if horiz else QPointF(b.x(), b.y() - dy)
            path.moveTo(a)
            path.cubicTo(c1, c2, b)
            return path, [c2, b]
        path.moveTo(pts[0])
        for q in pts[1:]:
            path.lineTo(q)
        return path, pts

    def paint_wire(self, p, exp):
        path, tail = self.wire_path()
        if path.isEmpty():
            return
        p.setPen(self.pen())
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)
        if self.d.get("color2"):
            pen = QPen(QColor(self.d["color2"]), self.d["sw"])
            pen.setCapStyle(Qt.FlatCap)
            pen.setDashPattern([3, 3])
            p.setPen(pen)
            p.drawPath(path)
        a = self.d.get("arrow", "none")
        if a in ("end", "both") and len(tail) >= 2:
            self._arrow_head(p, tail[-2], tail[-1])
        if a in ("mid",) and len(tail) >= 2:
            pts = self.points()
            i = max(0, len(pts) // 2 - 1)
            m = (pts[i] + pts[i + 1]) / 2
            self._arrow_head(p, pts[i], m)
        for q in self.d.get("dots", []):
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(self.d["color"]))
            p.drawEllipse(QPointF(*q), 1.6 + self.d["sw"] * 0.3, 1.6 + self.d["sw"] * 0.3)

    def _old_paint_wire(self, p, exp):
        pts = self._polyline(p, self.pen())
        if self.d.get("color2") and len(pts) >= 2:
            pen = QPen(QColor(self.d["color2"]), self.d["sw"])
            pen.setCapStyle(Qt.FlatCap)
            pen.setDashPattern([3, 3])
            p.setPen(pen)
            p.drawPolyline(QPolygonF(pts))
        for q in self.d.get("dots", []):  # points de jonction éventuels
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(self.d["color"]))
            p.drawEllipse(QPointF(*q), 1.6, 1.6)

    def paint_freehand(self, p, exp):
        if not self.d.get("plugs"):
            self._polyline(p, self.pen())
            return
        pts = self.points()
        if len(pts) < 2:
            return
        # lissage du tracé
        path = QPainterPath(pts[0])
        for i in range(1, len(pts) - 1):
            mid = (pts[i] + pts[i + 1]) / 2
            path.quadTo(pts[i], mid)
        path.lineTo(pts[-1])
        pen = self.pen()
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)
        # fiches banane aux deux bouts
        for a, b in ((pts[min(3, len(pts) - 1)], pts[0]), (pts[max(-4, -len(pts))], pts[-1])):
            ang = math.degrees(math.atan2(b.y() - a.y(), b.x() - a.x()))
            p.save()
            p.translate(b)
            p.rotate(ang)
            sw = self.d["sw"]
            L, W = 4 + sw * 2.2, 1.6 + sw * 1.1
            p.setPen(QPen(QColor("#222222"), 0.4))
            p.setBrush(QColor(self.d["color"]))
            p.drawRoundedRect(QRectF(-L, -W, L, 2 * W), W * 0.6, W * 0.6)
            p.setBrush(QColor("#b0b0b0"))
            p.drawRoundedRect(QRectF(0, -W * 0.38, L * 0.55, W * 0.76), W * 0.3, W * 0.3)
            p.restore()

    def paint_highlight(self, p, exp):
        c = QColor(self.d["color"])
        c.setAlphaF(0.35)
        pen = QPen(c, self.d["sw"])
        pen.setCapStyle(Qt.FlatCap)
        pen.setJoinStyle(Qt.RoundJoin)
        self._polyline(p, pen)

    def paint_wall(self, p, exp):
        pts = self.points()
        if len(pts) < 2:
            return
        w = self.d.get("thick", 20) * pts_per_cm(self.plan_denom())
        poly = QPolygonF(pts)
        outer = QPen(QColor(self.d["color"]), w + 2 * self.d["sw"] * 0.5)
        outer.setCapStyle(Qt.SquareCap)
        outer.setJoinStyle(Qt.MiterJoin)
        p.setPen(outer)
        p.drawPolyline(poly)
        inner = QPen(QColor(self.d.get("fill") or "#b0b0b0"), max(w - self.d["sw"], 0.1))
        inner.setCapStyle(Qt.SquareCap)
        inner.setJoinStyle(Qt.MiterJoin)
        p.setPen(inner)
        p.drawPolyline(poly)

    def paint_dim(self, p, exp):
        pts = self.points()
        if len(pts) < 2:
            return
        a, b = pts[0], pts[1]
        pen = self.pen(dash="solid")
        p.setPen(pen)
        p.drawLine(a, b)
        ang = math.atan2(b.y() - a.y(), b.x() - a.x())
        # traits obliques d'architecte + petites lignes d'attache
        for q in (a, b):
            d1 = QPointF(3 * math.cos(ang + math.pi / 4), 3 * math.sin(ang + math.pi / 4))
            p.drawLine(q - d1, q + d1)
            n = QPointF(-math.sin(ang) * 4, math.cos(ang) * 4)
            p.drawLine(q - n, q + n)
        length = math.hypot(b.x() - a.x(), b.y() - a.y())
        txt = self.d.get("text") or self.dim_text(length)
        size = self.d.get("size", 7)
        p.save()
        mid = (a + b) / 2
        p.translate(mid)
        deg = math.degrees(ang)
        if deg > 90 or deg <= -90:
            deg += 180
        p.rotate(deg)
        p.scale(size / 100, size / 100)
        f = text_font(size)
        p.setFont(f)
        fm = QFontMetricsF(f)
        p.setPen(QColor(self.d["color"]))
        p.drawText(QPointF(-fm.horizontalAdvance(txt) / 2, -fm.descent() - 120), txt)
        p.restore()

    def dim_text(self, length_pts):
        mode = self.d.get("unit", "real")
        if mode == "mm":
            return f"{length_pts / MM:.0f} mm"
        cm = length_pts / pts_per_cm(self.plan_denom())
        if cm >= 100:
            return f"{cm / 100:.2f} m".replace(".", ",")
        return f"{cm:.0f} cm"

    def paint_rect(self, p, exp):
        p.setPen(self.pen() if self.d["sw"] > 0 else Qt.NoPen)
        fill = self.d.get("fill")
        p.setBrush(QColor(fill) if fill else Qt.NoBrush)
        p.drawRect(self.local_rect())

    def paint_ellipse(self, p, exp):
        p.setPen(self.pen() if self.d["sw"] > 0 else Qt.NoPen)
        fill = self.d.get("fill")
        p.setBrush(QColor(fill) if fill else Qt.NoBrush)
        p.drawEllipse(self.local_rect())

    def paint_text(self, p, exp):
        size = self.d.get("size", 10)
        f = item_font(self.d)
        fm = QFontMetricsF(f)
        lines = (self.d.get("text") or "").split("\n")
        width = max(rich_width(fm, l) for l in lines) if lines else 0
        align = self.d.get("align", "left")
        p.save()
        p.scale(size / 100, size / 100)
        p.setFont(f)
        bg = self.d.get("bg")
        for i, line in enumerate(lines):
            lw = rich_width(fm, line)
            x = 0 if align == "left" else (width - lw) / 2 if align == "center" else width - lw
            y = i * fm.lineSpacing()
            if bg and line:
                c = QColor(bg)
                c.setAlphaF(0.55)
                p.fillRect(QRectF(x - 6, y, lw + 12, fm.lineSpacing()), c)
            p.setPen(QColor(self.d["color"]))
            draw_rich(p, fm, x, fm.ascent() + y, line)
        p.restore()

    def image(self):
        key = self.d.get("png", "")[:64] + str(len(self.d.get("png", "")))
        img = _img_cache.get(key)
        if img is None:
            img = QImage.fromData(base64.b64decode(self.d.get("png", "")))
            _img_cache[key] = img
        return img

    def paint_image(self, p, exp):
        p.setRenderHint(p.RenderHint.SmoothPixmapTransform)
        p.drawImage(self.local_rect(), self.image())

    def _paint_field(self, p, exp):
        if exp:
            return
        t = self.typ
        r = self.local_rect()
        col = QColor("#1565c0") if t == "field_link" else QColor("#7b1fa2")
        pen = QPen(col, 0.8)
        pen.setStyle(Qt.DashLine)
        p.setPen(pen)
        p.setBrush(QColor(col.red(), col.green(), col.blue(), 22))
        if t == "field_radio":
            p.drawEllipse(r)
            if self.d.get("value"):
                p.setBrush(col)
                p.drawEllipse(r.adjusted(r.width() * .28, r.height() * .28, -r.width() * .28, -r.height() * .28))
        else:
            p.drawRect(r)
        if t == "field_check" and self.d.get("value"):
            p.drawLine(r.topLeft(), r.bottomRight())
            p.drawLine(r.topRight(), r.bottomLeft())
        if t == "field_combo":
            s = min(r.height() * 0.5, 8)
            c = QPointF(r.right() - s, r.center().y())
            p.setBrush(col)
            p.drawPolygon(QPolygonF([c + QPointF(-s / 2, -s / 4), c + QPointF(s / 2, -s / 4), c + QPointF(0, s / 3)]))
        val = self.d.get("value")
        if t in ("field_text", "field_combo") and val:
            p.save()
            fs = min(r.height() * 0.62, 11)
            f = text_font(fs)
            fm = QFontMetricsF(f)
            p.translate(r.left() + 3, r.center().y() - fm.height() * fs / 200)
            p.scale(fs / 100, fs / 100)
            p.setFont(f)
            p.setPen(QColor("#111111"))
            p.drawText(QPointF(0, fm.ascent()), str(val))
            p.restore()
            p.setPen(pen)
        caption = {"field_sig": "✍ Signature : ", "field_link": "🔗 ", "field_combo": "▾ "}.get(t, "")
        txt = caption + (self.d.get("url") or (f"page {self.d.get('page')}" if t == "field_link" else "")
                         if t == "field_link" else self.d.get("name", ""))
        p.save()
        p.translate(r.left() + 2, r.top() + 2)
        p.scale(0.06, 0.06)
        p.setPen(col)
        p.setFont(text_font(6))
        p.drawText(QPointF(0, 80), txt)
        p.restore()

    paint_field_text = paint_field_check = paint_field_combo = _paint_field
    paint_field_radio = paint_field_sig = paint_field_link = _paint_field

    # ------------------------------------------------------------ formes avec texte (GRAFCET, algorigramme, carte mentale)
    def node_pins(self):
        r = self.local_rect()
        w, h = r.width(), r.height()
        sh = self.d.get("shape", "rect")
        if sh == "transition":
            return [QPointF(w / 2, 0), QPointF(w / 2, h)]
        if sh == "step_cond":
            return [QPointF(w * 0.86, -4 * MM), QPointF(w, h / 2), QPointF(w / 2, h), QPointF(0, h / 2)]
        if sh in ("and_bar", "or_bar"):
            return [QPointF(w * k, y) for y in (0, h) for k in (1 / 6, 0.5, 5 / 6)]
        if sh in ("action", "action_cond"):
            return [QPointF(0, h / 2)]
        if sh == "renvoi":
            return [QPointF(0, h / 2)]
        return [QPointF(w / 2, 0), QPointF(w, h / 2), QPointF(w / 2, h), QPointF(0, h / 2)]

    def node_font(self):
        return text_font(self.d.get("size", 9), self.d.get("bold", False), self.d.get("font", "Helvetica"),
                         self.d.get("italic", False))

    def node_text_box(self):
        """Zone où s'écrit le texte (coordonnées locales)."""
        r = self.local_rect()
        sh = self.d.get("shape", "rect")
        if sh == "transition":
            fs = self.d.get("size", 9)
            fm = QFontMetricsF(self.node_font())
            lines = (self.d.get("text") or "").split("\n")
            tw = max((fm.horizontalAdvance(l) for l in lines), default=0) * fs / 100
            th = fm.lineSpacing() * len(lines) * fs / 100
            x = r.width() / 2 + 6 * MM
            return QRectF(x, r.height() / 2 - th / 2, tw + 2, th), Qt.AlignLeft | Qt.AlignVCenter
        if sh in ("action", "action_cond"):
            stub = 5 * MM
            q = self.d.get("qual")
            x = stub + (8 * MM if q else 0)
            return QRectF(x, 0, r.width() - x, r.height()), Qt.AlignCenter
        if sh == "para":
            return r.adjusted(r.height() * 0.35, 0, -r.height() * 0.35, 0), Qt.AlignCenter
        if sh == "subprog":
            return r.adjusted(4 * MM / 2, 0, -4 * MM / 2, 0), Qt.AlignCenter
        if sh == "renvoi":
            return r.adjusted(r.height() * 0.6, 0, 0, 0), Qt.AlignCenter
        return r, Qt.AlignCenter

    def node_extra_rect(self):
        box, _ = self.node_text_box()
        r = self.local_rect().united(box)
        if self.d.get("shape") == "step_cond":
            r = r.united(QRectF(0, -4.5 * MM, 45 * MM, 4.5 * MM))
        if self.d.get("shape") == "action_cond":
            r = r.united(QRectF(0, -5.5 * MM, self.local_rect().width() + 40 * MM, 5.5 * MM))
        if self.d.get("shape") == "transition" and self.d.get("label"):
            r = r.united(QRectF(-14 * MM, 0, 14 * MM, self.local_rect().height()))
        return r

    def paint_node(self, p, exp):
        r = self.local_rect()
        w, h = r.width(), r.height()
        sh = self.d.get("shape", "rect")
        pen = self.pen()
        p.setPen(pen)
        fill = self.d.get("fill")
        p.setBrush(QColor(fill) if fill else Qt.NoBrush)
        if sh == "zone":
            p.setBrush(Qt.NoBrush)
            p.drawRect(r)
            if self.d.get("text"):
                self._draw_text(p, QRectF(3 * MM, 1.5 * MM, w - 6 * MM, 6 * MM), self.d["text"], Qt.AlignLeft | Qt.AlignVCenter)
            return
        if sh in ("rect", "step"):
            p.drawRect(r)
        elif sh == "cartouche":
            self._paint_cartouche(p, r)
            return
        elif sh == "step_cond":
            p.drawRect(r)
            xc = w * 0.86
            p.drawLine(QPointF(xc, 0), QPointF(xc, -4 * MM))
            if self.d.get("cond"):
                self._draw_text(p, QRectF(xc + 1.5 * MM, -4 * MM, 40 * MM, 4 * MM), self.d["cond"],
                                Qt.AlignLeft | Qt.AlignVCenter, 0.85)
        elif sh == "step_init":
            p.drawRect(r)
            k = min(w, h) * 0.12
            p.setBrush(Qt.NoBrush)
            p.drawRect(r.adjusted(k, k, -k, -k))
        elif sh == "macro":
            p.drawRect(r)
            k = h * 0.14
            p.drawLine(QPointF(0, k), QPointF(w, k))
            p.drawLine(QPointF(0, h - k), QPointF(w, h - k))
        elif sh == "round":
            p.drawRoundedRect(r, min(h / 2, 4 * MM), min(h / 2, 4 * MM))
        elif sh == "terminal":
            p.drawRoundedRect(r, h / 2, h / 2)
        elif sh == "ellipse":
            p.drawEllipse(r)
        elif sh == "diamond":
            p.drawPolygon(QPolygonF([QPointF(w / 2, 0), QPointF(w, h / 2), QPointF(w / 2, h), QPointF(0, h / 2)]))
        elif sh == "para":
            k = h * 0.35
            p.drawPolygon(QPolygonF([QPointF(k, 0), QPointF(w, 0), QPointF(w - k, h), QPointF(0, h)]))
        elif sh == "hex":
            k = h * 0.35
            p.drawPolygon(QPolygonF([QPointF(k, 0), QPointF(w - k, 0), QPointF(w, h / 2), QPointF(w - k, h),
                                     QPointF(k, h), QPointF(0, h / 2)]))
        elif sh == "subprog":
            p.drawRect(r)
            k = 2 * MM
            p.drawLine(QPointF(k, 0), QPointF(k, h))
            p.drawLine(QPointF(w - k, 0), QPointF(w - k, h))
        elif sh == "note":
            k = min(w, h) * 0.25
            p.drawPolygon(QPolygonF([QPointF(0, 0), QPointF(w - k, 0), QPointF(w, k), QPointF(w, h), QPointF(0, h)]))
            p.drawPolyline(QPolygonF([QPointF(w - k, 0), QPointF(w - k, k), QPointF(w, k)]))
        elif sh == "action_cond":
            # action conditionnelle (NF EN 60848) : trait vertical au-dessus du rectangle d'action,
            # la condition (assignation) s'écrit à droite du trait
            stub = 5 * MM
            p.drawLine(QPointF(0, h / 2), QPointF(stub, h / 2))
            p.drawRect(QRectF(stub, 0, w - stub, h))
            if self.d.get("qual"):
                p.drawLine(QPointF(stub + 8 * MM, 0), QPointF(stub + 8 * MM, h))
                self._draw_text(p, QRectF(stub, 0, 8 * MM, h), self.d["qual"], Qt.AlignCenter, 0.85)
            xc = stub + (w - stub) / 2
            p.drawLine(QPointF(xc, 0), QPointF(xc, -5 * MM))
            if self.d.get("cond"):
                self._draw_text(p, QRectF(xc + 1.5 * MM, -5 * MM, 40 * MM, 4.5 * MM), self.d["cond"],
                                Qt.AlignLeft | Qt.AlignVCenter, 0.85)
        elif sh == "action":
            stub = 5 * MM
            p.drawLine(QPointF(0, h / 2), QPointF(stub, h / 2))
            p.drawRect(QRectF(stub, 0, w - stub, h))
            if self.d.get("qual"):
                p.drawLine(QPointF(stub + 8 * MM, 0), QPointF(stub + 8 * MM, h))
                self._draw_text(p, QRectF(stub, 0, 8 * MM, h), self.d["qual"], Qt.AlignCenter, 0.85)
        elif sh == "transition":
            p.drawLine(QPointF(w / 2, 0), QPointF(w / 2, h))
            bar = QPen(QColor(self.d["color"]), max(1.6, self.d["sw"] * 1.8))
            bar.setCapStyle(Qt.FlatCap)
            p.setPen(bar)
            p.drawLine(QPointF(w / 2 - 4 * MM, h / 2), QPointF(w / 2 + 4 * MM, h / 2))
            p.setPen(pen)
            if self.d.get("label"):
                self._draw_text(p, QRectF(-14 * MM, 0, 14 * MM + w / 2 - 5 * MM, h), self.d["label"],
                                Qt.AlignRight | Qt.AlignVCenter, 0.85)
        elif sh == "and_bar":
            p.drawLine(QPointF(0, 0), QPointF(w, 0))
            p.drawLine(QPointF(0, h), QPointF(w, h))
        elif sh == "or_bar":
            p.drawLine(QPointF(0, h / 2), QPointF(w, h / 2))
        elif sh == "renvoi":
            p.drawPolygon(QPolygonF([QPointF(0, h / 2), QPointF(h * 0.6, 0), QPointF(w, 0), QPointF(w, h),
                                     QPointF(h * 0.6, h)]))
        if self.d.get("active") and sh in ("step", "step_init"):
            p.setBrush(QColor(self.d["color"]))
            p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(w / 2, h * 0.8), 1.6, 1.6)
        box, align = self.node_text_box()
        if self.d.get("text"):
            self._draw_text(p, box, self.d["text"], align)

    def _paint_cartouche(self, p, r):
        w, h = r.width(), r.height()
        p.setBrush(QColor("#ffffff"))
        p.drawRect(r)
        row = h / 4
        p.setPen(QPen(QColor(self.d["color"]), self.d["sw"] * 0.6))
        for i in (1, 2, 3):
            p.drawLine(QPointF(0, row * i), QPointF(w, row * i))
        p.drawLine(QPointF(w * 0.6, row), QPointF(w * 0.6, h))
        d = self.d
        cells = [
            (QRectF(2, 0, w - 4, row), d.get("title", ""), 1.35, True),
            (QRectF(2, row, w * 0.6 - 4, row), f"Auteur : {d.get('author', '')}", 1, False),
            (QRectF(w * 0.6 + 2, row, w * 0.4 - 4, row), f"Classe : {d.get('classe', '')}", 1, False),
            (QRectF(2, row * 2, w * 0.6 - 4, row), f"{d.get('school', '')}", 1, False),
            (QRectF(w * 0.6 + 2, row * 2, w * 0.4 - 4, row), f"Échelle : {d.get('scale', '')}", 1, False),
            (QRectF(2, row * 3, w * 0.6 - 4, row), f"Date : {d.get('date', '')}", 1, False),
            (QRectF(w * 0.6 + 2, row * 3, w * 0.4 - 4, row), f"Folio : {d.get('folio', '')}", 1, False),
        ]
        bold0 = d.get("bold", False)
        for box, txt, sc, bold in cells:
            d["bold"] = bold
            self._draw_text(p, box, txt, Qt.AlignLeft | Qt.AlignVCenter, sc)
        d["bold"] = bold0

    def _draw_text(self, p, box, text, align, scale=1.0):
        fs = self.d.get("size", 9) * scale
        f = self.node_font()
        fm = QFontMetricsF(f)
        lines = text.split("\n")
        k = fs / 100
        th = fm.lineSpacing() * len(lines) * k
        p.save()
        p.setPen(QColor(self.d.get("text_color") or self.d["color"]))
        p.setFont(f)
        if align & Qt.AlignVCenter or align == Qt.AlignCenter:
            y0 = box.top() + (box.height() - th) / 2
        else:
            y0 = box.top()
        for i, line in enumerate(lines):
            lw = rich_width(fm, line) * k
            if align & Qt.AlignLeft:
                x = box.left()
            elif align & Qt.AlignRight:
                x = box.right() - lw
            else:
                x = box.left() + (box.width() - lw) / 2
            p.save()
            p.translate(x, y0 + i * fm.lineSpacing() * k)
            p.scale(k, k)
            draw_rich(p, fm, 0, fm.ascent(), line)
            p.restore()
        p.restore()

    # ------------------------------------------------------------ agrandissement à la souris
    def resizable(self):
        return self.typ in ("symbol", "image", "node", "rect", "ellipse", "text") + FIELD_TYPES

    def proportional(self):
        return self.typ in ("symbol", "image", "node", "text")

    def start_resize(self):
        self._rs = {"scale": self.d.get("scale", 1.0), "w": self.d.get("w"), "h": self.d.get("h"),
                    "size": self.d.get("size", 10), "rect": self.local_rect(), "d": dict(self.d)}

    def do_resize(self, scene_pt, keep_ratio):
        rs = getattr(self, "_rs", None)
        if not rs:
            return
        r0 = rs["rect"]
        inv, _ = (self.sceneTransform()).inverted()
        q = inv.map(scene_pt)
        fx = max(0.05, (q.x() - r0.left()) / max(r0.width(), 1e-6))
        fy = max(0.05, (q.y() - r0.top()) / max(r0.height(), 1e-6))
        f = max(fx, fy)
        if self.typ == "symbol":
            self.d["scale"] = round(max(0.1, rs["scale"] * f), 3)
        elif self.typ == "text":
            self.d["size"] = round(max(3, rs["size"] * f), 1)
        else:
            if keep_ratio or self.proportional():
                fx = fy = f
            self.d["w"] = max(2, rs["w"] * fx)
            self.d["h"] = max(2, rs["h"] * fy)
        self.update_geom()

    # ------------------------------------------------------------ sauvegarde
    def to_dict(self):
        d = dict(self.d)
        d["x"], d["y"], d["z"] = self.pos().x(), self.pos().y(), self.zValue()
        return d


def image_to_b64(img: QImage):
    from PySide6.QtCore import QBuffer, QIODevice
    buf = QBuffer()
    buf.open(QIODevice.WriteOnly)
    img.save(buf, "PNG")
    return base64.b64encode(bytes(buf.data())).decode()
