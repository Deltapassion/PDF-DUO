"""PDF DUO — fenêtre principale.

Lire, annoter, signer, remplir des PDF ; dessiner des schémas électriques et des plans
avec bibliothèques de symboles ; convertir Word / ODF <-> PDF.
"""
import base64
import json
import math
import os
import sys
import tempfile

import pymupdf
from PySide6.QtCore import (QBuffer, QByteArray, QIODevice, QMarginsF, QMimeData, QPointF, QRectF,
                            QSettings, QSize, QSizeF, Qt, QThread, QTimer, Signal)
from PySide6.QtGui import (QAction, QActionGroup, QColor, QIcon, QImage, QKeySequence, QPageSize,
                           QPainter, QPdfWriter, QPen, QPixmap, QBrush, QTransform, QFont)
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (QFontComboBox, QAbstractItemView, QApplication, QCheckBox, QColorDialog, QComboBox,
                               QDialog, QDialogButtonBox, QDockWidget, QDoubleSpinBox, QFileDialog,
                               QFormLayout, QGraphicsItem, QGraphicsScene, QGraphicsView, QHBoxLayout,
                               QHeaderView, QInputDialog, QLabel, QLineEdit, QListView, QListWidget,
                               QListWidgetItem, QMainWindow, QMenu, QMessageBox, QPlainTextEdit,
                               QProgressDialog, QPushButton, QScrollArea, QSpinBox, QTableWidget,
                               QTableWidgetItem, QToolBar, QToolButton, QVBoxLayout, QWidget)

from . import convert
from .i18n import T
from .items import BOX_TYPES, MM, POLY_TYPES, PItem, image_to_b64, pts_per_cm
from .signature import SignatureDialog
from . import theme as th
from .icons import icon as make_icon
from .symbols import BY_ID, CATEGORIES as SYM_CATEGORIES, SYMBOLS
from . import nodes as ND
CATEGORIES = SYM_CATEGORIES + ND.CATEGORIES

APP_NAME = "PDF DUO"
APP_VERSION = "1.3.1"
SITE_URL = "https://deltapassion.github.io/PDF-DUO/"
RELEASES_URL = "https://github.com/Deltapassion/PDF-DUO/releases/latest"
KOFI_URL = "https://ko-fi.com/djlatinjazz"
CREDIT = "Jacques Branas, en collaboration avec Claude.ai"
GAP = 24
MIME_ITEMS = "application/x-pdfduo-items"
MIME_SYMBOL = "application/x-pdfduo-symbol"
EMB_ORIG, EMB_ITEMS = "pdfduo-original.pdf", "pdfduo-items.json"

PAPER = {"A4 portrait": (595.28, 841.89), "A4 paysage": (841.89, 595.28),
         "A3 portrait": (841.89, 1190.55), "A3 paysage": (1190.55, 841.89),
         "A5 portrait": (419.53, 595.28), "Lettre US": (612, 792)}

TOOLS = [
    ("select", "Sélection", "Sélectionner, déplacer (Échap)"),
    ("pan", "Main", "Faire défiler la page"),
    ("text", "Texte", "Cliquer pour écrire un texte"),
    ("line", "Trait", "Trait droit (Maj = angle par pas de 15°)"),
    ("arrow", "Flèche", "Flèche"),
    ("wire", "Fil", "Fil de schéma à angles droits : clic par point ; un clic sur une borne accroche le fil et le termine"),
    ("link", "Liaison", "Relier deux bornes : cliquer une borne puis l'autre (tracé automatique à angles droits)"),
    ("rect", "Rectangle", "Rectangle"),
    ("ellipse", "Ellipse", "Cercle / ellipse (Maj = cercle)"),
    ("freehand", "Crayon", "Dessin à main levée"),
    ("highlight", "Surligneur", "Surligner"),
    ("flying", "Fil volant", "Fil de connexion à main levée avec fiches banane aux deux bouts (montage « fils volants »)"),
    ("wall", "Mur", "Mur à l'échelle : clic par angle, double-clic pour finir"),
    ("dim", "Cote", "Cote : glisser d'un point à l'autre (longueur réelle à l'échelle)"),
    ("door", "Porte", "Poser une porte dans un mur (elle s'aligne et prend l'épaisseur du mur)"),
    ("door2", "Porte double", "Poser une porte double dans un mur"),
    ("window", "Fenêtre", "Poser une fenêtre dans un mur"),
    ("capture", "Capture", "Capturer une zone en image (copiée dans le presse-papiers)"),
    ("field_text", "Champ texte", "Créer un champ de formulaire à remplir"),
    ("field_check", "Case à cocher", "Créer une case à cocher de formulaire"),
    ("field_combo", "Liste", "Créer une liste déroulante de formulaire"),
    ("field_radio", "Bouton radio", "Créer un bouton radio (choix unique dans un groupe)"),
    ("field_sig", "Zone signature", "Créer une zone où une autre personne pourra signer (Acrobat…)"),
    ("field_link", "Lien", "Créer une zone cliquable vers une page ou une adresse web"),
]
FIELD_TOOLS = ("field_text", "field_check", "field_combo", "field_radio", "field_sig", "field_link")
PLAN_TOOLS = ("wall", "dim", "door", "door2", "window")


CONDUCTORS = [
    ("Phase – marron", "#8b4513", None), ("Phase – noir", "#111111", None), ("Phase – gris", "#7f7f7f", None),
    ("Phase – rouge", "#d32f2f", None), ("Neutre – bleu", "#1e63c8", None),
    ("Terre – vert/jaune", "#2e9b3a", "#f2d21b"), ("Retour lampe – violet", "#7b1fa2", None),
    ("Navette – orange", "#ef6c00", None), ("Commande – rouge clair", "#ff5252", None),
    ("Fibre optique – bleu", "#4fa3d9", None), ("Ethernet cuivre – noir", "#202020", None),
    ("Coaxial – gris", "#757575", None), ("Air comprimé (pneumatique)", "#1565c0", None),
]


def pin_dir(item, idx):
    """Direction de sortie d'une borne : 'h' (fil horizontal) ou 'v'."""
    pins = item.pins_scene()
    c = item.mapToScene(item.local_rect().center())
    if idx >= len(pins):
        return "h"
    d = pins[idx] - c
    return "h" if abs(d.x()) >= abs(d.y()) else "v"


def route(a, da, b, db, snapf=None):
    """Tracé à angles droits entre deux points (da / db : 'h' ou 'v')."""
    if abs(a.x() - b.x()) < 0.01 or abs(a.y() - b.y()) < 0.01:
        return [a, b]
    if da == "h" and db == "h":
        xm = (a.x() + b.x()) / 2
        if snapf:
            xm = snapf(QPointF(xm, a.y())).x()
        return [a, QPointF(xm, a.y()), QPointF(xm, b.y()), b]
    if da == "v" and db == "v":
        ym = (a.y() + b.y()) / 2
        if snapf:
            ym = snapf(QPointF(a.x(), ym)).y()
        return [a, QPointF(a.x(), ym), QPointF(b.x(), ym), b]
    if da == "h":
        return [a, QPointF(b.x(), a.y()), b]
    return [a, QPointF(a.x(), b.y()), b]


SPECIAL_CHARS = ["Ω", "ω", "Φ", "φ", "Π", "π", "√", "Δ", "δ", "α", "β", "γ", "λ", "θ", "μ", "ρ", "σ", "Σ", "τ",
                 "η", "ε", "°", "±", "×", "÷", "≈", "≠", "≤", "≥", "∞", "→", "←", "↔", "⇒", "²", "³", "½", "¼",
                 "₁", "₂", "₃", "⏚", "⎓", "∼", "∫", "∑", "∈", "∀", "⊕", "·", "¬"]


