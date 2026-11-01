"""Conversions Word / ODF / images <-> PDF.

Ordre d'essai pour Word / ODT -> PDF :
  1. LibreOffice en mode invisible (« headless ») : le plus fidèle, gratuit ;
  2. Microsoft Word s'il est installé (Windows : automatisation COM ; macOS : AppleScript) ;
  3. conversion intégrée à PDF DUO pour les .docx et .txt (python-docx + Qt) : texte, titres,
     listes, tableaux, images, en-têtes / pieds de page ; mise en page complexe simplifiée.
- PDF -> Word (.docx) : pdf2docx (toujours sans LibreOffice).
- PDF -> ODT et Word <-> ODT : LibreOffice, ou Microsoft Word sous Windows.
"""
import os
import shutil
import subprocess
import sys
import tempfile

OFFICE_EXT = (".doc", ".docx", ".odt", ".rtf", ".txt", ".ppt", ".pptx", ".odp", ".xls", ".xlsx", ".ods", ".odg")
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".webp")


def find_soffice():
    for name in ("soffice", "libreoffice"):
        p = shutil.which(name)
        if p:
            return p
    candidates = []
    if sys.platform.startswith("win"):
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")):
            candidates.append(os.path.join(base, "LibreOffice", "program", "soffice.exe"))
    elif sys.platform == "darwin":
        candidates.append("/Applications/LibreOffice.app/Contents/MacOS/soffice")
    else:
        candidates += ["/usr/bin/soffice", "/usr/lib/libreoffice/program/soffice",
                       "/snap/bin/libreoffice", "/var/lib/flatpak/exports/bin/org.libreoffice.LibreOffice"]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


class ConversionError(Exception):
    pass


def _soffice_convert(src, fmt, outdir):
    exe = find_soffice()
    if not exe:
        raise ConversionError("LibreOffice est introuvable. Installez-le (gratuit : libreoffice.org) "
                              "pour convertir les documents Word et ODF.")
    profile = tempfile.mkdtemp(prefix="pdfduo-lo-")
    cmd = [exe, f"-env:UserInstallation=file:///{profile.replace(os.sep, '/').lstrip('/')}",
           "--headless", "--norestore", "--convert-to", fmt, "--outdir", outdir, src]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        raise ConversionError("La conversion a pris trop de temps.")
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    base = os.path.splitext(os.path.basename(src))[0]
    ext = fmt.split(":")[0]
    out = os.path.join(outdir, base + "." + ext)
    if not os.path.exists(out):
        raise ConversionError("LibreOffice n'a pas pu convertir le fichier.\n" + (r.stderr or r.stdout)[-800:])
    return out


LAST_ENGINE = ""   # « libreoffice », « word » ou « integree » : moteur utilisé pour la dernière conversion

NO_ENGINE = ("Aucun outil de conversion n'est disponible pour ce type de fichier.\n"
             "Installez LibreOffice (gratuit : libreoffice.org) ou Microsoft Word.")


# ---------------------------------------------------------------- Microsoft Word
WORD_FORMATS = {"pdf": 17, "docx": 16, "odt": 23}


def find_word():
    """Chemin (macOS) ou « COM » (Windows) si Microsoft Word est installé, sinon None."""
    if sys.platform.startswith("win"):
        try:
            import winreg
            winreg.CloseKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"Word.Application\CLSID"))
            return "COM"
        except OSError:
            return None
    if sys.platform == "darwin":
        for app in ("/Applications/Microsoft Word.app", os.path.expanduser("~/Applications/Microsoft Word.app")):
            if os.path.exists(app):
                return app
    return None


_PS_WORD = r"""
$ErrorActionPreference = 'Stop'
$w = New-Object -ComObject Word.Application
try {
  $w.Visible = $false; $w.DisplayAlerts = 0
  $d = $w.Documents.Open($env:PDFDUO_SRC, $false, $true, $false)
  if ([int]$env:PDFDUO_FMT -eq 17) { $d.ExportAsFixedFormat($env:PDFDUO_DST, 17) }
  else { $d.SaveAs2($env:PDFDUO_DST, [int]$env:PDFDUO_FMT) }
  $d.Close(0)
} finally { $w.Quit() }
"""


