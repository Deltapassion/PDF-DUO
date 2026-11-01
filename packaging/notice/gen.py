"""Génère la notice illustrée (HTML + PDF) dans les six langues.
Captures : img/<langue>/*.jpg (produites par caps.py). Sorties : docs/notice/ et pdfduo/notices/."""
import sys, os, html, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from texts import T
from figs import F
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.environ.get("PDFDUO_ROOT", os.path.join(HERE, "..", "..")))
APP = os.environ.get("PDFDUO_APP", ROOT + "/pdfduo")
DOCS = ROOT + "/docs"; OUT_WEB = DOCS + "/notice"; OUT_APP = APP + "/notices"
os.makedirs(OUT_WEB, exist_ok=True); os.makedirs(OUT_APP, exist_ok=True)
NAMES = dict(fr="Français", en="English", es="Español", pt="Português", de="Deutsch", it="Italiano")
VER = "1.0.0"
INTRO = dict(
 fr="PDF DUO sert à lire, remplir et signer des PDF, à dessiner des schémas électriques, pneumatiques et réseau, des GRAFCET et des plans de logement, et à convertir Word / ODF ↔ PDF. Il est pensé pour les élèves et les professeurs de lycée professionnel (MELEC, CIEL), et rend aussi service à la vie du lycée : affiches, formulaires d'adhésion et documents signés de la MDL. Les numéros rouges des captures renvoient aux listes placées dessous.",
 en="PDF DUO lets you read, fill in and sign PDFs, draw electrical, pneumatic and network diagrams, GRAFCETs and floor plans, and convert Word / ODF ↔ PDF. It is designed for vocational-school students and teachers, and is also handy for school life: posters, membership forms and signed documents for the student association. The red numbers on the screenshots refer to the lists below them.",
 es="PDF DUO sirve para leer, rellenar y firmar PDF, dibujar esquemas eléctricos, neumáticos y de red, GRAFCET y planos de vivienda, y convertir Word / ODF ↔ PDF. Está pensado para alumnos y profesores de formación profesional, y también es útil para la vida del centro: carteles, fichas de inscripción y documentos firmados de la asociación de alumnos. Los números rojos de las capturas remiten a las listas de debajo.",
 pt="O PDF DUO serve para ler, preencher e assinar PDF, desenhar esquemas elétricos, pneumáticos e de rede, GRAFCET e plantas de habitação, e converter Word / ODF ↔ PDF. Foi pensado para alunos e professores do ensino profissional, e também é útil para a vida da escola: cartazes, fichas de inscrição e documentos assinados da associação de estudantes. Os números vermelhos das capturas remetem para as listas abaixo.",
 de="PDF DUO dient zum Lesen, Ausfüllen und Unterschreiben von PDFs, zum Zeichnen von Schalt-, Pneumatik- und Netzwerkplänen, GRAFCETs und Grundrissen sowie zum Konvertieren Word / ODF ↔ PDF. Es ist für Schülerinnen, Schüler und Lehrkräfte an Berufsschulen gedacht und hilft auch im Schulleben: Plakate, Mitgliedsformulare und unterschriebene Dokumente der Schülervertretung. Die roten Nummern auf den Bildern verweisen auf die Listen darunter.",
 it="PDF DUO serve a leggere, compilare e firmare PDF, disegnare schemi elettrici, pneumatici e di rete, GRAFCET e piante di abitazioni, e convertire Word / ODF ↔ PDF. È pensato per studenti e docenti degli istituti professionali ed è utile anche per la vita della scuola: manifesti, moduli d'iscrizione e documenti firmati dell'associazione studentesca. I numeri rossi delle immagini rimandano agli elenchi sottostanti.")
