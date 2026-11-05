"""Tableaux : modèle (cellules, fusions, formules) et fenêtre d'édition."""
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import (QAbstractItemView, QCheckBox, QColorDialog, QComboBox, QDialog,
                               QDialogButtonBox, QDoubleSpinBox, QFormLayout, QGridLayout,
                               QHBoxLayout, QLabel, QMessageBox, QPushButton, QSpinBox,
                               QTableWidget, QTableWidgetItem, QToolButton, QVBoxLayout)

from . import calc
from .i18n import T

MM = 72 / 25.4


def new_table(rows=4, cols=3, x=0, y=0, w=None, h=None, header=True):
    w = w or cols * 30 * MM
    h = h or rows * 8 * MM
    cells = {}
    if header:
        for c in range(cols):
            cells[f"0,{c}"] = calc.col_name(c)
    return {"type": "table", "x": x, "y": y, "w": w, "h": h, "rows": rows, "cols": cols,
            "cells": cells, "spans": {}, "colw": [1.0] * cols, "rowh": [1.0] * rows,
            "size": 9, "header": header, "head_fill": "#dce8f5", "align": "center",
            "color": "#000000", "sw": 0.8, "fill": "#ffffff"}


def fix(d):
    """Remet d'aplomb un tableau (listes de largeurs, fusions hors limites)."""
    R, C = max(1, int(d.get("rows", 1))), max(1, int(d.get("cols", 1)))
    d["rows"], d["cols"] = R, C
    cw = list(d.get("colw") or [])
    rh = list(d.get("rowh") or [])
    d["colw"] = (cw + [1.0] * C)[:C]
    d["rowh"] = (rh + [1.0] * R)[:R]
    d["cells"] = {k: v for k, v in (d.get("cells") or {}).items() if _in(k, R, C) and str(v) != ""}
    sp = {}
    for k, (rs, cs) in (d.get("spans") or {}).items():
        if _in(k, R, C):
            r, c = _rc(k)
            rs, cs = max(1, min(rs, R - r)), max(1, min(cs, C - c))
            if rs > 1 or cs > 1:
                sp[k] = [rs, cs]
    d["spans"] = sp
    return d


def _rc(k):
    r, c = k.split(",")
    return int(r), int(c)


def _in(k, R, C):
    try:
        r, c = _rc(k)
    except ValueError:
        return False
    return 0 <= r < R and 0 <= c < C


def covered(d):
    """Cases masquées par une fusion → case d'ancrage."""
    out = {}
    for k, (rs, cs) in (d.get("spans") or {}).items():
        r0, c0 = _rc(k)
        for r in range(r0, r0 + rs):
            for c in range(c0, c0 + cs):
                if (r, c) != (r0, c0):
                    out[(r, c)] = (r0, c0)
    return out


def raw_number(txt):
    s = str(txt).strip().replace(" ", "").replace(" ", "")
    if not s:
        return None
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def show_num(v, dec=None):
    from . import i18n
    s = f"{v:.{int(dec)}f}" if dec not in (None, "", -1) else calc.fmt(v, 8)
    return s if i18n.LANG == "en" else s.replace(".", ",")


def compute(d):
    """Valeurs affichées : {(r, c): texte}. Les formules commencent par « = »."""
    cells = d.get("cells") or {}
    cache, busy = {}, set()

    def value(r, c):
        key = (r, c)
        if key in cache:
            return cache[key]
        txt = str(cells.get(f"{r},{c}", ""))
        if txt.startswith("="):
            if key in busy:
                raise calc.CalcError("référence circulaire")
            busy.add(key)
            try:
                v = calc.evaluate(txt, cell_value=num)
            finally:
                busy.discard(key)
        else:
            v = raw_number(txt)
        cache[key] = v
        return v

    def num(r, c):
        if not (0 <= r < d["rows"] and 0 <= c < d["cols"]):
            return None
        return value(r, c)

    out = {}
    for k, txt in cells.items():
        r, c = _rc(k)
        txt = str(txt)
        if txt.startswith("="):
            try:
                v = value(r, c)
                out[(r, c)] = show_num(v, d.get("dec"))
            except calc.CalcError as e:
                out[(r, c)] = "#" + T("ERREUR") if "circulaire" not in str(e) else "#" + T("CIRCULAIRE")
        else:
            out[(r, c)] = txt
    return out


