"""Icônes des outils (SVG 24 × 24, trait de la couleur du thème)."""
from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

P = {
    "select": '<path d="M5 3 L5 19 L9.5 14.5 L12.5 21 L15 20 L12 13.5 L18 13.5 Z"/>',
    "pan": '<path d="M12 3 V21 M3 12 H21 M12 3 L9.5 5.5 M12 3 L14.5 5.5 M12 21 L9.5 18.5 M12 21 L14.5 18.5 '
           'M3 12 L5.5 9.5 M3 12 L5.5 14.5 M21 12 L18.5 9.5 M21 12 L18.5 14.5"/>',
    "text": '<path d="M5 5 H19 M12 5 V20 M9 20 H15"/>',
    "line": '<path d="M4 20 L20 4"/>',
    "arrow": '<path d="M4 20 L19 5 M11 5 H19 V13"/>',
    "wire": '<path d="M3 17 H10 V7 H21"/><circle cx="3" cy="17" r="1.6" fill="CC"/><circle cx="21" cy="7" r="1.6" fill="CC"/>',
    "link": '<rect x="2" y="9" width="5" height="6" rx="1"/><rect x="17" y="9" width="5" height="6" rx="1"/>'
            '<path d="M7 12 H10 V6 H14 V12 H17" stroke-dasharray="0"/>',
    "rect": '<rect x="4" y="6" width="16" height="12" rx="1.5"/>',
    "ellipse": '<ellipse cx="12" cy="12" rx="8.5" ry="6.5"/>',
    "freehand": '<path d="M3 17 C6 8, 9 8, 10 13 S15 19, 17 11 S20 6, 21 8"/>',
    "highlight": '<path d="M14 4 L20 10 L11 19 L5 19 L5 13 Z M5 19 L3 21" /><path d="M3 22 H21" stroke-width="3" opacity=".5"/>',
    "wall": '<path d="M3 5 H21 V19 H3 Z" stroke-width="1"/><path d="M3 5 H21 V19 H3 Z" stroke-width="4" opacity=".55"/>',
    "dim": '<path d="M3 12 H21 M3 8 V16 M21 8 V16 M5 10 L7 14 M17 10 L19 14"/>',
    "capture": '<path d="M3 8 V3 H8 M16 3 H21 V8 M21 16 V21 H16 M8 21 H3 V16"/><circle cx="12" cy="12" r="3.5"/>',
    "field_text": '<rect x="3" y="7" width="18" height="10" rx="1.5"/><path d="M7 10 V14"/>',
    "field_check": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 12 L11 15 L16 9"/>',
    "field_combo": '<rect x="3" y="7" width="18" height="10" rx="1.5"/><path d="M14 11 L16 13 L18 11 M14 7 V17"/>',
    "field_radio": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.5" fill="CC"/>',
    "field_sig": '<rect x="3" y="6" width="18" height="12" rx="1.5"/><path d="M6 15 C8 10, 9 10, 10 13 S13 14, 14 12 L18 12"/>',
    "field_link": '<path d="M10 14 L14 10 M8.5 11.5 L6.5 13.5 A3 3 0 0 0 10.5 17.5 L12.5 15.5 M15.5 12.5 L17.5 10.5 '
                  'A3 3 0 0 0 13.5 6.5 L11.5 8.5"/>',
    "door": '<path d="M3 20 H21" stroke-width="2.6" opacity=".55"/><path d="M6 20 V5" stroke-width="2.2"/><path d="M6 5 A15 15 0 0 1 21 20" stroke-width="1"/>',
    "door2": '<path d="M2 20 H22" stroke-width="2.6" opacity=".55"/><path d="M3 20 V11 M21 20 V11" stroke-width="2"/>'
             '<path d="M3 11 A9 9 0 0 1 12 20 M21 11 A9 9 0 0 0 12 20" stroke-width="1"/>',
    "window": '<path d="M2 16 H22 M2 20 H22" stroke-width="1.2"/><path d="M2 16 V20 M22 16 V20"/>'
              '<path d="M2 16 A10 10 0 0 1 12 6 A10 10 0 0 1 22 16" stroke-dasharray="2 2" stroke-width="1"/>',
    "open": '<path d="M3 7 V19 H19 L22 10 H7 L4 19 M3 7 H9 L11 9 H18 V10"/>',
    "save": '<path d="M4 4 H17 L20 7 V20 H4 Z M8 4 V9 H15 V4 M7 20 V14 H17 V20"/>',
    "print": '<path d="M7 9 V3 H17 V9 M5 17 H3 V9 H21 V17 H19 M7 14 H17 V21 H7 Z"/>',
    "undo": '<path d="M9 14 L4 9 L9 4 M4 9 H14 A6 6 0 0 1 14 21 H9"/>',
    "redo": '<path d="M15 14 L20 9 L15 4 M20 9 H10 A6 6 0 0 0 10 21 H15"/>',
    "zoom_in": '<circle cx="10" cy="10" r="6.5"/><path d="M15 15 L21 21 M7 10 H13 M10 7 V13"/>',
    "zoom_out": '<circle cx="10" cy="10" r="6.5"/><path d="M15 15 L21 21 M7 10 H13"/>',
    "zoom_page": '<rect x="6" y="3" width="12" height="18" rx="1"/><path d="M9 8 H15 M9 12 H15 M9 16 H13"/>',
    "zoom_width": '<path d="M3 12 H21 M3 12 L6 9 M3 12 L6 15 M21 12 L18 9 M21 12 L18 15 M3 5 V19 M21 5 V19"/>',
    "flying": '<path d="M5 18 C8 6, 14 20, 19 6" stroke-width="1.7"/><rect x="2" y="17" width="5" height="4" rx="1" fill="CC"/><rect x="17" y="3" width="5" height="4" rx="1" fill="CC"/>',
    "signature": '<path d="M3 17 C5 10, 7 9, 8 13 S11 16, 12 13 S15 9, 16 12 L21 12 M3 21 H21"/>',
    "bold": '<path d="M7 4 H13 A4 4 0 0 1 13 12 H7 Z M7 12 H14 A4 4 0 0 1 14 20 H7 Z" stroke-width="2.4"/>',
    "italic": '<path d="M10 4 H18 M6 20 H14 M14 4 L10 20"/>',
    "underline": '<path d="M7 4 V11 A5 5 0 0 0 17 11 V4 M5 21 H19"/>',
    "align_left": '<path d="M4 6 H20 M4 10 H14 M4 14 H20 M4 18 H12"/>',
    "align_center": '<path d="M4 6 H20 M7 10 H17 M4 14 H20 M8 18 H16"/>',
    "align_right": '<path d="M4 6 H20 M10 10 H20 M4 14 H20 M12 18 H20"/>',
}


def icon(name, color="#333333", size=24):
    body = P.get(name)
    if body is None:
        return QIcon()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">'
           f'<g fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
           f'{body.replace("CC", color)}</g></svg>')
    r = QSvgRenderer(QByteArray(svg.encode()))
    ic = QIcon()
    for s in (size, size * 2):
        pm = QPixmap(s, s)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        r.render(p, QRectF(0, 0, s, s))
        p.end()
        ic.addPixmap(pm)
    return ic