CSS = """
body{font-family:'DejaVu Sans',Arial,sans-serif;color:#1d2733;font-size:10.5pt;line-height:1.5;margin:0 auto;max-width:900px;padding:0 16px}
header{display:flex;align-items:center;gap:16px;border-bottom:3px solid #1f6feb;padding:10px 0 12px;margin-bottom:12px}
header img{width:64px;height:64px}
h1{margin:0;font-size:24pt;color:#0d3b78}
.sub{color:#4a5a6a;margin-top:2px}
.ver{font-size:9pt;color:#6b7785}
.intro{background:#eef4fc;border-radius:8px;padding:10px 14px;margin:0 0 6px}
h2{color:#1f6feb;font-size:14pt;margin:20px 0 6px;border-left:5px solid #1f6feb;padding-left:8px;break-after:avoid}
p{margin:4px 0 6px}
code{background:#eef3fa;border-radius:3px;padding:0 3px;font-size:9.5pt}
figure{margin:10px 0 14px;break-inside:avoid}
figure .row{display:flex;gap:12px;align-items:flex-start}
figure .row img{flex:1;min-width:0}
figure img{width:100%;border:1px solid #c8d3df;border-radius:6px;display:block}
figcaption{font-size:9.5pt;color:#4a5a6a;font-style:italic;margin-top:4px;text-align:center}
ol.leg{list-style:none;padding:0;margin:6px 0 0;columns:2;column-gap:22px;font-size:9.5pt}
ol.leg li{display:flex;gap:8px;align-items:flex-start;margin:0 0 4px;break-inside:avoid}
ol.leg b{flex:none;background:#e53935;color:#fff;border-radius:50%;width:20px;height:20px;line-height:20px;text-align:center;font-size:9pt}
nav{font-size:9.5pt;margin:8px 0 10px}
nav a{color:#1f6feb;margin-right:10px;text-decoration:none}
footer{margin-top:20px;border-top:1px solid #c8d3df;padding-top:6px;font-size:8.5pt;color:#6b7785}
@media (max-width:640px){ol.leg{columns:1} figure .row{flex-direction:column}}
@media print{nav{display:none} body{max-width:none;padding:0}}
"""
def figure(lang, imgs, cap, leg, base):
    imgs = [imgs] if isinstance(imgs, str) else imgs
    W = {"06-reseau.jpg": 78, "08-signature.jpg": 62, "09-texte.jpg": 62, "10-conversions.jpg": 46, "05-grafcet.jpg": 88}
    one = len(imgs) == 1
    tags = "".join(f'<img src="{base}{lang}/{i}" alt="{html.escape(cap)}"' + (f' style="width:{W.get(i, 94)}%;margin:0 auto"' if one else '') + '>' for i in imgs)
    body = f'<div class="row">{tags}</div>' if len(imgs) > 1 else tags
    lg = ""
    if leg:
        lg = '<ol class="leg">' + "".join(f"<li><b>{n}</b><span>{html.escape(t)}</span></li>" for n, t in enumerate(leg, 1)) + "</ol>"
    return f"<figure>{body}<figcaption>{html.escape(cap)}</figcaption>{lg}</figure>"

