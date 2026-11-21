"""Reconnaissance de texte (OCR) pour les PDF scannés.

PyMuPDF contient déjà le moteur Tesseract : il suffit des fichiers de langue (« traineddata »),
téléchargés une seule fois depuis le dépôt officiel tesseract-ocr/tessdata_fast (1 à 5 Mo par langue).
Le texte reconnu est ajouté en couche invisible sur la page : l'aspect ne change pas, mais on peut
chercher, sélectionner, copier et traduire le texte (loupe de traduction).
"""
import os
import urllib.request

import pymupdf

from . import translate as TR

URL = "https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/{}.traineddata"

# (code Tesseract, nom affiché, code de langue de PDF DUO)
LANGS = [("fra", "Français", "fr"), ("eng", "English", "en"), ("spa", "Español", "es"), ("por", "Português", "pt"),
         ("deu", "Deutsch", "de"), ("ita", "Italiano", "it"), ("ell", "Ελληνικά", "el"), ("chi_sim", "中文", "zh"),
         ("rus", "Русский", "ru"), ("ukr", "Українська", "uk"), ("ara", "العربية", "ar"), ("sqi", "Shqip", "sq"),
         ("tur", "Türkçe", "tr"), ("ron", "Română", "ro"), ("pol", "Polski", "pl"), ("nld", "Nederlands", "nl")]

FONT_CANDIDATES = [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\segoeui.ttf",
                   "/Library/Fonts/Arial Unicode.ttf", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
                   "/System/Library/Fonts/Supplemental/Arial.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans.ttf",
                   "/usr/share/fonts/dejavu/DejaVuSans.ttf"]


def tessdir():
    d = os.path.join(TR.data_dir(), "tessdata")
    os.makedirs(d, exist_ok=True)
    return d


def missing(codes):
    return [c for c in codes if not os.path.exists(os.path.join(tessdir(), c + ".traineddata"))]


def download(codes, progress=None):
    """Télécharge les fichiers de langue manquants. progress(i, n) après chaque fichier."""
    todo = missing(codes)
    for i, c in enumerate(todo):
        dest = os.path.join(tessdir(), c + ".traineddata")
        req = urllib.request.Request(URL.format(c), headers=TR.UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        if len(data) < 10000:
            raise TR.TranslateError(c)
        with open(dest + ".tmp", "wb") as f:
            f.write(data)
        os.replace(dest + ".tmp", dest)
        if progress:
            progress(i + 1, len(todo))


def recognise(pdf_bytes, pages, lang, only_empty=True, dpi=300, progress=None, cancel=None):
    """Renvoie {n° de page: [(x0, y0, x1, y1, mot), …]} pour les pages demandées (travail sur une copie)."""
    doc = pymupdf.open("pdf", pdf_bytes)
    out = {}
    for k, pno in enumerate(pages):
        if cancel and cancel():
            break
        page = doc[pno]
        if only_empty and page.get_text().strip():
            if progress:
                progress(k + 1, len(pages))
            continue
        tp = page.get_textpage_ocr(language=lang, dpi=dpi, full=True, tessdata=tessdir())
        lines = {}                                   # mots regroupés par ligne : les espaces sont conservés
        for w in page.get_text("words", textpage=tp):
            if w[4].strip():
                lines.setdefault((w[5], w[6]), []).append(w)
        out[pno] = [(min(a[0] for a in ws), min(a[1] for a in ws), max(a[2] for a in ws), max(a[3] for a in ws),
                     " ".join(a[4] for a in sorted(ws, key=lambda a: a[0]))) for ws in lines.values()]
        if progress:
            progress(k + 1, len(pages))
    return out


def _fallback_font():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def apply(doc, words):
    """Ajoute les mots reconnus en texte invisible (mode de rendu 3) sur les pages du document."""
    ff = _fallback_font()
    total = 0
    for pno, lst in words.items():
        page = doc[pno]
        fonts_ok = False
        for x0, y0, x1, y1, w in lst:
            h = max(1.0, y1 - y0)
            fs = h * 0.85
            try:
                w.encode("cp1252")
                name = "helv"
            except UnicodeEncodeError:
                if not ff:
                    continue
                if not fonts_ok:
                    page.insert_font(fontname="ocrf", fontfile=ff)
                    fonts_ok = True
                name = "ocrf"
            try:
                tl = pymupdf.get_text_length(w, fontname="helv", fontsize=fs) if name == "helv" else \
                    pymupdf.Font(fontfile=ff).text_length(w, fontsize=fs)
                sx = (x1 - x0) / tl if tl > 0 else 1
                base = pymupdf.Point(x0, y1 - h * 0.2)
                page.insert_text(base, w, fontsize=fs, fontname=name, render_mode=3,
                                 morph=(base, pymupdf.Matrix(sx, 1)))
                total += 1
            except Exception:
                continue
    return total
