"""Calculatrice scientifique et graphique (fenêtre indépendante)."""
import math

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QDialog, QDoubleSpinBox,
                               QFormLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QListWidget, QPushButton, QRadioButton, QSizePolicy, QTabWidget,
                               QVBoxLayout, QWidget)

from . import calc
from .i18n import T


def err_text(e):
    m = str(e)
    if " : " in m:
        a, b = m.split(" : ", 1)
        return T(a) + " : " + b
    return T(m)

COLORS = ("#1565c0", "#d32f2f", "#2e7d32")


def nice_step(span, n=10):
    raw = span / max(1, n)
    p = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * p:
            return m * p
    return 10 * p


def show(v):
    from . import i18n
    s = calc.fmt(v, 12)
    return s if i18n.LANG == "en" else s.replace(".", ",")


class Plot(QWidget):
    moved = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(420, 320)
        self.setMouseTracking(True)
        self.funcs = []          # (texte, fonction, couleur)
        self.xmin, self.xmax, self.ymin, self.ymax = -10.0, 10.0, -10.0, 10.0
        self._drag = None

    def to_px(self, x, y, r):
        return QPointF(r.left() + (x - self.xmin) / (self.xmax - self.xmin) * r.width(),
                       r.bottom() - (y - self.ymin) / (self.ymax - self.ymin) * r.height())

    def draw(self, p, r, scale=1.0):
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(r, QColor("#ffffff"))
        sx, sy = nice_step(self.xmax - self.xmin), nice_step(self.ymax - self.ymin)
        f = QFont("DejaVu Sans")
        f.setPixelSize(max(8, int(10 * scale)))
        p.setFont(f)
        # quadrillage
        p.setPen(QPen(QColor("#e3e8ee"), 1 * scale))
        x = math.ceil(self.xmin / sx) * sx
        while x <= self.xmax + 1e-12:
            a = self.to_px(x, 0, r)
            p.drawLine(QPointF(a.x(), r.top()), QPointF(a.x(), r.bottom()))
            x += sx
        y = math.ceil(self.ymin / sy) * sy
        while y <= self.ymax + 1e-12:
            a = self.to_px(0, y, r)
            p.drawLine(QPointF(r.left(), a.y()), QPointF(r.right(), a.y()))
            y += sy
        # axes
        o = self.to_px(0, 0, r)
        ox = min(max(o.x(), r.left()), r.right())
        oy = min(max(o.y(), r.top()), r.bottom())
        p.setPen(QPen(QColor("#37474f"), 1.4 * scale))
        p.drawLine(QPointF(r.left(), oy), QPointF(r.right(), oy))
        p.drawLine(QPointF(ox, r.top()), QPointF(ox, r.bottom()))
        p.setPen(QColor("#455a64"))
        x = math.ceil(self.xmin / sx) * sx
        while x <= self.xmax + 1e-12:
            if abs(x) > sx / 1000:
                a = self.to_px(x, 0, r)
                p.drawLine(QPointF(a.x(), oy - 3 * scale), QPointF(a.x(), oy + 3 * scale))
                if r.left() + 8 * scale < a.x() < r.right() - 8 * scale:
                    ty = oy + 3 * scale if oy + 18 * scale < r.bottom() else oy - 17 * scale
                    p.drawText(QRectF(a.x() - 30 * scale, ty, 60 * scale, 14 * scale), Qt.AlignHCenter | Qt.AlignTop, show(round(x, 10)))
            x += sx
        y = math.ceil(self.ymin / sy) * sy
        while y <= self.ymax + 1e-12:
            if abs(y) > sy / 1000:
                a = self.to_px(0, y, r)
                p.drawLine(QPointF(ox - 3 * scale, a.y()), QPointF(ox + 3 * scale, a.y()))
                if r.top() + 8 * scale < a.y() < r.bottom() - 8 * scale:
                    if ox - 64 * scale > r.left():
                        p.drawText(QRectF(ox - 64 * scale, a.y() - 7 * scale, 60 * scale, 14 * scale), Qt.AlignRight | Qt.AlignVCenter, show(round(y, 10)))
                    else:
                        p.drawText(QRectF(ox + 5 * scale, a.y() - 7 * scale, 60 * scale, 14 * scale), Qt.AlignLeft | Qt.AlignVCenter, show(round(y, 10)))
            y += sy
        p.drawText(QRectF(r.right() - 20 * scale, oy - 18 * scale, 16 * scale, 14 * scale), Qt.AlignRight, "x")
        p.drawText(QRectF(ox + 5 * scale, r.top() + 2 * scale, 16 * scale, 14 * scale), Qt.AlignLeft, "y")
        # courbes
        p.save()
        p.setClipRect(r)
        n = int(max(200, r.width() * 1.5))
        ly = r.top() + 6 * scale
        for txt, fn, colr in self.funcs:
            path = QPainterPath()
            started = False
            prev = None
            for i in range(n + 1):
                xv = self.xmin + (self.xmax - self.xmin) * i / n
                yv = fn(xv)
                if yv is None or abs(yv) > 1e9:
                    started = False
                    prev = None
                    continue
                q = self.to_px(xv, yv, r)
                if started and prev is not None and abs(q.y() - prev.y()) > r.height() * 2:
                    started = False     # asymptote : on lève le crayon
                if started:
                    path.lineTo(q)
                else:
                    path.moveTo(q)
                    started = True
                prev = q
            p.setPen(QPen(QColor(colr), 2.2 * scale))
            p.setBrush(Qt.NoBrush)
            p.drawPath(path)
        p.restore()
        if self.funcs:      # légende dans un cartouche blanc
            fm = p.fontMetrics()
            lw = max(fm.horizontalAdvance("y = " + t) for t, _, _ in self.funcs) + 14 * scale
            box = QRectF(r.left() + 4 * scale, r.top() + 4 * scale, lw, 15 * scale * len(self.funcs) + 6 * scale)
            p.setPen(QPen(QColor("#cfd8dc"), 1 * scale))
            p.setBrush(QColor(255, 255, 255, 235))
            p.drawRect(box)
            for i, (txt, _, colr) in enumerate(self.funcs):
                p.setPen(QColor(colr))
                p.drawText(QRectF(box.left() + 7 * scale, box.top() + 3 * scale + i * 15 * scale, lw, 14 * scale), Qt.AlignLeft, "y = " + txt)
        p.setPen(QPen(QColor("#90a4ae"), 1 * scale))
        p.setBrush(Qt.NoBrush)
        p.drawRect(r)

    def paintEvent(self, e):
        p = QPainter(self)
        self.draw(p, QRectF(self.rect()).adjusted(1, 1, -1, -1))
        p.end()

    def image(self, w=1600, h=1200):
        img = QImage(w, h, QImage.Format_ARGB32)
        img.fill(QColor("white"))
        p = QPainter(img)
        self.draw(p, QRectF(2, 2, w - 4, h - 4), scale=w / 600)
        p.end()
        return img

    def mouseMoveEvent(self, e):
        r = QRectF(self.rect())
        x = self.xmin + (e.position().x() - r.left()) / r.width() * (self.xmax - self.xmin)
        y = self.ymin + (r.bottom() - e.position().y()) / r.height() * (self.ymax - self.ymin)
        if self._drag is not None:
            px, py, x0, x1, y0, y1 = self._drag
            dx = (e.position().x() - px) / r.width() * (x1 - x0)
            dy = (e.position().y() - py) / r.height() * (y1 - y0)
            self.xmin, self.xmax, self.ymin, self.ymax = x0 - dx, x1 - dx, y0 + dy, y1 + dy
            self.update()
            self.window().sync_range()
        self.moved.emit(f"x = {show(round(x, 4))}   y = {show(round(y, 4))}")

    def mousePressEvent(self, e):
        self._drag = (e.position().x(), e.position().y(), self.xmin, self.xmax, self.ymin, self.ymax)

    def mouseReleaseEvent(self, e):
        self._drag = None

    def wheelEvent(self, e):
        k = 0.85 if e.angleDelta().y() > 0 else 1 / 0.85
        r = QRectF(self.rect())
        cx = self.xmin + (e.position().x() - r.left()) / r.width() * (self.xmax - self.xmin)
        cy = self.ymin + (r.bottom() - e.position().y()) / r.height() * (self.ymax - self.ymin)
        self.xmin, self.xmax = cx + (self.xmin - cx) * k, cx + (self.xmax - cx) * k
        self.ymin, self.ymax = cy + (self.ymin - cy) * k, cy + (self.ymax - cy) * k
        self.update()
        self.window().sync_range()


