"""Fenêtre de signature : dessiner à la souris / au stylet, ou importer une image."""
import os

from PySide6.QtCore import QPointF, QRect, QStandardPaths, Qt
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPen
from .i18n import T
from PySide6.QtWidgets import (QCheckBox, QColorDialog, QDialog, QFileDialog, QHBoxLayout, QLabel,
                               QPushButton, QVBoxLayout, QWidget)


def sig_path():
    d = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "signature.png")


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(640, 240)
        self.paths = []
        self.color = QColor("#0d2a7a")
        self.image = None
        self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, e):
        p = QPainterPath(e.position())
        self.paths.append(p)
        self._last = e.position()
        self.update()

    def mouseMoveEvent(self, e):
        if not self.paths:
            return
        pos = e.position()
        mid = (self._last + pos) / 2
        self.paths[-1].quadTo(self._last, mid)
        self._last = pos
        self.update()

    def clear(self):
        self.paths, self.image = [], None
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.fillRect(self.rect(), Qt.white)
        p.setPen(QPen(QColor("#ccc"), 1, Qt.DashLine))
        y = int(self.height() * 0.75)
        p.drawLine(20, y, self.width() - 20, y)
        self.draw(p)

    def draw(self, p, scale=1.0):
        p.setRenderHint(QPainter.Antialiasing)
        if self.image is not None:
            img = self.image.scaled(self.size() * scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            p.drawImage(0, 0, img)
        pen = QPen(self.color, 3.2 * scale, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        p.setPen(pen)
        p.scale(scale, scale)
        for path in self.paths:
            p.drawPath(path)

    def result(self):
        s = 3
        img = QImage(self.width() * s, self.height() * s, QImage.Format_ARGB32)
        img.fill(Qt.transparent)
        p = QPainter(img)
        self.draw(p, s)
        p.end()
        # rogner aux pixels non transparents
        r = None
        for path in self.paths:
            br = path.boundingRect()
            r = br if r is None else r.united(br)
        if self.image is not None and not self.paths:
            return self.image
        if r is None:
            return None
        rr = QRect(int((r.left() - 6) * s), int((r.top() - 6) * s), int((r.width() + 12) * s), int((r.height() + 12) * s))
        return img.copy(rr.intersected(img.rect()))


class SignatureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(T("Signature"))
        self.canvas = Canvas()
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(T("Signez dans le cadre avec la souris, le pavé tactile ou un stylet :")))
        lay.addWidget(self.canvas)
        row = QHBoxLayout()
        for txt, fn in (("Effacer", self.canvas.clear), ("Couleur…", self.pick_color),
                        ("Importer une image…", self.import_img), ("Signature mémorisée", self.load_saved)):
            b = QPushButton(T(txt))
            b.clicked.connect(fn)
            row.addWidget(b)
        lay.addLayout(row)
        self.remember = QCheckBox(T("Mémoriser cette signature sur cet ordinateur"))
        self.remember.setChecked(True)
        lay.addWidget(self.remember)
        row2 = QHBoxLayout()
        row2.addStretch()
        ok = QPushButton(T("Placer la signature"))
        ok.setDefault(True)
        ok.clicked.connect(self.accept)
        cancel = QPushButton(T("Annuler"))
        cancel.clicked.connect(self.reject)
        row2.addWidget(cancel)
        row2.addWidget(ok)
        lay.addLayout(row2)
        self.img = None
        if os.path.exists(sig_path()):
            self.load_saved()

    def pick_color(self):
        c = QColorDialog.getColor(self.canvas.color, self)
        if c.isValid():
            self.canvas.color = c
            self.canvas.update()

    def import_img(self):
        f, _ = QFileDialog.getOpenFileName(self, T("Image de signature"), "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if f:
            img = QImage(f)
            if img.width() > 900:
                img = img.scaledToWidth(900, Qt.SmoothTransformation)
            img = img.convertToFormat(QImage.Format_ARGB32)
            # fond blanc -> transparent
            for y in range(img.height()):
                for x in range(img.width()):
                    c = img.pixelColor(x, y)
                    if c.red() > 235 and c.green() > 235 and c.blue() > 235:
                        img.setPixelColor(x, y, QColor(0, 0, 0, 0))
            self.canvas.clear()
            self.canvas.image = img
            self.canvas.update()

    def load_saved(self):
        if os.path.exists(sig_path()):
            self.canvas.clear()
            self.canvas.image = QImage(sig_path())
            self.canvas.update()

    def accept(self):
        self.img = self.canvas.result()
        if self.img is None:
            return
        if self.remember.isChecked():
            self.img.save(sig_path())
        super().accept()
