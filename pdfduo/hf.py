"""En-tête, pied de page et numérotation automatique des pages.

Réglages enregistrés avec le document (« hf ») et dessinés sur chaque page par un élément HFItem :
ils suivent l'ajout, la suppression et le déplacement des pages. L'en-tête et le pied de page peuvent être
découpés en tableau (1 à 4 colonnes, 1 ou 2 lignes) pour obtenir des zones distinctes (établissement, titre du TP,
nom de l'élève, date…). Champs automatiques : {page}, {pages}, {date}, {titre}.
"""
import datetime
import os

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFontMetricsF, QPen
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout,
                               QGraphicsItem, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QSpinBox, QVBoxLayout, QWidget, QApplication)

from .i18n import T
from .items import MM, draw_rich, rich_layout, rich_width, text_font

# modèles de numérotation : (clé, exemple affiché, modèle)
def num_models():
    from . import i18n
    if i18n.LANG == "zh":
        return [("n", "1", "{page}"), ("dash", "– 1 –", "– {page} –"), ("page", "第 1 页", "第 {page} 页"),
                ("n_of", "1 / 5", "{page} / {pages}"), ("page_of", "第 1 页 / 共 5 页", "第 {page} 页 / 共 {pages} 页"),
                ("page_sur", "第 1 页，共 5 页", "第 {page} 页，共 {pages} 页"), ("p", "p. 1", "p. {page}")]
    pg, of = T("Page"), T("sur")
    return [("n", "1", "{page}"), ("dash", "– 1 –", "– {page} –"), ("page", f"{pg} 1", f"{pg} {{page}}"),
            ("n_of", "1 / 5", "{page} / {pages}"), ("page_of", f"{pg} 1 / 5", f"{pg} {{page}} / {{pages}}"),
            ("page_sur", f"{pg} 1 {of} 5", f"{pg} {{page}} {of} {{pages}}"), ("p", "p. 1", "p. {page}")]


POSITIONS = [("bc", "Pied de page – au centre"), ("br", "Pied de page – à droite"), ("bl", "Pied de page – à gauche"),
             ("tr", "En-tête – à droite"), ("tc", "En-tête – au centre"), ("tl", "En-tête – à gauche")]


def default_cfg():
    return {"num": False, "num_model": "page_of", "num_tpl": None, "num_pos": "bc", "num_start": 1,
            "skip_first": False, "size": 9, "margin": 10.0, "color": "#37474f",
            "head": {"on": False, "rows": 1, "cols": 3, "cells": [["", "", ""]], "frame": True, "line": False},
            "foot": {"on": False, "rows": 1, "cols": 3, "cells": [["", "", ""]], "frame": False, "line": True}}


def active(cfg):
    return bool(cfg) and (cfg.get("num") or cfg.get("head", {}).get("on") or cfg.get("foot", {}).get("on"))


def fill(text, page, pages, title):
    return (text.replace("{page}", str(page)).replace("{pages}", str(pages))
            .replace("{date}", datetime.date.today().strftime("%d/%m/%Y")).replace("{titre}", title)
            .replace("{title}", title))


