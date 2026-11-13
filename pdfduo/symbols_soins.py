"""Bibliothèque 1.3.2 : soins infirmiers (bandages, matériel médical de base, trousse de secours).
Dessins originaux (aucun logo de marque)."""
from .symbols import add, t

INF = "Soins infirmiers – matériel de soins"

_O = 'stroke="CC" stroke-width="1.2"'          # contour
_G = "#2e8b57"                                 # vert secours
_R = "#e53935"


def _cross(cx, cy, s, col=_G):
    a = s / 3
    return (f'<path d="M{cx - a} {cy - s} h{2 * a} v{2 * a} h{2 * a} v{2 * a} h{-2 * a} v{2 * a} h{-2 * a} '
            f'v{-2 * a} h{-2 * a} v{-2 * a} h{2 * a} Z" fill="{col}" stroke="none"/>')


# ---------------------------------------------------------------- trousse et pansements
add("inf_trousse_ouverte", "Trousse de secours ouverte (contenu)", INF, 80, 60,
    f'<rect x="4" y="20" width="72" height="36" rx="5" fill="#ffffff" {_O}/>'
    f'<path d="M4 20 L10 4 H70 L76 20" fill="#e8f5e9" {_O}/>' + _cross(40, 12, 5)
    + f'<rect x="9" y="26" width="14" height="24" rx="2" fill="#f5f5f5" {_O}/>'          # compresses
    + '<path d="M11 31 H21 M11 36 H21 M11 41 H21" stroke="#bdbdbd" stroke-width="1"/>'
    + f'<circle cx="35" cy="38" r="9" fill="#fafafa" {_O}/><circle cx="35" cy="38" r="3" fill="#e0e0e0" stroke="none"/>'   # bande
    + f'<rect x="48" y="26" width="10" height="22" rx="2" fill="#81d4fa" {_O}/><rect x="50" y="22" width="6" height="5" fill="#455a64" stroke="none"/>'  # flacon
    + f'<path d="M63 30 L72 48 M72 30 L63 48" stroke="#78909c" stroke-width="2"/>'
    + '<circle cx="62.5" cy="27.5" r="2.3" fill="none" stroke="#78909c" stroke-width="1.2"/>'
    + '<circle cx="72.5" cy="27.5" r="2.3" fill="none" stroke="#78909c" stroke-width="1.2"/>')
add("inf_compresses", "Compresses stériles (sachet)", INF, 60, 50,
    f'<rect x="6" y="6" width="48" height="38" rx="2" fill="#e3f2fd" {_O}/>'
    '<path d="M6 12 H54" stroke="#90caf9" stroke-width="1.4" stroke-dasharray="3 2"/>'
    f'<rect x="14" y="18" width="32" height="20" fill="#ffffff" {_O}/>'
    '<path d="M14 23 H46 M14 28 H46 M14 33 H46 M22 18 V38 M30 18 V38 M38 18 V38" stroke="#e0e0e0" stroke-width="0.8"/>'
    + t(30, 11, "STÉRILE", 4.5, "bold"))
add("inf_bande_gaze", "Bande de gaze (rouleau)", INF, 70, 50,
    f'<path d="M30 25 H66 V37 H30 Z" fill="#ffffff" {_O}/>'
    '<path d="M36 25 V37 M44 25 V37 M52 25 V37 M60 25 V37" stroke="#e0e0e0" stroke-width="0.8"/>'
    f'<ellipse cx="22" cy="25" rx="16" ry="18" fill="#fafafa" {_O}/>'
    f'<ellipse cx="22" cy="25" rx="10" ry="11" fill="none" stroke="#e0e0e0" stroke-width="1"/>'
    f'<ellipse cx="22" cy="25" rx="4" ry="4.5" fill="#d7ccc8" {_O}/>')
add("inf_bande_elastique", "Bande élastique de contention", INF, 70, 50,
    f'<path d="M30 25 H66 V37 H30 Z" fill="#e8d5b0" {_O}/>'
    '<path d="M30 28 H66 M30 31 H66 M30 34 H66" stroke="#c9b28a" stroke-width="0.7"/>'
    f'<ellipse cx="22" cy="25" rx="16" ry="18" fill="#efe0c2" {_O}/>'
    f'<ellipse cx="22" cy="25" rx="10" ry="11" fill="none" stroke="#c9b28a" stroke-width="1"/>'
    f'<ellipse cx="22" cy="25" rx="4" ry="4.5" fill="#a1887f" {_O}/>'
    f'<rect x="58" y="40" width="8" height="5" rx="1" fill="#b0bec5" {_O}/>')