class TextDialog(QDialog):
    """Saisie de texte avec palette de caractères spéciaux et racine carrée sur tout le nombre."""

    def __init__(self, parent, title, label, text=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(label))
        from .spell import SpellTextEdit
        self.edit = SpellTextEdit(text)
        self.edit.setMinimumSize(420, 110)
        lay.addWidget(self.edit)
        grid = QWidget()
        g = QHBoxLayout(grid)
        g.setContentsMargins(0, 0, 0, 0)
        g.setSpacing(2)
        from PySide6.QtWidgets import QGridLayout
        gl = QGridLayout()
        gl.setSpacing(2)
        for i, ch in enumerate(SPECIAL_CHARS):
            b = QToolButton(text=ch)
            b.setMinimumSize(28, 26)
            b.clicked.connect(lambda _=False, c=ch: self.edit.insertPlainText(c))
            gl.addWidget(b, i // 18, i % 18)
        lay.addLayout(gl)
        row = QHBoxLayout()
        sq = QPushButton(T("√ sur tout le nombre"))
        sq.setToolTip(T("Écrit √{…} : la barre de la racine couvre tout ce qui est entre les accolades"))
        sq.clicked.connect(self.insert_sqrt)
        row.addWidget(sq)
        row.addStretch()
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        row.addWidget(bb)
        lay.addLayout(row)
        self.edit.setFocus()

    def insert_sqrt(self):
        cur = self.edit.textCursor()
        sel = cur.selectedText()
        cur.insertText("√{" + sel + "}")
        if not sel:
            cur.movePosition(cur.MoveOperation.Left)
            self.edit.setTextCursor(cur)
        self.edit.setFocus()

    @staticmethod
    def get(parent, title, label, text=""):
        d = TextDialog(parent, title, label, text)
        ok = d.exec()
        return d.edit.toPlainText(), bool(ok)


def snap_angle(a, b, step=15):
    dx, dy = b.x() - a.x(), b.y() - a.y()
    L = math.hypot(dx, dy)
    ang = round(math.degrees(math.atan2(dy, dx)) / step) * step
    return QPointF(a.x() + L * math.cos(math.radians(ang)), a.y() + L * math.sin(math.radians(ang)))


def qimage_from_pix(pix):
    fmt = QImage.Format_RGB888 if pix.n == 3 else QImage.Format_RGBA8888
    return QImage(pix.samples, pix.width, pix.height, pix.stride, fmt).copy()


def node_icon(d, size=56):
    it = PItem(dict(d))
    br = it.boundingRect()
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    k = min((size - 6) / max(br.width(), 1), (size - 6) / max(br.height(), 1))
    p.translate(size / 2, size / 2)
    p.scale(k, k)
    p.translate(-br.center())
    p.setTransform(it.transform() * p.transform())
    it.paint(p, None)
    p.end()
    return QIcon(pm)


def sym_icon(s, size=56, color="#202020"):
    w, h, _ = s.geometry()
    k = min((size - 6) / w, (size - 6) / h)
    sw = 1.4 if s.kind == "paper" else max(1.4, 1.6 / k)
    r = QSvgRenderer(QByteArray(s.svg(color, sw).encode()))
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    r.render(p, QRectF((size - w * k) / 2, (size - h * k) / 2, w * k, h * k))
    p.end()
    return QIcon(pm)


def star_icon(icon, size=56):
    """Ajoute une petite étoile dorée en haut à droite d'une icône (symbole favori)."""
    from PySide6.QtGui import QPolygonF
    pm = icon.pixmap(size, size)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    cx, cy, r1, r2 = size - 9, 9, 8, 3.4
    pts = [QPointF(cx + (r1 if i % 2 == 0 else r2) * math.sin(i * math.pi / 5), cy - (r1 if i % 2 == 0 else r2) * math.cos(i * math.pi / 5))
           for i in range(10)]
    p.setPen(QPen(QColor("#8d6e00"), 1))
    p.setBrush(QColor("#ffc107"))
    p.drawPolygon(QPolygonF(pts))
    p.end()
    return QIcon(pm)


# ====================================================================== scène et pages
class PageItem(QGraphicsItem):
    def __init__(self, idx, w, h):
        super().__init__()
        self.idx, self.w, self.h = idx, w, h
        self.img, self.scale_ = None, 0
        self.setZValue(-1000)
        self.setAcceptedMouseButtons(Qt.NoButton)

    def boundingRect(self):
        return QRectF(-2, -2, self.w + 6, self.h + 6)

    def paint(self, p, opt, w=None):
        p.fillRect(QRectF(3, 3, self.w, self.h), QColor(0, 0, 0, 40))
        p.fillRect(QRectF(0, 0, self.w, self.h), Qt.white)
        if self.img is not None:
            p.setRenderHint(QPainter.SmoothPixmapTransform)
            p.drawImage(QRectF(0, 0, self.w, self.h), self.img)


class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.plan_denom = 50
        self.snap = True
        self.grid_step = 2.5 * MM
        self.show_grid = True
        self.exporting = False
        self.no_snap = False
        self.setBackgroundBrush(QColor("#5f6368"))


# ====================================================================== vue et outils
class View(QGraphicsView):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.tool = "select"
        self.temp = None        # élément en cours de tracé
        self.ghost = None       # symbole / image qui suit la souris
        self.start = None
        self.poly = []
        self._pan = None
        self.last_scene_pos = QPointF()
        self.moved = False

    # -------------------------------------------------------------- utilitaires
    def zoom(self):
        return self.transform().m11()

    def set_zoom(self, z):
        z = max(0.1, min(z, 16))
        self.setTransform(self.transform().fromScale(z, z))
        self.mw.zoom_changed()

    def snap(self, p, force=False):
        s = self.scene()
        if (s.snap or force) and not (QApplication.keyboardModifiers() & Qt.AltModifier):
            g = s.grid_step
            return QPointF(round(p.x() / g) * g, round(p.y() / g) * g)
        return QPointF(p)

    def handle_at(self, vpos):
        """Poignée d'agrandissement (coin bas-droit) sous le curseur, pour un élément sélectionné."""
        for it in self.scene().selectedItems():
            if isinstance(it, PItem) and it.resizable():
                c = self.mapFromScene(it.mapToScene(it.local_rect().bottomRight()))
                if abs(c.x() - vpos.x()) <= 7 and abs(c.y() - vpos.y()) <= 7:
                    return it
        return None

    def find_pin(self, sp):
        """Borne de symbole la plus proche du curseur : (point, (uid, indice), item) ou (None, None, None)."""
        tol = 7 / max(self.zoom(), 0.01)
        best, bd = (None, None, None), tol
        r = QRectF(sp.x() - tol * 4, sp.y() - tol * 4, tol * 8, tol * 8)
        for it in self.scene().items(r):
            if not isinstance(it, PItem) or getattr(it, "is_temp", False) or it.typ not in ("symbol", "node"):
                continue
            for i, q in enumerate(it.pins_scene()):
                d = math.hypot(q.x() - sp.x(), q.y() - sp.y())
                if d <= bd:
                    best, bd = (q, (it.d["uid"], i), it), d
        return best

    def set_tool(self, tool):
        self.cancel_temp()
        self.tool = tool
        self.setDragMode(QGraphicsView.ScrollHandDrag if tool == "pan"
                         else QGraphicsView.RubberBandDrag if tool == "select" else QGraphicsView.NoDrag)
        movable = tool == "select"
        for it in self.scene().items():
            if isinstance(it, PItem) and it is not self.ghost:
                it.setFlag(QGraphicsItem.ItemIsMovable, movable)
                it.setFlag(QGraphicsItem.ItemIsSelectable, movable)
        self.viewport().setCursor(Qt.ArrowCursor if tool == "select" else Qt.CrossCursor)

    def cancel_temp(self):
        for attr in ("temp", "ghost"):
            it = getattr(self, attr)
            if it is not None:
                if it.scene():
                    self.scene().removeItem(it)
                setattr(self, attr, None)
        self.poly = []
        self.start = None
        self.conn_a = None
        self.hover_pin = None

    def set_ghost(self, d):
        self.cancel_temp()
        self.ghost = PItem(d)
        self.ghost.is_temp = True
        self.ghost.setFlags(QGraphicsItem.GraphicsItemFlag(0))
        self.ghost.setOpacity(0.55)
        self.ghost.setZValue(10000)
        self.scene().addItem(self.ghost)
        self.ghost.update_geom()
        self.move_ghost(self.last_scene_pos)

    def find_wall(self, sp):
        """Mur le plus proche : (point projeté sur l'axe, angle en degrés, épaisseur cm) ou None."""
        best, bd = None, None
        tol = 8 / max(self.zoom(), 0.01)
        for it in self.scene().items(QRectF(sp.x() - 60, sp.y() - 60, 120, 120)):
            if not isinstance(it, PItem) or it.typ != "wall" or getattr(it, "is_temp", False):
                continue
            half = it.d.get("thick", 20) * pts_per_cm(self.scene().plan_denom) / 2
            pts = [it.mapToScene(q) for q in it.points()]
            for a, b in zip(pts, pts[1:]):
                dx, dy = b.x() - a.x(), b.y() - a.y()
                L2 = dx * dx + dy * dy
                if L2 < 1e-6:
                    continue
                tt = max(0, min(1, ((sp.x() - a.x()) * dx + (sp.y() - a.y()) * dy) / L2))
                q = QPointF(a.x() + tt * dx, a.y() + tt * dy)
                dist = math.hypot(sp.x() - q.x(), sp.y() - q.y())
                if dist <= half + tol and (bd is None or dist < bd):
                    if self.scene().snap:
                        # aimanter le long du mur au pas de la grille
                        L = math.sqrt(L2)
                        g = self.scene().grid_step
                        tt = max(0, min(1, round(tt * L / g) * g / L))
                        q = QPointF(a.x() + tt * dx, a.y() + tt * dy)
                    best, bd = (q, math.degrees(math.atan2(dy, dx)), it.d.get("thick", 20)), dist
        return best

    def move_ghost(self, sp):
        if self.ghost is None:
            return
        g = self.ghost
        sym = g.sym() if g.typ == "symbol" else None
        anchor = getattr(sym, "wall_anchor", None) if sym else None
        if anchor:
            wall = self.find_wall(sp)
            if wall:
                q, ang, thick = wall
                prm = g.d.setdefault("params", sym.defaults())
                if prm.get("mur") != thick:
                    prm["mur"] = thick
                if not g.d.get("_user_angle"):
                    base = (-ang) % 360
                    # l'ouverture se fait du côté où se trouve la souris (R pour inverser)
                    th_ = math.radians(ang)
                    n = (math.sin(th_), -math.cos(th_))
                    side = (sp.x() - q.x()) * n[0] + (sp.y() - q.y()) * n[1]
                    flip = (side < 0) != bool(g.d.get("_flip180", False))
                    g.d["angle"] = (base + (180 if flip else 0)) % 360
                g.update_geom()
                ax, ay = anchor(prm)
                u = g.sym_unit()
                A = QPointF(ax * u, ay * u)
                g.setPos(q - g.transform().map(A))
                return
        c = g.local_rect().center()
        g.setPos(self.snap(sp - c))

    def new_temp(self, d):
        it = PItem(d)
        it.is_temp = True
        it.setFlags(QGraphicsItem.GraphicsItemFlag(0))
        self.scene().addItem(it)
        self.temp = it
        return it

    # -------------------------------------------------------------- dessin de la grille
    def drawForeground(self, p, rect):
        s = self.scene()
        if s.exporting:
            return
        if self.tool in ("wire", "link"):
            acc = QColor(self.mw.accent)
            p.setPen(QPen(acc, 0))
            p.setBrush(Qt.NoBrush)
            rr = 2.2 / max(self.zoom(), 0.01) * 1.6
            for it in self.scene().items(rect):
                if isinstance(it, PItem) and it.typ in ("symbol", "node") and not getattr(it, "is_temp", False):
                    for q in it.pins_scene():
                        p.drawEllipse(q, rr, rr)
            if self.hover_pin is not None:
                c = QColor(acc)
                c.setAlpha(120)
                p.setBrush(c)
                p.drawEllipse(self.hover_pin, rr * 2, rr * 2)
        if not s.show_grid:
            return
        g = s.grid_step
        z = self.zoom()
        k = 1
        while g * k * z < 7:
            k *= 2
        step = g * k
        dot = QPen(QColor(30, 100, 200, 110), 0)
        p.setPen(dot)
        for pg in self.mw.page_items:
            pr = QRectF(pg.pos().x(), pg.pos().y(), pg.w, pg.h).intersected(rect)
            if pr.isEmpty():
                continue
            ox, oy = pg.pos().x(), pg.pos().y()
            x0 = ox + math.ceil((pr.left() - ox) / step) * step
            y0 = oy + math.ceil((pr.top() - oy) / step) * step
            pts = []
            y = y0
            while y <= pr.bottom():
                x = x0
                while x <= pr.right():
                    pts.append(QPointF(x, y))
                    x += step
                y += step
            if len(pts) < 60000:
                p.drawPoints(pts)

    # -------------------------------------------------------------- souris
    def wheelEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            f = 1.15 if e.angleDelta().y() > 0 else 1 / 1.15
            self.set_zoom(self.zoom() * f)
        else:
            super().wheelEvent(e)
            self.mw.schedule_render()

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.mw.schedule_render()

    def mousePressEvent(self, e):
        sp = self.mapToScene(e.position().toPoint())
        self.last_scene_pos = sp
        if e.button() == Qt.MiddleButton:
            self._pan = e.position()
            self.viewport().setCursor(Qt.ClosedHandCursor)
            return
        t = self.tool
        if t == "select" and e.button() == Qt.LeftButton:
            h = self.handle_at(e.position())
            if h is not None:
                self.resizing = h
                h.start_resize()
                return
        if t in ("select", "pan"):
            self.moved = False
            super().mousePressEvent(e)
            return
        if e.button() == Qt.RightButton:
            if t == "link" and self.temp is not None:
                self.cancel_temp()
                return
            if t in ("wire", "wall") and self.temp is not None:
                self.finish_poly()
            else:
                self.mw.set_tool("select")
            return
        if e.button() != Qt.LeftButton:
            return
        mw = self.mw
        p = self.snap(sp)
        if t == "symbol_place" or t == "image_place":
            if self.ghost is not None:
                d = self.ghost.to_dict()
                mw.add_item(d)
                mw.commit()
                if t == "image_place":
                    mw.set_tool("select")
            return
        if t == "text":
            txt, ok = TextDialog.get(self, T("Texte"), T("Saisissez le texte :"))
            if ok and txt.strip():
                mw.add_item({"type": "text", "x": p.x(), "y": p.y(), "text": txt, "size": mw.cur_text_size,
                             "color": mw.cur_color, **mw.text_style})
                mw.commit()
            return
        if t == "link":
            pin, conn, item = self.find_pin(sp)
            if pin is None:
                self.mw.statusBar().showMessage(T("Cliquer sur une borne (petits cercles) d'un symbole"), 3000)
                return
            if self.temp is None:
                self.conn_a = (pin, conn, item)
                self.new_temp({"type": "wire", "x": 0, "y": 0, "pts": [[pin.x(), pin.y()], [pin.x(), pin.y()]],
                               "color": mw.cur_color, "color2": mw.cur_color2, "sw": mw.cur_sw, "dash": mw.cur_dash})
            else:
                a, ca, ia = self.conn_a
                if conn == ca:
                    return
                mode = mw.route_combo.currentData()
                pts = [a, pin] if mode in ("straight", "curve") else \
                    route(a, pin_dir(ia, ca[1]), pin, pin_dir(item, conn[1]), self.snap)
                self.scene().removeItem(self.temp)
                d = dict(self.temp.d)
                self.temp = None
                o = pts[0]
                d.update(x=o.x(), y=o.y(), pts=[[q.x() - o.x(), q.y() - o.y()] for q in pts], ca=list(ca), cb=list(conn),
                         route=mode, arrow="end" if mw.arrow_cb.isChecked() else "none")
                mw.add_item(d)
                self.conn_a = None
                mw.commit()
            return
        if t == "wire":
            pin, conn, item = self.find_pin(sp)
            if pin is not None:
                p = pin
            if self.temp is None:
                self.poly = [p]
                self.conn_a = conn
                self.new_temp({"type": "wire", "x": 0, "y": 0, "pts": [[p.x(), p.y()], [p.x(), p.y()]],
                               "color": mw.cur_color, "color2": mw.cur_color2, "sw": mw.cur_sw, "dash": mw.cur_dash})
            else:
                last = self.poly[-1]
                if pin is not None:
                    # accrochage sur une borne : on rejoint la borne à angle droit et on termine
                    if abs(last.x() - p.x()) > 0.01 and abs(last.y() - p.y()) > 0.01:
                        # le dernier segment arrive dans l'axe de la borne
                        self.poly.append(QPointF(last.x(), p.y()) if pin_dir(item, conn[1]) == "h"
                                         else QPointF(p.x(), last.y()))
                    self.poly.append(p)
                    self.finish_poly(conn_b=conn)
                    return
                q = self.constrain_poly(last, p)
                if q != last:
                    self.poly.append(q)
                self.update_poly(q)
            return
        if t == "wall":
            if self.temp is None:
                self.poly = [p]
                d = {"type": t, "x": 0, "y": 0, "pts": [[p.x(), p.y()], [p.x(), p.y()]],
                     "color": mw.cur_color if t == "wire" else "#000000",
                     "sw": mw.cur_sw if t == "wire" else 0.8, "dash": mw.cur_dash if t == "wire" else "solid"}
                if t == "wall":
                    d["thick"] = mw.wall_thick.value()
                self.new_temp(d)
            else:
                q = self.constrain_poly(self.poly[-1], p)
                if q != self.poly[-1]:
                    self.poly.append(q)
                self.update_poly(q)
            return
        # tracés par glisser
        self.start = p
        d = {"x": 0, "y": 0, "color": mw.cur_color, "sw": mw.cur_sw, "dash": mw.cur_dash}
        if t in ("line", "arrow", "dim"):
            d.update(type="dim" if t == "dim" else "line", pts=[[p.x(), p.y()], [p.x(), p.y()]],
                     arrow="end" if t == "arrow" else "none")
            if t == "dim":
                d["sw"] = 0.5
        elif t == "flying":
            col = mw.cur_color if mw.cur_color.lower() != "#000000" else "#d32f2f"
            d.update(type="freehand", pts=[[sp.x(), sp.y()]], plugs=True, color=col, sw=max(mw.cur_sw, 1.6))
        elif t in ("freehand", "highlight"):
            d.update(type=t, pts=[[p.x(), p.y()]])
            if t == "highlight":
                d.update(color="#ffeb3b", sw=12)
        elif t in ("rect", "ellipse", "capture") + FIELD_TOOLS:
            d.update(type="rect" if t in ("capture",) else t, x=p.x(), y=p.y(), w=1, h=1)
            if t == "capture":
                d.update(color="#1e88e5", sw=0.8, dash="dash")
        self.new_temp(d)

    def constrain_poly(self, last, p):
        if QApplication.keyboardModifiers() & Qt.ShiftModifier:
            return snap_angle(last, p) if self.tool == "wall" else p
        if abs(p.x() - last.x()) >= abs(p.y() - last.y()):
            return QPointF(p.x(), last.y())
        return QPointF(last.x(), p.y())

    def update_poly(self, cur):
        pts = self.poly + [cur]
        self.temp.d["pts"] = [[q.x(), q.y()] for q in pts]
        self.temp.update_geom()

    def finish_poly(self, conn_b=None):
        it = self.temp
        self.temp = None
        pts = []
        for q in self.poly:
            if not pts or q != pts[-1]:
                pts.append(q)
        self.scene().removeItem(it)
        self.poly = []
        if len(pts) >= 2:
            o = pts[0]
            d = dict(it.d)
            d["x"], d["y"] = o.x(), o.y()
            d["pts"] = [[q.x() - o.x(), q.y() - o.y()] for q in pts]
            if d["type"] == "wire":
                if self.conn_a:
                    d["ca"] = list(self.conn_a)
                if conn_b:
                    d["cb"] = list(conn_b)
            self.conn_a = None
            self.mw.add_item(d)
            self.mw.commit()

    def mouseMoveEvent(self, e):
        sp = self.mapToScene(e.position().toPoint())
        self.last_scene_pos = sp
        self.mw.show_coords(sp)
        if self._pan is not None:
            d = e.position() - self._pan
            self._pan = e.position()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - int(d.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - int(d.y()))
            return
        t = self.tool
        if getattr(self, "resizing", None) is not None:
            self.resizing.do_resize(sp, bool(e.modifiers() & Qt.ShiftModifier))
            return
        if t == "select" and not (e.buttons() & Qt.LeftButton):
            self.viewport().setCursor(Qt.SizeFDiagCursor if self.handle_at(e.position()) is not None else Qt.ArrowCursor)
        if t in ("select", "pan"):
            if e.buttons() & Qt.LeftButton:
                self.moved = True
            super().mouseMoveEvent(e)
            return
        if self.ghost is not None:
            self.move_ghost(sp)
            return
        if t in ("wire", "link"):
            pin, conn, item = self.find_pin(sp)
            if pin != self.hover_pin:
                self.hover_pin = pin
                self.viewport().update()
            if t == "link" and self.temp is not None:
                a, ca, ia = self.conn_a
                b = pin if pin is not None else self.snap(sp)
                db = pin_dir(item, conn[1]) if pin is not None else ("h" if pin_dir(ia, ca[1]) == "v" else "v")
                mode = self.mw.route_combo.currentData()
                pts = [a, b] if mode in ("straight", "curve") else route(a, pin_dir(ia, ca[1]), b, db, self.snap)
                self.temp.d["route"] = mode
                self.temp.d["pts"] = [[q.x(), q.y()] for q in pts]
                self.temp.update_geom()
                return
            if t == "wire" and self.temp is not None and pin is not None:
                self.update_poly(QPointF(pin))
                return
        if self.temp is None:
            return
        p = self.snap(sp)
        it = self.temp
        if t in ("wire", "wall"):
            self.update_poly(self.constrain_poly(self.poly[-1], p))
        elif t in ("line", "arrow", "dim"):
            if e.modifiers() & Qt.ShiftModifier:
                p = snap_angle(self.start, p)
            it.d["pts"][1] = [p.x(), p.y()]
            it.update_geom()
        elif t in ("freehand", "highlight", "flying"):
            last = it.d["pts"][-1]
            if math.hypot(sp.x() - last[0], sp.y() - last[1]) > 1.5:
                it.d["pts"].append([sp.x(), sp.y()])
                it.update_geom()
        else:
            x0, y0 = self.start.x(), self.start.y()
            w, h = p.x() - x0, p.y() - y0
            if t == "ellipse" and e.modifiers() & Qt.ShiftModifier:
                m = max(abs(w), abs(h))
                w, h = math.copysign(m, w or 1), math.copysign(m, h or 1)
            it.setPos(min(x0, x0 + w), min(y0, y0 + h))
            it.d["w"], it.d["h"] = max(abs(w), 1), max(abs(h), 1)
            it.update_geom()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MiddleButton:
            self._pan = None
            self.set_tool_cursor()
            return
        t = self.tool
        if getattr(self, "resizing", None) is not None:
            self.resizing = None
            self.mw.commit()
            self.mw.refresh_props()
            return
        if t in ("select", "pan"):
            super().mouseReleaseEvent(e)
            if t == "select":
                self.mw.commit()
            return
        if self.temp is None or t in ("wire", "wall", "link") or e.button() != Qt.LeftButton:
            return
        it = self.temp
        self.temp = None
        self.scene().removeItem(it)
        d = it.to_dict()
        mw = self.mw
        if t == "capture":
            r = QRectF(it.pos().x(), it.pos().y(), d["w"], d["h"])
            if r.width() > 3 and r.height() > 3:
                mw.capture_region(r, e.globalPosition().toPoint())
            return
        if d["type"] in ("line", "dim", "freehand", "highlight"):
            pts = d["pts"]
            if len(pts) < 2 or (len(pts) == 2 and math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]) < 2):
                return
            o = pts[0]
            d["x"], d["y"] = o
            d["pts"] = [[x - o[0], y - o[1]] for x, y in pts]
        elif d["w"] < 3 or d["h"] < 3:
            return
        if t in FIELD_TOOLS:
            if not mw.setup_field(d, t):
                return
        mw.add_item(d)
        mw.commit()

    def contextMenuEvent(self, e):
        """Clic droit sur un élément (outil Sélection) : ordre, rotation, copier, favoris…"""
        if self.tool != "select":
            return
        it = self.itemAt(e.pos())
        if not isinstance(it, PItem):
            return
        mw = self.mw
        if not it.isSelected():
            mw.scene.clearSelection()
            it.setSelected(True)
        m = QMenu(self)
        m.addAction("⬆ " + T("Premier plan")).triggered.connect(lambda: mw.z_selected(1))
        m.addAction("⬇ " + T("Arrière-plan")).triggered.connect(lambda: mw.z_selected(-1))
        m.addSeparator()
        m.addAction(T("Tourner de 90° (sens trigonométrique)    R")).triggered.connect(lambda: mw.rotate_selected(90))
        m.addAction(T("Miroir horizontal (gauche ↔ droite)    H")).triggered.connect(lambda: mw.mirror_selected("fh"))
        m.addSeparator()
        m.addAction(T("Copier")).triggered.connect(mw.copy)
        m.addAction(T("Dupliquer")).triggered.connect(mw.duplicate)
        m.addAction(T("Supprimer")).triggered.connect(mw.delete_selected)
        key = it.d.get("sym") if it.typ == "symbol" else None
        if key:
            m.addSeparator()
            fav = key in mw.favs
            m.addAction(("☆ " + T("Retirer des favoris")) if fav else ("★ " + T("Ajouter aux favoris"))).triggered.connect(
                lambda: mw.toggle_favorite(key))
        if it.typ == "table":
            m.addSeparator()
            m.addAction(T("Modifier le tableau (cases, formules, fusion)…")).triggered.connect(lambda: mw.edit_table(it))
        m.exec(e.globalPos())

    def mouseDoubleClickEvent(self, e):
        if self.tool in ("wire", "wall") and self.temp is not None:
            self.finish_poly()
            return
        if self.tool == "select":
            it = self.itemAt(e.position().toPoint())
            if isinstance(it, PItem) and (it.typ in ("node", "table") or it.typ.startswith("field")):
                self.mw.edit_interactive(it)
                return
            if isinstance(it, PItem) and it.typ == "text":
                txt, ok = TextDialog.get(self, T("Texte"), T("Modifier le texte :"), it.d.get("text", ""))
                if ok:
                    it.d["text"] = txt
                    it.update_geom()
                    self.mw.commit()
                    self.mw.refresh_props()
                return
        super().mouseDoubleClickEvent(e)

    def set_tool_cursor(self):
        self.viewport().setCursor(Qt.ArrowCursor if self.tool in ("select",) else
                                  Qt.OpenHandCursor if self.tool == "pan" else Qt.CrossCursor)

    def keyPressEvent(self, e):
        k, mods = e.key(), e.modifiers()
        if k == Qt.Key_Escape:
            if (getattr(self.mw, "presenting", False) and self.tool == "select" and self.temp is None
                    and self.ghost is None):
                self.mw.toggle_presentation(False)
                return
            if self.tool in ("wire", "wall") and self.temp is not None:
                self.finish_poly()
            self.mw.set_tool("select")
            return
        if k in (Qt.Key_Return, Qt.Key_Enter) and self.temp is not None and self.tool in ("wire", "wall"):
            self.finish_poly()
            return
        if self.ghost is not None and k in (Qt.Key_R, Qt.Key_H, Qt.Key_V, Qt.Key_E):
            g = self.ghost.d
            gs = self.ghost.sym() if self.ghost.typ == "symbol" else None
            if k == Qt.Key_R and gs is not None and getattr(gs, "wall_anchor", None):
                g["_flip180"] = not g.get("_flip180", False)
                self.move_ghost(self.last_scene_pos)
                return
            if k == Qt.Key_R:
                g["angle"] = (g["angle"] + (-90 if mods & Qt.ShiftModifier else 90)) % 360
            elif k == Qt.Key_E:
                g["angle"] = (g["angle"] + (-15 if mods & Qt.ShiftModifier else 15)) % 360
            elif k == Qt.Key_H:
                g["fh"] = not g["fh"]
            else:
                g["fv"] = not g["fv"]
            self.ghost.update_geom()
            self.move_ghost(self.last_scene_pos)
            return
        if self.tool == "select" and self.scene().selectedItems() and not (mods & Qt.ControlModifier):
            mw = self.mw
            if k == Qt.Key_R:
                mw.rotate_selected(-90 if mods & Qt.ShiftModifier else 90)
                return
            if k == Qt.Key_E:
                mw.rotate_selected(-15 if mods & Qt.ShiftModifier else 15)
                return
            if k == Qt.Key_H:
                mw.mirror_selected("fh")
                return
            if k == Qt.Key_V:
                mw.mirror_selected("fv")
                return
            if k in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                st = 0.25 if mods & Qt.ShiftModifier else (self.scene().grid_step if self.scene().snap else 1)
                dx = {Qt.Key_Left: -st, Qt.Key_Right: st}.get(k, 0)
                dy = {Qt.Key_Up: -st, Qt.Key_Down: st}.get(k, 0)
                self.scene().no_snap = bool(mods & Qt.ShiftModifier)
                for it in self.scene().selectedItems():
                    it.moveBy(dx, dy)
                self.scene().no_snap = False
                mw.commit()
                return
        super().keyPressEvent(e)

    # -------------------------------------------------------------- glisser-déposer
    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat(MIME_SYMBOL) or e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        sp = self.mapToScene(e.position().toPoint())
        md = e.mimeData()
        if md.hasFormat(MIME_SYMBOL):
            sid = bytes(md.data(MIME_SYMBOL)).decode()
            d = self.mw.symbol_dict(sid)
            it = PItem(d)
            c = it.local_rect().center()
            p = self.snap(sp - c)
            d["x"], d["y"] = p.x(), p.y()
            self.mw.add_item(d)
            self.mw.commit()
            e.acceptProposedAction()
            return
        for url in md.urls():
            f = url.toLocalFile()
            if f.lower().endswith(convert.IMAGE_EXT):
                self.mw.insert_image_file(f, sp)
            else:
                self.mw.open_file(f)
            break
        e.acceptProposedAction()


class SymbolList(QListWidget):
    def mimeData(self, items):
        md = QMimeData()
        if items:
            md.setData(MIME_SYMBOL, QByteArray(items[0].data(Qt.UserRole).encode()))
        return md

    def mimeTypes(self):
        return [MIME_SYMBOL]


class ColorButton(QPushButton):
    changed = Signal(str)

    def __init__(self, color="#000000"):
        super().__init__()
        self.setFixedWidth(46)
        self.set_color(color)
        self.clicked.connect(self.pick)

    def set_color(self, c):
        self.color = c
        self.setStyleSheet(f"background:{c}; border:1px solid #888; min-height:20px;")

    def pick(self):
        c = QColorDialog.getColor(QColor(self.color), self, T("Couleur"))
        if c.isValid():
            self.set_color(c.name())
            self.changed.emit(c.name())


class Worker(QThread):
    done = Signal(object, object)

    def __init__(self, fn, *a):
        super().__init__()
        self.fn, self.a = fn, a

    def run(self):
        try:
            self.done.emit(self.fn(*self.a), None)
        except Exception as ex:  # noqa
            self.done.emit(None, ex)