class HFItem(QGraphicsItem):
    """En-tête, pied de page et numéro d'une page (au-dessus de la page, sous les dessins)."""

    def __init__(self, mw, pg):
        super().__init__()
        self.mw, self.pg = mw, pg
        self.setZValue(-900)
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setPos(pg.pos())

    def boundingRect(self):
        return QRectF(0, 0, self.pg.w, self.pg.h)

    def band(self, part, cfg, top):
        r = cfg[part]
        size, m = cfg.get("size", 9), cfg.get("margin", 10) * MM
        rh = size * 1.9
        h = rh * max(1, r.get("rows", 1))
        y = m if top else self.pg.h - m - h
        return QRectF(m, y, self.pg.w - 2 * m, h), rh

    def paint(self, p, opt, w=None):
        cfg = self.mw.hf
        if not active(cfg):
            return
        idx = self.pg.idx
        if cfg.get("skip_first") and idx == 0:
            return
        pages = len(self.mw.page_items)
        start = int(cfg.get("num_start", 1))
        num = idx + start - (1 if cfg.get("skip_first") else 0)
        tot = pages - 1 + start - (1 if cfg.get("skip_first") else 0)
        title = (self.mw.doc.metadata or {}).get("title") or (os.path.splitext(os.path.basename(self.mw.path))[0]
                                                               if self.mw.path else "")
        f = text_font(cfg.get("size", 9))
        fm = QFontMetricsF(f)
        k = cfg.get("size", 9) / 100
        col = QColor(cfg.get("color", "#37474f"))
        p.setRenderHint(p.RenderHint.Antialiasing)

        def text(box, s, align):
            s = fill(s, num, tot, title)
            if not s:
                return
            lines = s.split("\n")
            bases, th = rich_layout(fm, lines)
            p.save()
            p.setFont(f)
            p.setPen(col)
            y0 = box.top() + (box.height() - th * k) / 2
            for line, base in zip(lines, bases):
                lw = rich_width(fm, line) * k
                pad = 1.5 * MM
                x = box.left() + pad if align == "l" else box.right() - pad - lw if align == "r" \
                    else box.left() + (box.width() - lw) / 2
                p.save()
                p.translate(x, y0)
                p.scale(k, k)
                draw_rich(p, fm, 0, base, line)
                p.restore()
            p.restore()

        pen = QPen(col, 0.6)
        for part, top in (("head", True), ("foot", False)):
            r = cfg.get(part) or {}
            if not r.get("on"):
                continue
            box, rh = self.band(part, cfg, top)
            rows, cols = max(1, r.get("rows", 1)), max(1, r.get("cols", 1))
            ws = r.get("widths") or []
            if len(ws) != cols or sum(ws) <= 0:
                ws = [1] * cols
            xs = [box.left()]
            for v in ws:
                xs.append(xs[-1] + v / sum(ws) * box.width())
            aligns = {1: "c", 2: "lr", 3: "lcr", 4: "lccr"}[cols]
            cells = r.get("cells") or []
            for ri in range(rows):
                for ci in range(cols):
                    cell = QRectF(xs[ci], box.top() + ri * rh, xs[ci + 1] - xs[ci], rh)
                    s = cells[ri][ci] if ri < len(cells) and ci < len(cells[ri]) else ""
                    text(cell, s, aligns[ci] if cols > 1 else "c")
            p.save()
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            if r.get("frame"):
                p.drawRect(box)
                for x in xs[1:-1]:
                    p.drawLine(QPointF(x, box.top()), QPointF(x, box.bottom()))
                for ri in range(1, rows):
                    y = box.top() + ri * rh
                    p.drawLine(QPointF(box.left(), y), QPointF(box.right(), y))
            elif r.get("line"):
                y = box.bottom() + 1.5 * MM if top else box.top() - 1.5 * MM
                p.drawLine(QPointF(box.left(), y), QPointF(box.right(), y))
            p.restore()
        if cfg.get("num"):
            pos = cfg.get("num_pos", "bc")
            tpl = cfg.get("num_tpl") or dict((a, c) for a, _, c in num_models()).get(cfg.get("num_model"), "{page}")
            part, top = ("head", True) if pos[0] == "t" else ("foot", False)
            box, rh = self.band(part, cfg, top)
            r = cfg.get(part) or {}
            if r.get("on"):
                # case du tableau du même côté (gauche / centre / droite) : si elle est vide, le numéro s'y écrit,
                # sinon il se place juste au-dessus du pied de page (ou sous l'en-tête), sans toucher le trait
                cols = max(1, r.get("cols", 1))
                side = {"l": 0, "c": cols // 2, "r": cols - 1}[pos[1]]
                row = 0 if top else max(1, r.get("rows", 1)) - 1
                cells = r.get("cells") or []
                used = row < len(cells) and side < len(cells[row]) and cells[row][side].strip()
                if not used and (cols % 2 == 1 or pos[1] != "c"):
                    box = QRectF(box.left(), box.top() + row * rh, box.width(), rh)
                else:
                    gap = 2.5 * MM
                    box = QRectF(box.left(), box.bottom() + gap, box.width(), rh) if top else \
                        QRectF(box.left(), box.top() - rh - gap, box.width(), rh)
            else:
                box = QRectF(box.left(), box.top(), box.width(), rh)
            text(box, tpl, pos[1])


class HFDialog(QDialog):
    """Pages › En-tête, pied de page et numérotation… — chaque changement se voit tout de suite sur les pages."""

    TOKENS = [("{page}", "N° de page"), ("{pages}", "Nombre de pages"), ("{date}", "Date"), ("{titre}", "Titre")]

    def __init__(self, mw):
        super().__init__(mw)
        self.mw = mw
        self.old = mw.hf
        import copy
        self.cfg = copy.deepcopy(mw.hf) if mw.hf else default_cfg()
        self.setWindowTitle(T("En-tête, pied de page et numérotation"))
        self.last_edit = None
        lay = QVBoxLayout(self)

        # --- numérotation
        g = QGroupBox(T("Numérotation automatique des pages"))
        g.setCheckable(True)
        g.setChecked(bool(self.cfg.get("num")))
        g.toggled.connect(lambda v: self.set("num", v))
        f = QFormLayout(g)
        self.model = QComboBox()
        for key, ex, tpl in num_models():
            self.model.addItem(ex, key)
        self.model.setCurrentIndex(max(0, self.model.findData(self.cfg.get("num_model", "page_of"))))
        self.model.currentIndexChanged.connect(self.model_changed)
        f.addRow(T("Modèle"), self.model)
        pos = QComboBox()
        for key, lab in POSITIONS:
            pos.addItem(T(lab), key)
        pos.setCurrentIndex(max(0, pos.findData(self.cfg.get("num_pos", "bc"))))
        pos.currentIndexChanged.connect(lambda i: self.set("num_pos", pos.itemData(i)))
        f.addRow(T("Position"), pos)
        st = QSpinBox(minimum=0, maximum=9999, value=int(self.cfg.get("num_start", 1)))
        st.valueChanged.connect(lambda v: self.set("num_start", v))
        f.addRow(T("Premier numéro"), st)
        lay.addWidget(g)

        # --- en-tête et pied de page
        self.grids = {}
        for part, title in (("head", "En-tête"), ("foot", "Pied de page")):
            lay.addWidget(self.part_box(part, T(title)))

        # --- champs automatiques
        tk = QHBoxLayout()
        tk.addWidget(QLabel(T("Insérer dans la case choisie :")))
        for tok, lab in self.TOKENS:
            b = QPushButton(T(lab))
            b.setToolTip(tok)
            b.setFocusPolicy(Qt.NoFocus)
            b.clicked.connect(lambda _=False, t=tok: self.insert_token(t))
            tk.addWidget(b)
        tk.addStretch(1)
        lay.addLayout(tk)

        # --- présentation
        g2 = QGroupBox(T("Présentation"))
        f2 = QFormLayout(g2)
        sz = QDoubleSpinBox(decimals=1, minimum=5, maximum=24, value=float(self.cfg.get("size", 9)), suffix=" pt")
        sz.valueChanged.connect(lambda v: self.set("size", v))
        f2.addRow(T("Taille du texte"), sz)
        mg = QDoubleSpinBox(decimals=1, minimum=3, maximum=40, value=float(self.cfg.get("margin", 10)), suffix=" mm")
        mg.valueChanged.connect(lambda v: self.set("margin", v))
        f2.addRow(T("Distance au bord de la page"), mg)
        sk = QCheckBox(T("Rien sur la première page (page de garde)"))
        sk.setChecked(bool(self.cfg.get("skip_first")))
        sk.toggled.connect(lambda v: self.set("skip_first", v))
        f2.addRow("", sk)
        lay.addWidget(g2)

        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        rm = bb.addButton(T("Tout retirer"), QDialogButtonBox.ResetRole)
        rm.clicked.connect(self.remove_all)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        lay.addWidget(bb)
        self.model_changed(self.model.currentIndex(), apply=False)
        self.apply()

    def part_box(self, part, title):
        r = self.cfg[part]
        g = QGroupBox(title)
        g.setCheckable(True)
        g.setChecked(bool(r.get("on")))
        g.toggled.connect(lambda v: self.set_part(part, "on", v))
        v = QVBoxLayout(g)
        row = QHBoxLayout()
        row.addWidget(QLabel(T("Zones (tableau) :")))
        cols = QSpinBox(minimum=1, maximum=4, value=int(r.get("cols", 3)), suffix=" " + T("colonne(s)"))
        rows = QSpinBox(minimum=1, maximum=2, value=int(r.get("rows", 1)), suffix=" " + T("ligne(s)"))
        row.addWidget(cols)
        row.addWidget(rows)
        fr = QCheckBox(T("Encadrer (tableau)"))
        fr.setChecked(bool(r.get("frame")))
        fr.toggled.connect(lambda val: self.set_part(part, "frame", val))
        row.addWidget(fr)
        ln = QCheckBox(T("Trait de séparation"))
        ln.setChecked(bool(r.get("line")))
        ln.toggled.connect(lambda val: self.set_part(part, "line", val))
        row.addWidget(ln)
        row.addStretch(1)
        v.addLayout(row)
        holder = QWidget()
        grid = QGridLayout(holder)
        grid.setContentsMargins(0, 0, 0, 0)
        v.addWidget(holder)
        wrow = QHBoxLayout()
        wrow.addWidget(QLabel(T("Largeurs des colonnes (%) :")))
        we = QLineEdit(", ".join(str(int(x)) for x in (r.get("widths") or [])))
        we.setPlaceholderText(T("égales (ex. 30, 40, 30)"))
        we.textChanged.connect(lambda t: self.set_widths(part, t))
        wrow.addWidget(we, 1)
        v.addLayout(wrow)
        self.grids[part] = (grid, holder)
        cols.valueChanged.connect(lambda n: self.resize_cells(part, rows.value(), n))
        rows.valueChanged.connect(lambda n: self.resize_cells(part, n, cols.value()))
        self.build_cells(part)
        return g

    def build_cells(self, part):
        grid, holder = self.grids[part]
        while grid.count():
            w = grid.takeAt(0).widget()
            if w:
                w.deleteLater()
        r = self.cfg[part]
        hints = {1: ["{titre}"], 2: [T("Établissement"), T("Date : {date}")],
                 3: [T("Établissement"), T("Titre du TP"), T("Nom :")], 4: [T("Établissement"), T("Classe"), T("Titre"), T("Nom :")]}
        for ri in range(r["rows"]):
            for ci in range(r["cols"]):
                e = QLineEdit(r["cells"][ri][ci])
                e.setPlaceholderText(hints[r["cols"]][ci] if ri == 0 else "")
                e.textChanged.connect(lambda t, ri=ri, ci=ci: self.set_cell(part, ri, ci, t))
                e.installEventFilter(self)
                grid.addWidget(e, ri, ci)

    def eventFilter(self, obj, ev):
        from PySide6.QtCore import QEvent
        if ev.type() == QEvent.FocusIn and isinstance(obj, QLineEdit):
            self.last_edit = obj
        return False

    def insert_token(self, tok):
        e = self.last_edit
        if e is None:
            return
        e.insert(tok)
        e.setFocus()

    def resize_cells(self, part, rows, cols):
        r = self.cfg[part]
        old = r.get("cells") or []
        r["cells"] = [[(old[i][j] if i < len(old) and j < len(old[i]) else "") for j in range(cols)] for i in range(rows)]
        r["rows"], r["cols"] = rows, cols
        if len(r.get("widths") or []) != cols:
            r["widths"] = []
        self.build_cells(part)
        self.apply()

    def set_widths(self, part, t):
        try:
            ws = [float(x) for x in t.replace(";", ",").split(",") if x.strip()]
        except ValueError:
            return
        self.cfg[part]["widths"] = ws
        self.apply()

    def set_cell(self, part, ri, ci, t):
        self.cfg[part]["cells"][ri][ci] = t
        self.apply()

    def set_part(self, part, key, v):
        self.cfg[part][key] = v
        self.apply()

    def set(self, key, v):
        self.cfg[key] = v
        self.apply()

    def model_changed(self, i, apply=True):
        key = self.model.itemData(i)
        self.cfg["num_model"] = key
        self.cfg["num_tpl"] = dict((a, c) for a, _, c in num_models()).get(key, "{page}")
        if apply:
            self.apply()

    def apply(self):
        self.mw.hf = self.cfg
        self.mw.refresh_hf()

    def remove_all(self):
        self.cfg = default_cfg()
        self.mw.hf = None
        self.mw.refresh_hf()
        self.done(2)

    def reject(self):
        self.mw.hf = self.old
        self.mw.refresh_hf()
        super().reject()
