"""Correcteur orthographique de PDF DUO (hors ligne, six langues).

Dictionnaires : listes de fréquences de mots (pdfduo/notices/dictionnaires/<langue>.json.gz).
Les mots inconnus sont soulignés en rouge ; clic droit pour les suggestions,
« Ajouter au dictionnaire » ou « Ignorer ».
"""
import gzip
import json
import os
import re
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QStyledItemDelegate

from .i18n import T

LANGS = ("fr", "en", "es", "pt", "de", "it")
_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
_LETTERS = {
    "fr": "abcdefghijklmnopqrstuvwxyzàâäçéèêëîïôöùûüÿœæ",
    "en": "abcdefghijklmnopqrstuvwxyz",
    "es": "abcdefghijklmnopqrstuvwxyzáéíóúüñ",
    "pt": "abcdefghijklmnopqrstuvwxyzáàâãçéêíóôõú",
    "de": "abcdefghijklmnopqrstuvwxyzäöüß",
    "it": "abcdefghijklmnopqrstuvwxyzàèéìíòóù",
}
# vocabulaire technique des sections professionnelles, absent des listes de fréquences
_TECH = {
    "fr": """contacteur contacteurs sectionneur sectionneurs disjoncteur disjoncteurs différentiel différentiels télérupteur
    télérupteurs minuterie bornier borniers goulotte goulottes grafcet algorigramme logigramme bobine bobines
    temporisation temporisé temporisée réceptivité réceptivités consignation déconsignation balisage habilitation
    électrotechnique électrotechnicien domotique photovoltaïque onduleur onduleurs régulateur régulateurs parafoudre
    parafoudres équipotentielle équipotentielles câblage câbler câblé câblée raccordement interrupteur interrupteurs
    va-et-vient variateur variateurs luminaire luminaires plafonnier plafonniers convecteur convecteurs vérin vérins
    distributeur distributeurs électrovanne électrovannes pneumatique pneumatiques capteur capteurs actionneur actionneurs
    préactionneur préactionneurs automate automates fibre switch routeur routeurs ethernet wifi vidéosurveillance
    caméra caméras schéma schémas ampèremètre voltmètre multimètre oscilloscope wattmètre ohmmètre résistance
    condensateur inductance transformateur triphasé triphasée monophasé monophasée neutre phase terre
    prothésiste prothèse prothèses orthodontique implant bridge couronne magasinier transpalette gerbeur palette
    palettes logistique manutention secourisme défibrillateur électrisation électrocution""",
}
_cache = {}
_state = {"enabled": True, "lang": "auto", "personal": set(), "ignored": set()}


def _dict_path(lang):
    here = os.path.dirname(os.path.abspath(__file__))
    roots = [here]
    base = getattr(sys, "_MEIPASS", None)
    if base:
        roots.append(os.path.join(base, "pdfduo"))
    for r in roots:
        p = os.path.join(r, "notices", "dictionnaires", f"{lang}.json.gz")
        if os.path.exists(p):
            return p
    return None


def words_for(lang):
    """Dictionnaire {mot: fréquence} de la langue (chargé une seule fois)."""
    if lang not in _cache:
        p = _dict_path(lang)
        d = {}
        if p:
            try:
                with gzip.open(p, "rt", encoding="utf-8") as f:
                    d = json.load(f)
            except (OSError, ValueError):
                d = {}
        for w in _TECH.get(lang, "").split():
            d.setdefault(w, 1)
        _cache[lang] = d
    return _cache[lang]


def configure(enabled=None, lang=None, personal=None):
    if enabled is not None:
        _state["enabled"] = bool(enabled)
    if lang is not None:
        _state["lang"] = lang
    if personal is not None:
        _state["personal"] = set(personal)


def current_lang():
    if _state["lang"] in LANGS:
        return _state["lang"]
    from . import i18n
    return i18n.LANG if i18n.LANG in LANGS else "en"


def is_enabled():
    return _state["enabled"]


def personal_words():
    return sorted(_state["personal"])


def add_personal(word):
    _state["personal"].add(word.lower())
    try:
        from PySide6.QtCore import QSettings
        QSettings("Jacques Branas", "PDF DUO").setValue("dico_perso", sorted(_state["personal"]))
    except Exception:  # noqa: BLE001 – la mémorisation est facultative
        pass


def ignore(word):
    _state["ignored"].add(word.lower())


