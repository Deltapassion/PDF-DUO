"""Assembler plusieurs PDF en un seul document (ex. dossier technique de TP à partir de documentations
de fabricants différents) : choix des pages de chaque fichier, ordre, signets et page de sommaire."""
import os

import pymupdf
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
                               QFileDialog, QCheckBox, QLineEdit, QLabel, QMessageBox, QHeaderView, QAbstractItemView)

from .i18n import T

IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")


def parse_pages(txt, n):
    """« toutes » / vide → toutes les pages ; sinon « 1-3,5,8- » (numérotation à partir de 1)."""
    txt = (txt or "").strip().lower()
    if not txt or txt in (T("toutes").lower(), "all", "*"):
        return list(range(n))
    pages = []
    for part in txt.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a = int(a) if a else 1
            b = int(b) if b else n
            pages += [p for p in range(a - 1, min(b, n)) if p >= 0]
        else:
            p = int(part) - 1
            if 0 <= p < n:
                pages.append(p)
    return pages


def open_any(path):
    d = pymupdf.open(path)
    if not d.is_pdf:
        d = pymupdf.open("pdf", d.convert_to_pdf())
    return d


def build(entries, bookmarks=True, summary_title=""):
    """entries : [(chemin, texte des pages, titre du signet)] → document PyMuPDF assemblé."""
    out = pymupdf.open()
    marks = []
    for path, ptxt, title in entries:
        src = open_any(path)
        pages = parse_pages(ptxt, len(src))
        if not pages:
            continue
        marks.append((title, len(out)))
        for p in pages:
            out.insert_pdf(src, from_page=p, to_page=p)
    if summary_title and marks:
        r = pymupdf.paper_rect("a4")
        pg = out.new_page(0, width=r.width, height=r.height)
        marks = [(t, p + 1) for t, p in marks]
        y = 90
        pg.insert_text((60, y), summary_title, fontsize=22, fontname="hebo")
        y += 40
        for t, p in marks:
            if y > r.height - 60:
                break
            label = t if len(t) < 70 else t[:67] + "…"
            pg.insert_text((70, y), label, fontsize=12, fontname="helv")
            pg.insert_text((r.width - 110, y), f"p. {p + 1}", fontsize=12, fontname="helv")
            pg.draw_line((70, y + 4), (r.width - 70, y + 4), color=(0.8, 0.8, 0.8), width=0.4)
            pg.insert_link({"kind": pymupdf.LINK_GOTO, "page": p, "from": pymupdf.Rect(65, y - 13, r.width - 65, y + 5),
                            "to": pymupdf.Point(0, 0)})
            y += 24
    if bookmarks and marks:
        out.set_toc([[1, t, p + 1] for t, p in marks])
    return out


