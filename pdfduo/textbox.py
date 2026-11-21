"""Zone de texte écrite directement sur la page (sans fenêtre de saisie).

On dessine la zone à la souris ; un éditeur se place exactement à cet endroit, à la taille du texte affiché,
et une palette de caractères spéciaux s'ouvre juste en dessous : fond clair légèrement translucide (on devine
la page sans que la palette devienne illisible) ; le caractère survolé est surligné en jaune et montré en grand
avant d'être inséré.
"""
from PySide6.QtCore import QEvent, QObject, QPointF, QRect, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QTextOption
from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QToolButton, QVBoxLayout)

from .i18n import T
from .items import item_font

PALETTE_CSS = """
QFrame#tbPalette { background: rgba(252, 252, 250, 238); border: 1px solid #90a4ae; border-radius: 8px; }
QFrame#tbPalette QLabel { color: #37474f; background: transparent; }
QFrame#tbPalette QLabel#tbPreview { background: #fff59d; color: #000; border: 2px solid #212121; border-radius: 6px;
                                    font-size: 30px; font-weight: bold; }
QFrame#tbPalette QToolButton { background: rgba(255, 255, 255, 230); color: #263238; border: 1px solid #cfd8dc;
                               border-radius: 4px; font-size: 16px; min-width: 26px; min-height: 26px; padding: 0; }
QFrame#tbPalette QToolButton:hover { background: #ffd600; color: #000; border: 2px solid #000; font-weight: bold; }
QFrame#tbPalette QToolButton:pressed { background: #ff8f00; color: #000; }
QFrame#tbPalette QPushButton { background: #e3f2fd; color: #0d47a1; border: 1px solid #90caf9; border-radius: 4px;
                               padding: 3px 8px; }
QFrame#tbPalette QPushButton:hover { background: #ffd600; color: #000; border: 2px solid #000; }
"""