def is_correct(word):
    if len(word) < 2 or word.isupper():          # sigles (KM1, RIA, GTL…) et lettres seules
        return True
    w = word.lower()
    if w in _state["personal"] or w in _state["ignored"]:
        return True
    d = words_for(current_lang())
    if not d:
        return True                               # dictionnaire absent : on ne souligne rien
    return w in d


def misspelled(text):
    """Liste (début, longueur, mot) des mots inconnus d'un texte."""
    if not _state["enabled"]:
        return []
    return [(m.start(), len(m.group()), m.group()) for m in _WORD.finditer(text) if not is_correct(m.group())]


def _edits1(w, letters):
    splits = [(w[:i], w[i:]) for i in range(len(w) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits if b for c in letters]
    inserts = [a + c + b for a, b in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def suggestions(word, n=6):
    lang = current_lang()
    d = words_for(lang)
    if not d:
        return []
    w = word.lower()
    letters = _LETTERS.get(lang, _LETTERS["en"])
    e1 = _edits1(w, letters)
    cands = [x for x in e1 if x in d]
    if (len(cands) < 3 and len(w) <= 9) or (not cands and len(w) <= 12):
        seen = set(cands)
        for e in e1:
            for x in _edits1(e, letters):
                if x in d and x not in seen:
                    seen.add(x)
                    cands.append(x)
    cands.sort(key=lambda x: -d.get(x, 0))
    out = cands[:n]
    if word[:1].isupper():
        out = [x[:1].upper() + x[1:] for x in out]
    return out


# ------------------------------------------------------------------------- widgets
class SpellHighlighter(QSyntaxHighlighter):
    def __init__(self, doc):
        super().__init__(doc)
        self.fmt = QTextCharFormat()
        self.fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.fmt.setUnderlineColor(QColor("#e53935"))

    def highlightBlock(self, text):
        for start, length, _ in misspelled(text):
            self.setFormat(start, length, self.fmt)


class SpellTextEdit(QPlainTextEdit):
    """Zone de texte avec soulignement des fautes et suggestions au clic droit."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.highlighter = SpellHighlighter(self.document())
        self.on_personal_change = None

    def contextMenuEvent(self, e):
        menu = self.createStandardContextMenu()
        cur = self.cursorForPosition(e.pos())
        cur.select(QTextCursor.WordUnderCursor)
        word = cur.selectedText().strip("'’-")
        if word and _WORD.fullmatch(word) and is_enabled() and not is_correct(word):
            first = menu.actions()[0] if menu.actions() else None
            sugg = suggestions(word)
            acts = []
            for s in sugg:
                a = menu.addAction(s)
                f = a.font()
                f.setBold(True)
                a.setFont(f)
                a.triggered.connect(lambda _=False, s=s, c=QTextCursor(cur): self._replace(c, s))
                acts.append(a)
            if not sugg:
                a = menu.addAction(T("(aucune suggestion)"))
                a.setEnabled(False)
                acts.append(a)
            add = menu.addAction(T("Ajouter au dictionnaire"))
            add.triggered.connect(lambda _=False, w=word: self._add(w))
            ign = menu.addAction(T("Ignorer"))
            ign.triggered.connect(lambda _=False, w=word: self._ignore(w))
            sep = menu.addSeparator()
            for a in acts + [add, ign, sep]:
                menu.removeAction(a)
            for a in acts + [add, ign, sep]:
                menu.insertAction(first, a)
        menu.exec(e.globalPos())

    def _replace(self, cur, s):
        cur.insertText(s)

    def _add(self, w):
        add_personal(w)
        if callable(self.on_personal_change):
            self.on_personal_change()
        self.highlighter.rehighlight()

    def _ignore(self, w):
        ignore(w)
        self.highlighter.rehighlight()


class SpellLineEdit(SpellTextEdit):
    """Éditeur d'une ligne (cases de tableau) avec correction orthographique."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTabChangesFocus(True)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.clearFocus()          # valide la case (le délégué récupère le texte)
            return
        super().keyPressEvent(e)


class SpellDelegate(QStyledItemDelegate):
    """Délégué de QTableWidget : les cases s'éditent avec correction orthographique."""

    def createEditor(self, parent, option, index):
        ed = SpellLineEdit(parent)
        ed.setFrameStyle(0)
        return ed

    def setEditorData(self, editor, index):
        editor.setPlainText(index.data(Qt.EditRole) or "")
        editor.moveCursor(QTextCursor.End)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.toPlainText().replace("\n", " "), Qt.EditRole)