add("inf_pansement", "Pansement adhésif", INF, 70, 30,
    f'<rect x="4" y="6" width="62" height="18" rx="9" fill="#f0c9a0" {_O}/>'
    f'<rect x="24" y="8" width="22" height="14" rx="2" fill="#ffffff" stroke="#e0b48a" stroke-width="1"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="0.7" fill="#d4a373" stroke="none"/>'
              for x in (10, 14, 18, 52, 56, 60) for y in (12, 18)))
add("inf_sparadrap", "Sparadrap (rouleau adhésif)", INF, 60, 50,
    f'<path d="M30 34 H56 V44 H30 Z" fill="#ffffff" {_O}/>'
    f'<circle cx="24" cy="25" r="19" fill="#ffffff" {_O}/><circle cx="24" cy="25" r="11" fill="#e3f2fd" {_O}/>'
    '<circle cx="24" cy="25" r="15" fill="none" stroke="#e0e0e0" stroke-width="0.8"/>')
add("inf_echarpe", "Écharpe triangulaire (bras en écharpe)", INF, 60, 70,
    '<circle cx="30" cy="10" r="7" fill="#5d4037" stroke="none"/>'
    '<path d="M18 20 H42 L46 62 H14 Z" fill="#78909c" stroke="none"/>'
    '<path d="M18 22 L14 44 Q14 50 22 50 H44" stroke="#f2c6a0" stroke-width="6" fill="none" stroke-linecap="round"/>'
    f'<path d="M16 34 L44 22 L46 54 L16 52 Z" fill="#ffffff" {_O} stroke-linejoin="round"/>'
    '<path d="M44 22 L22 18" stroke="#ffffff" stroke-width="3"/>')
add("inf_bandage_main", "Bandage de la main", INF, 50, 70,
    '<path d="M14 66 V40 L8 26 Q6 22 10 21 L16 30 V12 Q16 8 20 8 Q23 8 23 12 V28 V8 Q23 4 27 4 Q30 4 30 8 V28 V10 '
    'Q30 6 34 6 Q37 6 37 10 V30 V16 Q37 12 40 12 Q43 12 43 16 V44 Q43 56 36 60 V66 Z" fill="#f2c6a0" stroke="CC" stroke-width="1.2"/>'
    f'<path d="M14 36 Q28 32 43 36 V56 Q28 52 14 56 Z" fill="#ffffff" {_O}/>'
    '<path d="M14 42 L43 40 M14 48 L43 46 M14 52 L43 52" stroke="#e0e0e0" stroke-width="1"/>'
    f'<path d="M14 58 Q28 56 37 58 V64 Q28 62 14 64 Z" fill="#ffffff" {_O}/>')
add("inf_poche_froid", "Poche de froid instantané", INF, 60, 50,
    f'<rect x="6" y="8" width="48" height="34" rx="6" fill="#bbdefb" {_O}/>'
    '<path d="M30 14 V36 M20 20 L40 30 M40 20 L20 30" stroke="#1e88e5" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M27 15 L30 18 L33 15 M27 35 L30 32 L33 35" stroke="#1e88e5" stroke-width="1.4" fill="none"/>')
add("inf_couverture_survie", "Couverture de survie", INF, 70, 50,
    '<path d="M6 10 L40 6 L64 14 L60 44 L28 46 L8 38 Z" fill="#ffd54f" stroke="#b28704" stroke-width="1.2"/>'
    '<path d="M6 10 L40 6 L64 14 L36 18 Z" fill="#cfd8dc" stroke="#78909c" stroke-width="1"/>'
    '<path d="M22 14 L30 42 M40 8 L44 44 M14 22 L58 30" stroke="#f9a825" stroke-width="0.8"/>')