def page(lang, base, icon):
    d = T[lang]; secs = []
    for i, (h, paras) in enumerate(d["sec"]):
        body = "".join(f"<p>{x}</p>" for x in paras)
        body += "".join(figure(lang, *f, base) for f in F[lang].get(i, []))
        secs.append(f"<section><h2>{html.escape(h)}</h2>{body}</section>")
    nav = "".join(f'<a href="notice-{l}.html">{NAMES[l]}</a>' for l in T) + f' · <a href="notice-{lang}.pdf">PDF</a> · <a href="../index.html">PDF DUO</a>'
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PDF DUO — {html.escape(d['title'])}</title><link rel="icon" href="../favicon.png"><style>{CSS}</style></head><body>
<nav>{nav}</nav>
<header><img src="{icon}" alt=""><div><h1>PDF DUO</h1><div class="sub">{html.escape(d['title'])} — {html.escape(d['sub'])}</div>
<div class="ver">Version {VER} · Jacques Branas, en collaboration avec Claude.ai</div></div></header>
<p class="intro">{INTRO[lang]}</p>
{''.join(secs)}
<footer>PDF DUO {VER} — GNU GPL v3 — deltapassion.github.io/PDF-DUO — ko-fi.com/djlatinjazz</footer></body></html>"""

# images pour le site
IMG = HERE + "/img"
if os.path.isdir(IMG):
    if os.path.exists(OUT_WEB + "/img"): shutil.rmtree(OUT_WEB + "/img")
    shutil.copytree(IMG, OUT_WEB + "/img")
else:
    IMG = OUT_WEB + "/img"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for lang in T:
        open(f"{OUT_WEB}/notice-{lang}.html", "w", encoding="utf-8").write(page(lang, "img/", "../icon.png"))
        tmp = f"{HERE}/_print-{lang}.html"
        open(tmp, "w", encoding="utf-8").write(page(lang, "file://" + IMG + "/", "file://" + DOCS + "/icon.png"))
        pg.goto("file://" + tmp); pg.wait_for_load_state("networkidle")
        pdf = pg.pdf(format="A4", print_background=True, display_header_footer=True, header_template="<span></span>",
                     footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#888">PDF DUO ' + VER + ' — <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                     margin=dict(top="13mm", bottom="15mm", left="13mm", right="13mm"))
        for o in (OUT_WEB, OUT_APP): open(f"{o}/notice-{lang}.pdf", "wb").write(pdf)
        os.remove(tmp); print(lang, len(pdf) // 1024, "Ko")
    b.close()

# ---------- notice unique avec choix de la langue (docs/notice/index.html)
FLAGS = dict(fr="🇫🇷", en="🇬🇧", es="🇪🇸", pt="🇵🇹", de="🇩🇪", it="🇮🇹")
DL = dict(fr="Télécharger le PDF", en="Download the PDF", es="Descargar el PDF", pt="Transferir o PDF", de="PDF herunterladen", it="Scarica il PDF")
BACK = dict(fr="Retour au site", en="Back to website", es="Volver al sitio", pt="Voltar ao site", de="Zurück zur Website", it="Torna al sito")
TOC = dict(fr="Sommaire", en="Contents", es="Índice", pt="Índice", de="Inhalt", it="Indice")
LBL = dict(fr="Langue", en="Language", es="Idioma", pt="Idioma", de="Sprache", it="Lingua")

def article(lang):
    d = T[lang]; secs = []; toc = []
    for i, (h, paras) in enumerate(d["sec"]):
        sid = f"{lang}-s{i+1}"
        body = "".join(f"<p>{x}</p>" for x in paras)
        body += "".join(figure(lang, *f, "img/") for f in F[lang].get(i, []))
        secs.append(f'<section id="{sid}"><h2>{html.escape(h)}</h2>{body}</section>')
        toc.append(f'<a href="#{sid}">{html.escape(h)}</a>')
    return (f'<article lang="{lang}" data-lang="{lang}" hidden>'
            f'<div class="head"><h1>{html.escape(d["title"])}</h1><div class="sub">{html.escape(d["sub"])}</div></div>'
            f'<p class="intro">{INTRO[lang]}</p>'
            f'<nav class="toc"><b>{TOC[lang]}</b>{"".join(toc)}</nav>'
            f'{"".join(secs)}</article>')

CSS2 = CSS.replace("max-width:900px;padding:0 16px", "max-width:none;padding:0;background:#f4f6f9") + """
.top{position:sticky;top:0;z-index:10;background:#0d3b78;color:#fff;box-shadow:0 2px 10px rgba(0,0,0,.18)}
.top{display:block;padding:0;margin:0;border:0} .top .in{flex:1;padding:8px clamp(12px,3vw,32px);display:flex;align-items:center;gap:12px}
.top a.brand{white-space:nowrap;display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:700;font-size:15pt;margin-right:auto}
.top a.brand img{width:34px;height:34px}
.top a.small{color:#cfe0f5;font-size:10pt;text-decoration:none;white-space:nowrap}
.top a.pdf{background:#fff;color:#0d3b78;border-radius:999px;padding:6px 12px;font-size:10pt;font-weight:700;text-decoration:none;white-space:nowrap}
.top select{font:inherit;font-size:11pt;border-radius:8px;border:0;padding:6px 8px;background:#fff;color:#0d3b78;font-weight:600;cursor:pointer}
main{max-width:920px;margin:18px auto 30px;background:#fff;border-radius:14px;padding:22px 28px;box-shadow:0 4px 20px rgba(13,59,120,.08)}
.head h1{font-size:24pt}
.toc{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:10pt;background:#f7f9fc;border:1px solid #e2e8f0;border-radius:8px;padding:10px 14px;margin:10px 0}
.toc b{width:100%;color:#0d3b78}
.toc a{color:#1f6feb;text-decoration:none}
section{scroll-margin-top:64px}
footer{max-width:920px;margin:0 auto 30px;padding:0 16px}
@media (max-width:640px){.top a.small{display:none} .top a.brand span{display:none} main{padding:16px;margin:10px 8px;border-radius:10px} .top a.pdf span{display:none}}
"""
opts = "".join(f'<option value="{l}">{FLAGS[l]} {NAMES[l]}</option>' for l in T)
JS = """
<script>
(function(){
  var L = %s, DL = %s, BACK = %s, LBL = %s;
  var sel = document.getElementById('lang'), pdf = document.getElementById('pdf'), back = document.getElementById('back');
  function pick(){
    var q = new URLSearchParams(location.search).get('lang'); if (L.indexOf(q) >= 0) return q;
    try { var s = localStorage.getItem('pdfduo-notice-lang'); if (L.indexOf(s) >= 0) return s; } catch(e) {}
    var n = (navigator.languages || [navigator.language || 'fr']);
    for (var i = 0; i < n.length; i++){ var c = String(n[i]).slice(0,2).toLowerCase(); if (L.indexOf(c) >= 0) return c; }
    return 'fr';
  }
  function show(l, keep){
    document.querySelectorAll('article').forEach(function(a){ a.hidden = a.dataset.lang !== l; });
    document.documentElement.lang = l; sel.value = l;
    pdf.href = 'notice-' + l + '.pdf'; pdf.querySelector('span').textContent = DL[l];
    back.textContent = BACK[l]; sel.setAttribute('aria-label', LBL[l]);
    document.title = 'PDF DUO — ' + document.querySelector('article[data-lang="'+l+'"] h1').textContent;
    try { localStorage.setItem('pdfduo-notice-lang', l); } catch(e) {}
    if (!keep){ var u = new URL(location.href); u.searchParams.set('lang', l); u.hash = ''; history.replaceState(null, '', u); window.scrollTo(0, 0); }
  }
  sel.addEventListener('change', function(){ show(sel.value); });
  var h = location.hash.match(/^#(\\w\\w)-s\\d+/);
  show(h && L.indexOf(h[1]) >= 0 ? h[1] : pick(), true);
})();
</script>
""" % tuple(__import__("json").dumps(x, ensure_ascii=False) for x in (list(T), DL, BACK, LBL))
index = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PDF DUO — Notice</title><meta name="description" content="Notice illustrée de PDF DUO en six langues.">
<link rel="icon" href="../favicon.png"><style>{CSS2}</style></head><body>
<header class="top"><div class="in">
  <a class="brand" href="../index.html"><img src="../icon.png" alt="">PDF DUO <span style="font-weight:400;font-size:10pt;opacity:.75">{VER}</span></a>
  <a class="small" id="back" href="../index.html">Retour au site</a>
  <a class="pdf" id="pdf" href="notice-fr.pdf" download>⬇ <span>Télécharger le PDF</span></a>
  <select id="lang" aria-label="Langue">{opts}</select>
</div></header>
<main>{''.join(article(l) for l in T)}</main>
<footer>PDF DUO {VER} — Jacques Branas, en collaboration avec Claude.ai — GNU GPL v3 — <a href="https://ko-fi.com/djlatinjazz">ko-fi.com/djlatinjazz</a></footer>
{JS}
<script data-goatcounter="https://deltapassion.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body></html>"""
open(OUT_WEB + "/index.html", "w", encoding="utf-8").write(index)
# les anciennes pages par langue redirigent vers la notice unique
for l in T:
    open(f"{OUT_WEB}/notice-{l}.html", "w", encoding="utf-8").write(
        f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html?lang={l}">'
        f'<link rel="canonical" href="index.html?lang={l}"><a href="index.html?lang={l}">PDF DUO</a>')
print("index.html ok")
