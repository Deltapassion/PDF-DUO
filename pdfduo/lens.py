"""Loupe de traduction de PDF DUO.

On laisse la souris immobile sur un paragraphe du PDF (ou sur un texte écrit dans PDF DUO) :
la fenêtre montre la zone agrandie, le texte d'origine et sa traduction.
Onglet « Écrire » : l'élève tape dans sa langue, obtient la phrase dans la langue du document
et peut l'insérer dans la page.
"""
from PySide6.QtCore import Qt, QObject, QEvent, QTimer, QRectF, QPointF, Signal, QRunnable, QThreadPool
from PySide6.QtGui import QColor, QPen, QBrush, QFont, QGuiApplication, QPixmap
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QTextEdit,
                               QTabWidget, QCheckBox, QGraphicsRectItem, QDialog, QFormLayout, QLineEdit,
                               QRadioButton, QButtonGroup, QDialogButtonBox, QProgressDialog, QMessageBox, QGridLayout, QSizeGrip, QSizePolicy,
                               QApplication)

from .i18n import T
from . import translate as TR


class Speaker:
    """Lecture à voix haute avec les voix installées dans le système (Windows : voix de Windows)."""
    def __init__(self):
        self.tts = None
        self.ok = None

    def engine(self):
        if self.ok is None:
            try:
                from PySide6.QtTextToSpeech import QTextToSpeech
                eng = QTextToSpeech.availableEngines()
                pref = next((e for e in ("winrt", "sapi", "speechd", "flite", "macos", "darwin") if e in eng), None)
                self.tts = QTextToSpeech(pref) if pref else QTextToSpeech()
                self.ok = True
            except Exception:
                self.ok = False
        return self.tts if self.ok else None

    def speak(self, text, lang):
        """Renvoie '' si la lecture démarre, sinon un message d'erreur."""
        from PySide6.QtCore import QLocale
        t = self.engine()
        if t is None:
            return T("La lecture à voix haute n'est pas disponible sur cet ordinateur.")
        from PySide6.QtTextToSpeech import QTextToSpeech
        if t.state() == QTextToSpeech.Speaking:
            t.stop()
            return ""
        code = {"nb": "no", "zh": "zh"}.get(lang, lang)
        locs = [l for l in t.availableLocales() if l.name().split("_")[0] == code]
        if not locs:
            return (T("Aucune voix « {l} » n'est installée sur cet ordinateur.").format(l=TR.LANG_NAME.get(lang, lang))
                    + "\n" + T("Windows : Paramètres › Heure et langue › Voix › Ajouter des voix."))
        pref = [l for l in locs if l.country() == QLocale(code).country()]
        t.setLocale((pref or locs)[0])
        vs = t.availableVoices()
        if vs:
            t.setVoice(vs[0])
        t.setRate(-0.1)
        t.say(text)
        return ""


SPEAKER = Speaker()


class ZoomEdit(QTextEdit):
    """Zone de texte : la molette agrandit ou réduit le texte (Ctrl ou Maj + molette : défilement) ;
    bouton 🔊 dans le coin pour entendre le texte."""
    def __init__(self, key, lang_fn, parent=None):
        super().__init__(parent)
        self.key, self.lang_fn = key, lang_fn
        self.extra = ""
        self.size = float(TR.settings().value("trad/size_" + key, 13))
        self.apply()
        from PySide6.QtWidgets import QToolButton
        self.say = QToolButton(self); self.say.setText("🔊"); self.say.setAutoRaise(True)
        self.say.setToolTip(T("Écouter"))
        self.say.setCursor(Qt.PointingHandCursor)
        self.say.clicked.connect(self.speak)
        self.say.setStyleSheet("QToolButton{font-size:15px;border:none}")
        self.setViewportMargins(0, 0, 28, 0)                # le texte ne passe pas sous le 🔊

    def speak(self):
        txt = self.toPlainText().strip()
        if txt and txt != "…":
            err = SPEAKER.speak(txt, self.lang_fn())
            if err:
                QMessageBox.information(self, T("Écouter"), err)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.say.move(self.width() - 28, 3)
        self.say.raise_()

    def wheelEvent(self, e):
        if e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier):
            return super().wheelEvent(e)
        self.size = max(7.0, min(60.0, self.size + (1 if e.angleDelta().y() > 0 else -1)))
        self.apply()
        TR.settings().setValue("trad/size_" + self.key, self.size)
        e.accept()

    def apply(self):
        # feuille de style (le thème de l'application impose sinon sa propre taille de police)
        super().setStyleSheet(f"QTextEdit {{ font-size: {self.size:g}pt; {self.extra} }}")

    def setStyleSheet(self, css):
        self.extra = css
        self.apply()