# ---------------------------------------------------------------- matériel de soins
add("inf_ciseaux", "Ciseaux à bouts ronds", INF, 70, 40,
    '<path d="M28 20 L66 8 Q68 9 66 11 L32 22 Z" fill="#b0bec5" stroke="CC" stroke-width="1"/>'
    '<path d="M28 20 L66 32 Q68 31 66 29 L32 18 Z" fill="#cfd8dc" stroke="CC" stroke-width="1"/>'
    '<circle cx="62" cy="10" r="2" fill="#cfd8dc" stroke="none"/><circle cx="62" cy="30" r="2" fill="#cfd8dc" stroke="none"/>'
    '<ellipse cx="13" cy="11" rx="9" ry="6" fill="none" stroke="#1e88e5" stroke-width="3.4"/>'
    '<ellipse cx="13" cy="29" rx="9" ry="6" fill="none" stroke="#1e88e5" stroke-width="3.4"/>'
    '<path d="M21 13 L30 19 M21 27 L30 21" stroke="#1e88e5" stroke-width="3.4" stroke-linecap="round"/>'
    '<circle cx="30" cy="20" r="1.6" fill="#455a64" stroke="none"/>')
add("inf_pince", "Pince à échardes", INF, 70, 30,
    '<path d="M4 13 L64 9 Q67 9 66 11 L10 15 Z" fill="#b0bec5" stroke="CC" stroke-width="1"/>'
    '<path d="M4 17 L64 21 Q67 21 66 19 L10 15 Z" fill="#cfd8dc" stroke="CC" stroke-width="1"/>'
    '<path d="M30 10.5 L34 11 M30 19.5 L34 19" stroke="#78909c" stroke-width="3"/>')
add("inf_thermometre", "Thermomètre médical électronique", INF, 70, 30,
    f'<path d="M4 15 L16 11 H60 Q66 11 66 15 Q66 19 60 19 H16 Z" fill="#ffffff" {_O}/>'
    '<path d="M4 15 L16 12.5 V17.5 Z" fill="#b0bec5" stroke="none"/>'
    f'<rect x="30" y="12.5" width="18" height="5" rx="1" fill="#c5e1a5" stroke="#558b2f" stroke-width="0.6"/>'
    '<text x="39" y="16.8" font-size="4.2" font-family="DejaVu Sans Mono, monospace" text-anchor="middle" fill="#1b1b1b" stroke="none">37,2</text>'
    '<circle cx="56" cy="15" r="2" fill="#1e88e5" stroke="none"/>')
add("inf_tensiometre", "Tensiomètre électronique (brassard)", INF, 80, 60,
    f'<rect x="4" y="8" width="34" height="44" rx="5" fill="#eceff1" {_O}/>'
    '<rect x="9" y="13" width="24" height="20" rx="2" fill="#c5e1a5" stroke="none"/>'
    + t(21, 21, "120", 6.5, "bold") + t(21, 29, "80", 6, "bold")
    + '<circle cx="21" cy="43" r="4" fill="#1e88e5" stroke="none"/>'
    '<path d="M38 30 Q48 30 50 22" stroke="#455a64" stroke-width="1.6" fill="none"/>'
    f'<path d="M48 10 H74 Q77 10 77 14 V36 Q77 40 74 40 H48 Q46 25 48 10 Z" fill="#1565c0" {_O}/>'
    '<path d="M54 14 V36 M70 14 V36" stroke="#90caf9" stroke-width="1"/>')
add("inf_stethoscope", "Stéthoscope", INF, 60, 70,
    '<path d="M16 6 Q10 6 10 14 V30 Q10 44 24 44 Q38 44 38 30 V14 Q38 6 32 6" stroke="#37474f" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    '<circle cx="16" cy="6" r="2.4" fill="#90a4ae" stroke="none"/><circle cx="32" cy="6" r="2.4" fill="#90a4ae" stroke="none"/>'
    '<path d="M24 44 V52 Q24 62 34 62 H38" stroke="#37474f" stroke-width="2.6" fill="none"/>'
    f'<circle cx="46" cy="62" r="8" fill="#b0bec5" {_O}/><circle cx="46" cy="62" r="4.5" fill="#eceff1" stroke="none"/>')
