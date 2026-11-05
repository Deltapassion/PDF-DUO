import sys, os
sys.path.insert(0, '/home/claude/pdfduo')
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
import faulthandler; faulthandler.dump_traceback_later(500, exit=True)
LANG = sys.argv[1]
from PySide6.QtWidgets import QApplication, QDockWidget, QToolBar, QWidget
from PySide6.QtCore import QPoint, QRect, QRectF, QPointF, Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QImage, QIcon
app = QApplication([])
app.setWindowIcon(QIcon('/home/claude/pdfduo/pdfduo/icon.png'))
from PySide6.QtCore import QSettings
QSettings("Jacques Branas", "PDF DUO").clear()
from pdfduo import i18n; i18n.set_language(LANG)
import pdfduo.app as A
A.MainWindow.maybe_save = lambda self: True
A.install_qt_translator(app)
from pdfduo.items import MM
OUT = f'/tmp/claude-0/notice/img/{LANG}/'; os.makedirs(OUT, exist_ok=True)
EX = '/home/claude/pdfduo/'
RED = QColor('#e53935')

def pump(n=3):
    for _ in range(n): app.processEvents()

def win(pdf=None, theme='clair', cat=None, size=(1680, 980)):
    w = A.MainWindow(); w.resize(*size); w.show(); pump()
    w.set_theme(theme); w.set_accent('#1f6feb')
    if pdf: w._open_pdf(pdf, pdf)
    if cat: w.cat_combo.setCurrentText(i18n.T(cat))
    pump(); w.zoom_page(); pump(); w.render_visible(); pump()
    return w

def rect_of(w, widget, pad=2):
    p = widget.mapTo(w, QPoint(0, 0))
    return QRect(p.x() - pad, p.y() - pad, widget.width() + 2 * pad, widget.height() + 2 * pad)

def dock(w, name): return w.findChild(QDockWidget, name)
def bar(w, name): return w.findChild(QToolBar, name)

def callouts(img, marks):
    p = QPainter(img); p.setRenderHint(QPainter.Antialiasing)
    for r, n in marks:
        r = r.intersected(QRect(2, 2, img.width() - 4, img.height() - 4))
        p.setPen(QPen(RED, 3)); p.setBrush(Qt.NoBrush); p.drawRoundedRect(r, 6, 6)
        R = 15; cx = min(max(r.left() + R + 2, R + 2), img.width() - R - 2); cy = min(max(r.top() - 4, R + 2), img.height() - R - 2)
        cx, cy = r.left() + R - 2, r.top() + R - 2
        p.setPen(QPen(QColor('white'), 2)); p.setBrush(RED); p.drawEllipse(QPointF(cx, cy), R, R)
        f = QFont('DejaVu Sans', 12); f.setBold(True); p.setFont(f); p.setPen(QColor('white'))
        p.drawText(QRectF(cx - R, cy - R, 2 * R, 2 * R), Qt.AlignCenter, str(n))
    p.end(); return img

def save(img, name):
    if isinstance(img, QImage): img.save(OUT + name, quality=86)
    else: img.toImage().save(OUT + name, quality=86)

# 1 — l'écran
w = win(EX + 'exemple-inversion.pdf', cat='Électricité – triphasé / puissance')
img = w.grab().toImage()
mb = w.menuBar(); qb = w.quick_bar
marks = [(rect_of(w, qb), 1)]
acts = mb.actions(); g0 = mb.actionGeometry(acts[0]); g1 = mb.actionGeometry(acts[-1])
pm = mb.mapTo(w, QPoint(0, 0)); marks.append((QRect(pm.x() + g0.left() - 2, pm.y(), g1.right() - g0.left() + 4, mb.height()), 2))
marks.append((rect_of(w, bar(w, 'outils')), 3))
st = bar(w, 'style'); et = bar(w, 'ecriture')
if st and st.isVisible(): marks.append((rect_of(w, st), 4))
if et and et.isVisible(): marks.append((rect_of(w, et), 5))
marks.append((rect_of(w, dock(w, 'biblio')), 6))
marks.append((rect_of(w, dock(w, 'props')), 7))
pgd = dock(w, 'pages')
if pgd and pgd.isVisible(): marks.append((rect_of(w, pgd), 8))
marks.append((rect_of(w, w.view, -4), 9))
save(callouts(img, marks), '01-ecran.jpg')