# ====================================================================== fenêtre principale
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("Jacques Branas", "PDF DUO")
        self.scene = Scene()
        self.view = View(self)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)
        self.doc = None
        self.path = None
        self.page_items = []
        self.undo_stack, self.undo_idx = [], -1
        self.saved_idx = 0
        self.cur_color, self.cur_sw, self.cur_dash, self.cur_text_size = "#000000", 1.0, "solid", 10.0
        self.cur_color2 = None
        self.text_style = {"font": "Helvetica", "bold": False, "italic": False, "underline": False,
                           "align": "left", "bg": None}
        self.accent = self.settings.value("accent", "#e53935")
        self._updating = False
        self.scene.on_moved = self.symbol_moved
        self.paste_count = 0
        self.workers = []
        self._render_timer = QTimer(self, singleShot=True, interval=80, timeout=self.render_visible)
        self._prop_timer = QTimer(self, singleShot=True, interval=500, timeout=self.commit)
        self.build_ui()
        self.scene.selectionChanged.connect(self.refresh_props)
        self.scene.selectionChanged.connect(self.sync_text_palette)
        self.resize(1400, 900)
        self.new_doc(PAPER["A4 portrait"], 1, ask=False)

    # ------------------------------------------------------------------ interface
    def build_ui(self):
        mb = self.menuBar()

        def act(menu, text, fn, sc=None, tip=None):
            a = QAction(text, self)
            if sc:
                a.setShortcut(QKeySequence(sc))
            if tip:
                a.setStatusTip(tip)
            a.triggered.connect(fn)
            menu.addAction(a)
            return a

        m = mb.addMenu(T("&Fichier"))
        act(m, T("Nouveau…"), lambda: self.new_doc(), "Ctrl+N")
        act(m, T("Ouvrir… (PDF, Word, ODT, images)"), self.open_dialog, "Ctrl+O")
        self.recent_menu = m.addMenu(T("Fichiers récents"))
        self.update_recent()
        m.addSeparator()
        act(m, T("Enregistrer"), self.save, "Ctrl+S")
        act(m, T("Enregistrer sous…"), self.save_as, "Ctrl+Shift+S")
        act(m, T("Exporter un PDF final (aplati, non modifiable)…"), self.export_flat)
        m.addSeparator()
        act(m, T("Imprimer…"), self.print_doc, "Ctrl+P")
        m.addSeparator()
        act(m, T("Quitter"), self.close, "Ctrl+Q")

        m = mb.addMenu(T("&Édition"))
        act(m, T("Annuler"), self.undo, "Ctrl+Z")
        act(m, T("Rétablir"), self.redo, "Ctrl+Y")
        m.addSeparator()
        act(m, T("Couper"), self.cut, "Ctrl+X")
        act(m, T("Copier"), self.copy, "Ctrl+C")
        act(m, T("Coller"), self.paste, "Ctrl+V")
        act(m, T("Dupliquer"), self.duplicate, "Ctrl+D")
        act(m, T("Supprimer"), self.delete_selected, "Del")
        act(m, T("Tout sélectionner"), self.select_all, "Ctrl+A")
        m.addSeparator()
        r = m.addMenu(T("Rotation et miroir"))
        act(r, T("Tourner de 90° (sens trigonométrique)    R"), lambda: self.rotate_selected(90))
        act(r, T("Tourner de 90° (sens horaire)    Maj+R"), lambda: self.rotate_selected(-90))
        act(r, T("Tourner de 15°    E"), lambda: self.rotate_selected(15))
        act(r, T("Tourner de -15°    Maj+E"), lambda: self.rotate_selected(-15))
        act(r, T("Angle précis…"), self.rotate_exact)
        act(r, T("Miroir horizontal (gauche ↔ droite)    H"), lambda: self.mirror_selected("fh"))
        act(r, T("Miroir vertical (haut ↔ bas)    V"), lambda: self.mirror_selected("fv"))
        o = m.addMenu(T("Ordre"))
        act(o, T("Premier plan"), lambda: self.z_selected(1))
        act(o, T("Arrière-plan"), lambda: self.z_selected(-1))

        m = mb.addMenu(T("&Affichage"))
        self.build_spell_menu(m)
        m.addSeparator()
        act(m, T("Zoom +"), lambda: self.view.set_zoom(self.view.zoom() * 1.25), "Ctrl++")
        act(m, T("Zoom −"), lambda: self.view.set_zoom(self.view.zoom() / 1.25), "Ctrl+-")
        act(m, T("Taille réelle (100 %)"), self.zoom_real, "Ctrl+0")
        act(m, T("Pleine largeur"), self.zoom_width, "Ctrl+1")
        act(m, T("Page entière"), self.zoom_page, "Ctrl+2")
        m.addSeparator()
        self.present_action = act(m, T("Mode présentation (plein écran)"), lambda: self.toggle_presentation(), "F11")
        self.present_action.setCheckable(True)
        m.addSeparator()
        self.palettes_menu = m.addMenu(T("Palettes (afficher / masquer)"))
        tm = m.addMenu(T("Thème"))
        tg = QActionGroup(self)
        for name in th.THEMES:
            a = QAction(T(name.capitalize()), self, checkable=True)
            a.setChecked(name == self.settings.value("theme", "bleu nuit"))
            a.triggered.connect(lambda _=False, n=name: self.set_theme(n))
            tg.addAction(a)
            tm.addAction(a)
        am = m.addMenu(T("Couleur d'accent"))
        for name, col in th.ACCENTS.items():
            a = am.addAction(T(name))
            pm = QPixmap(14, 14)
            pm.fill(QColor(col))
            a.setIcon(QIcon(pm))
            a.triggered.connect(lambda _=False, c=col: self.set_accent(c))
        am.addAction(T("Autre couleur…")).triggered.connect(self.pick_accent)
        act(m, T("Couleur du fond de travail…"), self.pick_workspace)
        act(m, T("Fond de travail par défaut"), lambda: self.set_workspace(None))
        lm = m.addMenu(T("Langue / Language / Idioma"))
        lg = QActionGroup(self)
        for code, name in (("fr", "Français"), ("en", "English"), ("es", "Español"), ("pt", "Português"),
                           ("de", "Deutsch"), ("it", "Italiano")):
            a = QAction(name, self, checkable=True)
            a.setChecked(code == self.settings.value("lang", "fr"))
            a.triggered.connect(lambda _=False, c=code: self.set_lang(c))
            lg.addAction(a)
            lm.addAction(a)

        m = mb.addMenu(T("&Pages"))
        act(m, T("Insérer une page blanche après"), self.page_insert_blank)
        act(m, T("Dupliquer la page"), self.page_duplicate)
        act(m, T("Supprimer la page"), self.page_delete)
        act(m, T("Monter la page"), lambda: self.page_move(-1))
        act(m, T("Descendre la page"), lambda: self.page_move(1))
        act(m, T("Pivoter la page à droite"), lambda: self.page_rotate(90))
        act(m, T("Pivoter la page à gauche"), lambda: self.page_rotate(-90))
        m.addSeparator()
        act(m, T("Ajouter un PDF à la fin (fusionner)…"), self.page_merge)
        act(m, T("Extraire des pages vers un nouveau PDF…"), self.page_extract)
        act(m, T("Diviser en un fichier par page…"), self.page_split)

        m = mb.addMenu(T("&Insertion"))
        act(m, T("Signature…"), self.insert_signature, "Ctrl+Shift+G")
        act(m, T("Image…"), self.insert_image_dialog)
        act(m, T("Cartouche (titre, auteur, date, échelle)"), self.insert_title_block)
        act(m, T("Organigramme d'entreprise (modèle à compléter)"), self.insert_orgchart)
        cm = m.addMenu(T("Caractère spécial (Ω, φ, π, √…)"))
        for ch in SPECIAL_CHARS:
            cm.addAction(ch).triggered.connect(lambda _=False, c=ch: self.insert_special(c))
        cm.addSeparator()
        cm.addAction(T("√ sur tout le nombre")).triggered.connect(lambda: self.insert_special("√{}"))
        m.addSeparator()
        act(m, T("GRAFCET : ajouter transition + étape sous la sélection"), self.grafcet_next, "Ctrl+G")

        m = mb.addMenu(T("&Tableau"))
        act(m, T("Insérer un tableau…"), self.insert_table, "Ctrl+Shift+T")
        act(m, T("Modifier le tableau (cases, formules, fusion)…"), lambda: self.table_op("edit"))
        m.addSeparator()
        act(m, T("Ajouter une ligne à la fin"), lambda: self.table_op("row+"))
        act(m, T("Ajouter une colonne à la fin"), lambda: self.table_op("col+"))
        act(m, T("Supprimer la dernière ligne"), lambda: self.table_op("row-"))
        act(m, T("Supprimer la dernière colonne"), lambda: self.table_op("col-"))
        m.addSeparator()
        act(m, T("Calculatrice scientifique et graphique…"), self.open_calculator, "Ctrl+K")

        m = mb.addMenu(T("&Conversions"))
        act(m, T("Convertir Word / ODT en PDF…"), self.conv_office_to_pdf)
        act(m, T("Exporter ce PDF en Word (.docx)…"), lambda: self.conv_pdf_to("docx"))
        act(m, T("Exporter ce PDF en ODT (.odt)…"), lambda: self.conv_pdf_to("odt"))
        act(m, T("Convertir Word ↔ ODT…"), self.conv_word_odt)
        m.addSeparator()
        act(m, T("Images → PDF…"), self.conv_images_to_pdf)
        act(m, T("Exporter les pages en images PNG…"), self.conv_pdf_to_png)

        m = mb.addMenu(T("&Aide"))
        act(m, T("Notice d'utilisation"), self.open_notice, "F1")
        act(m, T("Raccourcis clavier"), self.show_help)
        m.addSeparator()
        act(m, T("Faire un don (Ko-fi)…"), self.donate)
        act(m, T("Site web de PDF DUO"), lambda: self.open_url(SITE_URL))
        act(m, T("Rechercher une nouvelle version"), lambda: self.open_url(RELEASES_URL))
        m.addSeparator()
        act(m, T("À propos de PDF DUO"), self.about)

        # --- barre d'outils principale
        tb = QToolBar(T("Outils"))
        tb.setObjectName("outils")
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb.setIconSize(QSize(22, 22))
        self.addToolBar(Qt.LeftToolBarArea, tb)
        self.tool_group = QActionGroup(self)
        self.tool_actions = {}
        self.tool_bar = tb
        ft = QToolBar(T("Formulaire et signature"))
        ft.setObjectName("formulaire")
        ft.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        ft.setIconSize(QSize(18, 18))
        self.form_bar = ft
        self._plan_actions = []
        for tid, name, tip in TOOLS:
            if tid in ("text", "wire", "capture"):
                tb.addSeparator()
            a = QAction(T(name), self, checkable=True)
            a.setToolTip(T(tip))
            a.setStatusTip(T(tip))
            a.triggered.connect(lambda _=False, t=tid: self.set_tool(t))
            self.tool_group.addAction(a)
            if tid in FIELD_TOOLS:
                ft.addAction(a)
            elif tid in PLAN_TOOLS:
                self._plan_actions.append(a)
            else:
                tb.addAction(a)
            self.tool_actions[tid] = a
        sig = QAction(T("Signature"), self)
        sig.setToolTip(T("Signer : dessiner ou importer sa signature et la poser sur la page"))
        sig.triggered.connect(self.insert_signature)
        ft.addSeparator()
        ft.addAction(sig)
        self.tool_actions["signature"] = sig
        self.tool_actions["select"].setChecked(True)

        qb = QToolBar(T("Accès rapide"))
        qb.setObjectName("rapide")
        qb.setIconSize(QSize(20, 20))
        qb.setMovable(False)
        qb.setStyleSheet("QToolBar { border: none; padding: 0; spacing: 2px; background: transparent; }")
        self.menuBar().setCornerWidget(qb, Qt.TopLeftCorner)
        self.quick_bar = qb
        self.quick_actions = {}
        for key, tip, fn in (("open", "Ouvrir… (PDF, Word, ODT, images)", self.open_dialog), ("save", "Enregistrer", self.save),
                             ("print", "Imprimer…", self.print_doc), ("sep", "", None),
                             ("undo", "Annuler", self.undo), ("redo", "Rétablir", self.redo), ("sep2", "", None),
                             ("zoom_out", "Zoom −", lambda: self.view.set_zoom(self.view.zoom() / 1.25)),
                             ("zoom_in", "Zoom +", lambda: self.view.set_zoom(self.view.zoom() * 1.25)),
                             ("zoom_page", "Page entière", self.zoom_page), ("zoom_width", "Pleine largeur", self.zoom_width)):
            if fn is None:
                qb.addSeparator()
                continue
            a = QAction(T(tip), self)
            a.setToolTip(T(tip))
            a.setData(key)
            a.triggered.connect(fn)
            qb.addAction(a)
            self.quick_actions[key] = a
        pres_btn = QToolButton(text=" ⛶ ")
        pres_btn.setToolTip(T("Mode présentation (plein écran) — F11 ; Échap pour quitter"))
        pres_btn.clicked.connect(lambda: self.toggle_presentation())
        self._pres_btn = pres_btn
        sym_btn = QToolButton(text=" Ω √ ")
        sym_btn.setToolTip(T("Caractères spéciaux (Ω, φ, π, √…) : insérés dans le texte sélectionné ou le champ actif"))
        sym_btn.setPopupMode(QToolButton.InstantPopup)
        sm = QMenu(sym_btn)
        for ch in SPECIAL_CHARS:
            sm.addAction(ch).triggered.connect(lambda _=False, c=ch: self.insert_special(c))
        sm.addSeparator()
        sm.addAction(T("√ sur tout le nombre")).triggered.connect(lambda: self.insert_special("√{}"))
        sym_btn.setMenu(sm)
        calc_btn = QToolButton(text=" " + T("Calc") + " ")
        calc_btn.setToolTip(T("Calculatrice scientifique et graphique…") + "  (Ctrl+K)")
        calc_btn.clicked.connect(self.open_calculator)
        qb.addSeparator()
        qb.addWidget(sym_btn)
        qb.addWidget(calc_btn)
        qb.addWidget(pres_btn)

        st = QToolBar(T("Style"))
        st.setObjectName("style")
        self.addToolBar(st)
        self.addToolBar(ft)
        st.addWidget(QLabel(T(" Couleur ")))
        self.color_btn = ColorButton(self.cur_color)
        self.color_btn.changed.connect(self.set_cur_color)
        st.addWidget(self.color_btn)
        st.addWidget(QLabel(T("  Trait ")))
        self.sw_spin = QDoubleSpinBox(decimals=2, minimum=0.1, maximum=20, singleStep=0.25, value=1.0, suffix=" pt")
        self.sw_spin.valueChanged.connect(lambda v: setattr(self, "cur_sw", v))
        st.addWidget(self.sw_spin)
        self.dash_combo = QComboBox()
        for k, v in (("solid", "Continu"), ("dash", "Tirets"), ("dot", "Pointillés"), ("dashdot", "Mixte")):
            self.dash_combo.addItem(T(v), k)
        self.dash_combo.currentIndexChanged.connect(lambda i: setattr(self, "cur_dash", self.dash_combo.itemData(i)))
        st.addWidget(self.dash_combo)
        st.addWidget(QLabel(T("  Conducteur ")))
        self.cond_combo = QComboBox()
        self.cond_combo.addItem(T("Couleur libre"), None)
        for name, c1, c2 in CONDUCTORS:
            pm = QPixmap(26, 12)
            pm.fill(QColor(c1))
            if c2:
                pp = QPainter(pm)
                for x in range(3, 26, 8):
                    pp.fillRect(x, 0, 4, 12, QColor(c2))
                pp.end()
            self.cond_combo.addItem(QIcon(pm), T(name), (c1, c2))
        self.cond_combo.setToolTip(T("Couleur normalisée du fil (appliquée aux fils sélectionnés et aux prochains)"))
        self.cond_combo.currentIndexChanged.connect(self.set_conductor)
        st.addWidget(self.cond_combo)
        st.addWidget(QLabel(T("  Liaison ")))
        self.route_combo = QComboBox()
        for k, v in (("ortho", "Angles droits"), ("straight", "Droite"), ("curve", "Courbe")):
            self.route_combo.addItem(T(v), k)
        self.route_combo.setToolTip(T("Forme des liaisons (outil Liaison) : angles droits pour les schémas et le GRAFCET, courbe pour les cartes mentales"))
        st.addWidget(self.route_combo)
        self.arrow_cb = QCheckBox(T("Flèche"))
        self.arrow_cb.setToolTip(T("Ajouter une flèche au bout des liaisons (algorigramme, renvois GRAFCET)"))
        st.addWidget(self.arrow_cb)

        # --- palette d'écriture
        wt = QToolBar(T("Écriture"))
        wt.setObjectName("ecriture")
        self.addToolBarBreak()
        self.addToolBar(wt)
        self.write_bar = wt
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Helvetica"))
        self.font_combo.setMaximumWidth(190)
        self.font_combo.currentFontChanged.connect(lambda f: self.set_text_style("font", f.family()))
        wt.addWidget(self.font_combo)
        self.ts_spin = QDoubleSpinBox(decimals=1, minimum=3, maximum=200, value=10, suffix=" pt")
        self.ts_spin.valueChanged.connect(self.set_text_size)
        wt.addWidget(self.ts_spin)
        self.style_actions = {}
        for key, ic, tip, sc in (("bold", "bold", "Gras", "Ctrl+B"), ("italic", "italic", "Italique", "Ctrl+I"),
                                 ("underline", "underline", "Souligné", "Ctrl+U")):
            a = QAction(T(tip), self, checkable=True)
            a.setShortcut(QKeySequence(sc))
            a.setToolTip(f"{T(tip)} ({sc})")
            a.setData(ic)
            a.toggled.connect(lambda v, k=key: self.set_text_style(k, v))
            wt.addAction(a)
            self.style_actions[key] = a
        wt.addSeparator()
        ag = QActionGroup(self)
        for key, ic, tip in (("left", "align_left", "Aligner à gauche"), ("center", "align_center", "Centrer"),
                             ("right", "align_right", "Aligner à droite")):
            a = QAction(T(tip), self, checkable=True)
            a.setData(ic)
            a.setChecked(key == "left")
            a.triggered.connect(lambda _=False, k=key: self.set_text_style("align", k))
            ag.addAction(a)
            wt.addAction(a)
            self.style_actions["align_" + key] = a
        wt.addSeparator()
        wt.addWidget(QLabel(T("Couleur")))
        self.text_color_btn = ColorButton("#000000")
        self.text_color_btn.changed.connect(self.set_text_color)
        wt.addWidget(self.text_color_btn)
        wt.addWidget(QLabel(T("Surligner")))
        self.hl_combo = QComboBox()
        self.hl_combo.addItem(T("Aucun"), None)
        for name, col in (("Jaune", "#fff176"), ("Vert", "#a5f3a1"), ("Bleu", "#9fd3ff"), ("Rose", "#ffb3d9"),
                          ("Orange", "#ffcc80")):
            pm = QPixmap(14, 14)
            pm.fill(QColor(col))
            self.hl_combo.addItem(QIcon(pm), T(name), col)
        self.hl_combo.setToolTip(T("Surligner le texte (fond coloré derrière les lettres)"))
        self.hl_combo.currentIndexChanged.connect(lambda i: self.set_text_style("bg", self.hl_combo.itemData(i)))
        wt.addWidget(self.hl_combo)
        wsym = QToolButton(text=" Ω φ π √ ")
        wsym.setToolTip(T("Caractères spéciaux (Ω, φ, π, √…) : insérés dans le texte sélectionné ou le champ actif"))
        wsym.setPopupMode(QToolButton.InstantPopup)
        wm = QMenu(wsym)
        for ch in SPECIAL_CHARS:
            wm.addAction(ch).triggered.connect(lambda _=False, c=ch: self.insert_special(c))
        wm.addSeparator()
        wm.addAction(T("√ sur tout le nombre")).triggered.connect(lambda: self.insert_special("√{}"))
        wsym.setMenu(wm)
        wt.addWidget(wsym)
        hl = QAction(T("Surligneur libre"), self)
        hl.setData("highlight")
        hl.setToolTip(T("Outil surligneur (passer sur n'importe quelle zone de la page)"))
        hl.triggered.connect(lambda: self.set_tool("highlight"))
        wt.addAction(hl)

        gt = QToolBar(T("Plan, grille et échelle"))
        gt.setObjectName("grille")
        gt.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        gt.setIconSize(QSize(18, 18))
        self.addToolBar(gt)
        for a in self._plan_actions:
            gt.addAction(a)
        gt.addSeparator()
        st = gt
        self.grid_cb = QCheckBox(T("Grille"))
        self.grid_cb.setChecked(True)
        self.grid_cb.toggled.connect(self.toggle_grid)
        st.addWidget(self.grid_cb)
        self.snap_cb = QCheckBox(T("Aimanter"))
        self.snap_cb.setChecked(True)
        self.snap_cb.setToolTip(T("Aligne les points sur la grille (maintenir Alt pour désactiver)"))
        self.snap_cb.toggled.connect(lambda v: setattr(self.scene, "snap", v))
        st.addWidget(self.snap_cb)
        self.grid_combo = QComboBox()
        for lab, val in (("Pas 2,5 mm (schémas)", ("mm", 2.5)), ("Pas 5 mm", ("mm", 5)), ("Pas 1 mm", ("mm", 1)),
                         ("Pas 10 cm réels", ("cm", 10)), ("Pas 25 cm réels", ("cm", 25)), ("Pas 50 cm réels", ("cm", 50))):
            self.grid_combo.addItem(T(lab), val)
        self.grid_combo.currentIndexChanged.connect(self.update_grid_step)
        st.addWidget(self.grid_combo)
        st.addSeparator()
        st.addWidget(QLabel(T(" Échelle du plan 1/")))
        self.scale_combo = QComboBox(editable=True)
        for v in ("20", "50", "75", "100", "200", "500"):
            self.scale_combo.addItem(v)
        self.scale_combo.setCurrentText("50")
        self.scale_combo.currentTextChanged.connect(self.set_plan_scale)
        st.addWidget(self.scale_combo)
        st.addWidget(QLabel(T("  Mur ")))
        self.wall_thick = QDoubleSpinBox(decimals=0, minimum=3, maximum=80, value=20, suffix=" cm")
        self.wall_thick.setToolTip(T("Épaisseur des murs dessinés (20 cm mur extérieur, 7 cm cloison)"))
        st.addWidget(self.wall_thick)
        self.style_bar = self.findChild(QToolBar, "style")
        self.grid_bar = gt

        # --- bibliothèque
        dock = QDockWidget(T("Bibliothèque de symboles"), self)
        dock.setObjectName("biblio")
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        self.favs = [x for x in (self.settings.value("favoris") or []) if isinstance(x, str)]
        self.fav_cats = [x for x in (self.settings.value("categories_favorites") or []) if x in CATEGORIES]
        self.cat_combo = QComboBox()
        self.fill_categories()
        self.cat_combo.setCurrentIndex(1 if self.favs else 2)
        self.cat_combo.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.cat_combo.setMinimumContentsLength(12)
        self.search = QLineEdit(placeholderText=T("Rechercher (prise, contact, porte…)"))
        self.sym_list = SymbolList()
        self.sym_list.setViewMode(QListView.IconMode)
        self.sym_list.setIconSize(QSize(52, 52))
        self.sym_list.setGridSize(QSize(92, 96))
        self.sym_list.setWordWrap(True)
        self.sym_list.setResizeMode(QListView.Adjust)
        self.sym_list.setMovement(QListView.Static)
        self.sym_list.setDragEnabled(True)
        self.sym_list.setDragDropMode(QAbstractItemView.DragOnly)
        self.sym_list.itemClicked.connect(self.pick_symbol)
        self.sym_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sym_list.customContextMenuRequested.connect(self.symbol_menu)
        self.sym_list.setToolTip(T("Clic droit sur un symbole : ajouter aux favoris ou les retirer"))
        self._icons = {}
        self.cat_combo.currentIndexChanged.connect(self.fill_symbols)
        self.search.textChanged.connect(self.fill_symbols)
        crow = QHBoxLayout()
        crow.setSpacing(2)
        crow.addWidget(self.cat_combo, 1)
        self.cat_star = QToolButton(text="☆")
        self.cat_star.setToolTip(T("Mettre cette bibliothèque en favori (en tête de liste)"))
        self.cat_star.clicked.connect(self.toggle_fav_category)
        crow.addWidget(self.cat_star)
        lay.addLayout(crow)
        lay.addWidget(self.search)
        lay.addWidget(self.sym_list)
        hint = QLabel(T("Cliquer puis poser sur la page (R : tourner 90°, E : 15°, H / V : miroir, Échap : fin), "
                      "ou glisser-déposer."))
        hint.setWordWrap(True)
        hint.setStyleSheet("color:#666; font-size:11px;")
        lay.addWidget(hint)
        dock.setWidget(w)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.fill_symbols()

        # --- propriétés
        pd = QDockWidget(T("Propriétés"), self)
        pd.setObjectName("props")
        self.props_area = QScrollArea()
        self.props_area.setWidgetResizable(True)
        pd.setWidget(self.props_area)
        self.addDockWidget(Qt.RightDockWidgetArea, pd)
        self.refresh_props()
        self._right_docks = (dock, pd)

        # --- pages
        pg = QDockWidget(T("Pages"), self)
        pg.setObjectName("pages")
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        self.thumbs = QListWidget()
        w.setMaximumWidth(240)
        self.thumbs.setIconSize(QSize(110, 140))
        self.thumbs.setViewMode(QListView.ListMode)
        self.thumbs.itemClicked.connect(lambda it: self.goto_page(self.thumbs.row(it)))
        lay.addWidget(self.thumbs)
        row = QHBoxLayout()
        for txt, tip, fn in (("＋", "Insérer une page blanche", self.page_insert_blank),
                             ("✕", "Supprimer la page", self.page_delete),
                             ("▲", "Monter", lambda: self.page_move(-1)), ("▼", "Descendre", lambda: self.page_move(1)),
                             ("⟳", "Pivoter à droite", lambda: self.page_rotate(90))):
            b = QToolButton(text=txt, toolTip=tip)
            b.clicked.connect(fn)
            row.addWidget(b)
        lay.addLayout(row)
        pg.setWidget(w)
        self.addDockWidget(Qt.LeftDockWidgetArea, pg)

        # --- formulaires
        fd = QDockWidget(T("Formulaire"), self)
        fd.setObjectName("forms")
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.addWidget(QLabel(T("Champs du PDF (double-clic sur la valeur pour remplir) :")))
        self.form_table = QTableWidget(0, 3)
        self.form_table.setHorizontalHeaderLabels([T("Champ"), T("Type"), T("Valeur")])
        self.form_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.form_table.itemChanged.connect(self.form_value_changed)
        lay.addWidget(self.form_table)
        fd.setWidget(w)
        self.addDockWidget(Qt.LeftDockWidgetArea, fd)
        self.tabifyDockWidget(pg, fd)
        pg.raise_()

        for wdg in (self.tool_bar, self.style_bar, self.form_bar, self.write_bar, self.grid_bar, dock, pd, pg, fd):
            a = wdg.toggleViewAction()
            a.setText(wdg.windowTitle())
            self.palettes_menu.addAction(a)
        self.coord_label = QLabel()
        self.zoom_label = QLabel()
        self.statusBar().addPermanentWidget(self.coord_label)
        self.statusBar().addPermanentWidget(self.zoom_label)
        def sizes():
            self.resizeDocks(list(self._right_docks), [480, 420], Qt.Vertical)
            self.resizeDocks([pg, self._right_docks[0]], [190, 300], Qt.Horizontal)
        if not self.settings.value("state"):
            QTimer.singleShot(0, sizes)
        geo = self.settings.value("geometry")
        if geo:
            self.restoreGeometry(geo)
        stt = self.settings.value("state")
        if stt:
            self.restoreState(stt, 4)
        self.apply_theme()

    # ------------------------------------------------------------------ bibliothèque
    def fill_symbols(self):
        """Remplit la bibliothèque : les favoris passent toujours en tête (catégorie ★ Favoris à part)."""
        self.sym_list.clear()
        data = self.cat_combo.currentData()
        only_favs = data == "__fav__"
        cat = T(data) if data and data != "__fav__" else T("Tous les symboles")
        if hasattr(self, "cat_star"):
            self.cat_star.setText("★" if data in getattr(self, "fav_cats", []) else "☆")
            self.cat_star.setEnabled(bool(data) and data != "__fav__")
        q = self.search.text().strip().lower()
        favs = getattr(self, "favs", [])
        rows = []
        for s in SYMBOLS:
            if only_favs and not q and s.id not in favs:
                continue
            if not q and not only_favs and cat != T("Tous les symboles") and T(s.cat) != cat:
                continue
            if q and q not in s.name.lower() and q not in T(s.name).lower() and q not in s.id:
                continue
            rows.append((s.id, T(s.name), lambda s=s: sym_icon(s, color=getattr(self, "icon_color", "#202020"))))
        for pr in ND.PRESETS:
            key = "node:" + pr.id
            if only_favs and not q and key not in favs:
                continue
            if not q and not only_favs and cat != T("Tous les symboles") and T(pr.cat) != cat:
                continue
            if q and q not in pr.name.lower() and q not in T(pr.name).lower():
                continue
            rows.append((key, T(pr.name), lambda pr=pr: node_icon({**pr.d, "color": getattr(self, "icon_color", "#202020")})))
        order = {k: i for i, k in enumerate(favs)}
        rows.sort(key=lambda r: (0, order[r[0]]) if r[0] in order else (1, 0))
        for key, name, make in rows:
            if key not in self._icons:
                self._icons[key] = make()
            icon = self._icons[key]
            if key in order:
                if ("★", key) not in self._icons:
                    self._icons[("★", key)] = star_icon(icon)
                icon = self._icons[("★", key)]
            it = QListWidgetItem(icon, name)
            it.setData(Qt.UserRole, key)
            it.setToolTip(name + ("  ★" if key in order else ""))
            self.sym_list.addItem(it)
        if only_favs and not rows:
            it = QListWidgetItem(T("Aucun favori : clic droit sur un symbole › Ajouter aux favoris"))
            it.setFlags(Qt.NoItemFlags)
            self.sym_list.addItem(it)

    def fill_categories(self, keep=None):
        """Liste des bibliothèques : Tous, ★ Favoris, puis les bibliothèques favorites, puis les autres."""
        cb = self.cat_combo
        cb.blockSignals(True)
        cb.clear()
        cb.addItem(T("Tous les symboles"), None)
        cb.addItem("★ " + T("Favoris"), "__fav__")
        for c in self.fav_cats:
            cb.addItem("★ " + T(c), c)
        for c in CATEGORIES:
            if c not in self.fav_cats:
                cb.addItem(T(c), c)
        if keep is not None:
            i = cb.findData(keep)
            cb.setCurrentIndex(i if i >= 0 else 0)
        cb.blockSignals(False)

    def toggle_fav_category(self):
        c = self.cat_combo.currentData()
        if not c or c == "__fav__":
            return
        if c in self.fav_cats:
            self.fav_cats.remove(c)
        else:
            self.fav_cats.append(c)
        self.settings.setValue("categories_favorites", list(self.fav_cats))
        self.fill_categories(keep=c)
        self.fill_symbols()

    def symbol_menu(self, pos):
        it = self.sym_list.itemAt(pos)
        key = it.data(Qt.UserRole) if it else None
        if not key:
            return
        m = QMenu(self)
        if key in self.favs:
            a = m.addAction("☆ " + T("Retirer des favoris"))
        else:
            a = m.addAction("★ " + T("Ajouter aux favoris"))
        if m.exec(self.sym_list.viewport().mapToGlobal(pos)) is a:
            self.toggle_favorite(key)

    def toggle_favorite(self, key):
        if key in self.favs:
            self.favs.remove(key)
        else:
            self.favs.append(key)
        self.settings.setValue("favoris", list(self.favs))
        self.fill_symbols()

    def symbol_dict(self, sid):
        if sid.startswith("node:"):
            d = json.loads(json.dumps(ND.BY_ID[sid[5:]].d))
            d.update(x=0, y=0)
            if ND.BY_ID[sid[5:]].cat == ND.ORG and d.get("text"):
                d["text"] = "\n".join(T(x) for x in d["text"].split("\n"))
            if d.get("shape") in ("step", "step_init"):
                nums = [int(i.d["text"]) for i in self.items() if i.typ == "node"
                        and i.d.get("shape") in ("step", "step_init", "step_cond") and str(i.d.get("text", "")).isdigit()]
                if nums:
                    d["text"] = str(max(nums) + 1)
            return d
        s = BY_ID[sid]
        d = {"type": "symbol", "sym": sid, "x": 0, "y": 0, "color": self.cur_color,
             "sw": self.cur_sw if s.kind == "paper" else 0.7, "scale": getattr(s, "default_scale", 1.0),
             "label": self.next_label(getattr(s, "default_label", "")),
             "pins": s.pin_names}
        if s.params:
            d["params"] = s.defaults()
            if "mur" in d["params"]:
                d["params"]["mur"] = self.wall_thick.value()
        return d

    def next_label(self, base):
        """KM1 -> KM2 si KM1 existe déjà avec un autre symbole du même genre ? On garde le repère proposé."""
        return base

    def pick_symbol(self, it):
        sid = it if isinstance(it, str) else it.data(Qt.UserRole)
        self.set_tool("symbol_place")
        self.view.set_ghost(self.symbol_dict(sid))
        self.view.setFocus()
        if sid in ("porte", "porte_double", "fenetre1", "fenetre2", "baie", "porte_coul", "porte_garage"):
            self.statusBar().showMessage(T("Passer sur un mur : l'ouverture s'y aligne toute seule. H / V : changer le sens d'ouverture."))
        else:
            self.statusBar().showMessage(T("Cliquer pour poser — R / E tourner, H / V miroir, Échap pour finir"))

    # ------------------------------------------------------------------ outils
    def set_tool(self, t):
        opening = {"door": "porte", "door2": "porte_double", "window": "fenetre2"}.get(t)
        if opening:
            self.pick_symbol(opening)
            self.tool_actions[t].setChecked(True)
            return
        self.view.set_tool(t)
        if t in self.tool_actions:
            self.tool_actions[t].setChecked(True)
        else:
            chk = self.tool_group.checkedAction()
            if chk:
                chk.setChecked(False)
        if t == "wall":
            self.grid_combo.setCurrentIndex(3)
        self.view.setFocus()

    def set_cur_color(self, c):
        self.cur_color = c
        sel = self.selected()
        if sel:
            for it in sel:
                it.d["color"] = c
                it.update_geom()
            self.commit()
            self.refresh_props()

    def toggle_grid(self, v):
        self.scene.show_grid = v
        self.view.viewport().update()

    def update_grid_step(self):
        unit, val = self.grid_combo.currentData()
        self.scene.grid_step = val * MM if unit == "mm" else val * pts_per_cm(self.scene.plan_denom)
        self.view.viewport().update()

    def set_plan_scale(self, txt):
        try:
            v = int(txt)
        except ValueError:
            return
        if v <= 0:
            return
        self.scene.plan_denom = v
        for it in self.items():
            it.update_geom()
        self.update_grid_step()
        self.commit()

    # ------------------------------------------------------------------ apparence
    def apply_theme(self):
        t = self.settings.value("theme", "bleu nuit")
        if t not in th.THEMES:
            t = "clair"
        app = QApplication.instance()
        app.setStyle("Fusion")
        app.setPalette(th.palette(t, self.accent))
        app.setStyleSheet(th.stylesheet(t, self.accent))
        col = th.THEMES[t]["text"]
        for tid, a in self.tool_actions.items():
            a.setIcon(make_icon(tid, col))
        for a in self.write_bar.actions():
            if a.data():
                a.setIcon(make_icon(a.data(), col))
        for k, a in self.quick_actions.items():
            a.setIcon(make_icon(k, col))
        self.icon_color = col
        self._icons = {}
        self.fill_symbols()
        work = self.settings.value("workspace") or th.THEMES[t]["work"]
        self.scene.setBackgroundBrush(QColor(work))
        self.view.viewport().update()

    def insert_special(self, ch):
        w = QApplication.focusWidget()
        if isinstance(w, QLineEdit):
            w.insert(ch)
            return
        if isinstance(w, QPlainTextEdit):
            w.insertPlainText(ch)
            return
        sel = [i for i in self.selected() if i.typ in ("text", "node")]
        if sel:
            for it in sel:
                it.d["text"] = (it.d.get("text") or "") + ch
                it.update_geom()
            self.commit()
            self.refresh_props()
            return
        c = self.view.mapToScene(self.view.viewport().rect().center())
        self.add_item({"type": "text", "x": c.x(), "y": c.y(), "text": ch, "size": self.cur_text_size,
                       "color": self.cur_color, **self.text_style}, select=True)
        self.commit()

    def set_theme(self, name):
        self.settings.setValue("theme", name)
        self.apply_theme()

    def set_accent(self, c):
        self.accent = c
        self.settings.setValue("accent", c)
        self.apply_theme()

    def pick_accent(self):
        c = QColorDialog.getColor(QColor(self.accent), self, T("Couleur d'accent"))
        if c.isValid():
            self.set_accent(c.name())

    def pick_workspace(self):
        c = QColorDialog.getColor(self.scene.backgroundBrush().color(), self, "Fond de travail")
        if c.isValid():
            self.set_workspace(c.name())

    def set_workspace(self, c):
        if c:
            self.settings.setValue("workspace", c)
        else:
            self.settings.remove("workspace")
        self.apply_theme()

    def set_lang(self, code):
        self.settings.setValue("lang", code)
        from .i18n import set_language
        set_language(code)
        QMessageBox.information(self, APP_NAME, T("La nouvelle langue sera appliquée au prochain démarrage de PDF DUO."))

    def set_conductor(self, i):
        data = self.cond_combo.itemData(i)
        if not data:
            self.cur_color2 = None
            return
        c1, c2 = data
        self.cur_color, self.cur_color2 = c1, c2
        self.color_btn.set_color(c1)
        sel = [it for it in self.selected() if it.typ in ("wire", "line")]
        for it in sel:
            it.d["color"], it.d["color2"] = c1, c2
            it.update_geom()
        if sel:
            self.commit()
            self.refresh_props()

    def selected_texts(self):
        return [i for i in self.selected() if i.typ == "text"]

    def set_text_style(self, key, val):
        self.text_style[key] = val
        sel = self.selected_texts()
        for it in sel:
            it.d[key] = val
            it.update_geom()
        if sel:
            self._prop_timer.start()

    def set_text_size(self, v):
        self.cur_text_size = v
        sel = self.selected_texts()
        for it in sel:
            it.d["size"] = v
            it.update_geom()
        if sel:
            self._prop_timer.start()

    def set_text_color(self, c):
        sel = self.selected_texts()
        if sel:
            for it in sel:
                it.d["color"] = c
                it.update_geom()
            self._prop_timer.start()
        else:
            self.cur_color = c
            self.color_btn.set_color(c)

    def sync_text_palette(self):
        """Quand on sélectionne un texte, la palette d'écriture affiche son style."""
        sel = self.selected_texts()
        if not sel:
            return
        d = sel[0].d
        widgets = [self.font_combo, self.ts_spin, self.hl_combo] + list(self.style_actions.values())
        for w in widgets:
            w.blockSignals(True)
        self.font_combo.setCurrentFont(QFont(d.get("font", "Helvetica")))
        self.ts_spin.setValue(d.get("size", 10))
        for k in ("bold", "italic", "underline"):
            self.style_actions[k].setChecked(bool(d.get(k)))
        self.style_actions["align_" + d.get("align", "left")].setChecked(True)
        self.hl_combo.setCurrentIndex(max(0, self.hl_combo.findData(d.get("bg"))))
        self.text_color_btn.set_color(d.get("color", "#000000"))
        for w in widgets:
            w.blockSignals(False)

    # ------------------------------------------------------------------ zones interactives
    def setup_field(self, d, t):
        n = len([i for i in self.items() if i.typ.startswith("field")]) + 1
        if t == "field_link":
            txt, ok = QInputDialog.getText(self, T("Lien"), T("Adresse web (https://…) ou numéro de page :"), text="1")
            if not ok or not txt.strip():
                return False
            txt = txt.strip()
            if txt.isdigit():
                d["page"] = int(txt)
            else:
                d["url"] = txt if "://" in txt or txt.startswith("mailto:") else "https://" + txt
            return True
        label = {"field_radio": "Nom du groupe (les boutons d'un même groupe s'excluent) :"}.get(t, "Nom du champ :")
        dflt = "choix" if t == "field_radio" else ("signature" if t == "field_sig" else f"champ{n}")
        name, ok = QInputDialog.getText(self, T("Zone interactive"), label, text=dflt)
        if not ok or not name:
            return False
        d["name"] = name
        if t == "field_combo":
            opts, ok = QInputDialog.getText(self, T("Liste déroulante"), T("Choix proposés (séparés par des virgules) :"),
                                            text="Oui, Non")
            if not ok:
                return False
            d["options"] = [o.strip() for o in opts.split(",") if o.strip()]
            d["value"] = d["options"][0] if d["options"] else ""
        else:
            d["value"] = "" if t in ("field_text", "field_sig") else False
        return True

    def edit_interactive(self, it):
        """Double-clic : modifier le texte d'une forme, remplir un champ, signer, suivre un lien."""
        t, d = it.typ, it.d
        if t == "table":
            self.edit_table(it)
            return
        if t == "node" and d.get("shape") == "cartouche":
            if self.edit_cartouche(d):
                it.update_geom()
                self.commit()
                self.refresh_props()
            return
        if t == "node":
            txt, ok = TextDialog.get(self, T("Texte"), T("Texte de la forme :"), d.get("text", ""))
            if ok:
                d["text"] = txt
                it.update_geom()
                self.commit()
                self.refresh_props()
            return
        if t == "field_text":
            v, ok = QInputDialog.getText(self, d.get("name", ""), T("Valeur :"), text=d.get("value", ""))
            if ok:
                d["value"] = v
        elif t == "field_combo":
            opts = d.get("options") or [""]
            cur = opts.index(d["value"]) if d.get("value") in opts else 0
            v, ok = QInputDialog.getItem(self, d.get("name", ""), T("Choix :"), opts, cur, False)
            if ok:
                d["value"] = v
        elif t == "field_check":
            d["value"] = not d.get("value")
        elif t == "field_radio":
            for o in self.items():
                if o.typ == "field_radio" and o.d.get("name") == d.get("name"):
                    o.d["value"] = False
                    o.update()
            d["value"] = True
        elif t == "field_sig":
            dlg = SignatureDialog(self)
            if dlg.exec() and dlg.img is not None:
                img = dlg.img
                r = QRectF(it.pos(), QSizeF(d["w"], d["h"]))
                k = min(r.width() / img.width(), r.height() / img.height())
                w, h = img.width() * k, img.height() * k
                self.add_item({"type": "image", "x": r.center().x() - w / 2, "y": r.center().y() - h / 2,
                               "w": w, "h": h, "png": image_to_b64(img), "sw": 0})
                self.scene.removeItem(it)
                self.commit()
                return
        elif t == "field_link":
            if d.get("url"):
                self.open_link_safely(d["url"])
            else:
                self.goto_page(int(d.get("page") or 1) - 1)
            return
        it.update()
        self.commit()
        self.refresh_forms()
        self.refresh_props()

    def grafcet_next(self):
        """Ajoute sous l'étape (ou la transition) sélectionnée : transition + étape suivante, reliées."""
        sel = [i for i in self.selected() if i.typ == "node" and i.d.get("shape") in ("step", "step_init", "step_cond", "transition")]
        if not sel:
            QMessageBox.information(self, APP_NAME, T("Sélectionner d'abord une étape (ou une transition) du GRAFCET."))
            return
        src = sel[0]
        gap = 4 * MM
        x_mid = src.mapToScene(src.local_rect().center()).x()
        bottom = src.pins_scene()[2] if src.d.get("shape") != "transition" else src.pins_scene()[1]
        new = []
        prev, prev_pin = src, (2 if src.d.get("shape") != "transition" else 1)
        y = bottom.y() + gap
        if src.d.get("shape") != "transition":
            n_tr = len([i for i in self.items() if i.typ == "node" and i.d.get("shape") == "transition"]) + 1
            tr = dict(ND.BY_ID["g_transition"].d)
            tr.update(x=x_mid - tr["w"] / 2, y=y, text=f"a{n_tr}", label=f"({n_tr})")
            tri = self.add_item(tr)
            self.add_link(prev, prev_pin, tri, 0)
            prev, prev_pin = tri, 1
            y = tri.pins_scene()[1].y() + gap
            new.append(tri)
        nums = [int(i.d["text"]) for i in self.items() if i.typ == "node"
                and i.d.get("shape") in ("step", "step_init", "step_cond") and str(i.d.get("text", "")).isdigit()]
        st = dict(ND.BY_ID["g_step"].d)
        st.update(x=x_mid - st["w"] / 2, y=y, text=str(max(nums + [0]) + 1))
        sti = self.add_item(st)
        self.add_link(prev, prev_pin, sti, 0)
        new.append(sti)
        self.scene.clearSelection()
        self.set_tool("select")
        sti.setSelected(True)
        self.commit()

    def add_link(self, a, ia, b, ib, route_mode="ortho", arrow="none"):
        pa, pb = a.pins_scene()[ia], b.pins_scene()[ib]
        pts = [pa, pb] if abs(pa.x() - pb.x()) < 0.01 or route_mode != "ortho" else route(pa, "v", pb, "v")
        o = pts[0]
        return self.add_item({"type": "wire", "x": o.x(), "y": o.y(), "pts": [[q.x() - o.x(), q.y() - o.y()] for q in pts],
                              "color": "#000000", "sw": 1.0, "ca": [a.d["uid"], ia], "cb": [b.d["uid"], ib],
                              "route": route_mode, "arrow": arrow})

    # ------------------------------------------------------------------ liaisons
    def symbol_moved(self, item):
        if not self._updating:
            self.update_connections(item.d.get("uid"))

    def update_connections(self, only_uid=None):
        """Les fils accrochés suivent les bornes des symboles."""
        self._updating = True
        try:
            syms = {i.d["uid"]: i for i in self.items() if i.typ in ("symbol", "node")}
            for w in self.items():
                if w.typ != "wire" or not (w.d.get("ca") or w.d.get("cb")):
                    continue
                if only_uid and only_uid not in ((w.d.get("ca") or [None])[0], (w.d.get("cb") or [None])[0]):
                    continue
                pos = w.pos()
                P = [QPointF(x + pos.x(), y + pos.y()) for x, y in w.d["pts"]]
                changed = False
                for key, idx in (("ca", 0), ("cb", -1)):
                    c = w.d.get(key)
                    if not c or c[0] not in syms:
                        continue
                    pins = syms[c[0]].pins_scene()
                    if c[1] >= len(pins):
                        continue
                    q = pins[c[1]]
                    i = idx if idx == 0 else len(P) - 1
                    if abs(P[i].x() - q.x()) < 0.01 and abs(P[i].y() - q.y()) < 0.01:
                        continue
                    changed = True
                    if w.d.get("route") in ("straight", "curve"):
                        P[i] = q
                    elif len(P) == 2:
                        o = P[1 - i]
                        P[i] = q
                        if abs(q.x() - o.x()) > 0.01 and abs(q.y() - o.y()) > 0.01:
                            bend = QPointF(o.x(), q.y())
                            P.insert(1, bend)
                    else:
                        j = 1 if i == 0 else len(P) - 2
                        n = P[j]
                        if abs(P[i].y() - n.y()) < 0.01:
                            P[j] = QPointF(n.x(), q.y())
                        else:
                            P[j] = QPointF(q.x(), n.y())
                        P[i] = q
                if changed:
                    w.d["pts"] = [[q.x() - pos.x(), q.y() - pos.y()] for q in P]
                    w.update_geom()
        finally:
            self._updating = False

    def update_junctions(self):
        """Points de jonction automatiques là où un fil arrive au milieu d'un autre ou quand 3 fils se rejoignent."""
        wires = [w for w in self.items() if w.typ == "wire"]
        polys = []
        for w in wires:
            pos = w.pos()
            polys.append([QPointF(x + pos.x(), y + pos.y()) for x, y in w.d["pts"]])
        ends = [(k, P[0]) for k, P in enumerate(polys)] + [(k, P[-1]) for k, P in enumerate(polys) if len(P) > 1]

        def near(a, b):
            return abs(a.x() - b.x()) < 0.3 and abs(a.y() - b.y()) < 0.3

        def on_seg(q, a, b):
            if near(q, a) or near(q, b):
                return False
            if abs(a.y() - b.y()) < 0.3 and abs(q.y() - a.y()) < 0.3:
                return min(a.x(), b.x()) < q.x() < max(a.x(), b.x())
            if abs(a.x() - b.x()) < 0.3 and abs(q.x() - a.x()) < 0.3:
                return min(a.y(), b.y()) < q.y() < max(a.y(), b.y())
            return False

        dots = {k: [] for k in range(len(wires))}
        for k, e in ends:
            count = sum(1 for k2, e2 in ends if near(e, e2))
            hit = count >= 3
            if not hit:
                for k2, P in enumerate(polys):
                    if k2 == k:
                        continue
                    if any(on_seg(e, P[i], P[i + 1]) for i in range(len(P) - 1)):
                        hit = True
                        break
            if hit and not any(near(e, d) for d in dots[k]):
                if not any(near(e, d) for kk in dots for d in dots[kk]):
                    dots[k].append(e)
        for k, w in enumerate(wires):
            pos = w.pos()
            nd = [[round(q.x() - pos.x(), 3), round(q.y() - pos.y(), 3)] for q in dots[k]]
            if nd != w.d.get("dots", []):
                w.d["dots"] = nd
                w.update()

    def remap_uids(self, dicts):
        import uuid
        m = {}
        for d in dicts:
            if d.get("uid"):
                nu = uuid.uuid4().hex[:10]
                m[d["uid"]] = nu
                d["uid"] = nu
        for d in dicts:
            for key in ("ca", "cb"):
                if d.get(key):
                    if d[key][0] in m:
                        d[key] = [m[d[key][0]], d[key][1]]
                    else:
                        d.pop(key)
        return dicts

    # ------------------------------------------------------------------ éléments
    def items(self):
        return [i for i in self.scene.items() if isinstance(i, PItem) and not getattr(i, "is_temp", False)]

    def selected(self):
        try:
            return [i for i in self.scene.selectedItems() if isinstance(i, PItem)]
        except RuntimeError:  # fenêtre en cours de fermeture
            return []

    def add_item(self, d, select=False):
        it = PItem(d)
        self.scene.addItem(it)
        it.update_geom()
        movable = self.view.tool == "select"
        it.setFlag(QGraphicsItem.ItemIsMovable, movable)
        it.setFlag(QGraphicsItem.ItemIsSelectable, movable or select)
        if select:
            it.setSelected(True)
        return it

    def rotate_selected(self, deg):
        for it in self.selected():
            it.d["angle"] = round((it.d["angle"] + deg) % 360, 4)
            it.update_geom()
        self.commit()
        self.refresh_props()

    def rotate_exact(self):
        sel = self.selected()
        if not sel:
            return
        v, ok = QInputDialog.getDouble(self, T("Rotation"), T("Angle (degrés, sens trigonométrique) :"),
                                       sel[0].d["angle"], -360, 360, 2)
        if ok:
            for it in sel:
                it.d["angle"] = v % 360
                it.update_geom()
            self.commit()
            self.refresh_props()

    def mirror_selected(self, key):
        for it in self.selected():
            it.d[key] = not it.d[key]
            it.update_geom()
        self.commit()
        self.refresh_props()

    def z_selected(self, direction):
        zs = [i.zValue() for i in self.items()] or [1]
        for it in self.selected():
            it.setZValue(max(zs) + 1 if direction > 0 else min(zs) - 1)
        self.commit()

    def delete_selected(self):
        sel = self.selected()
        for it in sel:
            self.scene.removeItem(it)
        if sel:
            self.commit()

    def select_all(self):
        self.set_tool("select")
        for it in self.items():
            it.setSelected(True)

    def duplicate(self):
        sel = self.selected()
        if not sel:
            return
        self.scene.clearSelection()
        off = self.scene.grid_step * 2
        for d in self.remap_uids([it.to_dict() for it in sel]):
            d["x"] += off
            d["y"] += off
            self.add_item(d, select=True)
        self.commit()

    # ------------------------------------------------------------------ presse-papiers
    def copy(self):
        sel = self.selected()
        if not sel:
            return
        md = QMimeData()
        md.setData(MIME_ITEMS, QByteArray(json.dumps([i.to_dict() for i in sel]).encode()))
        md.setImageData(self.render_items_image(sel))
        QApplication.clipboard().setMimeData(md)
        self.paste_count = 0
        self.statusBar().showMessage(f"{len(sel)} élément(s) copié(s) — aussi collable comme image dans Word / LibreOffice", 4000)

    def cut(self):
        self.copy()
        self.delete_selected()

    def paste(self):
        md = QApplication.clipboard().mimeData()
        self.set_tool("select")
        self.scene.clearSelection()
        if md.hasFormat(MIME_ITEMS):
            data = self.remap_uids(json.loads(bytes(md.data(MIME_ITEMS)).decode()))
            self.paste_count += 1
            off = self.scene.grid_step * 2 * self.paste_count
            for d in data:
                d["x"] += off
                d["y"] += off
                self.add_item(d, select=True)
            self.commit()
        elif md.hasImage():
            img = QImage(md.imageData())
            self.place_image(img, self.visible_center())
            self.commit()
        elif md.hasText() and md.text().strip():
            c = self.visible_center()
            self.add_item({"type": "text", "x": c.x(), "y": c.y(), "text": md.text(), "size": self.cur_text_size,
                           "color": self.cur_color}, select=True)
            self.commit()

    def visible_center(self):
        vp = self.view.viewport().rect()
        sp = self.view.mapToScene(self.view.mapFromGlobal(self.cursor().pos()))
        if vp.contains(self.view.mapFromGlobal(self.cursor().pos())):
            return sp
        return self.view.mapToScene(vp.center())

    def render_items_image(self, items, scale=4):
        r = QRectF()
        for it in items:
            r = r.united(it.sceneBoundingRect())
        r = r.adjusted(-2, -2, 2, 2)
        hidden = [i for i in self.scene.items() if i.isVisible() and i not in items and i.parentItem() is None]
        for i in hidden:
            i.setVisible(False)
        sel = self.scene.selectedItems()
        self.scene.exporting = True
        img = QImage(max(1, int(r.width() * scale)), max(1, int(r.height() * scale)), QImage.Format_ARGB32)
        img.fill(Qt.transparent)
        p = QPainter(img)
        p.setRenderHint(QPainter.Antialiasing)
        self.scene.render(p, QRectF(img.rect()), r)
        p.end()
        self.scene.exporting = False
        for i in hidden:
            i.setVisible(True)
        for i in sel:
            i.setSelected(True)
        return img

    # ------------------------------------------------------------------ capture de zone
    def capture_region(self, r, global_pos):
        scale = 3
        for pg in self.page_items:
            if QRectF(pg.pos(), QSizeF(pg.w, pg.h)).intersects(r):
                self.render_page(pg, scale)
        self.scene.exporting = True
        img = QImage(int(r.width() * scale), int(r.height() * scale), QImage.Format_ARGB32)
        img.fill(Qt.white)
        p = QPainter(img)
        p.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.scene.render(p, QRectF(img.rect()), r)
        p.end()
        self.scene.exporting = False
        QApplication.clipboard().setImage(img)
        self.statusBar().showMessage(T("Zone capturée et copiée — Ctrl+V pour la coller ici ou dans un autre logiciel"), 6000)
        menu = QMenu(self)
        a1 = menu.addAction(T("Coller comme image sur la page"))
        a2 = menu.addAction(T("Enregistrer l'image (PNG)…"))
        menu.addAction(T("Garder dans le presse-papiers"))
        ch = menu.exec(global_pos)
        if ch == a1:
            self.place_image(img, r.center(), width=r.width())
            self.commit()
        elif ch == a2:
            f, _ = QFileDialog.getSaveFileName(self, T("Enregistrer la capture"), T("capture.png"), "Image PNG (*.png)")
            if f:
                img.save(f if f.lower().endswith(".png") else f + ".png")

    # ------------------------------------------------------------------ images, signature
    def place_image(self, img, center, width=None, select=True):
        if img.isNull():
            return None
        w = width or min(img.width() / 3, 200)
        h = w * img.height() / max(img.width(), 1)
        d = {"type": "image", "x": center.x() - w / 2, "y": center.y() - h / 2, "w": w, "h": h,
             "png": image_to_b64(img), "sw": 0}
        self.set_tool("select")
        self.scene.clearSelection()
        return self.add_item(d, select=select)

    def insert_image_file(self, f, center):
        img = QImage(f)
        if img.isNull():
            QMessageBox.warning(self, APP_NAME, T("Image illisible."))
            return
        if img.width() > 2500:
            img = img.scaledToWidth(2500, Qt.SmoothTransformation)
        self.place_image(img, center, width=min(img.width() * 72 / 150, 400))
        self.commit()

    def insert_image_dialog(self):
        f, _ = QFileDialog.getOpenFileName(self, T("Insérer une image"), T(""), "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)")
        if f:
            self.insert_image_file(f, self.view.mapToScene(self.view.viewport().rect().center()))

    def insert_signature(self):
        dlg = SignatureDialog(self)
        if dlg.exec() and dlg.img is not None:
            img = dlg.img
            w = 50 * MM
            h = w * img.height() / max(img.width(), 1)
            self.set_tool("image_place")
            self.view.set_ghost({"type": "image", "x": 0, "y": 0, "w": w, "h": h, "png": image_to_b64(img), "sw": 0})
            self.statusBar().showMessage(T("Cliquer à l'endroit où placer la signature (taille réglable dans Propriétés)"))

    # ------------------------------------------------------------------ correcteur orthographique
    def build_spell_menu(self, parent):
        from . import spell
        st = self.settings
        spell.configure(enabled=st.value("ortho_actif", "true") in (True, "true", "1", 1),
                        lang=st.value("ortho_langue", "auto") or "auto",
                        personal=[x for x in (st.value("dico_perso") or []) if isinstance(x, str)])
        sm = parent.addMenu(T("Correcteur orthographique"))
        a = sm.addAction(T("Souligner les fautes d'orthographe"))
        a.setCheckable(True)
        a.setChecked(spell.is_enabled())
        a.toggled.connect(lambda on: (spell.configure(enabled=on), st.setValue("ortho_actif", "true" if on else "false")))
        sm.addSeparator()
        from PySide6.QtGui import QActionGroup
        g = QActionGroup(self)
        names = [("auto", T("Langue du logiciel")), ("fr", "Français"), ("en", "English"), ("es", "Español"),
                 ("pt", "Português"), ("de", "Deutsch"), ("it", "Italiano")]
        cur = st.value("ortho_langue", "auto") or "auto"
        for code, name in names:
            b = sm.addAction(name)
            b.setCheckable(True)
            b.setChecked(code == cur)
            g.addAction(b)
            b.triggered.connect(lambda _=False, c=code: (spell.configure(lang=c), st.setValue("ortho_langue", c)))
        sm.addSeparator()
        sm.addAction(T("Dictionnaire personnel…")).triggered.connect(self.edit_personal_dict)

    def save_personal_dict(self):
        from . import spell
        self.settings.setValue("dico_perso", spell.personal_words())

    def edit_personal_dict(self):
        from . import spell
        dlg = QDialog(self)
        dlg.setWindowTitle(T("Dictionnaire personnel"))
        lay = QVBoxLayout(dlg)
        lay.addWidget(QLabel(T("Un mot par ligne (mots techniques, noms propres…) :")))
        ed = QPlainTextEdit("\n".join(spell.personal_words()))
        ed.setMinimumSize(320, 300)
        lay.addWidget(ed)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(dlg.accept)
        bb.rejected.connect(dlg.reject)
        lay.addWidget(bb)
        if dlg.exec():
            words = [w.strip().lower() for w in ed.toPlainText().split("\n") if w.strip()]
            spell.configure(personal=words)
            self.save_personal_dict()

    # ------------------------------------------------------------------ tableaux et calculatrice
    def insert_table(self):
        from .table import InsertTableDialog, new_table
        dlg = InsertTableDialog(self)
        if not dlg.exec():
            return
        R, C = dlg.rows.value(), dlg.cols.value()
        pg = self.page_items[self.current_page()]
        w = min(C * 30 * MM, pg.w - 30 * MM)
        h = R * 8 * MM
        c = self.view.mapToScene(self.view.viewport().rect().center())
        d = new_table(R, C, c.x() - w / 2, c.y() - h / 2, w, h, dlg.header.isChecked())
        self.set_tool("select")
        self.scene.clearSelection()
        it = self.add_item(d, select=True)
        self.commit()
        self.edit_table(it)

    def edit_table(self, it):
        from .table import TableDialog
        dlg = TableDialog(it.d, self)
        if dlg.exec():
            it.d.update(dlg.result())
            it.update_geom()
            self.commit()
            self.refresh_props()

    def table_op(self, op):
        from .table import fix
        tabs = [i for i in self.selected() if i.typ == "table"]
        if not tabs:
            QMessageBox.information(self, APP_NAME, T("Sélectionner d'abord un tableau (clic sur son bord ou dedans)."))
            return
        it = tabs[0]
        d = it.d
        if op == "edit":
            self.edit_table(it)
            return
        R, C = d["rows"], d["cols"]
        if op == "row+":
            d["h"] = d["h"] * (R + 1) / R
            d["rows"] = R + 1
        elif op == "col+":
            d["w"] = d["w"] * (C + 1) / C
            d["cols"] = C + 1
            d["colw"] = list(d.get("colw") or [1.0] * C) + [sum(d.get("colw") or [1.0]) / C]
        elif op == "row-" and R > 1:
            d["h"] = d["h"] * (R - 1) / R
            d["rows"] = R - 1
        elif op == "col-" and C > 1:
            d["w"] = d["w"] * (C - 1) / C
            d["cols"] = C - 1
        fix(d)
        it.update_geom()
        self.commit()
        self.refresh_props()

    def open_calculator(self):
        from .calculator import CalculatorDialog
        if getattr(self, "_calc", None) is None:
            self._calc = CalculatorDialog(self)
        self._calc.show()
        self._calc.raise_()
        self._calc.activateWindow()

    def insert_orgchart(self):
        """Pose un organigramme type (rapport de stage) déjà relié, à compléter par double-clic."""
        pg = self.page_items[self.current_page()]
        x0, y0, pw = pg.pos().x(), pg.pos().y(), pg.w
        cx = x0 + pw / 2

        def node(pid, x, y, text=None):
            d = json.loads(json.dumps(ND.BY_ID[pid].d))
            d.update(x=x - d["w"] / 2, y=y)
            if text is not None:
                d["text"] = text
            return self.add_item(d)

        title = node("o_titre", cx, y0 + 12 * MM, T("Organigramme de l'entreprise"))
        direc = node("o_direction", cx, y0 + 30 * MM, T("Direction") + "\n" + T("Nom Prénom"))
        assist = node("o_assistant", cx + 64 * MM, y0 + 32 * MM, T("Assistante de direction") + "\n" + T("Nom Prénom"))
        col = min(58 * MM, (pw - 20 * MM) / 3)
        ys, yp1, yp2 = y0 + 78 * MM, y0 + 104 * MM, y0 + 124 * MM
        services = [("o_service", T("Administratif et commercial")), ("o_service2", T("Service technique")),
                    ("o_service3", T("Logistique / magasin"))]
        self.add_link(direc, 1, assist, 3, "ortho")
        for k, (pid, name) in enumerate(services):
            x = cx + (k - 1) * col
            sv = node(pid, x, ys, name + "\n" + T("Responsable"))
            self.add_link(direc, 2, sv, 0, "ortho")
            if k == 1:
                tut = node("o_tuteur", x, yp1, T("Tuteur de stage") + "\n" + T("Nom Prénom"))
                sta = node("o_stagiaire", x, yp2, T("Stagiaire") + "\n" + T("Prénom NOM"))
                self.add_link(sv, 2, tut, 0, "ortho")
                self.add_link(tut, 2, sta, 0, "ortho")
            else:
                p1 = node("o_poste", x, yp1, T("Fonction") + "\n" + T("Nom Prénom"))
                p2 = node("o_poste", x, yp2, T("Fonction") + "\n" + T("Nom Prénom"))
                self.add_link(sv, 2, p1, 0, "ortho")
                self.add_link(p1, 2, p2, 0, "ortho")
        node("o_legende", cx - col, y0 + 146 * MM, T("Légende :") + "\n" + T("vert = mon poste de stage"))
        self.update_junctions() if hasattr(self, "update_junctions") else None
        self.commit()
        self.statusBar().showMessage(T("Double-cliquez sur une case pour écrire les noms ; les liaisons suivent les cases déplacées."), 10000)

    def insert_title_block(self):
        """Cartouche d'un seul bloc, posé en bas à droite de la page courante."""
        import datetime
        pg = self.page_items[self.current_page()]
        w, h = 100 * MM, 30 * MM
        d = {"type": "node", "shape": "cartouche", "w": w, "h": h, "size": 8, "sw": 0.8, "color": "#000000",
             "x": pg.pos().x() + pg.w - w - 10 * MM, "y": pg.pos().y() + pg.h - h - 10 * MM,
             "title": T("Plan de l'installation électrique"), "author": self.settings.value("author", ""),
             "school": self.settings.value("school", ""), "classe": "",
             "date": datetime.date.today().strftime("%d/%m/%Y"), "scale": f"1/{self.scene.plan_denom}",
             "folio": "1/1", "text": ""}
        if not self.edit_cartouche(d):
            return
        self.set_tool("select")
        self.scene.clearSelection()
        self.add_item(d, select=True)
        self.commit()

    CART_FIELDS = (("title", "Titre"), ("author", "Auteur"), ("school", "Établissement"), ("classe", "Classe"),
                   ("date", "Date"), ("scale", "Échelle"), ("folio", "Folio"))

    def edit_cartouche(self, d):
        dlg = QDialog(self)
        dlg.setWindowTitle(T("Cartouche"))
        f = QFormLayout(dlg)
        eds = {}
        for k, lab in self.CART_FIELDS:
            eds[k] = QLineEdit(str(d.get(k, "")))
            f.addRow(T(lab), eds[k])
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(dlg.accept)
        bb.rejected.connect(dlg.reject)
        f.addRow(bb)
        if not dlg.exec():
            return False
        for k, e in eds.items():
            d[k] = e.text()
        self.settings.setValue("author", d.get("author", ""))
        self.settings.setValue("school", d.get("school", ""))
        return True

    # ------------------------------------------------------------------ propriétés
    def refresh_props(self):
        sel = self.selected()
        w = QWidget()
        f = QFormLayout(w)
        f.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        if not sel:
            f.addRow(QLabel(T("Aucun élément sélectionné.\n\nAstuce : choisis un symbole dans la\n"
                            "bibliothèque ou un outil à gauche.")))
            self.props_area.setWidget(w)
            return
        it = sel[0]
        d = it.d
        types = {i.typ for i in sel}
        f.addRow(QLabel(f"<b>{len(sel)} élément(s)</b>" if len(sel) > 1 else f"<b>{self.item_title(it)}</b>"))

        def changed(key, val, geom=True):
            for i in sel:
                if key in i.d or key in ("angle", "fh", "fv", "color", "sw", "label", "fill", "dash", "arrow", "pins",
                                          "title", "author", "school", "classe", "date", "scale", "folio"):
                    i.d[key] = val
                    i.update_geom()
            self._prop_timer.start()

        ang = QDoubleSpinBox(decimals=1, minimum=-1, maximum=360, singleStep=15, value=d["angle"], suffix=" °", wrapping=True)
        ang.valueChanged.connect(lambda v: changed("angle", v % 360))
        rot_row = QHBoxLayout()
        rot_row.addWidget(ang)
        for txt, deg in (("↺90", 90), ("↻90", -90)):
            b = QToolButton(text=txt)
            b.clicked.connect(lambda _=False, g=deg: self.rotate_selected(g))
            rot_row.addWidget(b)
        f.addRow(T("Rotation"), rot_row)
        mir = QHBoxLayout()
        bh = QPushButton(T("Miroir ↔"))
        bh.setCheckable(True)
        bh.setChecked(d["fh"])
        bh.toggled.connect(lambda v: changed("fh", v))
        bv = QPushButton(T("Miroir ↕"))
        bv.setCheckable(True)
        bv.setChecked(d["fv"])
        bv.toggled.connect(lambda v: changed("fv", v))
        mir.addWidget(bh)
        mir.addWidget(bv)
        f.addRow(T("Miroir"), mir)
        if types - {"image"}:
            cb = ColorButton(d["color"])
            cb.changed.connect(lambda c: changed("color", c))
            f.addRow(T("Couleur"), cb)
        if types & {"symbol", "line", "wire", "rect", "ellipse", "freehand", "highlight", "dim", "wall"}:
            sw = QDoubleSpinBox(decimals=2, minimum=0, maximum=40, singleStep=0.25, value=d["sw"], suffix=" pt")
            sw.valueChanged.connect(lambda v: changed("sw", v))
            f.addRow(T("Épaisseur"), sw)
        if types & {"line", "wire", "rect", "ellipse", "freehand"}:
            dc = QComboBox()
            for k, v in (("solid", "Continu"), ("dash", "Tirets"), ("dot", "Pointillés"), ("dashdot", "Mixte")):
                dc.addItem(T(v), k)
            dc.setCurrentIndex(max(0, dc.findData(d.get("dash", "solid"))))
            dc.currentIndexChanged.connect(lambda i: changed("dash", dc.itemData(i)))
            f.addRow(T("Style"), dc)
        if it.typ in ("wire", "line"):
            cc = QComboBox()
            for i in range(self.cond_combo.count()):
                cc.addItem(self.cond_combo.itemIcon(i), self.cond_combo.itemText(i), self.cond_combo.itemData(i))
            cur = next((i for i in range(cc.count()) if cc.itemData(i) and cc.itemData(i)[0] == d["color"]
                        and cc.itemData(i)[1] == d.get("color2")), 0)
            cc.setCurrentIndex(cur)

            def setcond(i):
                dat = cc.itemData(i)
                if dat:
                    for x in sel:
                        if x.typ in ("wire", "line"):
                            x.d["color"], x.d["color2"] = dat
                            x.update_geom()
                    self._prop_timer.start()
            cc.currentIndexChanged.connect(setcond)
            f.addRow(T("Conducteur"), cc)
        if it.typ == "wire" and (d.get("ca") or d.get("cb")):
            det = QPushButton(T("Détacher des bornes"))
            def detach():
                for x in sel:
                    x.d.pop("ca", None)
                    x.d.pop("cb", None)
                self.commit()
                self.refresh_props()
            det.clicked.connect(detach)
            f.addRow(T("Liaison"), det)
        if it.typ == "line":
            ac = QComboBox()
            for k, v in (("none", "Aucune"), ("end", "À la fin"), ("start", "Au début"), ("both", "Aux deux bouts")):
                ac.addItem(T(v), k)
            ac.setCurrentIndex(max(0, ac.findData(d.get("arrow", "none"))))
            ac.currentIndexChanged.connect(lambda i: changed("arrow", ac.itemData(i)))
            f.addRow(T("Flèche"), ac)
        if it.typ == "symbol":
            sym = it.sym()
            sc = QDoubleSpinBox(decimals=0, minimum=10, maximum=2000, singleStep=10, value=d.get("scale", 1) * 100, suffix=" %")
            sc.valueChanged.connect(lambda v: changed("scale", v / 100))
            f.addRow(T("Taille"), sc)
            le = QLineEdit(d.get("label", ""))
            le.setPlaceholderText(T("ex. KM1, S1, H2, Q3"))
            le.textChanged.connect(lambda v: changed("label", v))
            f.addRow(T("Repère"), le)
            lp = QComboBox()
            for v in ("auto", "haut", "bas", "gauche", "droite"):
                lp.addItem(T(v), v)
            lp.setCurrentIndex(max(0, lp.findData(d.get("label_pos", "auto"))))
            lp.currentIndexChanged.connect(lambda i: [it2.d.__setitem__("label_pos", lp.itemData(i)) or it2.update_geom() for it2 in sel] and self._prop_timer.start())
            lr = QHBoxLayout()
            for txt, pos in (("◀ " + T("Repère à gauche"), "gauche"), (T("Repère à droite") + " ▶", "droite")):
                b = QPushButton(txt)
                b.clicked.connect(lambda _=False, ps=pos: lp.setCurrentIndex(lp.findData(ps)))
                lr.addWidget(b)
            f.addRow("", lr)
            f.addRow(T("Position du repère"), lp)
            if sym and sym.pins:
                pe = QLineEdit(d.get("pins", ""))
                pe.setPlaceholderText(sym.pin_names or T("ex. A1 A2"))
                pe.setToolTip(T("Numéros des bornes séparés par un espace (vide = aucun)"))
                pe.textChanged.connect(lambda v: changed("pins", v))
                f.addRow(T("Bornes"), pe)
            if sym and sym.params:
                for spec in sym.params:
                    key, lab, dflt = spec[0], spec[1], spec[2]
                    cur = d.get("params", {}).get(key, dflt)

                    def setp(v, key=key):
                        for i in sel:
                            if i.typ == "symbol" and i.sym() is sym:
                                i.d.setdefault("params", sym.defaults())[key] = v
                                i.update_geom()
                        self._prop_timer.start()
                    if len(spec) == 4 and isinstance(spec[3], list):
                        cb = QComboBox()
                        for opt in spec[3]:
                            cb.addItem(T(opt), opt)
                        i0 = cb.findData(str(cur))
                        cb.setCurrentIndex(i0 if i0 >= 0 else 0)
                        cb.currentIndexChanged.connect(lambda i, cb=cb, setp=setp: setp(cb.itemData(i)))
                        f.addRow(T(lab), cb)
                    elif len(spec) == 4:
                        le = QLineEdit(str(cur))
                        le.textChanged.connect(setp)
                        f.addRow(T(lab), le)
                    else:
                        sp = QDoubleSpinBox(decimals=0, minimum=spec[3], maximum=spec[4], value=float(cur))
                        sp.valueChanged.connect(setp)
                        f.addRow(T(lab), sp)
        if it.typ in BOX_TYPES:
            for key, lab in (("w", "Largeur"), ("h", "Hauteur")):
                sp = QDoubleSpinBox(decimals=1, minimum=1, maximum=5000, value=d[key] / MM, suffix=" mm")
                sp.valueChanged.connect(lambda v, key=key: changed(key, v * MM))
                f.addRow(T(lab), sp)
            if it.typ == "table":
                eb = QPushButton(T("Modifier le tableau (cases, formules, fusion)…"))
                eb.clicked.connect(lambda _=False, it=it: self.edit_table(it))
                f.addRow("", eb)
            if it.typ == "image":
                ratio = QPushButton(T("Garder les proportions"))
                def keep():
                    for i in sel:
                        if i.typ == "image":
                            img = i.image()
                            i.d["h"] = i.d["w"] * img.height() / max(1, img.width())
                            i.update_geom()
                    self.commit()
                    self.refresh_props()
                ratio.clicked.connect(keep)
                f.addRow("", ratio)
        if it.typ in ("rect", "ellipse"):
            fill_row = QHBoxLayout()
            fc = QCheckBox(T("Rempli"))
            fc.setChecked(bool(d.get("fill")))
            fb = ColorButton(d.get("fill") or "#ffffff")
            fc.toggled.connect(lambda v: changed("fill", fb.color if v else None))
            fb.changed.connect(lambda c: fc.isChecked() and changed("fill", c))
            fill_row.addWidget(fc)
            fill_row.addWidget(fb)
            f.addRow(T("Remplissage"), fill_row)
        if it.typ == "node" and d.get("shape") == "cartouche":
            for k, lab in self.CART_FIELDS:
                le = QLineEdit(str(d.get(k, "")))
                le.textChanged.connect(lambda v, k=k: changed(k, v))
                f.addRow(T(lab), le)
        elif it.typ == "node":
            te = QPlainTextEdit(d.get("text", ""))
            te.setMaximumHeight(80)
            te.textChanged.connect(lambda: changed("text", te.toPlainText()))
            f.addRow(T("Texte"), te)
            ts = QDoubleSpinBox(decimals=1, minimum=3, maximum=200, value=d.get("size", 9), suffix=" pt")
            ts.valueChanged.connect(lambda v: changed("size", v))
            f.addRow(T("Taille du texte"), ts)
            bc = QCheckBox(T("Gras"))
            bc.setChecked(d.get("bold", False))
            bc.toggled.connect(lambda v: changed("bold", v))
            f.addRow("", bc)
            fill_row = QHBoxLayout()
            fc = QCheckBox(T("Rempli"))
            fc.setChecked(bool(d.get("fill")))
            fb = ColorButton(d.get("fill") or "#ffffff")
            fc.toggled.connect(lambda v: changed("fill", fb.color if v else None))
            fb.changed.connect(lambda c: fc.isChecked() and changed("fill", c))
            fill_row.addWidget(fc)
            fill_row.addWidget(fb)
            f.addRow(T("Remplissage"), fill_row)
            sh = d.get("shape")
            if sh in ("action", "action_cond"):
                qe = QLineEdit(d.get("qual", ""))
                qe.setPlaceholderText("S, R, D=3s, C, L…")
                qe.textChanged.connect(lambda v: changed("qual", v))
                f.addRow(T("Qualificatif"), qe)
            if sh == "transition":
                le = QLineEdit(d.get("label", ""))
                le.setPlaceholderText("(1)")
                le.textChanged.connect(lambda v: changed("label", v))
                f.addRow(T("Numéro de transition"), le)
            if sh in ("step_cond", "action_cond"):
                ce = QLineEdit(d.get("cond", ""))
                ce.setPlaceholderText("ex. a . b")
                ce.textChanged.connect(lambda v: changed("cond", v))
                f.addRow(T("Condition (en haut)"), ce)
            if sh in ("step", "step_init", "step_cond"):
                ac = QCheckBox(T("Étape active (point)"))
                ac.setChecked(bool(d.get("active")))
                ac.toggled.connect(lambda v: changed("active", v))
                f.addRow("", ac)
                gb = QPushButton(T("Ajouter transition + étape (Ctrl+G)"))
                gb.clicked.connect(self.grafcet_next)
                f.addRow("", gb)
        if it.typ == "wire":
            rc = QComboBox()
            for k, v in (("ortho", "Angles droits"), ("straight", "Droite"), ("curve", "Courbe")):
                rc.addItem(T(v), k)
            rc.setCurrentIndex(max(0, rc.findData(d.get("route", "ortho"))))

            def setroute(i):
                for x in sel:
                    if x.typ == "wire":
                        x.d["route"] = rc.itemData(i)
                        pts = x.d["pts"]
                        if rc.itemData(i) != "ortho" and len(pts) > 2:
                            x.d["pts"] = [pts[0], pts[-1]]
                        x.update_geom()
                self.commit()
            rc.currentIndexChanged.connect(setroute)
            f.addRow(T("Tracé"), rc)
            wa = QComboBox()
            for k, v in (("none", "Aucune"), ("end", "À la fin"), ("mid", "Au milieu")):
                wa.addItem(T(v), k)
            wa.setCurrentIndex(max(0, wa.findData(d.get("arrow", "none"))))
            wa.currentIndexChanged.connect(lambda i: changed("arrow", wa.itemData(i)))
            f.addRow(T("Flèche"), wa)
        if it.typ == "text":
            te = QPlainTextEdit(d.get("text", ""))
            te.setMaximumHeight(90)
            te.textChanged.connect(lambda: changed("text", te.toPlainText()))
            f.addRow(T("Texte"), te)
            ts = QDoubleSpinBox(decimals=1, minimum=3, maximum=300, value=d.get("size", 10), suffix=" pt")
            ts.valueChanged.connect(lambda v: changed("size", v))
            f.addRow(T("Taille"), ts)
            bc = QCheckBox(T("Gras"))
            bc.setChecked(d.get("bold", False))
            bc.toggled.connect(lambda v: changed("bold", v))
            f.addRow("", bc)
        if it.typ == "wall":
            th = QDoubleSpinBox(decimals=0, minimum=3, maximum=80, value=d.get("thick", 20), suffix=" cm")
            th.valueChanged.connect(lambda v: changed("thick", v))
            f.addRow(T("Épaisseur du mur"), th)
            fb = ColorButton(d.get("fill") or "#b0b0b0")
            fb.changed.connect(lambda c: changed("fill", c))
            f.addRow(T("Remplissage"), fb)
        if it.typ == "dim":
            dt = QLineEdit(d.get("text", ""))
            dt.setPlaceholderText(T("automatique (") + it.dim_text(math.dist(*d["pts"][:2])) + ")")
            dt.textChanged.connect(lambda v: changed("text", v))
            f.addRow(T("Texte imposé"), dt)
            uc = QComboBox()
            uc.addItem("Longueur réelle (échelle)", "real")
            uc.addItem("Longueur sur le papier (mm)", "mm")
            uc.setCurrentIndex(max(0, uc.findData(d.get("unit", "real"))))
            uc.currentIndexChanged.connect(lambda i: changed("unit", uc.itemData(i)))
            f.addRow(T("Unité"), uc)
            ds = QDoubleSpinBox(decimals=1, minimum=3, maximum=50, value=d.get("size", 7), suffix=" pt")
            ds.valueChanged.connect(lambda v: changed("size", v))
            f.addRow(T("Taille du texte"), ds)
        if it.typ in FIELD_TOOLS and it.typ != "field_link":
            ne = QLineEdit(d.get("name", ""))
            ne.textChanged.connect(lambda v: changed("name", v))
            f.addRow(T("Nom du champ") if it.typ != "field_radio" else "Groupe", ne)
            if it.typ == "field_text":
                ve = QLineEdit(d.get("value", ""))
                ve.textChanged.connect(lambda v: changed("value", v))
                f.addRow(T("Valeur par défaut"), ve)
            elif it.typ == "field_combo":
                oe = QLineEdit(", ".join(d.get("options", [])))
                oe.textChanged.connect(lambda v: changed("options", [o.strip() for o in v.split(",") if o.strip()]))
                f.addRow(T("Choix (séparés par ,)"), oe)
            elif it.typ in ("field_check", "field_radio"):
                vc = QCheckBox(T("Cochée") if it.typ == "field_check" else "Sélectionné")
                vc.setChecked(bool(d.get("value")))
                vc.toggled.connect(lambda v: changed("value", v))
                f.addRow("", vc)
        if it.typ == "field_link":
            ue = QLineEdit(d.get("url", ""))
            ue.setPlaceholderText(T("https://… (vide = lien vers une page)"))
            ue.textChanged.connect(lambda v: changed("url", v))
            f.addRow(T("Adresse web"), ue)
            pe = QSpinBox(minimum=1, maximum=9999, value=int(d.get("page") or 1))
            pe.valueChanged.connect(lambda v: changed("page", v))
            f.addRow(T("ou page"), pe)
        pos_row = QHBoxLayout()
        page, rx, ry = self.page_coords(it.pos())
        px = QDoubleSpinBox(decimals=1, minimum=-2000, maximum=5000, value=rx / MM, suffix=" mm")
        py = QDoubleSpinBox(decimals=1, minimum=-2000, maximum=5000, value=ry / MM, suffix=" mm")

        def setpos():
            pg = self.page_items[page] if page < len(self.page_items) else None
            oy = pg.pos().y() if pg else 0
            self.scene.no_snap = True
            it.setPos(px.value() * MM, oy + py.value() * MM)
            self.scene.no_snap = False
            self._prop_timer.start()
        px.valueChanged.connect(setpos)
        py.valueChanged.connect(setpos)
        pos_row.addWidget(px)
        pos_row.addWidget(py)
        f.addRow(T("Position X / Y"), pos_row)
        dl = QPushButton(T("Supprimer"))
        dl.clicked.connect(self.delete_selected)
        f.addRow("", dl)
        self.props_area.setWidget(w)

    def item_title(self, it):
        if it.typ == "symbol":
            s = it.sym()
            return T(s.name) if s else T("Symbole")
        return {"line": "Trait", "wire": "Fil", "wall": "Mur", "freehand": "Dessin", "highlight": "Surlignage",
                "dim": "Cote", "rect": "Rectangle", "ellipse": "Ellipse", "table": "Tableau", "text": "Texte", "image": "Image",
                "field_text": "Champ texte", "field_check": "Case à cocher", "field_combo": "Liste déroulante",
                "field_radio": "Bouton radio", "field_sig": "Zone de signature", "field_link": "Lien",
                "node": "Forme" if it.d.get("shape") != "cartouche" else "Cartouche"}.get(it.typ, it.typ)

    # ------------------------------------------------------------------ pages : affichage
    def layout_pages(self):
        for pg in self.page_items:
            self.scene.removeItem(pg)
        self.page_items = []
        y = 0
        maxw = 0
        for i, page in enumerate(self.doc):
            r = page.rect
            pg = PageItem(i, r.width, r.height)
            pg.setPos(0, y)
            self.scene.addItem(pg)
            self.page_items.append(pg)
            y += r.height + GAP
            maxw = max(maxw, r.width)
        self.scene.setSceneRect(QRectF(-200, -100, maxw + 400, y + 200))
        self.schedule_render()
        self.refresh_thumbs()
        self.refresh_forms()

    def schedule_render(self):
        self._render_timer.start()

    def render_page(self, pg, scale):
        page = self.doc[pg.idx]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
        pg.img = qimage_from_pix(pix)
        pg.scale_ = scale
        pg.update()

    def render_visible(self):
        if not self.doc:
            return
        vis = self.view.mapToScene(self.view.viewport().rect()).boundingRect()
        margin = vis.height()
        zone = vis.adjusted(0, -margin, 0, margin)
        dpr = self.view.devicePixelRatioF()
        want = self.view.zoom() * dpr
        target = next((s for s in (1, 1.5, 2, 3, 4, 6) if s >= want), 6)
        for pg in self.page_items:
            r = QRectF(pg.pos(), QSizeF(pg.w, pg.h))
            if r.intersects(zone):
                if pg.img is None or pg.scale_ < target:
                    self.render_page(pg, target)
            elif not r.intersects(zone.adjusted(0, -margin * 3, 0, margin * 3)):
                pg.img, pg.scale_ = None, 0

    def invalidate_pages(self, idxs=None):
        for pg in self.page_items:
            if idxs is None or pg.idx in idxs:
                pg.img, pg.scale_ = None, 0
                pg.update()
        self.schedule_render()
        self.refresh_thumbs()

    def refresh_thumbs(self):
        self.thumbs.clear()
        if not self.doc:
            return
        for i, page in enumerate(self.doc):
            k = 110 / max(page.rect.width, page.rect.height) * 1.3
            pix = page.get_pixmap(matrix=pymupdf.Matrix(k, k), alpha=False)
            pm = QPixmap.fromImage(qimage_from_pix(pix))
            p = QPainter(pm)
            p.setPen(QColor("#999"))
            p.drawRect(pm.rect().adjusted(0, 0, -1, -1))
            p.end()
            it = QListWidgetItem(QIcon(pm), f"Page {i + 1}")
            self.thumbs.addItem(it)

    def zoom_changed(self):
        self.zoom_label.setText(f" {self.view.zoom() * 100 / (96 / 72):.0f} % ")
        self.schedule_render()

    def zoom_real(self):
        self.view.set_zoom(96 / 72 * self.view.logicalDpiX() / 96)

    def zoom_width(self):
        if self.page_items:
            pg = self.page_items[self.current_page()]
            vw = self.view.viewport().width() - 40
            self.view.set_zoom(vw / pg.w)
            self.view.centerOn(pg.w / 2, self.view.mapToScene(self.view.viewport().rect().center()).y())

    def zoom_page(self):
        if self.page_items:
            pg = self.page_items[self.current_page()]
            vp = self.view.viewport()
            self.view.set_zoom(min((vp.width() - 40) / pg.w, (vp.height() - 40) / pg.h))
            self.view.centerOn(pg.pos() + QPointF(pg.w / 2, pg.h / 2))

    def current_page(self):
        if not self.page_items:
            return 0
        cy = self.view.mapToScene(self.view.viewport().rect().center()).y()
        for pg in self.page_items:
            if cy < pg.pos().y() + pg.h + GAP / 2:
                return pg.idx
        return len(self.page_items) - 1

    def goto_page(self, i):
        if 0 <= i < len(self.page_items):
            pg = self.page_items[i]
            self.view.centerOn(pg.pos().x() + pg.w / 2, pg.pos().y() + min(pg.h / 2, self.view.viewport().height() / self.view.zoom() / 2 - 10))

    def page_coords(self, sp):
        for pg in self.page_items:
            if sp.y() < pg.pos().y() + pg.h + GAP / 2:
                return pg.idx, sp.x() - pg.pos().x(), sp.y() - pg.pos().y()
        if self.page_items:
            pg = self.page_items[-1]
            return pg.idx, sp.x() - pg.pos().x(), sp.y() - pg.pos().y()
        return 0, sp.x(), sp.y()

    def show_coords(self, sp):
        i, x, y = self.page_coords(sp)
        txt = f" Page {i + 1}  x = {x / MM:.1f} mm  y = {y / MM:.1f} mm "
        if self.view.tool in ("wall", "dim"):
            txt += f"(réel : {x / pts_per_cm(self.scene.plan_denom) / 100:.2f} m ; {y / pts_per_cm(self.scene.plan_denom) / 100:.2f} m) "
        self.coord_label.setText(txt)

    # ------------------------------------------------------------------ éléments <-> pages
    def gather_items(self):
        by = {}
        for it in self.items():
            c = it.sceneBoundingRect().center()
            i, _, _ = self.page_coords(c)
            pg = self.page_items[i]
            d = it.to_dict()
            d["x"] -= pg.pos().x()
            d["y"] -= pg.pos().y()
            by.setdefault(str(i), []).append(d)
        return by

    def restore_items(self, by):
        for it in self.items():
            self.scene.removeItem(it)
        for k, lst in by.items():
            i = int(k)
            if i >= len(self.page_items):
                continue
            pg = self.page_items[i]
            for d in lst:
                d = dict(d)
                d["x"] += pg.pos().x()
                d["y"] += pg.pos().y()
                self.add_item(d)

    # ------------------------------------------------------------------ annuler / rétablir
    def commit(self, doc_changed=False):
        if not self.doc:
            return
        n_fields = len([i for i in self.items() if i.typ.startswith("field")])
        if n_fields != getattr(self, "_n_fields", -1):
            self._n_fields = n_fields
            QTimer.singleShot(0, self.refresh_forms)
        self.update_connections()
        self.update_junctions()
        items = json.dumps(self.gather_items(), sort_keys=True)
        last = self.undo_stack[self.undo_idx] if self.undo_idx >= 0 else None
        docb = self.doc.tobytes() if (doc_changed or last is None) else last[0]
        meta = json.dumps({"denom": self.scene.plan_denom})
        if last and last[1] == items and last[0] is docb and last[2] == meta:
            return
        self.undo_stack = self.undo_stack[: self.undo_idx + 1]
        self.undo_stack.append((docb, items, meta))
        if len(self.undo_stack) > 150:
            self.undo_stack.pop(0)
            self.saved_idx -= 1
        self.undo_idx = len(self.undo_stack) - 1
        self.update_title()

    def restore_state(self, idx):
        docb, items, meta = self.undo_stack[idx]
        cur = self.undo_stack[self.undo_idx][0]
        if docb is not cur:
            self.doc = pymupdf.open("pdf", docb)
            self.layout_pages()
        m = json.loads(meta)
        self.scale_combo.blockSignals(True)
        self.scale_combo.setCurrentText(str(m["denom"]))
        self.scale_combo.blockSignals(False)
        self.scene.plan_denom = m["denom"]
        self.undo_idx = idx
        self.restore_items(json.loads(items))
        self.update_title()
        self.refresh_props()

    def undo(self):
        if self.view.temp is not None or self.view.ghost is not None:
            self.set_tool("select")
        if self.undo_idx > 0:
            self.restore_state(self.undo_idx - 1)

    def redo(self):
        if self.undo_idx < len(self.undo_stack) - 1:
            self.restore_state(self.undo_idx + 1)

    def is_dirty(self):
        return self.undo_idx != self.saved_idx

    def update_title(self):
        name = os.path.basename(self.path) if self.path else "Sans titre"
        self.setWindowTitle(f"{'• ' if self.is_dirty() else ''}{name} — {APP_NAME}")

    # ------------------------------------------------------------------ documents
    def maybe_save(self):
        if not self.is_dirty():
            return True
        r = QMessageBox.question(self, APP_NAME, T("Le document a été modifié. Enregistrer les modifications ?"),
                                 QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if r == QMessageBox.Save:
            return self.save()
        return r == QMessageBox.Discard

    def set_document(self, doc, path=None, items=None, denom=None):
        self.view.cancel_temp()
        self.doc = doc
        self.path = path
        if denom:
            self.scene.plan_denom = denom
            self.scale_combo.blockSignals(True)
            self.scale_combo.setCurrentText(str(denom))
            self.scale_combo.blockSignals(False)
            self.update_grid_step()
        for it in self.items():
            self.scene.removeItem(it)
        self.layout_pages()
        if items:
            self.restore_items(items)
        self.undo_stack, self.undo_idx = [], -1
        self.commit()
        self.saved_idx = self.undo_idx
        self.update_title()
        QTimer.singleShot(0, self.zoom_width)
        QTimer.singleShot(10, lambda: self.goto_page(0))

    def new_doc(self, size=None, n=None, ask=True):
        if ask:
            if not self.maybe_save():
                return
            dlg = QDialog(self)
            dlg.setWindowTitle(T("Nouveau document"))
            f = QFormLayout(dlg)
            fmt = QComboBox()
            fmt.addItems(PAPER.keys())
            f.addRow(T("Format"), fmt)
            np = QSpinBox(minimum=1, maximum=200, value=1)
            f.addRow(T("Nombre de pages"), np)
            bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            bb.accepted.connect(dlg.accept)
            bb.rejected.connect(dlg.reject)
            f.addRow(bb)
            if not dlg.exec():
                return
            size, n = PAPER[fmt.currentText()], np.value()
        doc = pymupdf.open()
        for _ in range(n):
            doc.new_page(width=size[0], height=size[1])
        self.set_document(doc)

    def open_dialog(self):
        if not self.maybe_save():
            return
        start = self.settings.value("lastdir", os.path.expanduser("~"))
        f, _ = QFileDialog.getOpenFileName(
            self, T("Ouvrir"), start,
            "Documents (*.pdf *.docx *.doc *.odt *.rtf *.txt *.pptx *.odp *.png *.jpg *.jpeg *.bmp *.tif *.tiff);;"
            "PDF (*.pdf);;Word / ODF (*.docx *.doc *.odt *.rtf);;Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;Tous (*)")
        if f:
            self.open_file(f)

    def open_file(self, f):
        self.settings.setValue("lastdir", os.path.dirname(f))
        ext = os.path.splitext(f)[1].lower()
        if ext in convert.OFFICE_EXT:
            self.run_task(T("Conversion en PDF…"), convert.office_to_pdf, (f,),
                          lambda out: (self._open_pdf(out, display_path=None, title_hint=f), self.conversion_note()))
            return
        if ext in convert.IMAGE_EXT:
            img = pymupdf.open(f)
            pdf = pymupdf.open("pdf", img.convert_to_pdf())
            self.set_document(pdf)
            return
        self._open_pdf(f, display_path=f)

    def _open_pdf(self, f, display_path=None, title_hint=None):
        try:
            doc = pymupdf.open(f)
        except Exception as ex:
            QMessageBox.critical(self, APP_NAME, T("Impossible d'ouvrir ce fichier :") + f"\n{ex}")
            return
        if doc.needs_pass:
            pw, ok = QInputDialog.getText(self, APP_NAME, T("Ce PDF est protégé. Mot de passe :"), QLineEdit.Password)
            if not ok or not doc.authenticate(pw):
                QMessageBox.warning(self, APP_NAME, T("Mot de passe incorrect."))
                return
        items, denom = None, None
        try:
            names = doc.embfile_names()
        except Exception:
            names = []
        if EMB_ORIG in names and EMB_ITEMS in names:
            meta = json.loads(doc.embfile_get(EMB_ITEMS).decode())
            items, denom = meta.get("items"), meta.get("denom")
            # valeurs saisies entre-temps dans Acrobat, un navigateur… : on les reprend
            filled = {}
            for page in doc:
                for wdg in page.widgets() or []:
                    filled.setdefault(wdg.field_name, []).append(wdg)
            for lst in (items or {}).values():
                for d in lst:
                    ws = filled.get(d.get("name")) if d.get("type", "").startswith("field") else None
                    if not ws:
                        continue
                    t = d["type"]
                    if t == "field_text" or t == "field_combo":
                        d["value"] = ws[0].field_value or ""
                    elif t == "field_check":
                        d["value"] = ws[0].field_value not in (False, "Off", "", None)
                    elif t == "field_radio":
                        for wdg in ws:
                            if (abs(wdg.rect.x0 - d["x"]) < 2 and abs(wdg.rect.y0 - d["y"]) < 2) or len(ws) == 1:
                                d["value"] = wdg.field_value not in (False, "Off", "", None)
            doc = pymupdf.open("pdf", doc.embfile_get(EMB_ORIG))
        else:
            doc = pymupdf.open("pdf", doc.tobytes())
        self.set_document(doc, display_path, items, denom)
        if display_path:
            self.add_recent(display_path)
        if title_hint:
            self.statusBar().showMessage(f"{os.path.basename(title_hint)} converti en PDF (pensez à « Enregistrer sous »)", 8000)

    def add_recent(self, f):
        rec = [r for r in (self.settings.value("recent") or []) if r != f]
        rec.insert(0, f)
        self.settings.setValue("recent", rec[:10])
        self.update_recent()

    def update_recent(self):
        self.recent_menu.clear()
        for r in self.settings.value("recent") or []:
            a = self.recent_menu.addAction(r)
            a.triggered.connect(lambda _=False, r=r: self.maybe_save() and self.open_file(r))

    def build_output(self, flat=False):
        """Fusionne les éléments dessinés (en vectoriel) dans le PDF et renvoie les octets."""
        self.view.cancel_temp() if self.view.temp is not None else None
        out = pymupdf.open("pdf", self.doc.tobytes())
        by = self.gather_items()
        draw_pages = {int(k) for k, v in by.items() if any(not d["type"].startswith("field") for d in v)}
        if draw_pages:
            buf = QBuffer()
            buf.open(QIODevice.WriteOnly)
            writer = QPdfWriter(buf)
            writer.setResolution(72)
            writer.setCreator(APP_NAME)

            def unrot(i):
                page = self.doc[i]
                ur = page.rect * page.derotation_matrix
                return abs(ur.width), abs(ur.height), page.derotation_matrix

            def set_size(pg):
                w0, h0, _ = unrot(pg.idx)
                writer.setPageSize(QPageSize(QSizeF(w0 / MM, h0 / MM), QPageSize.Millimeter, "", QPageSize.ExactMatch))
                writer.setPageMargins(QMarginsF(0, 0, 0, 0))

            set_size(self.page_items[0])
            painter = QPainter(writer)
            painter.setRenderHint(QPainter.Antialiasing)
            hidden = [pg for pg in self.page_items] + [i for i in self.items() if i.typ.startswith("field")]
            if self.view.ghost is not None:
                hidden.append(self.view.ghost)
            sel = self.scene.selectedItems()
            self.scene.clearSelection()
            for h in hidden:
                h.setVisible(False)
            self.scene.exporting = True
            bg = self.scene.backgroundBrush()
            self.scene.setBackgroundBrush(Qt.NoBrush)
            try:
                for i, pg in enumerate(self.page_items):
                    if i > 0:
                        set_size(pg)
                        writer.newPage()
                    if i in draw_pages:
                        # les éléments sont dessinés dans l'espace « non tourné » de la page,
                        # pour rester justes sur les pages pivotées (/Rotate)
                        w0, h0, m = unrot(i)
                        src = QRectF(pg.pos().x(), pg.pos().y(), pg.w, pg.h)
                        dpr = writer.width() / w0
                        painter.save()
                        painter.setTransform(QTransform(m.a, m.b, m.c, m.d, m.e, m.f) * QTransform.fromScale(dpr, dpr))
                        self.scene.render(painter, QRectF(0, 0, pg.w, pg.h), src, Qt.IgnoreAspectRatio)
                        painter.restore()
            finally:
                painter.end()
                self.scene.setBackgroundBrush(bg)
                self.scene.exporting = False
                for h in hidden:
                    h.setVisible(True)
                for s in sel:
                    s.setSelected(True)
            overlay = pymupdf.open("pdf", bytes(buf.data()))
            for i in sorted(draw_pages):
                page = out[i]
                w0, h0, _ = unrot(i)
                page.show_pdf_page(pymupdf.Rect(0, 0, w0, h0), overlay, i, keep_proportion=False, overlay=True)
        # champs de formulaire
        for k, lst in by.items():
            page = out[int(k)]
            for d in lst:
                if not d["type"].startswith("field"):
                    continue
                w = pymupdf.Widget()
                w.field_name = d.get("name") or "champ"
                x, y = d["x"], d["y"]
                w.rect = pymupdf.Rect(x, y, x + d["w"], y + d["h"]) * page.derotation_matrix
                t = d["type"]
                if t == "field_link":
                    lk = {"from": w.rect}
                    if d.get("url"):
                        lk.update(kind=pymupdf.LINK_URI, uri=d["url"])
                    else:
                        lk.update(kind=pymupdf.LINK_GOTO, page=max(0, min(len(out) - 1, int(d.get("page") or 1) - 1)),
                                  to=pymupdf.Point(0, 0))
                    page.insert_link(lk)
                    continue
                if t == "field_text":
                    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
                    w.field_value = d.get("value") or ""
                    w.text_fontsize = 0
                elif t == "field_combo":
                    w.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
                    w.choice_values = d.get("options") or ["—"]
                    w.field_value = d.get("value") or w.choice_values[0]
                elif t == "field_radio":
                    w.field_type = pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON
                    w.field_value = bool(d.get("value"))
                elif t == "field_sig":
                    w.field_type = pymupdf.PDF_WIDGET_TYPE_SIGNATURE
                else:
                    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
                    w.field_value = bool(d.get("value"))
                w.border_color = (0.45, 0.2, 0.6)
                w.border_width = 0.5
                page.add_widget(w)
        try:
            if out.is_form_pdf:
                out.need_appearances(True)
        except Exception:
            pass
        out.set_metadata({**(self.doc.metadata or {}), "creator": f"{APP_NAME} {APP_VERSION}", "producer": APP_NAME})
        if not flat and by:
            meta = json.dumps({"items": by, "denom": self.scene.plan_denom, "version": APP_VERSION})
            out.embfile_add(EMB_ORIG, self.doc.tobytes(), filename=EMB_ORIG, desc="PDF DUO : document d'origine")
            out.embfile_add(EMB_ITEMS, meta.encode(), filename=EMB_ITEMS, desc="PDF DUO : éléments modifiables")
        return out.tobytes(garbage=3, deflate=True)

    def save(self):
        if not self.path or not self.path.lower().endswith(".pdf"):
            return self.save_as()
        return self.write_pdf(self.path)

    def save_as(self):
        start = self.path or os.path.join(self.settings.value("lastdir", os.path.expanduser("~")), "document.pdf")
        f, _ = QFileDialog.getSaveFileName(self, T("Enregistrer sous"), start, "PDF (*.pdf)")
        if not f:
            return False
        if not f.lower().endswith(".pdf"):
            f += ".pdf"
        ok = self.write_pdf(f)
        if ok:
            self.path = f
            self.add_recent(f)
            self.update_title()
        return ok

    def write_pdf(self, f, flat=False):
        try:
            data = self.build_output(flat)
            tmp = f + ".tmp"
            with open(tmp, "wb") as fh:
                fh.write(data)
            os.replace(tmp, f)
        except Exception as ex:
            QMessageBox.critical(self, APP_NAME, T("Enregistrement impossible :") + f"\n{ex}")
            return False
        if not flat:
            self.saved_idx = self.undo_idx
            self.update_title()
        self.statusBar().showMessage(T("Enregistré :") + f" {f}", 5000)
        return True

    def export_flat(self):
        base = os.path.splitext(self.path or "document.pdf")[0] + "-final.pdf"
        f, _ = QFileDialog.getSaveFileName(self, T("Exporter le PDF final"), base, "PDF (*.pdf)")
        if f:
            self.write_pdf(f if f.lower().endswith(".pdf") else f + ".pdf", flat=True)

    def print_doc(self):
        printer = QPrinter(QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)
        if not dlg.exec():
            return
        doc = pymupdf.open("pdf", self.build_output(flat=True))
        p = QPainter(printer)
        first = True
        rng = range(len(doc))
        if printer.printRange() == QPrinter.PageRange:
            rng = range(max(0, printer.fromPage() - 1), min(len(doc), printer.toPage()))
        for i in rng:
            if not first:
                printer.newPage()
            first = False
            img = qimage_from_pix(doc[i].get_pixmap(dpi=300, alpha=False))
            r = p.viewport()
            sz = img.size().scaled(r.size(), Qt.KeepAspectRatio)
            p.drawImage(QRectF((r.width() - sz.width()) / 2, (r.height() - sz.height()) / 2, sz.width(), sz.height()), img)
        p.end()

    # ------------------------------------------------------------------ opérations sur les pages
    def page_op(self, fn, mapping, transform=None):
        by = self.gather_items()
        fn(self.doc)
        new = {}
        for k, lst in by.items():
            j = mapping(int(k))
            if j is None:
                continue
            if transform:
                lst = [transform(int(k), d) for d in lst]
            new.setdefault(str(j), []).extend(lst)
        self.doc = pymupdf.open("pdf", self.doc.tobytes())
        self.layout_pages()
        self.restore_items(new)
        self.commit(doc_changed=True)

    def page_insert_blank(self):
        i = self.current_page()
        r = self.doc[i].rect
        self.page_op(lambda d: d.new_page(pno=i + 1, width=r.width, height=r.height),
                     lambda k: k if k <= i else k + 1)
        self.goto_page(i + 1)

    def page_duplicate(self):
        i = self.current_page()
        by = self.gather_items()
        self.page_op(lambda d: d.fullcopy_page(i, i + 1 if i + 1 < len(d) else -1),
                     lambda k: k if k <= i else k + 1)
        if str(i) in by:
            pg = self.page_items[i + 1]
            for d in by[str(i)]:
                d = dict(d)
                d["x"] += pg.pos().x()
                d["y"] += pg.pos().y()
                self.add_item(d)
            self.commit()

    def page_delete(self):
        if len(self.doc) <= 1:
            QMessageBox.information(self, APP_NAME, T("Le document doit garder au moins une page."))
            return
        i = self.current_page()
        if QMessageBox.question(self, APP_NAME, T("Supprimer la page {n} ?").format(n=i + 1)) != QMessageBox.Yes:
            return
        self.page_op(lambda d: d.delete_page(i), lambda k: None if k == i else (k if k < i else k - 1))

    def page_move(self, delta):
        i = self.current_page()
        j = i + delta
        if not 0 <= j < len(self.doc):
            return

        def fn(d):
            if delta > 0:
                d.move_page(i, j + 1 if j + 1 < len(d) else -1)
            else:
                d.move_page(i, j)
        self.page_op(fn, lambda k: j if k == i else (i if k == j else k))
        self.goto_page(j)

    def page_rotate(self, deg):
        i = self.current_page()
        w, h = self.doc[i].rect.width, self.doc[i].rect.height

        def tr(k, d):
            if k != i:
                return d
            it = PItem(d)
            c = it.local_rect().center()
            cx, cy = d["x"] + c.x(), d["y"] + c.y()
            if deg == 90:      # sens horaire
                nx, ny = h - cy, cx
                d["angle"] = (d["angle"] - 90) % 360
            else:
                nx, ny = cy, w - cx
                d["angle"] = (d["angle"] + 90) % 360
            d["x"], d["y"] = nx - c.x(), ny - c.y()
            return d
        self.page_op(lambda d: d[i].set_rotation((d[i].rotation + deg) % 360), lambda k: k, tr)

    def page_merge(self):
        f, _ = QFileDialog.getOpenFileName(self, T("Ajouter un document à la fin"), self.settings.value("lastdir", ""),
                                           "Documents (*.pdf *.docx *.doc *.odt *.png *.jpg *.jpeg)")
        if not f:
            return

        def merge(pdf_path):
            other = pymupdf.open(pdf_path)
            if other.is_pdf is False:
                other = pymupdf.open("pdf", other.convert_to_pdf())
            n = len(self.doc)
            self.page_op(lambda d: d.insert_pdf(other), lambda k: k)
            self.goto_page(n)

        if f.lower().endswith(convert.OFFICE_EXT):
            self.run_task("Conversion en PDF…", convert.office_to_pdf, (f,), merge)
        else:
            merge(f)

    def parse_ranges(self, txt, n):
        pages = []
        for part in txt.replace(" ", "").split(","):
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                a = int(a) if a else 1
                b = int(b) if b else n
                pages += list(range(a - 1, min(b, n)))
            else:
                pages.append(int(part) - 1)
        return [p for p in pages if 0 <= p < n]

    def page_extract(self):
        n = len(self.doc)
        txt, ok = QInputDialog.getText(self, T("Extraire des pages"), f"Pages à extraire (ex. 1-3,5) sur {n} :",
                                       text=str(self.current_page() + 1))
        if not ok:
            return
        try:
            pages = self.parse_ranges(txt, n)
        except ValueError:
            QMessageBox.warning(self, APP_NAME, T("Plage de pages incorrecte."))
            return
        if not pages:
            return
        f, _ = QFileDialog.getSaveFileName(self, T("Enregistrer les pages extraites"), T("extrait.pdf"), "PDF (*.pdf)")
        if not f:
            return
        full = pymupdf.open("pdf", self.build_output(flat=True))
        full.select(pages)
        full.save(f if f.lower().endswith(".pdf") else f + ".pdf", garbage=3, deflate=True)
        self.statusBar().showMessage(f"{len(pages)} page(s) extraite(s)", 5000)

    def page_split(self):
        d = QFileDialog.getExistingDirectory(self, T("Dossier où enregistrer les pages"))
        if not d:
            return
        full = pymupdf.open("pdf", self.build_output(flat=True))
        base = os.path.splitext(os.path.basename(self.path or "document"))[0]
        for i in range(len(full)):
            one = pymupdf.open()
            one.insert_pdf(full, from_page=i, to_page=i)
            one.save(os.path.join(d, f"{base}-page{i + 1:03d}.pdf"), garbage=3, deflate=True)
        self.statusBar().showMessage(f"{len(full)} fichiers créés dans {d}", 6000)

    # ------------------------------------------------------------------ formulaires
    def refresh_forms(self):
        self.form_table.blockSignals(True)
        self.form_table.setRowCount(0)
        self._widgets = []
        if self.doc:
            for pno, page in enumerate(self.doc):
                for wdg in page.widgets() or []:
                    r = self.form_table.rowCount()
                    self.form_table.insertRow(r)
                    name = QTableWidgetItem(wdg.field_name or "")
                    name.setFlags(name.flags() & ~Qt.ItemIsEditable)
                    typ = QTableWidgetItem(wdg.field_type_string)
                    typ.setFlags(typ.flags() & ~Qt.ItemIsEditable)
                    val = QTableWidgetItem()
                    if wdg.field_type in (pymupdf.PDF_WIDGET_TYPE_CHECKBOX, pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON):
                        val.setFlags((val.flags() | Qt.ItemIsUserCheckable) & ~Qt.ItemIsEditable)
                        on = wdg.field_value not in (False, "Off", "", None)
                        val.setCheckState(Qt.Checked if on else Qt.Unchecked)
                    else:
                        val.setText(str(wdg.field_value or ""))
                    for c, x in enumerate((name, typ, val)):
                        self.form_table.setItem(r, c, x)
                    self._widgets.append((pno, wdg.xref))
        for it in sorted(self.items(), key=lambda i: (i.pos().y(), i.pos().x())):
            if it.typ not in ("field_text", "field_check", "field_combo", "field_radio"):
                continue
            r = self.form_table.rowCount()
            self.form_table.insertRow(r)
            name = QTableWidgetItem(it.d.get("name", ""))
            name.setFlags(name.flags() & ~Qt.ItemIsEditable)
            typ = QTableWidgetItem(T(self.item_title(it)))
            typ.setFlags(typ.flags() & ~Qt.ItemIsEditable)
            val = QTableWidgetItem()
            if it.typ in ("field_check", "field_radio"):
                val.setFlags((val.flags() | Qt.ItemIsUserCheckable) & ~Qt.ItemIsEditable)
                val.setCheckState(Qt.Checked if it.d.get("value") else Qt.Unchecked)
            else:
                val.setText(str(it.d.get("value") or ""))
            for c, x in enumerate((name, typ, val)):
                self.form_table.setItem(r, c, x)
            self._widgets.append(("item", it.d["uid"]))
        self.form_table.blockSignals(False)

    def form_value_changed(self, item):
        if item.column() != 2:
            return
        pno, xref = self._widgets[item.row()]
        if pno == "item":
            for it in self.items():
                if it.d.get("uid") == xref:
                    if it.typ in ("field_check", "field_radio"):
                        on = item.checkState() == Qt.Checked
                        if on and it.typ == "field_radio":
                            for o in self.items():
                                if o.typ == "field_radio" and o.d.get("name") == it.d.get("name"):
                                    o.d["value"] = False
                                    o.update()
                        it.d["value"] = on
                    elif it.typ == "field_combo" and item.text() not in (it.d.get("options") or []):
                        it.d.setdefault("options", []).append(item.text())
                        it.d["value"] = item.text()
                    else:
                        it.d["value"] = item.text()
                    it.update()
            self.commit()
            QTimer.singleShot(0, self.refresh_forms)
            return
        page = self.doc[pno]
        for wdg in page.widgets():
            if wdg.xref == xref:
                if wdg.field_type in (pymupdf.PDF_WIDGET_TYPE_CHECKBOX, pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON):
                    wdg.field_value = wdg.on_state() if item.checkState() == Qt.Checked else "Off"
                else:
                    wdg.field_value = item.text()
                wdg.update()
                break
        self.doc = pymupdf.open("pdf", self.doc.tobytes())
        by = self.gather_items()
        self.layout_pages()
        self.restore_items(by)
        self.commit(doc_changed=True)

    # ------------------------------------------------------------------ conversions
    def run_task(self, label, fn, args, on_done):
        prog = QProgressDialog(label, None, 0, 0, self)
        prog.setWindowTitle(APP_NAME)
        prog.setWindowModality(Qt.WindowModal)
        prog.setMinimumDuration(0)
        prog.show()
        w = Worker(fn, *args)

        def fin(res, err):
            prog.close()
            self.workers.remove(w)
            if err:
                QMessageBox.critical(self, APP_NAME, T("Échec :") + f"\n{err}")
            else:
                on_done(res)
        w.done.connect(fin)
        self.workers.append(w)
        w.start()

    def conversion_note(self):
        """Signale dans la barre d'état quel outil a fait la conversion."""
        eng = getattr(convert, "LAST_ENGINE", "")
        if eng == "integree":
            self.statusBar().showMessage(T("Converti par PDF DUO (LibreOffice et Word absents) : mise en page simplifiée. "
                                           "Pour une conversion fidèle, installez LibreOffice (gratuit)."), 15000)
        elif eng == "word":
            self.statusBar().showMessage(T("Converti avec Microsoft Word."), 8000)

    def conv_office_to_pdf(self):
        files, _ = QFileDialog.getOpenFileNames(self, T("Documents Word / ODT à convertir en PDF"),
                                                self.settings.value("lastdir", ""),
                                                "Documents (*.docx *.doc *.odt *.rtf *.txt *.pptx *.odp *.xlsx *.ods)")
        if not files:
            return

        def job(files):
            outs = []
            for f in files:
                outs.append(convert.office_to_pdf(f, os.path.splitext(f)[0] + ".pdf"))
            return outs

        def done(outs):
            self.conversion_note()
            r = QMessageBox.question(self, APP_NAME, T("PDF créé(s) à côté des originaux :") + f" {len(outs)}\n\n"
                                     + T("Ouvrir le premier dans PDF DUO ?"))
            if r == QMessageBox.Yes and self.maybe_save():
                self.open_file(outs[0])
        self.run_task(T("Conversion en PDF…"), job, (files,), done)

    def conv_pdf_to(self, fmt):
        base = os.path.splitext(self.path or "document")[0] + "." + fmt
        f, _ = QFileDialog.getSaveFileName(self, f"Exporter en {fmt.upper()}", base,
                                           "Word (*.docx)" if fmt == "docx" else "OpenDocument (*.odt)")
        if not f:
            return
        if not f.lower().endswith("." + fmt):
            f += "." + fmt
        tmp = os.path.join(tempfile.mkdtemp(prefix="pdfduo-"), "source.pdf")
        with open(tmp, "wb") as fh:
            fh.write(self.build_output(flat=True))
        fn = convert.pdf_to_docx if fmt == "docx" else convert.pdf_to_odt
        self.run_task(f"Conversion en {fmt.upper()}…", fn, (tmp, f),
                      lambda out: QMessageBox.information(self, APP_NAME, T("Fichier créé :") + f"\n{out}"))

    def conv_word_odt(self):
        f, _ = QFileDialog.getOpenFileName(self, T("Document à convertir (Word ↔ ODT)"), self.settings.value("lastdir", ""),
                                           "Documents (*.docx *.doc *.odt *.rtf)")
        if not f:
            return
        target = "odt" if not f.lower().endswith(".odt") else "docx"
        out = os.path.splitext(f)[0] + "." + target
        out, _ = QFileDialog.getSaveFileName(self, T("Enregistrer sous"), out,
                                             "OpenDocument (*.odt)" if target == "odt" else "Word (*.docx)")
        if out:
            self.run_task("Conversion…", convert.office_to_office, (f, out),
                          lambda o: QMessageBox.information(self, APP_NAME, T("Fichier créé :") + f"\n{o}"))

    def conv_images_to_pdf(self):
        files, _ = QFileDialog.getOpenFileNames(self, T("Images à assembler en PDF"), self.settings.value("lastdir", ""),
                                                "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.gif)")
        if not files or not self.maybe_save():
            return
        doc = pymupdf.open()
        for f in files:
            img = pymupdf.open(f)
            doc.insert_pdf(pymupdf.open("pdf", img.convert_to_pdf()))
        self.set_document(doc)

    def conv_pdf_to_png(self):
        d = QFileDialog.getExistingDirectory(self, T("Dossier des images"))
        if not d:
            return
        dpi, ok = QInputDialog.getInt(self, T("Résolution"), T("Résolution (dpi) :"), 200, 50, 600)
        if not ok:
            return
        full = pymupdf.open("pdf", self.build_output(flat=True))
        base = os.path.splitext(os.path.basename(self.path or "document"))[0]
        for i, page in enumerate(full):
            page.get_pixmap(dpi=dpi).save(os.path.join(d, f"{base}-{i + 1:03d}.png"))
        self.statusBar().showMessage(f"{len(full)} image(s) enregistrée(s)", 5000)

    # ------------------------------------------------------------------ aide
    def show_help(self):
        QMessageBox.information(self, T("Raccourcis"), (
            "<b>Outils</b> : Échap revient à la sélection ; clic droit termine un fil / un mur.<br>"
            "<b>Pendant la pose d'un symbole</b> : R tourne de 90°, Maj+R de −90°, E de 15°, H miroir ↔, V miroir ↕.<br>"
            "<b>Sur la sélection</b> : mêmes touches R / E / H / V, flèches pour déplacer (Maj = finement), Suppr.<br>"
            "<b>Angle précis</b> : panneau Propriétés ou Édition › Rotation › Angle précis.<br>"
            "<b>Aimantation</b> : maintenir Alt pour poser librement hors grille.<br>"
            "<b>Trait / cote</b> : Maj pour des angles par pas de 15°. <b>Ellipse</b> : Maj pour un cercle.<br>"
            "<b>Capture</b> : outil Capture puis glisser ; l'image va au presse-papiers (Ctrl+V).<br>"
            "<b>Copier</b> (Ctrl+C) : les éléments se recollent dans PDF DUO <i>et</i> comme image dans Word.<br>"
            "<b>Zoom</b> : Ctrl+molette ; molette = défilement ; bouton du milieu = déplacer la vue."))

    # ------------------------------------------------------------ mode présentation (plein écran)
    def toggle_presentation(self, on=None):
        """Plein écran sans palettes : seule la page reste visible. Le haut (menus, zoom, annuler…)
        réapparaît quand la souris touche le bord supérieur de l'écran."""
        if on is None:
            on = not getattr(self, "presenting", False)
        if on == getattr(self, "presenting", False):
            return
        self.presenting = on
        self.present_action.setChecked(on)
        if on:
            self._pres_state = self.saveState(99)
            self._pres_max = self.isMaximized()
            self._pres_bars = [b for b in self.findChildren(QToolBar)
                               if b.isVisible() and b is not self.quick_bar and self.toolBarArea(b) == Qt.TopToolBarArea]
            keep = {self.quick_bar, self.findChild(QToolBar, "outils"), self.findChild(QDockWidget, "biblio")}
            for w in self.findChildren(QDockWidget) + self.findChildren(QToolBar):
                if w not in keep:
                    w.hide()
            bib = self.findChild(QDockWidget, "biblio")
            if bib is not None:
                bib.show()
                self._pres_bib_max = bib.maximumWidth()
                narrow = 2 * self.sym_list.gridSize().width() + 34
                bib.setMaximumWidth(narrow)
                self.resizeDocks([bib], [narrow], Qt.Horizontal)
            tools = self.findChild(QToolBar, "outils")
            if tools is not None:
                tools.show()
            self.statusBar().hide()
            self.menuBar().hide()
            self.showFullScreen()
            if not hasattr(self, "_pres_timer"):
                self._pres_timer = QTimer(self, interval=120, timeout=self._presentation_hover)
            self._pres_timer.start()
            self._pres_shown = False
            QTimer.singleShot(250, self.zoom_page)
            self._presentation_hint()
        else:
            self._pres_timer.stop()
            self.menuBar().show()
            self.statusBar().show()
            if self.isFullScreen():
                self.showMaximized() if self._pres_max else self.showNormal()
            bib = self.findChild(QDockWidget, "biblio")
            if bib is not None:
                bib.setMaximumWidth(getattr(self, "_pres_bib_max", 16777215))
            self.restoreState(self._pres_state, 99)
            hint = getattr(self, "_pres_hint", None)
            if hint:
                hint.hide()

    def _presentation_hover(self):
        """Affiche le haut quand la souris est contre le bord supérieur, le masque ensuite."""
        from PySide6.QtGui import QCursor
        y = self.mapFromGlobal(QCursor.pos()).y()
        if not self._pres_shown and y <= 4:
            self.menuBar().show()
            for b in self._pres_bars:
                b.show()
            self._pres_shown = True
        elif self._pres_shown:
            bottom = self.menuBar().height() + sum(b.height() for b in self._pres_bars) + 30
            if y > bottom and QApplication.activePopupWidget() is None and not self.menuBar().activeAction():
                self.menuBar().hide()
                for b in self._pres_bars:
                    b.hide()
                self._pres_shown = False

    def _presentation_hint(self):
        hint = getattr(self, "_pres_hint", None)
        if hint is None:
            hint = self._pres_hint = QLabel(self)
            hint.setStyleSheet("QLabel{background:rgba(20,30,45,210);color:white;border-radius:10px;padding:10px 18px;font-size:13px}")
            hint.setAttribute(Qt.WA_TransparentForMouseEvents)
        hint.setText(T("Mode présentation — les outils (à gauche) et la bibliothèque (à droite) restent visibles · "
                       "touchez le haut de l'écran pour les menus et le zoom · F11 ou Échap pour quitter"))
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignCenter)

        def place():
            hint.setFixedWidth(min(760, self.width() - 40))
            hint.adjustSize()
            hint.move((self.width() - hint.width()) // 2, 40)
            hint.show()
            hint.raise_()
        QTimer.singleShot(400, place)
        QTimer.singleShot(5000, hint.hide)

    def open_link_safely(self, url):
        """Ouvre un lien venant d'un document. Seuls http, https et mailto s'ouvrent directement :
        un lien vers un fichier ou un programme (file:, smb:, javascript:…) pourrait lancer un logiciel
        malveillant caché dans un PDF reçu, donc on le refuse."""
        from PySide6.QtCore import QUrl
        u = QUrl.fromUserInput(str(url).strip())
        if u.scheme().lower() not in ("http", "https", "mailto") or not u.isValid():
            QMessageBox.warning(self, APP_NAME, T("Ce lien n'a pas été ouvert par sécurité : seuls les liens web (http, https) "
                                                  "et les adresses e-mail sont autorisés.") + "\n\n" + str(url)[:300])
            return
        r = QMessageBox.question(self, APP_NAME, T("Ouvrir ce lien dans le navigateur ?") + "\n\n" + u.toDisplayString()[:300])
        if r == QMessageBox.Yes:
            self.open_url(u.toString())

    def open_url(self, url):
        from PySide6.QtGui import QDesktopServices
        from PySide6.QtCore import QUrl
        QDesktopServices.openUrl(QUrl(url))

    def open_notice(self):
        from PySide6.QtGui import QDesktopServices
        from PySide6.QtCore import QUrl
        from . import i18n as _i
        lang = _i.LANG
        here = os.path.dirname(os.path.abspath(__file__))
        base = getattr(sys, "_MEIPASS", None)
        cands = []
        for root in (here, os.path.join(base, "pdfduo") if base else None):
            if root:
                cands += [os.path.join(root, "notices", f"notice-{lang}.pdf"),
                          os.path.join(root, "notices", "notice-en.pdf"),
                          os.path.join(root, "notices", "notice-fr.pdf")]
        for c in cands:
            if os.path.exists(c):
                QDesktopServices.openUrl(QUrl.fromLocalFile(c))
                return
        self.open_url(f"{SITE_URL}notice/notice-{lang}.html")

    def maybe_donate_reminder(self):
        """Rappel discret : au 5e lancement puis tous les 40 lancements (désactivable)."""
        n = int(self.settings.value("launches", 0) or 0) + 1
        self.settings.setValue("launches", n)
        if str(self.settings.value("no_donate_reminder", "0")) in ("1", "true"):
            return
        if n == 5 or (n > 5 and (n - 5) % 40 == 0):
            QTimer.singleShot(1500, lambda: self.donate(auto=True))

    def donate(self, auto=False):
        dlg = QDialog(self)
        dlg.setWindowTitle(T("Soutenir PDF DUO"))
        lay = QVBoxLayout(dlg)
        lab = QLabel(
            "<h3>☕ " + T("Soutenir PDF DUO") + "</h3>"
            "<p>" + T("PDF DUO est gratuit et libre, sans publicité.") + "</p>"
            "<p>" + T("S'il vous rend service, en classe ou ailleurs, un petit don aide à le faire évoluer : "
                      "nouveaux symboles, corrections, nouvelles langues.") + "</p>"
            f'<p><a style="color:#29abe0;font-weight:bold" href="{KOFI_URL}">{KOFI_URL.replace("https://", "")}</a></p>'
            "<p>" + T("Merci !") + " — Jacques Branas</p>")
        lab.setWordWrap(True)
        lab.setOpenExternalLinks(True)
        lab.setMinimumWidth(380)
        lay.addWidget(lab)
        row = QHBoxLayout()
        b = QPushButton("☕  " + T("Faire un don sur Ko-fi"))
        b.setDefault(True)
        b.setStyleSheet("QPushButton{background:#29abe0;color:white;font-weight:bold;padding:8px 16px;border-radius:6px}")
        b.clicked.connect(lambda: (self.open_url(KOFI_URL), dlg.accept()))
        row.addWidget(b)
        c = QPushButton(T("Plus tard"))
        c.clicked.connect(dlg.reject)
        row.addWidget(c)
        lay.addLayout(row)
        if auto:
            chk = QCheckBox(T("Ne plus afficher ce rappel"))
            lay.addWidget(chk)
        dlg.exec()
        if auto and chk.isChecked():
            self.settings.setValue("no_donate_reminder", "1")

    def about(self):
        box = QMessageBox(self)
        box.setWindowTitle(APP_NAME)
        box.setIconPixmap(self.windowIcon().pixmap(64, 64))
        box.setTextFormat(Qt.RichText)
        box.setText(
            f"<h3>{APP_NAME} {APP_VERSION}</h3>"
            "<p>" + T("Lire, annoter, signer et remplir des PDF, dessiner des schémas électriques "
                      "et des plans d'installation, convertir Word / ODF ↔ PDF.") + "</p>"
            f"<p>{CREDIT}</p>"
            f'<p><a href="{SITE_URL}">deltapassion.github.io/PDF-DUO</a></p>'
            "<p>" + T("Logiciel libre sous licence GNU GPL v3 ou ultérieure.") + "<br>"
            "Qt (PySide6), PyMuPDF, pdf2docx, LibreOffice.</p>")
        kb = box.addButton("☕ " + T("Faire un don"), QMessageBox.ActionRole)
        box.addButton(QMessageBox.Ok)
        box.exec()
        if box.clickedButton() is kb:
            self.donate()

    def closeEvent(self, e):
        if not self.maybe_save():
            e.ignore()
            return
        if getattr(self, "presenting", False):
            self.toggle_presentation(False)     # sinon les palettes resteraient cachées au prochain lancement
        try:
            self.scene.selectionChanged.disconnect(self.refresh_props)
        except (RuntimeError, TypeError):
            pass
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("state", self.saveState(4))
        e.accept()


def install_qt_translator(app):
    """Traduit les boutons standard de Qt (OK, Annuler, Oui, Non…) dans la langue choisie."""
    from PySide6.QtCore import QLibraryInfo, QTranslator
    from . import i18n
    path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
    tr = QTranslator(app)
    for name in (i18n.LANG, {"pt": "pt_PT"}.get(i18n.LANG, ""), {"pt": "pt_BR"}.get(i18n.LANG, "")):
        if name and tr.load("qtbase_" + name, path):
            app.installTranslator(tr)
            app._qt_tr = tr
            return True
    return False


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("Jacques Branas")
    from .i18n import set_language
    set_language(QSettings("Jacques Branas", "PDF DUO").value("lang", "fr"))
    install_qt_translator(app)
    app.setApplicationVersion(APP_VERSION)
    here = os.path.dirname(os.path.abspath(__file__))
    ico = os.path.join(here, "icon.png")
    if os.path.exists(ico):
        app.setWindowIcon(QIcon(ico))
    w = MainWindow()
    w.show()
    w.maybe_donate_reminder()
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        w.open_file(sys.argv[1])
    sys.exit(app.exec())