def _word_convert(src, dst, fmt):
    word = find_word()
    if not word:
        raise ConversionError(NO_ENGINE)
    src, dst = os.path.abspath(src), os.path.abspath(dst)
    if os.path.exists(dst):
        os.remove(dst)
    if word == "COM":
        env = dict(os.environ, PDFDUO_SRC=src, PDFDUO_DST=dst, PDFDUO_FMT=str(WORD_FORMATS[fmt]))
        cmd = ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", _PS_WORD]
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            r = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=300, creationflags=flags)
        except (OSError, subprocess.TimeoutExpired) as e:
            raise ConversionError(f"Microsoft Word n'a pas pu convertir le fichier ({e}).")
    else:
        if fmt not in ("pdf", "docx"):
            raise ConversionError(NO_ENGINE)
        ff = "format PDF" if fmt == "pdf" else "format document"
        esc = lambda x: x.replace("\\", "\\\\").replace('"', '\\"')
        script = (f'tell application "Microsoft Word"\n'
                  f'  open POSIX file "{esc(src)}"\n'
                  f'  set d to active document\n'
                  f'  save as d file name (POSIX file "{esc(dst)}" as string) file format {ff}\n'
                  f'  close d saving no\n'
                  f'end tell')
        try:
            r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=300)
        except (OSError, subprocess.TimeoutExpired) as e:
            raise ConversionError(f"Microsoft Word n'a pas pu convertir le fichier ({e}).")
    if not os.path.exists(dst) or os.path.getsize(dst) == 0:
        raise ConversionError("Microsoft Word n'a pas pu convertir le fichier.\n" + ((r.stderr or r.stdout) or "")[-600:])
    return dst


# ---------------------------------------------------------------- conversion intégrée (.docx -> PDF)
def _emu_px(v):
    return float(v) / 9525.0 if v else 0.0          # EMU -> pixels à 96 ppp


def _esc(t):
    import html
    return html.escape(t).replace("\t", "&emsp;").replace("\n", "<br>")


