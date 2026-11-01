import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
import faulthandler; faulthandler.dump_traceback_later(150, exit=True)
LANG = sys.argv[1]
from PySide6.QtWidgets import QApplication, QDockWidget, QToolBar, QWidget
from PySide6.QtCore import QPoint, QRect, QRectF, QPointF, Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QImage, QIcon
app = QApplication([])
app.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'pdfduo', 'icon.png')))
from pdfduo import i18n; i18n.set_language(LANG)
import pdfduo.app as A
A.install_qt_translator(app)
from pdfduo.items import MM
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', LANG) + '/'; os.makedirs(OUT, exist_ok=True)
EX = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'exemples') + '/'
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
    b.hide()
for d in w.findChildren(QDockWidget):
    d.hide()
w.statusBar().hide(); pump(5)
w.zoom_page(); pump(3); w.render_visible(); pump(3)
hint = getattr(w, "_pres_hint", None)
if hint:
    hint.setFixedWidth(760); hint.adjustSize(); hint.move((w.width() - hint.width()) // 2, 40); hint.show(); hint.raise_()
pump(3)
save(w.grab(), '13-plein-ecran.jpg')
if hint: hint.hide()
w.menuBar().show()
for b in w._pres_bars: b.show()
pump(5); w.render_visible(); pump(3)
img = w.grab().toImage()
save(callouts(img, [(rect_of(w, w.menuBar(), 1), 1)]), '14-plein-ecran-menu.jpg')
w.close()

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