class CharPalette(QFrame):
    """Palette de caractères spéciaux posée sous la zone de texte en cours d'écriture."""

    COLS = 12

    def __init__(self, parent, chars, insert, finish):
        super().__init__(parent)
        self.setObjectName("tbPalette")
        self.setStyleSheet(PALETTE_CSS)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFocusPolicy(Qt.NoFocus)
        self.insert = insert
        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 6, 8, 6)
        lay.setSpacing(8)
        left = QVBoxLayout()
        self.preview = QLabel("Ω")
        self.preview.setObjectName("tbPreview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setFixedSize(54, 54)
        self.preview.setToolTip(T("Caractère qui sera inséré"))
        left.addWidget(self.preview, 0, Qt.AlignHCenter)
        lay.addLayout(left)
        right = QVBoxLayout()
        right.setSpacing(4)
        grid = QGridLayout()
        grid.setSpacing(3)
        grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        for i, ch in enumerate(chars):
            b = QToolButton(text=ch)
            b.setFocusPolicy(Qt.NoFocus)
            b.setAutoRaise(False)
            b.setFixedSize(32, 30)
            b.clicked.connect(lambda _=False, c=ch: self.pick(c))
            b.installEventFilter(self)
            grid.addWidget(b, i // self.COLS, i % self.COLS)
        right.addLayout(grid)
        self.info = QLabel(T("Survolez un caractère : il est surligné et montré en grand ; un clic l'insère."))
        self.info.setWordWrap(True)
        right.addWidget(self.info)
        row = left
        sq = QPushButton("√ " + T("Racine"))
        sq.setFocusPolicy(Qt.NoFocus)
        sq.setToolTip(T("Ouvre une petite fenêtre : écrivez ce qui va sous la racine. Un clic sur une racine : pour la modifier."))
        sq.clicked.connect(lambda: self.insert("√{}"))
        row.addWidget(sq)
        fr = QPushButton("a⁄b " + T("Fraction"))
        fr.setFocusPolicy(Qt.NoFocus)
        fr.setToolTip(T("Ouvre une petite fenêtre : on écrit le haut, puis le bas ; le trait s'allonge tout seul. "
                        "Un clic sur une fraction : pour la modifier."))
        fr.clicked.connect(lambda: self.insert("FRACTION"))
        row.addWidget(fr)
        ok = QPushButton("✓ " + T("Terminer"))
        ok.setFocusPolicy(Qt.NoFocus)
        ok.setToolTip(T("Termine la zone de texte (aussi : Échap, Ctrl+Entrée ou un clic ailleurs sur la page)"))
        ok.clicked.connect(finish)
        row.addWidget(ok)
        self.formula = QLabel()
        self.formula.setObjectName("tbFormula")
        self.formula.setStyleSheet("QLabel#tbFormula { background: #ffffff; border: 1px solid #b0bec5; border-radius: 4px; }")
        self.formula.setToolTip(T("Aperçu de la formule de la ligne en cours"))
        self.formula.hide()
        right.addWidget(self.formula)
        lay.addLayout(right)
        self.adjustSize()

    def show_formula(self, line, color):
        """Aperçu de la ligne en cours quand elle contient une fraction ou une racine."""
        from PySide6.QtGui import QFontMetricsF, QImage, QPainter, QPixmap
        from .items import rich_layout, rich_width, draw_rich, text_font
        if not line or not ("√{" in line or ("{" in line and "|" in line)):
            if self.formula.isVisible():
                self.formula.hide()
                self.adjustSize()
            return
        f = text_font(10)
        fm = QFontMetricsF(f)
        k = 0.24                                    # police de 100 px affichée à 24 px
        bases, th = rich_layout(fm, [line])
        w = int(rich_width(fm, line) * k) + 16
        h = int(th * k) + 12
        img = QImage(max(w, 40), max(h, 30), QImage.Format_ARGB32)
        img.fill(QColor("#ffffff"))
        p = QPainter(img)
        p.setRenderHint(QPainter.Antialiasing)
        p.translate(8, 6)
        p.scale(k, k)
        p.setFont(f)
        p.setPen(QColor(color))
        draw_rich(p, fm, 0, bases[0], line)
        p.end()
        pm = QPixmap.fromImage(img)
        if pm.width() > 430:
            pm = pm.scaledToWidth(430, Qt.SmoothTransformation)
        self.formula.setPixmap(pm)
        if not self.formula.isVisible():
            self.formula.show()
        self.adjustSize()

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.Enter and isinstance(obj, QToolButton):
            self.preview.setText(obj.text())
        return False

    def pick(self, ch):
        self.preview.setText(ch)
        self.insert(ch)


class InlineEditor(QObject):
    """Édition d'une zone de texte (PItem « textbox ») directement sur la page."""

    def __init__(self, view, item, chars, is_new=False):
        super().__init__(view)
        self.view, self.item, self.is_new = view, item, is_new
        self.mw = view.mw
        vp = view.viewport()
        self.edit = MathTextEdit(vp)
        self.edit.on_formula_click = self.formula_clicked
        self.edit.setFrameShape(QFrame.NoFrame)
        self.edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)
        self.edit.textChanged.connect(self.place)
        self.palette_chars = chars
        self.palette = CharPalette(vp, chars, self.insert, self.finish)
        item.setVisible(False)
        self.place()
        self.edit.set_code(item.d.get("text", ""))
        self.place()
        self.edit.show()
        self.palette.show()
        self.edit.setFocus()
        c = self.edit.textCursor()
        c.movePosition(c.MoveOperation.End)
        self.edit.setTextCursor(c)
        for sb in (view.horizontalScrollBar(), view.verticalScrollBar()):
            sb.valueChanged.connect(self.place)
        self.done = False

    # ------------------------------------------------------------------ placement
    def place(self, *_):
        if getattr(self, "done", False):
            return
        v, it = self.view, self.item
        z = v.zoom()
        d = it.d
        f = QFont(item_font(d))
        px = max(4, round(d.get("size", 10) * z))
        f.setPixelSize(px)
        col = QColor(d.get("color", "#000000"))
        # la feuille de style de l'application impose sa police : on la redonne ici, à la taille affichée sur la page
        css = ("QTextEdit { background: rgba(255, 253, 231, 235); color: %s; border: 1px dashed #1e88e5; "
               "padding: 0px; font-family: '%s'; font-size: %dpx; font-weight: %s; font-style: %s; }"
               % (col.name(), f.family(), px, "bold" if d.get("bold") else "normal",
                  "italic" if d.get("italic") else "normal"))
        if self.edit.styleSheet() != css:
            self.edit.setFont(f)
            self.edit.setStyleSheet(css)
        self.edit.restyle(px, col.name(), bool(d.get("bold")), bool(d.get("italic")), f.family())
        pad = it.TB_PAD * z
        tl = v.mapFromScene(it.scenePos())
        w = max(30, round(d.get("w", 150) * z))
        # marge du document : les fractions et les racines dépassent un peu au-dessus de la ligne ; la zone
        # d'écriture est décalée d'autant pour que le texte reste exactement à sa place sur la page
        m = int(px * 0.35)
        if self.edit.document().documentMargin() != m:
            self.edit.document().setDocumentMargin(m)
        self.edit.document().setTextWidth(max(10, w - 2 * int(pad) - 4 + 2 * m))
        doc_h = self.edit.document().size().height()
        h = max(round(d.get("h", 20) * z) + 2 * m,
                int(max(doc_h, self.edit.fontMetrics().lineSpacing() + 2 * m) + 2 * pad + 6))
        self.edit.setViewportMargins(int(pad), int(pad), int(pad), int(pad))
        self.edit.setGeometry(QRect(tl.x() - m, tl.y() - m, w + 2 * m, h))
        self.edit.verticalScrollBar().setValue(0)
        vp = v.viewport().rect()
        pw, ph = self.palette.sizeHint().width(), self.palette.sizeHint().height()
        px = min(max(4, tl.x()), max(4, vp.width() - pw - 4))
        py = tl.y() - m + h + 6
        if py + ph > vp.height() - 4:                   # pas de place dessous : au-dessus de la zone
            py = max(4, tl.y() - m - ph - 6)
        self.palette.setGeometry(px, py, pw, ph)

    def preview(self):
        if not getattr(self, "done", False):
            self.palette.show_formula(self.edit.textCursor().block().text(), self.item.d.get("color", "#000000"))
            self.place()

    # ------------------------------------------------------------------ saisie
    def insert(self, txt, back=0):
        if txt in ("FRACTION", "√{}"):                  # petite fenêtre, puis formule affichée telle quelle
            sel = self.edit.textCursor().selectedText()
            code = RootDialog.ask_root(self.view, self.palette_chars, sel) if txt == "√{}" else \
                ask_formula(self.view, self.palette_chars, None, sel)
            if code:
                self.edit.insert_formula(code)
            self.edit.setFocus()
            return
        c = self.edit.textCursor()
        c.insertText(txt)
        self.edit.setTextCursor(c)
        self.edit.setFocus()

    def formula_clicked(self, pos, code):
        """Un clic sur une fraction ou une racine : sa fenêtre s'ouvre, déjà remplie."""
        new = ask_formula(self.view, self.palette_chars, code)
        c = QTextCursor(self.edit.document())
        c.setPosition(pos)
        if new:
            c.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            c.removeSelectedText()
            self.edit.insert_formula(new, c)
            c.movePosition(QTextCursor.NoMove)
        self.edit.setTextCursor(c)
        self.edit.setFocus()

    def eventFilter(self, obj, ev):
        if obj is self.edit and ev.type() == QEvent.KeyPress:
            if ev.key() == Qt.Key_Escape or (ev.key() in (Qt.Key_Return, Qt.Key_Enter)
                                             and ev.modifiers() & Qt.ControlModifier):
                QTimer.singleShot(0, self.finish)
                return True
        if obj is self.edit and ev.type() == QEvent.FocusOut:
            QTimer.singleShot(120, self._maybe_finish)
        return False

    def _maybe_finish(self):
        if self.done:
            return
        from PySide6.QtWidgets import QApplication
        fw = QApplication.focusWidget()
        if fw is self.edit or (fw is not None and self.palette.isAncestorOf(fw)):
            return
        if QApplication.activePopupWidget() is not None or QApplication.activeModalWidget() is not None:
            return                                       # menu du clic droit (correcteur) : on reste en édition
        self.finish()

    def finish(self):
        if self.done:
            return
        self.done = True
        v, it = self.view, self.item
        for sb in (v.horizontalScrollBar(), v.verticalScrollBar()):
            try:
                sb.valueChanged.disconnect(self.place)
            except Exception:
                pass
        txt = self.edit.code().rstrip()
        self.edit.hide()
        self.palette.hide()
        self.edit.deleteLater()
        self.palette.deleteLater()
        if getattr(v, "inline", None) is self:
            v.inline = None
        if not txt.strip():
            if it.scene() is not None:
                it.scene().removeItem(it)
            if not self.is_new:
                self.mw.commit()
        else:
            it.d["text"] = txt
            it.setVisible(True)
            it.update_geom()
            it.update()
            self.mw.commit()
            self.mw.scene.clearSelection()
            it.setSelected(True)
            self.mw.refresh_props()
        v.setFocus()


# ---------------------------------------------------------------------- saisie d'une fraction
def find_fraction(text, pos):
    """Fraction {haut|bas} qui contient la position du curseur : (début, fin, haut, bas) ou None."""
    from .items import _match, _top_bar
    best = None
    for i, c in enumerate(text):
        if c != "{" or (i > 0 and text[i - 1] == "√"):
            continue
        j = _match(text, i)
        if j < 0 or not (i <= pos <= j + 1):
            continue
        inner = text[i + 1:j]
        k = _top_bar(inner)
        if k >= 0 and (best is None or i > best[0]):
            best = (i, j + 1, inner[:k].strip(), inner[k + 1:].strip())
    return best


class FractionDialog(QDialog):
    """Une case pour le haut, un trait, une case pour le bas : comme on l'écrit sur une feuille."""

    def __init__(self, parent, chars, num="", den=""):
        super().__init__(parent)
        self.setWindowTitle("a⁄b " + T("Fraction"))
        self.setStyleSheet(PALETTE_CSS.replace("QFrame#tbPalette ", "QDialog ")
                           + "QDialog QLabel { color: #263238; } QLineEdit { font-size: 22px; padding: 4px; background: #ffffff; color: #000000; "
                           "border: 1px solid #90a4ae; border-radius: 4px; } QLineEdit:focus { border: 2px solid #1e88e5; "
                           "background: #fffde7; }")
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(T("Écrivez le haut, puis le bas (Entrée passe à la case suivante) :")))
        self.num = QLineEdit(num)
        self.num.setAlignment(Qt.AlignCenter)
        self.num.setPlaceholderText(T("en haut (ex. U)"))
        bar = QFrame()
        bar.setFrameShape(QFrame.HLine)
        bar.setLineWidth(3)
        bar.setStyleSheet("QFrame { color: #263238; border: 2px solid #263238; }")
        self.den = QLineEdit(den)
        self.den.setAlignment(Qt.AlignCenter)
        self.den.setPlaceholderText(T("en bas (ex. I)"))
        for wdg in (self.num, bar, self.den):
            lay.addWidget(wdg)
        self.prev = QLabel()
        self.prev.setAlignment(Qt.AlignCenter)
        self.prev.setMinimumHeight(70)
        self.prev.setStyleSheet("QLabel { background: #ffffff; border: 1px solid #b0bec5; border-radius: 4px; }")
        lay.addWidget(QLabel(T("Aperçu :")))
        lay.addWidget(self.prev)
        grid = QGridLayout()
        grid.setSpacing(2)
        for i, ch in enumerate(chars):
            b = QToolButton(text=ch)
            b.setFocusPolicy(Qt.NoFocus)
            b.setFixedSize(30, 28)
            b.setStyleSheet("QToolButton { font-size: 15px; } QToolButton:hover { background: #ffd600; color: #000; "
                            "border: 2px solid #000; font-weight: bold; }")
            b.clicked.connect(lambda _=False, c=ch: self.put(c))
            grid.addWidget(b, i // 18, i % 18)
        lay.addLayout(grid)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        lay.addWidget(bb)
        self.last = self.num
        for e in (self.num, self.den):
            e.textChanged.connect(self.update_preview)
            e.installEventFilter(self)
        self.num.returnPressed.connect(self.den.setFocus)
        self.den.returnPressed.connect(self.accept)
        self.update_preview()
        (self.den if num and not den else self.num).setFocus()

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.FocusIn and obj in (self.num, self.den):
            self.last = obj
        return False

    def put(self, ch):
        self.last.insert(ch)
        self.last.setFocus()

    def code(self):
        n, d = self.num.text().strip(), self.den.text().strip()
        return "{" + n + "|" + d + "}"

    def update_preview(self):
        from PySide6.QtGui import QFontMetricsF, QImage, QPainter, QPixmap
        from .items import rich_layout, rich_width, draw_rich, text_font
        line = self.code()
        f = text_font(10)
        fm = QFontMetricsF(f)
        k = 0.3
        bases, th = rich_layout(fm, [line])
        img = QImage(int(rich_width(fm, line) * k) + 20, int(th * k) + 14, QImage.Format_ARGB32)
        img.fill(QColor("#ffffff"))
        p = QPainter(img)
        p.setRenderHint(QPainter.Antialiasing)
        p.translate(10, 7)
        p.scale(k, k)
        p.setFont(f)
        p.setPen(QColor("#000000"))
        draw_rich(p, fm, 0, bases[0], line)
        p.end()
        self.prev.setPixmap(QPixmap.fromImage(img))

    @staticmethod
    def ask(parent, chars, num="", den=""):
        d = FractionDialog(parent, chars, num, den)
        return d.code() if d.exec() and (d.num.text().strip() or d.den.text().strip()) else None


def edit_fraction(parent, edit, chars):
    """Bouton « Fraction » d'une zone d'écriture (QPlainTextEdit / QTextEdit) : nouvelle fraction, ou modification de
    celle où se trouve le curseur ; le texte sélectionné devient le haut."""
    c = edit.textCursor()
    blk = c.block()
    pos = c.position() - blk.position()
    hit = None if c.hasSelection() else find_fraction(blk.text(), pos)
    if hit:
        code = FractionDialog.ask(parent, chars, hit[2], hit[3])
        if code:
            c.setPosition(blk.position() + hit[0])
            c.setPosition(blk.position() + hit[1], c.MoveMode.KeepAnchor)
            c.insertText(code)
    else:
        code = FractionDialog.ask(parent, chars, c.selectedText())
        if code:
            c.insertText(code)
    edit.setTextCursor(c)
    edit.setFocus()


# ---------------------------------------------------------------------- éditeur « tel qu'à l'impression »
from PySide6.QtGui import QTextCharFormat, QTextCursor, QTextFormat, QTextImageFormat, QImage, QPainter
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QTextEdit

CODE_PROP = QTextFormat.UserProperty + 7


def split_formulas(text):
    """Découpe en morceaux : ("t", texte) ou ("f", code d'une fraction / racine de premier niveau)."""
    from .items import _match, _top_bar
    out, buf, i = [], "", 0
    while i < len(text):
        if text.startswith("√{", i):
            j = _match(text, i + 1)
            if j > 0:
                if buf:
                    out.append(("t", buf)); buf = ""
                out.append(("f", text[i:j + 1]))
                i = j + 1
                continue
        if text[i] == "{":
            j = _match(text, i)
            if j > 0 and _top_bar(text[i + 1:j]) >= 0:
                if buf:
                    out.append(("t", buf)); buf = ""
                out.append(("f", text[i:j + 1]))
                i = j + 1
                continue
        buf += text[i]
        i += 1
    if buf:
        out.append(("t", buf))
    return out


def formula_image(code, px, color, bold=False, italic=False, family="Helvetica"):
    """Image d'une formule, centrée verticalement sur le trait de fraction (alignement « milieu » de la ligne)."""
    from PySide6.QtGui import QFontMetricsF
    from .items import rich_extent, rich_width, draw_rich, text_font
    f = text_font(10, bold, family, italic)
    fm = QFontMetricsF(f)
    k = px / 100
    up, dn = rich_extent(fm, code)
    axis = fm.ascent() * 0.30
    half = max(up - axis, dn + axis) + 14         # symétrique autour du trait (+ marge pour l épaisseur des traits)
    w = rich_width(fm, code) + 8
    dpr = 2
    img = QImage(int(w * k * dpr) + 2, int(2 * half * k * dpr) + 2, QImage.Format_ARGB32_Premultiplied)
    img.fill(Qt.transparent)
    img.setDevicePixelRatio(dpr)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing)
    p.setRenderHint(QPainter.TextAntialiasing)
    p.scale(k, k)
    p.setFont(f)
    p.setPen(QColor(color))
    draw_rich(p, fm, 4, half + axis, code)
    p.end()
    return img