def _docx_html(doc, resources):
    """Transforme le document python-docx en HTML compris par QTextDocument."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    from docx.oxml.ns import qn
    ALIGN = {0: "left", 1: "center", 2: "right", 3: "justify"}

    def run_html(run):
        out = []
        for child in run._r.iterchildren():
            tag = child.tag.split("}")[1]
            if tag == "t":
                out.append(_esc(child.text or ""))
            elif tag == "tab":
                out.append("&emsp;")
            elif tag == "br":
                out.append('</p><p style="page-break-before:always">' if child.get(qn("w:type")) == "page" else "<br>")
            elif tag == "drawing":
                for blip in child.iter(qn("a:blip")):
                    rid = blip.get(qn("r:embed"))
                    part = doc.part.related_parts.get(rid)
                    if part is None:
                        continue
                    name = f"img{len(resources)}"
                    resources[name] = part.blob
                    ext = next(child.iter(qn("wp:extent")), None)
                    w = _emu_px(ext.get("cx")) if ext is not None else 0
                    h = _emu_px(ext.get("cy")) if ext is not None else 0
                    size = f' width="{w:.0f}" height="{h:.0f}"' if w and h else ""
                    out.append(f'<img src="{name}"{size}>')
        txt = "".join(out)
        if not txt:
            return ""
        f = run.font
        st = []
        if f.size:
            st.append(f"font-size:{f.size.pt:.1f}pt")
        if f.name:
            st.append(f"font-family:'{f.name}'")
        try:
            if f.color is not None and f.color.type is not None and f.color.rgb is not None:
                st.append(f"color:#{f.color.rgb}")
        except (AttributeError, ValueError):
            pass
        if f.highlight_color:
            st.append("background-color:#fff176")
        if run.bold:
            txt = f"<b>{txt}</b>"
        if run.italic:
            txt = f"<i>{txt}</i>"
        if run.underline:
            txt = f"<u>{txt}</u>"
        if f.strike:
            txt = f"<s>{txt}</s>"
        if f.superscript:
            txt = f"<sup>{txt}</sup>"
        if f.subscript:
            txt = f"<sub>{txt}</sub>"
        return f'<span style="{";".join(st)}">{txt}</span>' if st else txt

    def para_html(p, in_cell=False):
        body = "".join(run_html(r) for r in p.runs) or "&nbsp;"
        style = (p.style.name if p.style is not None else "") or ""
        css = []
        if p.alignment is not None and int(p.alignment) in ALIGN:
            css.append(f"text-align:{ALIGN[int(p.alignment)]}")
        pf = p.paragraph_format
        if pf.left_indent:
            css.append(f"margin-left:{pf.left_indent.pt:.0f}pt")
        if pf.first_line_indent:
            css.append(f"text-indent:{pf.first_line_indent.pt:.0f}pt")
        if pf.space_before is not None:
            css.append(f"margin-top:{pf.space_before.pt:.0f}pt")
        if pf.space_after is not None:
            css.append(f"margin-bottom:{pf.space_after.pt:.0f}pt")
        if pf.page_break_before:
            css.append("page-break-before:always")
        c = f' style="{";".join(css)}"' if css else ""
        low = style.lower()
        for lvl in range(1, 7):
            if low in (f"heading {lvl}", f"titre {lvl}"):
                return f"<h{lvl}{c}>{body}</h{lvl}>", None
        if low in ("title", "titre"):
            return f"<h1{c}>{body}</h1>", None
        numbered = p._p.pPr is not None and p._p.pPr.numPr is not None
        if numbered or "list" in low or "liste" in low:
            kind = "ol" if "number" in low or "numéro" in low else "ul"
            return f"<li{c}>{body}</li>", kind
        return f"<p{c}>{body}</p>", None

    def table_html(t):
        rows = []
        for row in t.rows:
            cells = []
            seen = set()
            for cell in row.cells:
                if id(cell._tc) in seen:
                    continue
                seen.add(id(cell._tc))
                span = cell._tc.grid_span if hasattr(cell._tc, "grid_span") else 1
                inner = "".join(para_html(p, True)[0] for p in cell.paragraphs)
                inner += "".join(table_html(x) for x in cell.tables)
                cs = f' colspan="{span}"' if span and span > 1 else ""
                cells.append(f'<td valign="top"{cs}>{inner}</td>')
            rows.append("<tr>" + "".join(cells) + "</tr>")
        return ('<table border="1" cellspacing="0" cellpadding="4" width="100%" '
                'style="border-collapse:collapse;border-color:#777">' + "".join(rows) + "</table>")

    parts, open_list = [], None
    for el in doc.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            h, kind = para_html(Paragraph(el, doc))
            if kind != open_list:
                if open_list:
                    parts.append(f"</{open_list}>")
                if kind:
                    parts.append(f"<{kind}>")
                open_list = kind
            parts.append(h)
        elif tag == "tbl":
            if open_list:
                parts.append(f"</{open_list}>")
                open_list = None
            parts.append(table_html(Table(el, doc)))
    if open_list:
        parts.append(f"</{open_list}>")
    return "".join(parts)


def _hf_text(part):
    try:
        if part is None or part.is_linked_to_previous and not part.paragraphs:
            return ""
        return " ".join(p.text for p in part.paragraphs if p.text.strip())
    except Exception:
        return ""


def builtin_to_pdf(src, dst):
    """Conversion intégrée : .docx (et .txt) -> PDF, sans LibreOffice ni Word."""
    from PySide6.QtCore import QMarginsF, QRectF, QSizeF, Qt, QUrl
    from PySide6.QtGui import (QColor, QFont, QImage, QPageLayout, QPageSize, QPainter, QPdfWriter,
                               QTextDocument)
    ext = os.path.splitext(src)[1].lower()
    page_w, page_h, margins = 210.0, 297.0, (20.0, 20.0, 20.0, 20.0)   # mm : gauche, haut, droite, bas
    header = footer = ""
    font = QFont("Calibri", 11)
    resources = {}
    if ext == ".txt":
        raw = open(src, "rb").read()
        for enc in ("utf-8", "cp1252", "latin-1"):
            try:
                text = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        body = "<pre style=\"white-space:pre-wrap\">" + _esc(text).replace("<br>", "\n") + "</pre>"
        font = QFont("DejaVu Sans Mono", 10)
    elif ext == ".docx":
        try:
            import docx
        except ImportError:
            raise ConversionError(NO_ENGINE)
        try:
            d = docx.Document(src)
        except Exception as e:
            raise ConversionError(f"Ce fichier Word ne peut pas être lu ({e}).")
        sec = d.sections[0] if d.sections else None
        if sec is not None and sec.page_width and sec.page_height:
            page_w, page_h = sec.page_width.mm, sec.page_height.mm
            margins = tuple((m.mm if m is not None else 20.0) for m in
                            (sec.left_margin, sec.top_margin, sec.right_margin, sec.bottom_margin))
            header, footer = _hf_text(sec.header), _hf_text(sec.footer)
        try:
            nf = d.styles["Normal"].font
            font = QFont(nf.name or "Calibri", int(nf.size.pt) if nf.size else 11)
        except KeyError:
            pass
        body = _docx_html(d, resources)
    else:
        raise ConversionError(NO_ENGINE)

    DPI = 96.0
    mm = DPI / 25.4
    writer = QPdfWriter(dst)
    writer.setResolution(int(DPI))
    writer.setPageLayout(QPageLayout(QPageSize(QSizeF(page_w, page_h), QPageSize.Millimeter),
                                     QPageLayout.Portrait if page_h >= page_w else QPageLayout.Landscape,
                                     QMarginsF(0, 0, 0, 0)))
    writer.setTitle(os.path.splitext(os.path.basename(src))[0])
    writer.setCreator("PDF DUO")
    ml, mt, mr, mb = (m * mm for m in margins)
    cw, ch = page_w * mm - ml - mr, page_h * mm - mt - mb
    doc = QTextDocument()
    doc.setDefaultFont(font)
    doc.setDocumentMargin(0)
    doc.setDefaultStyleSheet("h1{font-size:20pt} h2{font-size:16pt} h3{font-size:13pt} td p{margin:0}")
    for name, blob in resources.items():
        img = QImage.fromData(blob)
        if not img.isNull():
            if img.width() > cw:
                img = img.scaledToWidth(int(cw), Qt.SmoothTransformation)
            doc.addResource(QTextDocument.ImageResource, QUrl(name), img)
    doc.setHtml(f"<html><body>{body}</body></html>")
    doc.setPageSize(QSizeF(cw, ch))
    n = max(1, doc.pageCount())
    p = QPainter(writer)
    small = QFont(font.family(), 8)
    for i in range(n):
        if i:
            writer.newPage()
        p.save()
        p.translate(ml, mt - i * ch)
        doc.drawContents(p, QRectF(0, i * ch, cw, ch))
        p.restore()
        p.setFont(small)
        p.setPen(QColor("#555555"))
        if header:
            p.drawText(QRectF(ml, mt * 0.35, cw, mt * 0.5), Qt.AlignLeft | Qt.AlignVCenter, header)
        foot = (footer + "    " if footer else "") + f"{i + 1} / {n}"
        p.drawText(QRectF(ml, page_h * mm - mb * 0.8, cw, mb * 0.5), Qt.AlignRight | Qt.AlignVCenter, foot)
    p.end()
    return dst


# ---------------------------------------------------------------- conversions publiques
def office_to_pdf(src, dst=None):
    """Word / ODT / ... -> PDF : LibreOffice, sinon Microsoft Word, sinon conversion intégrée."""
    global LAST_ENGINE
    if not dst:
        dst = os.path.join(tempfile.mkdtemp(prefix="pdfduo-"), os.path.splitext(os.path.basename(src))[0] + ".pdf")
    errors = []
    if find_soffice():
        try:
            out = _soffice_convert(src, "pdf", tempfile.mkdtemp(prefix="pdfduo-"))
            shutil.move(out, dst)
            LAST_ENGINE = "libreoffice"
            return dst
        except ConversionError as e:
            errors.append(str(e))
    if find_word():
        try:
            _word_convert(src, dst, "pdf")
            LAST_ENGINE = "word"
            return dst
        except ConversionError as e:
            errors.append(str(e))
    if os.path.splitext(src)[1].lower() in (".docx", ".txt"):
        builtin_to_pdf(src, dst)
        LAST_ENGINE = "integree"
        return dst
    raise ConversionError(errors[-1] if errors else NO_ENGINE)


def _to_office(src, dst, fmt):
    """Conversion vers .docx / .odt : LibreOffice, sinon Microsoft Word."""
    global LAST_ENGINE
    if find_soffice():
        tmp = tempfile.mkdtemp(prefix="pdfduo-")
        out = _soffice_convert(src, {"docx": "docx:MS Word 2007 XML", "odt": "odt"}.get(fmt, fmt), tmp)
        shutil.move(out, dst)
        shutil.rmtree(tmp, ignore_errors=True)
        LAST_ENGINE = "libreoffice"
        return dst
    if find_word():
        _word_convert(src, dst, fmt)
        LAST_ENGINE = "word"
        return dst
    raise ConversionError("Pour créer un fichier ." + fmt + ", installez LibreOffice (gratuit : libreoffice.org)"
                          + (" ou Microsoft Word." if sys.platform.startswith("win") else "."))


def pdf_to_docx(pdf, dst):
    try:
        from pdf2docx import Converter
    except ImportError:
        raise ConversionError("Le module pdf2docx manque (pip install pdf2docx).")
    cv = Converter(pdf)
    try:
        cv.convert(dst)
    finally:
        cv.close()
    return dst


def pdf_to_odt(pdf, dst):
    tmp = tempfile.mkdtemp(prefix="pdfduo-")
    base = os.path.splitext(os.path.basename(dst))[0]
    docx = os.path.join(tmp, base + ".docx")
    pdf_to_docx(pdf, docx)
    try:
        _to_office(docx, dst, "odt")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return dst


def office_to_office(src, dst):
    """Word <-> ODT directement (.docx -> .odt ou .odt -> .docx)."""
    return _to_office(src, dst, os.path.splitext(dst)[1].lstrip(".").lower())