add("inf_oxymetre", "Oxymètre de pouls (doigt)", INF, 60, 50,
    f'<rect x="12" y="10" width="40" height="30" rx="8" fill="#eceff1" {_O}/>'
    '<rect x="20" y="15" width="24" height="12" rx="1.5" fill="#263238" stroke="none"/>'
    '<text x="26" y="24" font-size="6" font-family="DejaVu Sans Mono, monospace" text-anchor="middle" fill="#80deea" stroke="none">98</text>'
    '<text x="38" y="24" font-size="6" font-family="DejaVu Sans Mono, monospace" text-anchor="middle" fill="#ffcc80" stroke="none">72</text>'
    '<path d="M2 30 H22 Q26 30 26 34 Q26 38 22 38 H2" fill="#f2c6a0" stroke="CC" stroke-width="1"/>'
    + t(32, 47, "SpO₂ %", 5))
add("inf_seringue", "Seringue", INF, 80, 30,
    '<path d="M2 15 H10 M6 9 V21" stroke="#455a64" stroke-width="2.6" stroke-linecap="round"/>'
    '<path d="M10 15 H20" stroke="#90a4ae" stroke-width="2.4"/>'
    f'<rect x="20" y="9" width="36" height="12" rx="1.5" fill="#e3f2fd" {_O}/>'
    '<rect x="21" y="10" width="20" height="10" fill="#bbdefb" stroke="none"/>'
    '<path d="M28 9 V12 M34 9 V12 M40 9 V12 M46 9 V12 M52 9 V12" stroke="CC" stroke-width="0.6"/>'
    '<path d="M18 7 V23" stroke="#455a64" stroke-width="2"/>'
    f'<path d="M56 12 H62 V18 H56 Z" fill="#ffffff" {_O}/><path d="M62 15 H78" stroke="#78909c" stroke-width="1"/>')
add("inf_gants", "Gants à usage unique", INF, 60, 70,
    '<path d="M16 66 V44 L8 30 Q6 26 10 25 L18 34 V12 Q18 8 22 8 Q25 8 25 12 V30 V6 Q25 2 29 2 Q32 2 32 6 V30 V8 '
    'Q32 4 36 4 Q39 4 39 8 V32 V14 Q39 10 42 10 Q45 10 45 14 V46 Q45 56 38 60 V66 Z" fill="#64b5f6" stroke="#1565c0" stroke-width="1.2"/>'
    '<path d="M16 60 H38" stroke="#1565c0" stroke-width="1"/>')
add("inf_masque", "Masque chirurgical", INF, 70, 50,
    '<path d="M18 14 Q6 14 4 24 Q6 34 18 34" stroke="#90a4ae" stroke-width="1.4" fill="none"/>'
    '<path d="M52 14 Q64 14 66 24 Q64 34 52 34" stroke="#90a4ae" stroke-width="1.4" fill="none"/>'
    f'<path d="M18 10 Q35 6 52 10 V38 Q35 44 18 38 Z" fill="#90caf9" {_O}/>'
    '<path d="M18 18 Q35 15 52 18 M18 25 Q35 22 52 25 M18 32 Q35 29 52 32" stroke="#64b5f6" stroke-width="1"/>'
    '<path d="M26 10.5 Q35 9 44 10.5" stroke="#eceff1" stroke-width="2"/>')
add("inf_gel", "Gel hydroalcoolique (flacon pompe)", INF, 40, 70,
    '<path d="M18 4 H30 V8 H22 V14" stroke="#455a64" stroke-width="2.4" fill="none"/>'
    '<rect x="16" y="14" width="10" height="8" fill="#455a64" stroke="none"/>'
    f'<path d="M9 26 Q9 22 13 22 H29 Q33 22 33 26 V64 Q33 66 31 66 H11 Q9 66 9 64 Z" fill="#b2ebf2" {_O}/>'
    '<rect x="12" y="34" width="18" height="20" rx="2" fill="#ffffff" stroke="none"/>'
    + '<path d="M21 38 Q16 45 21 50 Q26 45 21 38 Z" fill="#26c6da" stroke="none"/>')