# 2 — un symbole sélectionné, zoomé
sym = [i for i in w.items() if i.typ == 'symbol' and i.d.get('label', '').startswith('KM')]
it = sym[0] if sym else [i for i in w.items() if i.typ == 'symbol'][0]
w.scene.clearSelection(); it.setSelected(True); pump()
w.view.set_zoom(2.6); w.view.centerOn(it); pump(); w.render_visible(); pump()
img = w.grab().toImage()
r = it.sceneBoundingRect(); tl = w.view.mapFromScene(r.topLeft()); br = w.view.mapFromScene(r.bottomRight())
vp = w.view.viewport().mapTo(w, QPoint(0, 0))
callouts(img, [(QRect(vp + tl, vp + br).adjusted(-12, -12, 12, 12), 1), (rect_of(w, dock(w, 'props')), 2),
               (rect_of(w, w.cat_combo, 3), 3)])
save(img, '02-symbole.jpg'); w.close()

# 3 — fils et liaisons (exemple avec couleurs de conducteurs)
w = win(EX + 'exemple.pdf', cat='Électricité – domestique (schéma développé)')
w.view.set_zoom(1.9)
wires = [i for i in w.items() if i.typ == 'wire']
if wires:
    c = wires[len(wires) // 2]; w.view.centerOn(c)
pump(); w.render_visible(); pump()
img = w.grab().toImage()
tb = bar(w, 'outils')
ma = []
for k in ('wire', 'link'):
    a = w.tool_actions.get(k); bw = tb.widgetForAction(a) if a else None
    if bw: ma.append(rect_of(w, bw, 1))
marks = []
if ma: marks.append((ma[0].united(ma[-1]), 1))
marks.append((rect_of(w, w.cond_combo, 3), 2))
save(callouts(img, marks), '03-fils.jpg')

# 4 — plan à l'échelle
w.zoom_page(); pump()
walls = [i for i in w.items() if i.typ == 'wall']
if walls:
    w.view.set_zoom(1.5); w.view.centerOn(walls[0]); pump(); w.render_visible(); pump()
img = w.grab().toImage()
marks = []
def wfa(a):
    for b in w.findChildren(QToolBar):
        x = b.widgetForAction(a)
        if x and x.isVisible(): return x
pl = [wfa(w.tool_actions[k]) for k in ('wall', 'dim', 'door', 'door2', 'window') if k in w.tool_actions]
pl = [x for x in pl if x]
if pl:
    r0 = rect_of(w, pl[0], 1)
    for x in pl[1:]: r0 = r0.united(rect_of(w, x, 1))
    marks.append((r0, 1))
if w.scale_combo.isVisible() and w.scale_combo.mapTo(w, QPoint(0,0)).x() < w.width() - 40:
    marks.append((rect_of(w, w.scale_combo, 3), 2))
print('plan marks', len(marks))
save(callouts(img, marks), '04-plan.jpg'); w.close()

# 5 — GRAFCET
w = win(EX + 'exemple-grafcet.pdf', theme='sombre', cat='GRAFCET')
steps = [i for i in w.items() if i.typ == 'node' and i.d.get('shape') in ('step', 'step_init', 'transition', 'action')]
from functools import reduce
br = reduce(lambda a, b: a.united(b), [i.sceneBoundingRect() for i in steps])
w.view.fitInView(br.adjusted(-30, -30, 30, 30), Qt.KeepAspectRatio); pump(); w.render_visible(); pump()
img = w.grab().toImage()
save(callouts(img, [(rect_of(w, dock(w, 'biblio')), 1)]), '05-grafcet.jpg'); w.close()

# 6 — réseau CIEL
w = win(EX + 'exemple-reseau.pdf', theme='bleu nuit', cat='Réseau informatique')
save(w.grab(), '06-reseau.jpg'); w.close()

# 7 — formulaire
w = win(None)
w.new_doc((595.28, 841.89), 1, ask=False); pump()
T = i18n.T
w.add_item({'type': 'text', 'x': 25 * MM, 'y': 20 * MM, 'text': T('Formulaire et signature'), 'size': 16, 'bold': True})
for i, (lab, typ) in enumerate([(T('Champ texte'), 'field_text'), (T('Case à cocher'), 'field_check'), (T('Zone signature'), 'field_sig')]):
    y = (38 + i * 16) * MM
    w.add_item({'type': 'text', 'x': 25 * MM, 'y': y, 'text': lab, 'size': 11})
    d = {'type': typ, 'x': 75 * MM, 'y': y - 2 * MM, 'w': 60 * MM, 'h': 8 * MM, 'name': f'f{i}', 'value': ''}
    if typ == 'field_text': d['value'] = 'Jacques Branas'
    if typ == 'field_check': d.update(w=6 * MM, h=6 * MM, value=True)
    if typ == 'field_sig': d.update(h=14 * MM)
    w.add_item(d)
w.commit(); w.refresh_forms() if hasattr(w, 'refresh_forms') else None
w.view.set_zoom(1.6); w.view.centerOn(QPointF(80 * MM, 55 * MM)); pump(); w.render_visible(); pump()
img = w.grab().toImage()
ft = bar(w, 'formulaire')
marks = [(rect_of(w, ft), 1)]
fd = dock(w, 'forms')
if fd:
    fd.show(); fd.raise_(); pump(); img = w.grab().toImage()
if fd and fd.isVisible(): marks.append((rect_of(w, fd), 2))
save(callouts(img, marks), '07-formulaire.jpg')

# 8 — fenêtre signature
from pdfduo.signature import SignatureDialog
sd = SignatureDialog(w); sd.show(); pump()
cv = sd.canvas
try:
    from PySide6.QtGui import QPainterPath
    import math
    pts = [QPointF(20 + t * 3, 60 + 25 * math.sin(t / 6) * math.exp(-t / 120)) for t in range(0, 110)]
    path = QPainterPath(QPointF(40, 120))
    import random
    xs = [40, 70, 95, 120, 150, 175, 200, 235, 260, 300, 330, 360, 400, 430]
    for k, x in enumerate(xs[1:]):
        path.quadTo(QPointF(x - 15, 60 + (k % 3) * 35), QPointF(x, 125 - (k % 2) * 45))
    path.moveTo(60, 150); path.cubicTo(QPointF(200, 135), QPointF(320, 160), QPointF(450, 140))
    cv.paths.append(path); cv.update()
except Exception as e:
    print('sig', e)
pump(); save(sd.grab(), '08-signature.jpg'); sd.close()

# 9 — texte et caractères spéciaux
td = A.TextDialog(w, T('Texte'), T('Texte :'), 'U = √{230² + 12,5²}  Ω  φ  π')
td.show(); pump(); save(td.grab(), '09-texte.jpg'); td.close()

# 10 — menu conversions
m = [a.menu() for a in w.menuBar().actions() if a.menu() and 'onvers' in a.text() or (a.menu() and a.text() in ('&Konvertierung', '&Conversiones', '&Conversões', '&Conversioni'))]
mm = None
for a in w.menuBar().actions():
    if a.menu() and a.menu().actions() and any('PDF' in x.text() and '→' in x.text() for x in a.menu().actions()):
        mm = a.menu(); break
if mm:
    mm.popup(w.mapToGlobal(QPoint(300, 30))); pump(5); save(mm.grab(), '10-conversions.jpg'); mm.hide()
# 11 — menu aide
ha = w.menuBar().actions()[-1].menu()
ha.popup(w.mapToGlobal(QPoint(600, 30))); pump(5); save(ha.grab(), '11-aide.jpg'); ha.hide()


# 13-14 — mode présentation (plein écran)
w = win(EX + 'exemple-grafcet.pdf', theme='bleu nuit', cat='GRAFCET')
w.toggle_presentation(True)
pump(5)
w._pres_timer.stop()
w.showNormal(); w.resize(1680, 980); pump(5)
w.menuBar().hide()
for b in w.findChildren(QToolBar):
    if b.objectName() != "outils":
        b.hide()
for d in w.findChildren(QDockWidget):
    if d.objectName() != "biblio":
        d.hide()
w.resizeDocks([dock(w, 'biblio')], [2 * w.sym_list.gridSize().width() + 34], Qt.Horizontal)
w.statusBar().hide(); pump(5)
w.zoom_page(); pump(3); w.render_visible(); pump(3)
hint = getattr(w, "_pres_hint", None)
if hint:
    hint.setFixedWidth(760); hint.adjustSize(); hint.move((w.width() - hint.width()) // 2, 40); hint.show(); hint.raise_()
pump(3)
img = w.grab().toImage()
save(callouts(img, [(rect_of(w, bar(w, 'outils')), 1), (rect_of(w, dock(w, 'biblio')), 2)]), '13-plein-ecran.jpg')
if hint: hint.hide()
w.menuBar().show()
for b in w._pres_bars: b.show()
pump(5); w.render_visible(); pump(3)
img = w.grab().toImage()
save(callouts(img, [(rect_of(w, w.menuBar(), 1), 1)]), '14-plein-ecran-menu.jpg')
w.close()


# 15 — solaire
w = win(EX + 'exemple-solaire.pdf', theme='bleu nuit', cat='Énergie solaire – schéma technologique')
img = w.grab().toImage()
save(callouts(img, [(rect_of(w, dock(w, 'biblio')), 1)]), '15-solaire.jpg'); w.close()
# 16 — organigramme
w = win(None, theme='bleu nuit', cat='Organigramme')
w.new_doc((595.28, 841.89), 1, ask=False); pump()
w.insert_orgchart(); pump(); w.view.set_zoom(1.15); w.view.centerOn(QPointF(105 * MM, 80 * MM)); pump(); w.render_visible(); pump()
save(w.grab(), '16-organigramme.jpg'); w.close()

# 17/18 — tableau avec calculs
TBL = {"fr": ("Matériel", "Qté", "Prix unitaire (€)", "Total (€)", "Câble 2,5 mm²", "Disjoncteur 16 A", "Prise 2P+T", "TOTAL"),
       "en": ("Item", "Qty", "Unit price (€)", "Total (€)", "2.5 mm² cable", "16 A breaker", "Socket outlet", "TOTAL"),
       "es": ("Material", "Cant.", "Precio unitario (€)", "Total (€)", "Cable 2,5 mm²", "Magnetotérmico 16 A", "Enchufe", "TOTAL"),
       "pt": ("Material", "Qtd.", "Preço unitário (€)", "Total (€)", "Cabo 2,5 mm²", "Disjuntor 16 A", "Tomada", "TOTAL"),
       "de": ("Material", "Menge", "Einzelpreis (€)", "Summe (€)", "Kabel 2,5 mm²", "LS-Schalter 16 A", "Steckdose", "GESAMT"),
       "it": ("Materiale", "Q.tà", "Prezzo unitario (€)", "Totale (€)", "Cavo 2,5 mm²", "Interruttore 16 A", "Presa", "TOTALE")}[LANG]
from pdfduo.table import new_table, TableDialog
w = win(None, theme='bleu nuit')
w.new_doc((595.28, 841.89), 1, ask=False); pump()
pg = w.page_items[0]; x0, y0 = pg.pos().x(), pg.pos().y()
d = new_table(5, 4, x0 + 20 * MM, y0 + 25 * MM, 170 * MM, 42 * MM)
sm = "SOMME" if LANG == "fr" else "SUM"
d["cells"] = {"0,0": TBL[0], "0,1": TBL[1], "0,2": TBL[2], "0,3": TBL[3],
              "1,0": TBL[4], "1,1": "25", "1,2": "0,85" if LANG != "en" else "0.85", "1,3": "=B2*C2",
              "2,0": TBL[5], "2,1": "4", "2,2": "8,90" if LANG != "en" else "8.90", "2,3": "=B3 x C3",
              "3,0": TBL[6], "3,1": "6", "3,2": "4,20" if LANG != "en" else "4.20", "3,3": "=B4*C4",
              "4,0": TBL[7], "4,3": f"={sm}(D2:D4)"}
d["spans"] = {"4,0": [1, 3]}
d["colw"] = [1.6, 0.6, 1.0, 1.0]
t = w.add_item(d); t.setSelected(True); w.commit(); pump()
w.view.set_zoom(1.2); w.view.centerOn(QPointF(x0 + 105 * MM, y0 + 50 * MM)); pump(); w.render_visible(); pump()
img = w.grab().toImage()
tm = [a for a in w.menuBar().actions() if a.text() == i18n.T("&Tableau")]
marks = [(rect_of(w, dock(w, 'props')), 2)] if dock(w, 'props') else []
if tm:
    g = w.menuBar().actionGeometry(tm[0]); p0 = w.menuBar().mapTo(w, QPoint(0, 0))
    marks.insert(0, (QRect(p0.x() + g.x() - 2, p0.y() + g.y() - 2, g.width() + 4, g.height() + 4), 1))
save(callouts(img, marks), '17-tableau.jpg')
dlg = TableDialog(t.d, w); dlg.resize(980, 520); dlg.show(); dlg.tw.setCurrentCell(4, 3); pump(5)
save(dlg.grab(), '18-tableau-edition.jpg'); dlg.close()
# 19 — calculatrice graphique
from pdfduo.calculator import CalculatorDialog
from PySide6.QtWidgets import QTabWidget
c = CalculatorDialog(w); c.resize(900, 560); c.show(); pump()
c.disp.setText("(2+3)×√(16)"); c.equals(); c.disp.setText("sin(30)"); c.equals()
c.fx[2].setText("3sin(x)"); c.replot(); c.auto_y()
save(c.grab(), '19-calculatrice.jpg')
c.findChild(QTabWidget).setCurrentIndex(1); pump(5)
save(c.grab(), '20-graphique.jpg'); c.close(); w.close()
# 21 — prévention électrique, manutention, outils
w = win(None, theme='bleu nuit', cat='Prévention électrique – EPI, EIS, ECS')
w.new_doc((841.89, 595.28), 1, ask=False); pump()
pg = w.page_items[0]; x0, y0 = pg.pos().x(), pg.pos().y()
ids = ["epi_casque", "epi_gants", "epi_vetement", "epi_chaussures", "eis_tapis", "eis_cadenas", "eis_vat", "eis_macaron",
       "ecs_barriere", "ecs_pancarte", "ecs_malt", "sig_danger_elec", "emb_haut", "emb_fragile", "ghs_inflammable", "log_chariot",
       "dent_partielle", "oel_pince_denuder", "haut_echafaudage", "oinf_pince_rj45"]
for k, sid in enumerate(ids):
    dd = w.symbol_dict(sid); dd.update(x=x0 + (18 + (k % 5) * 52) * MM, y=y0 + (18 + (k // 5) * 44) * MM, scale=2.2)
    w.add_item(dd)
w.commit(); pump(); w.zoom_page(); pump(); w.render_visible(); pump()
img = w.grab().toImage()
save(callouts(img, [(rect_of(w, dock(w, 'biblio')), 1)]), '21-prevention.jpg'); w.close()

# 22 — favoris
QSettings("Jacques Branas", "PDF DUO").setValue("favoris", ["gqs_pls", "gqs_massage", "ind_barriere", "rob_uno", "rob_led", "inc_exit", "hab_gtl", "contact_no", "node:g_step"])
w = win(None, theme='bleu nuit')
w.cat_combo.setCurrentIndex(1); pump()
img = w.grab().toImage()
save(callouts(img, [(rect_of(w, w.cat_combo), 1), (rect_of(w, w.sym_list), 2)]), '22-favoris.jpg'); w.close()
QSettings("Jacques Branas", "PDF DUO").remove("favoris")
# 23 — équipements à états (pompage)
w = win(None, theme='bleu nuit', cat='Équipements industriels – électrotechnique')
w.new_doc((841.89, 595.28), 1, ask=False); pump()
pg = w.page_items[0]; x0, y0 = pg.pos().x(), pg.pos().y()
dd = w.symbol_dict("ind_pompage"); dd.update(x=x0 + 20 * MM, y=y0 + 30 * MM, scale=3.2); dd["label"] = ""
dd["params"].update({"puits": "Haut", "reservoir": "Bas", "pompe": "En marche"})
it = w.add_item(dd); w.commit(); it.setSelected(True); pump(); w.zoom_page(); pump(); w.render_visible(); pump()
img = w.grab().toImage()
save(callouts(img, [(rect_of(w, dock(w, 'props')), 1)]), '23-etats.jpg'); w.close()

# 24-25 — correcteur orthographique
from pdfduo import spell as _sp
_sp.configure(enabled=True, lang="auto")
PH = {"fr": "Le disjonteur protège l'installtion électrique.", "en": "The circuit braker protects the electrical instalation.",
      "es": "El interuptor protege la instalasión eléctrica.", "pt": "O disjuntor proteje a instalação elétrica.",
      "de": "Der Schalter schüzt die elektrische Anlage.", "it": "L'interuttore protegge l'impianto eletrico."}[LANG]
w = win(None, theme='bleu nuit')
td = A.TextDialog(w, i18n.T("Texte"), i18n.T("Saisissez le texte :"), PH)
td.show(); pump(5); save(td.grab(), '24-orthographe.jpg')
from PySide6.QtGui import QContextMenuEvent
import re as _re
mis = _sp.misspelled(PH)
if mis:
    start = mis[0][0] + 2
    cur = td.edit.textCursor(); cur.setPosition(start); r = td.edit.cursorRect(cur)
    def _grab_menu():
        from PySide6.QtWidgets import QMenu
        for m in app.topLevelWidgets():
            if isinstance(m, QMenu) and m.isVisible():
                pump(2); save(m.grab(), '25-orthographe-menu.jpg'); m.close(); return
    QTimer.singleShot(400, _grab_menu)
    pt = r.center()
    td.edit.contextMenuEvent(QContextMenuEvent(QContextMenuEvent.Mouse, pt, td.edit.viewport().mapToGlobal(pt)))
td.close(); w.close()

# 12 — don
def grab_dlg():
    from PySide6.QtWidgets import QDialog
    for d in app.topLevelWidgets():
        if isinstance(d, QDialog) and d.isVisible() and d is not w:
            pump(); save(d.grab(), '12-don.jpg'); d.reject(); return
QTimer.singleShot(400, grab_dlg)
w.donate()
print(LANG, 'ok', sorted(os.listdir(OUT)))
os._exit(0)