class CalculatorDialog(QDialog):
    def __init__(self, mw=None):
        super().__init__(mw)
        self.mw = mw
        self.setWindowTitle(T("Calculatrice scientifique et graphique"))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        self.resize(760, 560)
        self.ans = 0.0
        tabs = QTabWidget(self)
        lay = QVBoxLayout(self)
        lay.addWidget(tabs)
        tabs.addTab(self._calc_tab(), T("Calculatrice"))
        tabs.addTab(self._graph_tab(), T("Graphique"))

    # ------------------------------------------------------------------ calculatrice
    def _calc_tab(self):
        w = QWidget()
        h = QHBoxLayout(w)
        left = QVBoxLayout()
        self.disp = QLineEdit()
        self.disp.setPlaceholderText(T("Saisir un calcul, ex. (2+3)×√(16) puis Entrée"))
        f = self.disp.font()
        f.setPointSize(16)
        self.disp.setFont(f)
        self.disp.returnPressed.connect(self.equals)
        self.res = QLabel("0")
        f2 = QFont(f)
        f2.setPointSize(22)
        f2.setBold(True)
        self.res.setFont(f2)
        self.res.setStyleSheet("font-size:26px; font-weight:bold; padding:4px")
        self.disp.setStyleSheet("font-size:20px; padding:4px")
        self.res.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.res.setTextInteractionFlags(Qt.TextSelectableByMouse)
        left.addWidget(self.disp)
        left.addWidget(self.res)
        mode = QHBoxLayout()
        self.rad = QRadioButton(T("Radians"))
        self.deg = QRadioButton(T("Degrés"), checked=True)
        g = QButtonGroup(w)
        g.addButton(self.rad)
        g.addButton(self.deg)
        mode.addWidget(self.deg)
        mode.addWidget(self.rad)
        mode.addStretch(1)
        left.addLayout(mode)
        grid = QGridLayout()
        keys = [
            [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("π", "π"), ("e", "e"), ("C", None)],
            [("sin⁻¹", "asin("), ("cos⁻¹", "acos("), ("tan⁻¹", "atan("), ("(", "("), (")", ")"), ("⌫", None)],
            [("√", "√("), ("x²", "^2"), ("xʸ", "^"), ("7", "7"), ("8", "8"), ("9", "9")],
            [("ln", "ln("), ("log", "log("), ("eˣ", "exp("), ("4", "4"), ("5", "5"), ("6", "6")],
            [("1/x", "1/("), ("n!", "fact("), ("|x|", "abs("), ("1", "1"), ("2", "2"), ("3", "3")],
            [("÷", "÷"), ("×", "×"), ("−", "-"), ("+", "+"), ("0", "0"), (",", ",")],
            [("%", "%"), ("Ans", "Ans"), ("EXP", "*10^"), ("=", None)],
        ]
        for r, row in enumerate(keys):
            for c, (lab, ins) in enumerate(row):
                b = QPushButton(lab)
                b.setMinimumHeight(38)
                b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                b.setAutoDefault(False)
                if lab == "=":
                    b.setStyleSheet("background:#1565c0;color:white;font-weight:bold")
                    b.clicked.connect(self.equals)
                    grid.addWidget(b, r, c, 1, 3)
                    continue
                if lab == "C":
                    b.clicked.connect(self.clear)
                elif lab == "⌫":
                    b.clicked.connect(self.disp.backspace)
                else:
                    b.clicked.connect(lambda _=False, s=ins: self.put(s))
                if lab.isdigit() or lab == ",":
                    b.setStyleSheet("font-weight:bold")
                grid.addWidget(b, r, c)
        left.addLayout(grid, 1)
        h.addLayout(left, 3)
        right = QVBoxLayout()
        right.addWidget(QLabel(T("Historique (double-clic pour réutiliser)")))
        self.hist = QListWidget()
        self.hist.itemDoubleClicked.connect(lambda it: self.disp.setText(it.data(Qt.UserRole)))
        right.addWidget(self.hist, 1)
        cp = QPushButton(T("Copier le résultat"))
        cp.setAutoDefault(False)
        cp.clicked.connect(lambda: QApplication.clipboard().setText(self.res.text()))
        right.addWidget(cp)
        if self.mw is not None:
            ins = QPushButton(T("Insérer le calcul dans la page"))
            ins.setAutoDefault(False)
            ins.clicked.connect(self.insert_text)
            right.addWidget(ins)
        h.addLayout(right, 2)
        return w

    def put(self, s):
        self.disp.insert(s)
        self.disp.setFocus()

    def clear(self):
        self.disp.clear()
        self.res.setText("0")

    def equals(self):
        txt = self.disp.text().strip()
        if not txt:
            return
        calc.DEG["on"] = self.deg.isChecked()
        try:
            v = calc.evaluate(txt.replace("Ans", f"({self.ans!r})"))
        except calc.CalcError as e:
            self.res.setText(T("Erreur") + " : " + err_text(e))
            return
        finally:
            calc.DEG["on"] = False
        self.ans = v
        out = show(v)
        self.res.setText(out)
        self.hist.insertItem(0, f"{txt} = {out}")
        self.hist.item(0).setData(Qt.UserRole, txt)
        self.last = f"{txt} = {out}"

    def insert_text(self):
        line = getattr(self, "last", None)
        if not line or self.mw is None:
            return
        mw = self.mw
        c = mw.view.mapToScene(mw.view.viewport().rect().center())
        mw.set_tool("select")
        mw.scene.clearSelection()
        mw.add_item({"type": "text", "x": c.x(), "y": c.y(), "text": line, "size": 12}, select=True)
        mw.commit()

    # ------------------------------------------------------------------ graphique
    def _graph_tab(self):
        w = QWidget()
        h = QHBoxLayout(w)
        side = QVBoxLayout()
        form = QFormLayout()
        self.fx = []
        defaults = ("x^2 - 4", "2x + 1", "")
        for i in range(3):
            le = QLineEdit(defaults[i])
            le.setStyleSheet(f"color:{COLORS[i]}; font-weight:bold")
            le.returnPressed.connect(self.replot)
            self.fx.append(le)
            form.addRow(f"y{i + 1} =", le)
        self.rng = {}
        for key, lab, v in (("xmin", "x min", -10), ("xmax", "x max", 10), ("ymin", "y min", -10), ("ymax", "y max", 10)):
            sp = QDoubleSpinBox(decimals=3, minimum=-1e6, maximum=1e6, value=v)
            sp.setKeyboardTracking(False)
            sp.valueChanged.connect(self.range_changed)
            self.rng[key] = sp
            form.addRow(lab, sp)
        side.addLayout(form)
        self.gdeg = QCheckBox(T("Angles en degrés"))
        self.gdeg.toggled.connect(self.replot)
        side.addWidget(self.gdeg)
        for lab, fn in ((T("Tracer"), self.replot), (T("Ajuster l'axe y"), self.auto_y),
                        (T("Repère standard"), self.std_range)):
            b = QPushButton(lab)
            b.setAutoDefault(False)
            b.clicked.connect(fn)
            side.addWidget(b)
        self.gmsg = QLabel()
        self.gmsg.setWordWrap(True)
        side.addWidget(self.gmsg)
        side.addStretch(1)
        side.addWidget(QLabel(T("Molette : zoom · glisser : déplacer")))
        if self.mw is not None:
            b = QPushButton(T("Insérer le graphique dans la page"))
            b.setStyleSheet("font-weight:bold")
            b.setAutoDefault(False)
            b.clicked.connect(self.insert_graph)
            side.addWidget(b)
        cp = QPushButton(T("Copier l'image"))
        cp.setAutoDefault(False)
        cp.clicked.connect(lambda: QApplication.clipboard().setImage(self.plot.image()))
        side.addWidget(cp)
        h.addLayout(side, 1)
        col = QVBoxLayout()
        self.plot = Plot()
        self.coord = QLabel(" ")
        self.plot.moved.connect(self.coord.setText)
        col.addWidget(self.plot, 1)
        col.addWidget(self.coord)
        h.addLayout(col, 3)
        self.replot()
        return w

    def range_changed(self):
        if getattr(self, "_syncing", False):
            return
        v = {k: s.value() for k, s in self.rng.items()}
        if v["xmax"] <= v["xmin"] or v["ymax"] <= v["ymin"]:
            return
        self.plot.xmin, self.plot.xmax, self.plot.ymin, self.plot.ymax = v["xmin"], v["xmax"], v["ymin"], v["ymax"]
        self.plot.update()

    def sync_range(self):
        self._syncing = True
        for k in ("xmin", "xmax", "ymin", "ymax"):
            self.rng[k].setValue(getattr(self.plot, k))
        self._syncing = False

    def _wrap(self, fn):
        deg = self.gdeg.isChecked()

        def g(x):
            calc.DEG["on"] = deg
            try:
                return fn(x)
            finally:
                calc.DEG["on"] = False
        return g

    def replot(self):
        funcs, errs = [], []
        for i, le in enumerate(self.fx):
            txt = le.text().strip()
            if not txt:
                continue
            try:
                funcs.append((txt, self._wrap(calc.compile_fx(txt)), COLORS[i]))
            except calc.CalcError as e:
                errs.append(f"y{i + 1} : {err_text(e)}")
        self.plot.funcs = funcs
        self.gmsg.setText("<span style='color:#d32f2f'>" + "<br>".join(errs) + "</span>" if errs else "")
        self.range_changed()
        self.plot.update()

    def auto_y(self):
        ys = []
        for _, fn, _ in self.plot.funcs:
            for i in range(401):
                x = self.plot.xmin + (self.plot.xmax - self.plot.xmin) * i / 400
                y = fn(x)
                if y is not None and abs(y) < 1e7:
                    ys.append(y)
        if not ys:
            return
        ys.sort()
        lo, hi = ys[int(len(ys) * 0.02)], ys[int(len(ys) * 0.98) - 1 if len(ys) > 50 else -1]
        if hi - lo < 1e-9:
            lo, hi = lo - 1, hi + 1
        m = (hi - lo) * 0.1
        self.plot.ymin, self.plot.ymax = lo - m, hi + m
        self.sync_range()
        self.plot.update()

    def std_range(self):
        self.plot.xmin, self.plot.xmax, self.plot.ymin, self.plot.ymax = -10, 10, -10, 10
        self.sync_range()
        self.plot.update()

    def insert_graph(self):
        mw = self.mw
        img = self.plot.image()
        c = mw.view.mapToScene(mw.view.viewport().rect().center())
        mw.place_image(img, c, width=120 * 72 / 25.4)
        mw.commit()
        mw.statusBar().showMessage(T("Graphique inséré (redimensionnable comme une image)"), 5000)