class MathTextEdit(QTextEdit):
    """Zone d'écriture : les fractions et les racines s'affichent mises en forme ; un clic dessus les modifie."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        from .spell import SpellHighlighter
        self.highlighter = SpellHighlighter(self.document())
        self.on_formula_click = None
        self.px, self.color, self.style_ = 14, "#000000", (False, False, "Helvetica")
        self._n = 0
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)

    # ---- texte <-> document
    def set_code(self, text):
        self.clear()
        c = self.textCursor()
        for bi, line in enumerate(text.split("\n")):
            if bi:
                c.insertBlock()
            for kind, s in split_formulas(line):
                if kind == "t":
                    c.insertText(s, QTextCharFormat())
                else:
                    self.insert_formula(s, c)
        self.setTextCursor(c)

    def insert_formula(self, code, cursor=None):
        c = cursor or self.textCursor()
        self._n += 1
        name = f"formule{self._n}"
        bold, italic, fam = self.style_
        self.document().addResource(QTextDocument_ImageResource(), QUrl(name),
                                    formula_image(code, self.px, self.color, bold, italic, fam))
        fmt = QTextImageFormat()
        fmt.setName(name)
        fmt.setVerticalAlignment(QTextCharFormat.AlignMiddle)
        fmt.setProperty(CODE_PROP, code)
        fmt.setToolTip(T("Cliquez pour modifier"))
        c.insertImage(fmt)
        if cursor is None:
            self.setTextCursor(c)

    def code(self):
        out = []
        b = self.document().begin()
        while b.isValid():
            parts = []
            it = b.begin()
            while not it.atEnd():
                fr = it.fragment()
                if fr.isValid():
                    f = fr.charFormat()
                    code = f.property(CODE_PROP) if f.isImageFormat() else None
                    if code:
                        parts.append(code * fr.length() if fr.length() == 1 else code)
                    else:
                        parts.append(fr.text())
                it += 1
            out.append("".join(parts))
            b = b.next()
        return "\n".join(out)

    def restyle(self, px, color, bold, italic, family):
        """Nouvelle taille (zoom) : les formules sont redessinées à la bonne taille."""
        if (px, color, (bold, italic, family)) == (self.px, self.color, self.style_):
            return
        pos = self.textCursor().position()
        code = self.code()
        self.px, self.color, self.style_ = px, color, (bold, italic, family)
        self.blockSignals(True)
        self.set_code(code)
        self.blockSignals(False)
        c = self.textCursor()
        c.setPosition(min(pos, len(self.toPlainText())))
        self.setTextCursor(c)

    # ---- clic sur une formule
    def formula_at(self, pt):
        c = self.cursorForPosition(pt)
        for pos in (c.position(), c.position() - 1):
            if pos < 0:
                continue
            t = QTextCursor(self.document())
            t.setPosition(pos)
            t.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            f = t.charFormat()
            if f.isImageFormat() and f.property(CODE_PROP):
                a = QTextCursor(self.document()); a.setPosition(pos)
                r1 = self.cursorRect(a)
                a.setPosition(pos + 1)
                r2 = self.cursorRect(a)
                if min(r1.left(), r2.left()) - 2 <= pt.x() <= max(r1.left(), r2.left()) + 2:
                    return pos, f.property(CODE_PROP)
        return None

    def mousePressEvent(self, e):
        hit = self.formula_at(e.position().toPoint()) if e.button() == Qt.LeftButton else None
        if hit and callable(self.on_formula_click):
            e.accept()
            pos, code = hit
            QTimer.singleShot(0, lambda: self.on_formula_click(pos, code))
            return
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        self.viewport().setCursor(Qt.PointingHandCursor if self.formula_at(e.position().toPoint()) else Qt.IBeamCursor)
        super().mouseMoveEvent(e)

    def contextMenuEvent(self, e):
        from .spell import SpellTextEdit
        SpellTextEdit.contextMenuEvent(self, e)

    def _replace(self, cur, s):
        cur.insertText(s)

    def _add(self, w):
        from .spell import add_personal
        add_personal(w)
        self.highlighter.rehighlight()

    def _ignore(self, w):
        from .spell import ignore
        ignore(w)
        self.highlighter.rehighlight()


def QTextDocument_ImageResource():
    from PySide6.QtGui import QTextDocument
    return QTextDocument.ImageResource


class RootDialog(FractionDialog):
    """Racine : une seule case, sous la barre."""

    def __init__(self, parent, chars, inner=""):
        super().__init__(parent, chars, inner, "")
        self.setWindowTitle("√ " + T("Racine"))
        self.den.hide()
        for w in self.findChildren(QFrame):
            if w.frameShape() == QFrame.HLine:
                w.hide()
        self.findChildren(QLabel)[0].setText(T("Écrivez ce qui va sous la racine :"))
        self.num.setPlaceholderText(T("sous la racine (ex. P / R)"))
        self.num.returnPressed.disconnect()
        self.num.returnPressed.connect(self.accept)
        self.update_preview()

    def code(self):
        return "√{" + self.num.text().strip() + "}"

    @staticmethod
    def ask_root(parent, chars, inner=""):
        d = RootDialog(parent, chars, inner)
        return d.code() if d.exec() and d.num.text().strip() else None


def ask_formula(parent, chars, code=None, selected=""):
    """Ouvre la bonne fenêtre (fraction ou racine) ; renvoie le nouveau code ou None."""
    from .items import _top_bar
    if code and code.startswith("√{"):
        return RootDialog.ask_root(parent, chars, code[2:-1])
    if code:
        inner = code[1:-1]
        k = _top_bar(inner)
        return FractionDialog.ask(parent, chars, inner[:k].strip(), inner[k + 1:].strip())
    return FractionDialog.ask(parent, chars, selected)