# ------------------------------------------------------------------------------------ fenêtres
class InsertTableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(T("Insérer un tableau"))
        f = QFormLayout(self)
        self.rows = QSpinBox(minimum=1, maximum=200, value=5)
        self.cols = QSpinBox(minimum=1, maximum=40, value=4)
        self.header = QCheckBox(T("Première ligne = en-tête (gras, colorée)"), checked=True)
        f.addRow(T("Lignes"), self.rows)
        f.addRow(T("Colonnes"), self.cols)
        f.addRow(self.header)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        f.addRow(bb)


class TableDialog(QDialog):
    """Édition complète : cases, formules, lignes et colonnes, fusion."""

    def __init__(self, d, parent=None):
        super().__init__(parent)
        self.setWindowTitle(T("Modifier le tableau"))
        self.resize(900, 560)
        self.d = fix(dict(d))
        lay = QVBoxLayout(self)

        bar = QGridLayout()
        btn = lambda txt, fn, tip=None: self._btn(txt, fn, tip)
        row1 = [(T("+ Ligne au-dessus"), lambda: self.add_row(0)), (T("+ Ligne en dessous"), lambda: self.add_row(1)),
                (T("− Supprimer ligne(s)"), self.del_rows),
                (T("+ Colonne à gauche"), lambda: self.add_col(0)), (T("+ Colonne à droite"), lambda: self.add_col(1)),
                (T("− Supprimer colonne(s)"), self.del_cols)]
        row2 = [(T("Fusionner les cases"), self.merge), (T("Scinder"), self.split),
                ("√( )", lambda: self.insert_txt("√()", -1)), ("=SOMME()", lambda: self.insert_txt("=SOMME()", -1)),
                ("=MOYENNE()", lambda: self.insert_txt("=MOYENNE()", -1)), (T("Effacer"), self.clear_sel)]
        for i, (t, fn) in enumerate(row1):
            bar.addWidget(btn(t, fn), 0, i)
        for i, (t, fn) in enumerate(row2):
            bar.addWidget(btn(t, fn), 1, i)
        lay.addLayout(bar)

        self.tw = QTableWidget(self.d["rows"], self.d["cols"])
        self.tw.setSelectionMode(QAbstractItemView.ContiguousSelection)
        from .spell import SpellDelegate
        self.tw.setItemDelegate(SpellDelegate(self.tw))
        self.tw.setHorizontalHeaderLabels([calc.col_name(c) for c in range(self.d["cols"])])
        for k, v in self.d["cells"].items():
            r, c = _rc(k)
            self.tw.setItem(r, c, QTableWidgetItem(str(v)))
        for k, (rs, cs) in self.d["spans"].items():
            r, c = _rc(k)
            self.tw.setSpan(r, c, rs, cs)
        tot = sum(self.d["colw"]) or 1
        for c, wv in enumerate(self.d["colw"]):
            self.tw.setColumnWidth(c, max(30, int(wv / tot * 120 * self.d["cols"])))
        self.tw.itemChanged.connect(lambda *_: self.show_value())
        self.tw.currentCellChanged.connect(lambda *_: self.show_value())
        lay.addWidget(self.tw, 1)

        self.info = QLabel()
        self.info.setWordWrap(True)
        lay.addWidget(self.info)
        help_ = QLabel(T("Formules : commencer par « = ». Exemples : =A1+B1   =A2*3   =(B2-B3)/2   =√(A1)   =A1^2   "
                         "=SOMME(A1:A5)   =MOYENNE(B2:B6)   =MAX(…)  =MIN(…). Le « x » et « × » multiplient aussi."))
        help_.setWordWrap(True)
        help_.setStyleSheet("color:#607d8b")
        lay.addWidget(help_)

        opts = QHBoxLayout()
        self.size = QDoubleSpinBox(decimals=1, minimum=4, maximum=48, value=float(self.d.get("size", 9)), suffix=" pt")
        self.header = QCheckBox(T("En-tête"), checked=bool(self.d.get("header", True)))
        self.align = QComboBox()
        for a, lab in (("left", "Gauche"), ("center", "Centré"), ("right", "Droite")):
            self.align.addItem(T(lab), a)
        self.align.setCurrentIndex(max(0, self.align.findData(self.d.get("align", "center"))))
        self.head_col = self.d.get("head_fill", "#dce8f5")
        self.hc = QPushButton(T("Couleur en-tête"))
        self.hc.clicked.connect(self.pick_head)
        self._paint_hc()
        opts.addWidget(QLabel(T("Taille du texte")))
        opts.addWidget(self.size)
        self.dec = QComboBox()
        self.dec.addItem(T("Auto"), -1)
        for n in range(5):
            self.dec.addItem(str(n), n)
        self.dec.setCurrentIndex(max(0, self.dec.findData(self.d.get("dec", -1) if self.d.get("dec") is not None else -1)))
        opts.addWidget(QLabel(T("Décimales des résultats")))
        opts.addWidget(self.dec)
        opts.addWidget(QLabel(T("Alignement")))
        opts.addWidget(self.align)
        opts.addWidget(self.header)
        opts.addWidget(self.hc)
        opts.addStretch(1)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        opts.addWidget(bb)
        lay.addLayout(opts)
        self.show_value()

    def _btn(self, txt, fn, tip=None):
        b = QPushButton(txt)
        b.clicked.connect(fn)
        b.setAutoDefault(False)
        if tip:
            b.setToolTip(tip)
        return b

    def _paint_hc(self):
        self.hc.setStyleSheet(f"background:{self.head_col}; color:#000")

    def pick_head(self):
        c = QColorDialog.getColor(QColor(self.head_col), self, T("Couleur en-tête"))
        if c.isValid():
            self.head_col = c.name()
            self._paint_hc()

    # ------------------------------------------------------------ sélection
    def sel_range(self):
        rs = self.tw.selectedRanges()
        if rs:
            r = rs[0]
            return r.topRow(), r.bottomRow(), r.leftColumn(), r.rightColumn()
        r, c = max(0, self.tw.currentRow()), max(0, self.tw.currentColumn())
        return r, r, c, c

    def relabel(self):
        self.tw.setHorizontalHeaderLabels([calc.col_name(c) for c in range(self.tw.columnCount())])

    def add_row(self, below):
        r0, r1, _, _ = self.sel_range()
        self.tw.insertRow(r1 + 1 if below else r0)

    def add_col(self, right):
        _, _, c0, c1 = self.sel_range()
        self.tw.insertColumn(c1 + 1 if right else c0)
        self.relabel()

    def del_rows(self):
        r0, r1, _, _ = self.sel_range()
        if self.tw.rowCount() - (r1 - r0 + 1) < 1:
            return
        for r in range(r1, r0 - 1, -1):
            self.tw.removeRow(r)

    def del_cols(self):
        _, _, c0, c1 = self.sel_range()
        if self.tw.columnCount() - (c1 - c0 + 1) < 1:
            return
        for c in range(c1, c0 - 1, -1):
            self.tw.removeColumn(c)
        self.relabel()

    def merge(self):
        r0, r1, c0, c1 = self.sel_range()
        if r0 == r1 and c0 == c1:
            QMessageBox.information(self, T("Fusionner les cases"), T("Sélectionner d'abord plusieurs cases voisines."))
            return
        texts = []
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                it = self.tw.item(r, c)
                if it and it.text() and (r, c) != (r0, c0):
                    texts.append(it.text())
                    it.setText("")
        if texts:
            first = self.tw.item(r0, c0)
            base = first.text() if first else ""
            self.tw.setItem(r0, c0, QTableWidgetItem(" ".join([base] + texts).strip()))
        self.tw.setSpan(r0, c0, r1 - r0 + 1, c1 - c0 + 1)

    def split(self):
        r, c = max(0, self.tw.currentRow()), max(0, self.tw.currentColumn())
        if self.tw.rowSpan(r, c) > 1 or self.tw.columnSpan(r, c) > 1:
            self.tw.setSpan(r, c, 1, 1)
        r0, r1, c0, c1 = self.sel_range()
        for rr in range(r0, r1 + 1):
            for cc in range(c0, c1 + 1):
                if self.tw.rowSpan(rr, cc) > 1 or self.tw.columnSpan(rr, cc) > 1:
                    self.tw.setSpan(rr, cc, 1, 1)

    def clear_sel(self):
        r0, r1, c0, c1 = self.sel_range()
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                it = self.tw.item(r, c)
                if it:
                    it.setText("")

    def insert_txt(self, txt, back=0):
        r, c = max(0, self.tw.currentRow()), max(0, self.tw.currentColumn())
        it = self.tw.item(r, c)
        cur = it.text() if it else ""
        if txt.startswith("=") and cur.startswith("="):
            txt = txt[1:]
        elif not txt.startswith("=") and not cur.startswith("="):
            txt = "=" + txt
        self.tw.setItem(r, c, QTableWidgetItem(cur + txt))
        self.tw.setCurrentCell(r, c)
        self.tw.editItem(self.tw.item(r, c))

    # ------------------------------------------------------------ résultat
    def result(self):
        R, C = self.tw.rowCount(), self.tw.columnCount()
        d = dict(self.d)
        d["rows"], d["cols"] = R, C
        cells, spans, seen = {}, {}, set()
        for r in range(R):
            for c in range(C):
                it = self.tw.item(r, c)
                if it and it.text().strip():
                    cells[f"{r},{c}"] = it.text().strip()
                if (r, c) in seen:
                    continue
                rs, cs = self.tw.rowSpan(r, c), self.tw.columnSpan(r, c)
                if rs > 1 or cs > 1:
                    spans[f"{r},{c}"] = [rs, cs]
                    for rr in range(r, r + rs):
                        for cc in range(c, c + cs):
                            seen.add((rr, cc))
        d["cells"], d["spans"] = cells, spans
        widths = [max(1, self.tw.columnWidth(c)) for c in range(C)]
        tot = sum(widths)
        d["colw"] = [round(wv / tot * C, 4) for wv in widths]
        old_r = self.d["rows"]
        unit_h = self.d["h"] / max(1, sum(self.d["rowh"]))
        d["rowh"] = [1.0] * R
        d["h"] = unit_h * R if R != old_r else self.d["h"]
        old_c = self.d["cols"]
        if C != old_c:
            d["w"] = self.d["w"] * C / old_c
        d["size"] = self.size.value()
        d["header"] = self.header.isChecked()
        d["align"] = self.align.currentData()
        d["head_fill"] = self.head_col
        d["dec"] = None if self.dec.currentData() == -1 else self.dec.currentData()
        return fix(d)

    def show_value(self):
        r, c = self.tw.currentRow(), self.tw.currentColumn()
        if r < 0 or c < 0:
            self.info.setText("")
            return
        d = self.result()
        it = self.tw.item(r, c)
        txt = it.text() if it else ""
        name = f"{calc.col_name(c)}{r + 1}"
        if txt.startswith("="):
            val = compute(d).get((r, c), "")
            self.info.setText(f"<b>{name}</b>  {txt}  →  <b>{val}</b>")
        else:
            self.info.setText(f"<b>{name}</b>  {txt}")
        # repère visuel des cases à formule (avec le résultat en infobulle)
        vals = compute(d)
        self.tw.blockSignals(True)
        for rr in range(self.tw.rowCount()):
            for cc in range(self.tw.columnCount()):
                i2 = self.tw.item(rr, cc)
                if i2:
                    f = i2.text().startswith("=")
                    i2.setBackground(QBrush(QColor("#e8f5e9")) if f else QBrush())
                    i2.setToolTip(("= " + vals.get((rr, cc), "")) if f else "")
        self.tw.blockSignals(False)