class _Sig(QObject):
    done = Signal(int, str, str, str)       # n° de demande, traduction, moteur, erreur
    progress = Signal(int, int)
    finished = Signal(str)                  # erreur éventuelle


class _Job(QRunnable):
    def __init__(self, n, text, src, dst, sig):
        super().__init__()
        self.n, self.text, self.src, self.dst, self.sig = n, text, src, dst, sig

    def run(self):
        try:
            out, eng = TR.translate(self.text, self.src, self.dst)
            self.sig.done.emit(self.n, out, eng, "")
        except Exception as e:
            self.sig.done.emit(self.n, "", "", str(e) or e.__class__.__name__)


class _Download(QRunnable):
    def __init__(self, pairs, sig, cancel):
        super().__init__()
        self.pairs, self.sig, self.cancel = pairs, sig, cancel

    def run(self):
        try:
            idx = TR.fetch_index()
            for k, (a, b) in enumerate(self.pairs):
                TR.download_pair(a, b, lambda got, tot, k=k: (self.sig.progress.emit(
                    int((k + (got / tot if tot else 0)) * 1000 / len(self.pairs)), 1000), not self.cancel[0])[1], idx)
            self.sig.finished.emit("")
        except Exception as e:
            self.sig.finished.emit(str(e) or e.__class__.__name__)


def _lang_combo(cur):
    c = QComboBox()
    for code, name in TR.LANGS:
        c.addItem(name, code)
    i = c.findData(cur)
    c.setCurrentIndex(max(0, i))
    c.setMaxVisibleItems(20)
    return c


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle(T("Réglages de la traduction"))
        st = TR.settings()
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>" + T("Moteur de traduction") + "</b>"))
        self.grp = QButtonGroup(self)
        for key, txt in (("auto", T("Automatique : en ligne si internet répond, sinon hors ligne")),
                         ("online", T("En ligne uniquement (rapide, rien à installer)")),
                         ("offline", T("Hors ligne uniquement (aucun texte n'est envoyé sur internet)"))):
            rb = QRadioButton(txt); rb.setProperty("k", key)
            rb.setChecked(st.value("trad/mode", "auto") == key)
            self.grp.addButton(rb); lay.addWidget(rb)
        f = QFormLayout()
        self.email = QLineEdit(st.value("trad/email", "") or "")
        self.email.setPlaceholderText(T("facultatif : augmente le nombre de traductions par jour"))
        f.addRow(T("E-mail (service MyMemory) :"), self.email)
        self.lt = QLineEdit(st.value("trad/lt_url", "") or "")
        self.lt.setPlaceholderText("https://…  (" + T("laisser vide pour MyMemory") + ")")
        f.addRow(T("Serveur LibreTranslate :"), self.lt)
        self.key = QLineEdit(st.value("trad/lt_key", "") or "")
        f.addRow(T("Clé LibreTranslate :"), self.key)
        lay.addLayout(f)
        lay.addWidget(QLabel("<b>" + T("Langues hors ligne installées") + "</b>"))
        pairs = sorted(TR.installed_pairs())
        lay.addWidget(QLabel(", ".join(f"{TR.LANG_NAME.get(a, a)} → {TR.LANG_NAME.get(b, b)}" for a, b in pairs)
                             or T("aucune pour l'instant")))
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.save); bb.rejected.connect(self.reject)
        lay.addWidget(bb)

    def save(self):
        st = TR.settings()
        st.setValue("trad/mode", self.grp.checkedButton().property("k"))
        st.setValue("trad/email", self.email.text().strip())
        st.setValue("trad/lt_url", self.lt.text().strip())
        st.setValue("trad/lt_key", self.key.text().strip())
        self.accept()