class AssembleDialog(QDialog):
    def __init__(self, mw):
        super().__init__(mw)
        self.mw = mw
        self.setWindowTitle(T("Assembler des PDF (dossier technique)"))
        self.resize(760, 460)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(T("Ajoutez les fichiers dans l'ordre voulu. Colonne « Pages » : « toutes » ou par exemple 1-3,7,12-.")))
        self.tab = QTableWidget(0, 4)
        self.tab.setHorizontalHeaderLabels([T("Fichier"), T("Pages"), T("Nombre de pages"), T("Titre du signet")])
        h = self.tab.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Stretch); h.setSectionResizeMode(3, QHeaderView.Stretch)
        self.tab.setSelectionBehavior(QAbstractItemView.SelectRows)
        lay.addWidget(self.tab, 1)
        row = QHBoxLayout()
        for txt, fn in (("➕ " + T("Ajouter des fichiers…"), self.add_files), ("⬆", lambda: self.move(-1)),
                        ("⬇", lambda: self.move(1)), ("✖ " + T("Retirer"), self.remove)):
            b = QPushButton(txt); b.clicked.connect(fn); row.addWidget(b)
        row.addStretch(1)
        lay.addLayout(row)
        self.cb_marks = QCheckBox(T("Un signet par fichier (sommaire cliquable dans les lecteurs PDF)")); self.cb_marks.setChecked(True)
        lay.addWidget(self.cb_marks)
        r2 = QHBoxLayout()
        self.cb_sum = QCheckBox(T("Page de sommaire au début :")); self.cb_sum.setChecked(True)
        self.title = QLineEdit(T("Dossier technique"))
        r2.addWidget(self.cb_sum); r2.addWidget(self.title, 1)
        lay.addLayout(r2)
        r3 = QHBoxLayout(); r3.addStretch(1)
        go = QPushButton("📄 " + T("Créer le PDF…")); go.setDefault(True); go.clicked.connect(self.create)
        cl = QPushButton(T("Fermer")); cl.clicked.connect(self.reject)
        r3.addWidget(go); r3.addWidget(cl)
        lay.addLayout(r3)

    def add_files(self):
        fs, _ = QFileDialog.getOpenFileNames(self, T("Ajouter des fichiers…"), self.mw.settings.value("lastdir", ""),
                                             "PDF / images (*.pdf *.png *.jpg *.jpeg *.bmp *.tif *.tiff)")
        for f in fs:
            try:
                n = len(open_any(f))
            except Exception as e:
                QMessageBox.warning(self, "PDF DUO", T("Impossible d'ouvrir ce fichier :") + f"\n{f}\n{e}")
                continue
            r = self.tab.rowCount(); self.tab.insertRow(r)
            it = QTableWidgetItem(os.path.basename(f)); it.setData(Qt.UserRole, f); it.setToolTip(f)
            it.setFlags(it.flags() & ~Qt.ItemIsEditable)
            self.tab.setItem(r, 0, it)
            self.tab.setItem(r, 1, QTableWidgetItem(T("toutes")))
            nn = QTableWidgetItem(str(n)); nn.setFlags(nn.flags() & ~Qt.ItemIsEditable)
            self.tab.setItem(r, 2, nn)
            self.tab.setItem(r, 3, QTableWidgetItem(os.path.splitext(os.path.basename(f))[0]))

    def move(self, d):
        r = self.tab.currentRow()
        j = r + d
        if r < 0 or not (0 <= j < self.tab.rowCount()):
            return
        for c in range(4):
            a, b = self.tab.takeItem(r, c), self.tab.takeItem(j, c)
            self.tab.setItem(r, c, b); self.tab.setItem(j, c, a)
        self.tab.setCurrentCell(j, 0)

    def remove(self):
        r = self.tab.currentRow()
        if r >= 0:
            self.tab.removeRow(r)

    def entries(self):
        return [(self.tab.item(r, 0).data(Qt.UserRole), self.tab.item(r, 1).text(), self.tab.item(r, 3).text())
                for r in range(self.tab.rowCount())]

    def create(self):
        ents = self.entries()
        if not ents:
            return
        try:
            doc = build(ents, self.cb_marks.isChecked(), self.title.text().strip() if self.cb_sum.isChecked() else "")
        except ValueError:
            QMessageBox.warning(self, "PDF DUO", T("Plage de pages incorrecte."))
            return
        except Exception as e:
            QMessageBox.warning(self, "PDF DUO", str(e))
            return
        if not len(doc):
            return
        f, _ = QFileDialog.getSaveFileName(self, T("Créer le PDF…"), T("dossier-technique.pdf"), "PDF (*.pdf)")
        if not f:
            return
        f = f if f.lower().endswith(".pdf") else f + ".pdf"
        doc.save(f, garbage=3, deflate=True)
        if QMessageBox.question(self, "PDF DUO", T("PDF créé ({n} pages). L'ouvrir dans PDF DUO ?").format(n=len(doc))) == QMessageBox.Yes:
            self.accept()
            self.mw.open_file(f)