add("inf_antiseptique", "Flacon d'antiseptique", INF, 40, 70,
    '<rect x="15" y="4" width="10" height="10" rx="1" fill="#e53935" stroke="none"/>'
    f'<path d="M12 18 L15 14 H25 L28 18 V64 Q28 66 26 66 H14 Q12 66 12 64 Z" fill="#ffffff" {_O}/>'
    '<rect x="12" y="44" width="16" height="20" fill="#f57c00" stroke="none" opacity="0.85"/>'
    + _cross(20, 30, 6, _R))
add("inf_serum", "Sérum physiologique (unidoses)", INF, 60, 66,
    "".join(f'<path d="M{x} 18 V50 Q{x} 54 {x + 4} 54 H{x + 8} Q{x + 12} 54 {x + 12} 50 V18 L{x + 9} 14 V8 H{x + 3} V14 Z" '
            f'fill="#e1f5fe" stroke="CC" stroke-width="1"/><rect x="{x + 3}" y="4" width="6" height="4" fill="#4fc3f7" stroke="none"/>'
            for x in (6, 24, 42))
    + t(30, 63, "NaCl 0,9 %", 5, "bold"))
add("inf_haricot", "Haricot (plateau de soins)", INF, 70, 40,
    '<path d="M6 16 Q6 6 18 6 Q30 6 35 13 Q40 6 52 6 Q64 6 64 16 Q64 34 35 34 Q6 34 6 16 Z" fill="#cfd8dc" stroke="CC" stroke-width="1.2"/>'
    '<path d="M11 17 Q11 10 19 10 Q29 10 35 17 Q41 10 51 10 Q59 10 59 17 Q59 29 35 29 Q11 29 11 17 Z" fill="#eceff1" stroke="#90a4ae" stroke-width="1"/>')
add("inf_dasri", "Collecteur d'aiguilles (déchets de soins, DASRI)", INF, 50, 70,
    f'<path d="M8 22 H42 L38 66 H12 Z" fill="#fdd835" {_O}/>'
    f'<rect x="6" y="12" width="38" height="10" rx="2" fill="#f9a825" {_O}/>'
    '<rect x="18" y="14" width="14" height="5" rx="2" fill="#5d4037" stroke="none"/>'
    '<path d="M25 30 L33 50 H17 Z" fill="none" stroke="#212121" stroke-width="1.4" stroke-linejoin="round"/>'
    + t(25, 47, "!", 9, "bold"))
add("inf_glucometre", "Lecteur de glycémie (bandelette)", INF, 60, 60,
    f'<rect x="12" y="6" width="32" height="48" rx="6" fill="#eceff1" {_O}/>'
    '<rect x="16" y="12" width="24" height="18" rx="2" fill="#c5e1a5" stroke="none"/>'
    + t(28, 24, "1,05", 6.5, "bold") + t(28, 29, "g/L", 3.8)
    + '<circle cx="28" cy="42" r="4" fill="#90a4ae" stroke="none"/>'
    f'<rect x="24" y="54" width="8" height="5" fill="#ffffff" {_O}/><circle cx="28" cy="58" r="1" fill="{_R}" stroke="none"/>')
add("inf_brancard", "Brancard (transport du patient)", INF, 100, 40,
    '<path d="M4 16 H96" stroke="#455a64" stroke-width="3" stroke-linecap="round"/>'
    '<rect x="12" y="10" width="76" height="6" rx="2" fill="#1e88e5" stroke="none"/>'
    '<path d="M22 16 V30 M78 16 V30" stroke="#455a64" stroke-width="2.4"/>'
    '<circle cx="22" cy="33" r="3.5" fill="#263238" stroke="none"/><circle cx="78" cy="33" r="3.5" fill="#263238" stroke="none"/>')
add("inf_fauteuil", "Fauteuil roulant", INF, 60, 60,
    '<circle cx="24" cy="40" r="16" fill="none" stroke="#37474f" stroke-width="2.6"/>'
    '<circle cx="24" cy="40" r="2" fill="#37474f" stroke="none"/>'
    '<path d="M14 8 V32 H44 L50 52" stroke="#1e88e5" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M14 20 H36" stroke="#1e88e5" stroke-width="3" stroke-linecap="round"/>'
    '<circle cx="50" cy="54" r="3.5" fill="#37474f" stroke="none"/>')