class TranslateLens(QWidget):
    def __init__(self, mw):
        super().__init__(mw, Qt.Tool)
        self.mw = mw
        self.setWindowTitle("🔍 " + T("Loupe de traduction"))
        self.resize(460, 600)
        st = TR.settings()
        self.n = 0
        self.last_text = ""
        self.sig = _Sig(); self.sig.done.connect(self.on_done)
        self.pool = QThreadPool(self); self.pool.setMaxThreadCount(1)
        self.hl = None
        self.scene_pos = None

        lay = QVBoxLayout(self)
        self.src = _lang_combo(st.value("trad/src", "fr"))
        self.dst = _lang_combo(st.value("trad/dst", "en"))
        sw = QPushButton("⇄"); sw.setFixedWidth(34); sw.setToolTip(T("Inverser les langues"))
        sw.clicked.connect(self.swap)
        g = QGridLayout(); g.setColumnStretch(1, 1)
        self.l_doc = QLabel(T("Document :")); g.addWidget(self.l_doc, 0, 0); g.addWidget(self.src, 0, 1); g.addWidget(sw, 0, 2, 2, 1)
        self.l_dst = QLabel(T("Traduire en :")); g.addWidget(self.l_dst, 1, 0); g.addWidget(self.dst, 1, 1)
        lay.addLayout(g)
        for c in (self.src, self.dst):
            c.currentIndexChanged.connect(self.langs_changed)

        row2 = QHBoxLayout()
        self.pin = QCheckBox("📌 " + T("Figer")); self.pin.setToolTip(T("Garder le texte actuel même si la souris bouge"))
        self.status = QLabel(""); self.status.setStyleSheet("color: gray")
        gear = QPushButton("⚙"); gear.setToolTip(T("Réglages")); gear.setFixedWidth(34); gear.clicked.connect(self.open_settings)
        dl = QPushButton("💾"); dl.setFixedWidth(34)
        dl.setToolTip(T("Hors ligne…") + " " + T("Télécharger les langues pour traduire sans internet"))
        dl.clicked.connect(self.download)
        row2.addWidget(self.pin); row2.addWidget(self.status, 1); row2.addWidget(dl); row2.addWidget(gear)
        lay.addLayout(row2)

        tabs = QTabWidget(); lay.addWidget(tabs, 1)
        self.tabs = tabs
        # --- lire
        w = QWidget(); v = QVBoxLayout(w)
        self.zoom = QLabel(); self.zoom.setAlignment(Qt.AlignCenter); self.zoom.setMinimumHeight(30); self.zoom.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.zoom.setStyleSheet("background: white; border: 1px solid #999")
        v.addWidget(self.zoom, 1)
        big = QFont(); big.setPointSize(13)
        self.orig = ZoomEdit("orig", lambda: self.src.currentData()); self.orig.setPlaceholderText(
            T("Laissez la souris immobile sur un paragraphe du document…"))
        self.orig.textChanged.connect(self.orig_edited)
        self.trans = ZoomEdit("trans", lambda: self.dst.currentData()); self.trans.setReadOnly(True)
        self.trans.setStyleSheet("background: #fffbe6; color: #1a1a1a")
        v.addWidget(self.orig, 1); v.addWidget(self.trans, 1)
        b = QHBoxLayout()
        bc = QPushButton("📋 " + T("Copier")); bc.clicked.connect(lambda: QGuiApplication.clipboard().setText(self.trans.toPlainText()))
        bi = QPushButton("➕ " + T("Insérer dans la page")); bi.clicked.connect(lambda: self.insert(self.trans.toPlainText()))
        b.addWidget(bc); b.addWidget(bi); v.addLayout(b)
        self._btns = getattr(self, "_btns", []) + [(bc, "📋", T("Copier")), (bi, "➕", T("Insérer dans la page"))]
        tabs.addTab(w, "📖 " + T("Lire"))
        # --- écrire
        w = QWidget(); v = QVBoxLayout(w)
        self.w_hint = QLabel(); self.w_hint.setWordWrap(True); v.addWidget(self.w_hint)
        self.w_in = ZoomEdit("w_in", lambda: self.src.currentData()); v.addWidget(self.w_in, 1)
        self.w_in.textChanged.connect(lambda: self.write_timer.start())   # traduction au fil de la frappe
        bt = QPushButton("⬇ " + T("Traduire")); bt.clicked.connect(self.write_translate); v.addWidget(bt)
        self.w_out = ZoomEdit("w_out", lambda: self.dst.currentData()); self.w_out.setStyleSheet("background: #eef7ff; color: #1a1a1a")
        v.addWidget(self.w_out, 1)
        b = QHBoxLayout()
        bc = QPushButton("📋 " + T("Copier")); bc.clicked.connect(lambda: QGuiApplication.clipboard().setText(self.w_out.toPlainText()))
        bi = QPushButton("➕ " + T("Insérer dans la page")); bi.clicked.connect(lambda: self.insert(self.w_out.toPlainText()))
        b.addWidget(bc); b.addWidget(bi); v.addLayout(b)
        self._btns = getattr(self, "_btns", []) + [(bc, "📋", T("Copier")), (bi, "➕", T("Insérer dans la page"))]
        tabs.addTab(w, "✏ " + T("Écrire"))
        grip = QHBoxLayout(); grip.addStretch(1); grip.addWidget(QSizeGrip(self)); lay.addLayout(grip)
        self.update_hint()
        self.setMinimumSize(180, 160)
        for te in (self.orig, self.trans, self.w_in, self.w_out):
            te.setMinimumHeight(28)
        self.zoom.setMinimumWidth(10)
        for wd in self.findChildren(QPushButton):
            wd.setMinimumWidth(0)
        for c in (self.src, self.dst):
            c.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon); c.setMinimumContentsLength(3)
        try:
            geo = st.value("trad/geom")
            if geo is not None:
                self.restoreGeometry(geo)
        except Exception:
            pass

        self.timer = QTimer(self, singleShot=True, interval=600)
        self.timer.timeout.connect(self.pick)
        self.edit_timer = QTimer(self, singleShot=True, interval=900)
        self.write_timer = QTimer(self, singleShot=True, interval=800)
        self.write_timer.timeout.connect(self.write_translate)
        self.edit_timer.timeout.connect(lambda: self.request(self.orig.toPlainText(), force=True))
        mw.view.viewport().installEventFilter(self)

    # ---------------------------------------------------------- souris
    def eventFilter(self, obj, e):
        if self.isVisible() and e.type() == QEvent.MouseMove and not self.pin.isChecked():
            self.scene_pos = self.mw.view.mapToScene(e.position().toPoint())
            self.timer.start()
        return False

    def text_at(self, sp):
        """Texte sous le point (coordonnées de scène) et rectangle de scène correspondant."""
        mw = self.mw
        for it in mw.scene.items(sp):                         # texte écrit dans PDF DUO
            d = getattr(it, "d", None)
            if isinstance(d, dict) and d.get("type") == "text" and d.get("text", "").strip():
                return d["text"], it.sceneBoundingRect()
        if not mw.doc or not mw.page_items:
            return "", None
        i, x, y = mw.page_coords(sp)
        if i >= len(mw.doc):
            return "", None
        page = mw.doc[i]
        pg = mw.page_items[i]
        sx = pg.w / page.rect.width if page.rect.width else 1
        sy = pg.h / page.rect.height if page.rect.height else 1
        px, py = x / sx, y / sy
        for b in page.get_text("blocks"):
            if len(b) > 6 and b[6] != 0:
                continue                                     # bloc image
            x0, y0, x1, y1, txt = b[:5]
            if x0 - 3 <= px <= x1 + 3 and y0 - 3 <= py <= y1 + 3 and txt.strip():
                r = QRectF(x0 * sx, y0 * sy, (x1 - x0) * sx, (y1 - y0) * sy).translated(pg.pos())
                return " ".join(txt.split()), r
        return "", None

    def pick(self):
        if self.scene_pos is None:
            return
        txt, r = self.text_at(self.scene_pos)
        if not txt or txt == self.last_text:
            return
        self.show_highlight(r)
        self.show_zoom(r)
        self.orig.blockSignals(True); self.orig.setPlainText(txt); self.orig.blockSignals(False)
        self.request(txt)

    def show_highlight(self, r):
        sc = self.mw.scene
        if self.hl is None or self.hl.scene() is not sc:
            self.hl = QGraphicsRectItem()
            self.hl.setPen(QPen(QColor(255, 140, 0), 1.5))
            self.hl.setBrush(QBrush(QColor(255, 200, 0, 45)))
            self.hl.setZValue(1e6); self.hl.setAcceptedMouseButtons(Qt.NoButton)
            sc.addItem(self.hl)
        self.hl.setRect(r.adjusted(-3, -3, 3, 3)); self.hl.show()
        self.last_rect = QRectF(self.hl.rect())

    def show_zoom(self, r):
        v = self.mw.view
        vr = v.mapFromScene(r.adjusted(-4, -4, 4, 4)).boundingRect().intersected(v.viewport().rect())
        if vr.isEmpty():
            self.zoom.clear(); return
        self.hl.hide()
        pm = v.viewport().grab(vr)
        self._zoom_pm = pm
        self.hl.show()
        w = max(100, self.zoom.width() - 6)
        self.zoom.setPixmap(pm.scaled(w, max(30, self.zoom.height() - 4), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # ---------------------------------------------------------- traduction
    def codes(self):
        return self.src.currentData(), self.dst.currentData()

    def request(self, text, force=False, target=None):
        text = (text or "").strip()
        if not text or (text == self.last_text and not force and target is None):
            return
        src, dst = self.codes()
        if target is None:
            self.last_text = text
        self.n += 1
        self.target = target or "read"
        (self.trans if self.target == "read" else self.w_out).setPlainText("…")
        self.status.setText(T("Traduction…"))
        a, b = src, dst                                   # mêmes langues que celles choisies en haut
        self.pool.start(_Job(self.n, text, a, b, self.sig))

    def on_done(self, n, out, eng, err):
        if n != self.n:
            return
        box = self.trans if self.target == "read" else self.w_out
        if err:
            box.setPlainText("")
            self.status.setText("⚠ " + self.explain(err))
            return
        box.setPlainText(out)
        self.status.setText({"online": "🌐 " + T("en ligne"), "offline": "💾 " + T("hors ligne")}.get(eng, ""))

    def explain(self, err):
        if err == "modeles":
            return T("langues hors ligne non installées (bouton « Hors ligne… »)")
        return T("pas de connexion au service de traduction") if "urlopen" in err or "timed out" in err or "Errno" in err else err

    def orig_edited(self):
        self.edit_timer.start()

    def write_translate(self):
        self.request(self.w_in.toPlainText(), target="write")

    def langs_changed(self):
        st = TR.settings()
        st.setValue("trad/src", self.src.currentData()); st.setValue("trad/dst", self.dst.currentData())
        self.update_hint()
        if self.orig.toPlainText().strip():
            self.request(self.orig.toPlainText(), force=True)

    def update_hint(self):
        self.w_hint.setText(T("Écrivez en {a} : la phrase est traduite en {b}, prête à insérer dans le document.")
                            .format(a=self.src.currentText(), b=self.dst.currentText()))

    def swap(self):
        a, b = self.src.currentIndex(), self.dst.currentIndex()
        self.src.blockSignals(True); self.src.setCurrentIndex(b); self.src.blockSignals(False)
        self.dst.setCurrentIndex(a)

    # ---------------------------------------------------------- actions
    def insert(self, text):
        text = text.strip()
        if not text:
            return
        mw = self.mw
        sp = self.scene_pos or mw.view.mapToScene(mw.view.viewport().rect().center())
        width = 420
        lr = getattr(self, "last_rect", None)
        if lr is not None and self.hl is not None and self.hl.scene() is mw.scene:   # juste sous le dernier paragraphe lu
            sp = QPointF(lr.left() + 3, lr.bottom() + 6)
            width = max(160, lr.width() - 6)
        size = mw.cur_text_size
        per_line = max(20, int(width / (0.5 * size)))
        import textwrap
        text = "\n".join(textwrap.fill(p, per_line) for p in text.split("\n"))
        mw.add_item({"type": "text", "x": sp.x(), "y": sp.y(), "text": text, "size": size,
                          "color": "#1f4e9e", **mw.text_style}, select=True)
        mw.commit()

    def open_settings(self):
        SettingsDialog(self).exec()

    def download(self):
        src, dst = self.codes()
        pairs = []
        for a, b in (TR.needed_pairs(src, dst) + TR.needed_pairs(dst, src)):
            if (a, b) not in pairs and (a, b) not in TR.installed_pairs():
                pairs.append((a, b))
        if not pairs:
            QMessageBox.information(self, T("Hors ligne"), T("Ces langues sont déjà installées : la traduction fonctionne sans internet."))
            return
        try:
            import ctranslate2, sentencepiece  # noqa: F401
        except Exception:
            QMessageBox.warning(self, T("Hors ligne"), T("Le module de traduction hors ligne n'est pas présent dans cette installation."))
            return
        names = ", ".join(f"{TR.LANG_NAME.get(a, a)} → {TR.LANG_NAME.get(b, b)}" for a, b in pairs)
        if QMessageBox.question(self, T("Hors ligne"), T("Télécharger les langues suivantes (environ 100 Mo chacune, une seule fois) ?")
                                + "\n\n" + names) != QMessageBox.Yes:
            return
        dlg = QProgressDialog(T("Téléchargement des langues…"), T("Annuler"), 0, 1000, self)
        dlg.setWindowModality(Qt.WindowModal); dlg.setMinimumDuration(0); dlg.setValue(0)
        cancel = [False]
        dlg.canceled.connect(lambda: cancel.__setitem__(0, True))
        sig = _Sig()
        sig.progress.connect(lambda a, b: dlg.setValue(a))

        def fin(err):
            dlg.close()
            if err and not cancel[0]:
                QMessageBox.warning(self, T("Hors ligne"), T("Le téléchargement a échoué :") + "\n" + err)
            elif not err:
                QMessageBox.information(self, T("Hors ligne"), T("Langues installées : la traduction fonctionne maintenant sans internet."))
        sig.finished.connect(fin)
        self._dl = (sig, _Download(pairs, sig, cancel))
        QThreadPool.globalInstance().start(self._dl[1])

    def save_geom(self):
        TR.settings().setValue("trad/geom", self.saveGeometry())

    def resizeEvent(self, e):
        super().resizeEvent(e); self.save_geom()
        pm = getattr(self, '_zoom_pm', None)
        if pm is not None and not pm.isNull():
            self.zoom.setPixmap(pm.scaled(max(20, self.zoom.width() - 6), max(30, self.zoom.height() - 4), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        compact = self.width() < 340                       # fenêtre étroite : libellés réduits aux icônes
        if compact != getattr(self, "_compact", None):
            self._compact = compact
            self.l_doc.setText("📄" if compact else T("Document :"))
            self.l_dst.setText("➜" if compact else T("Traduire en :"))
            self.pin.setText("📌" if compact else "📌 " + T("Figer"))
            for btn, ico, txt in getattr(self, "_btns", []):
                btn.setText(ico if compact else ico + " " + txt); btn.setToolTip(txt)

    def moveEvent(self, e):
        super().moveEvent(e); self.save_geom()

    def hideEvent(self, e):
        if self.hl is not None:
            try:
                self.hl.hide()
            except RuntimeError:
                pass
        super().hideEvent(e)
