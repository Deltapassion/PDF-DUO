"""Brouillon 1.3.0 : gestes qui sauvent, biologie de base, robotique (Arduino, Raspberry Pi, micro:bit).
Dessins originaux (aucun logo de marque). À intégrer dans symbols.py après validation."""
import math
from .symbols import add, t, _W, _box

GQS = "Gestes qui sauvent – premiers secours"
BIO = "Biologie de base"
ROB = "Robotique – Arduino, Raspberry Pi, micro:bit"

_G, _SK, _VIC, _SAU = "#2e8b57", "#f2c6a0", "#1e88e5", "#e53935"   # vert secours, peau, victime, sauveteur


def _seg(pts, col, w=6):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def _head(x, y, r=5.5, col="#5d4037"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="none"/>'


def _green(body):
    return f'<g stroke="none"><rect x="2" y="2" width="56" height="56" rx="4" fill="{_G}"/>' + body + '</g>'


def _cross_w(cx, cy, s=8):
    return f'<path d="M{cx - s / 3} {cy - s} h{2 * s / 3} v{2 * s / 3} h{2 * s / 3} v{2 * s / 3} h{-2 * s / 3} v{2 * s / 3} h{-2 * s / 3} v{-2 * s / 3} h{-2 * s / 3} v{-2 * s / 3} h{2 * s / 3} Z" fill="#ffffff" stroke="none"/>'


_HEART = "M0 6 C-10 -2 -9 -12 -3 -12 C-1 -12 0 -10 0 -9 C0 -10 1 -12 3 -12 C9 -12 10 -2 0 6 Z"

# ---------------------------------------------------------------- gestes qui sauvent
add("gqs_croix", "Premiers secours (panneau)", GQS, 60, 60, _green(_cross_w(30, 30, 16)))
add("gqs_dae", "Défibrillateur automatisé externe – DAE (panneau)", GQS, 60, 60, _green(
    f'<g transform="translate(30 33) scale(2)"><path d="{_HEART}" fill="#ffffff"/></g>'
    f'<path d="M32 16 L24 33 H31 L27 46 L38 28 H31 Z" fill="{_G}" stroke="none"/>' + _cross_w(48, 12, 5)))
add("gqs_lavage_yeux", "Lavage oculaire (panneau)", GQS, 60, 60, _green(
    '<path d="M10 34 Q30 18 50 34 Q30 48 10 34 Z" fill="#ffffff"/><circle cx="30" cy="34" r="6" fill="' + _G + '"/>'
    + "".join(f'<path d="M{x} 8 Q{x + 2} 16 {x + 1} 22" stroke="#ffffff" stroke-width="2.4" fill="none" stroke-linecap="round"/>' for x in (20, 30, 40))))
add("gqs_douche", "Douche de sécurité (panneau)", GQS, 60, 60, _green(
    '<path d="M22 8 H38 L42 14 H18 Z" fill="#ffffff"/>' + "".join(f'<path d="M{x} 18 V24" stroke="#ffffff" stroke-width="1.6"/>' for x in (22, 27, 32, 37))
    + _head(30, 30, 4.5, "#ffffff") + _seg([(30, 36), (30, 48)], "#ffffff", 6) + _seg([(30, 48), (26, 56)], "#ffffff", 4) + _seg([(30, 48), (34, 56)], "#ffffff", 4)
    + _seg([(30, 38), (22, 32)], "#ffffff", 3.4) + _seg([(30, 38), (38, 32)], "#ffffff", 3.4)))
add("gqs_trousse", "Trousse de secours", GQS, 60, 50,
    '<path d="M22 12 V8 Q22 5 25 5 H35 Q38 5 38 8 V12" stroke="CC" stroke-width="2.4" fill="none"/>'
    f'<rect x="4" y="12" width="52" height="34" rx="5" fill="#ffffff" stroke="CC" stroke-width="1.6"/><rect x="4" y="12" width="52" height="7" rx="3" fill="{_G}" stroke="none"/>'
    f'<path d="M26 22 h8 v6 h6 v8 h-6 v6 h-8 v-6 h-6 v-8 h6 Z" fill="{_G}" stroke="none"/>')
add("gqs_alerter", "Alerter les secours : 15, 18, 112, 114", GQS, 70, 60,
    '<rect x="6" y="6" width="26" height="48" rx="5" fill="#263238" stroke="CC" stroke-width="1"/><rect x="9" y="12" width="20" height="32" rx="1.5" fill="#b3e5fc" stroke="none"/>'
    '<circle cx="19" cy="49" r="2" fill="#90a4ae" stroke="none"/>'
    + "".join(f'<path d="M{34 + i * 5} {20 - i * 3} Q{40 + i * 6} 28 {34 + i * 5} {36 + i * 3}" stroke="{_SAU}" stroke-width="2" fill="none"/>' for i in range(3))
    + t(19, 23, "15", 6.5, "bold") + t(19, 31, "18", 6.5, "bold") + t(19, 39, "112", 6.5, "bold") + t(56, 56, "114 (SMS)", 5))
add("gqs_proteger", "Protéger : baliser la zone (triangle)", GQS, 60, 50,
    f'<path d="M30 6 L54 44 H6 Z" fill="#ffffff" stroke="{_SAU}" stroke-width="5" stroke-linejoin="round"/><path d="M30 20 L40 37 H20 Z" fill="none" stroke="{_SAU}" stroke-width="1.4"/>'
    '<path d="M24 44 L22 48 M36 44 L38 48" stroke="#616161" stroke-width="2"/>')
add("gqs_victime", "Victime allongée sur le dos – vérifier la respiration", GQS, 90, 50,
    '<path d="M4 44 H86" stroke="#9e9e9e" stroke-width="1.2"/>' + _head(12, 34, 6)
    + _seg([(20, 37), (60, 37)], _VIC, 9) + _seg([(60, 38), (84, 39)], "#37474f", 7) + _seg([(24, 34), (44, 30)], _VIC, 4)
    + _seg([(30, 18), (22, 26)], _SAU, 2) + '<path d="M38 14 Q44 20 38 26 M42 10 Q50 20 42 30" stroke="#90a4ae" stroke-width="1.6" fill="none"/>'
    + t(46, 8, "10 s", 6, "bold"))
add("gqs_massage", "Massage cardiaque (compressions thoraciques)", GQS, 90, 60,
    '<path d="M4 54 H86" stroke="#9e9e9e" stroke-width="1.2"/>' + _head(10, 46, 5.5)
    + _seg([(17, 48), (55, 48)], _VIC, 8) + _seg([(55, 49), (84, 50)], "#37474f", 6)
    + _head(30, 14, 5.5) + _seg([(36, 19), (52, 30)], _SAU, 8) + _seg([(52, 30), (60, 44), (72, 52)], "#455a64", 7)
    + _seg([(37, 21), (30, 42)], _SAU, 4) + _seg([(40, 23), (32, 42)], _SAU, 4)
    + '<path d="M22 30 V38 M19 35 L22 39 L25 35" stroke="CC" stroke-width="1.4" fill="none"/>' + t(22, 27, "×30", 5.5, "bold"))
add("gqs_insufflation", "Libérer les voies aériennes et insuffler", GQS, 90, 60,
    '<path d="M4 54 H86" stroke="#9e9e9e" stroke-width="1.2"/>' + _head(16, 45, 5.5)
    + _seg([(23, 48), (60, 48)], _VIC, 8) + _seg([(60, 49), (86, 50)], "#37474f", 6)
    + _head(22, 32, 5.5) + _seg([(28, 34), (46, 26)], _SAU, 8) + _seg([(46, 26), (58, 40), (70, 50)], "#455a64", 7)
    + _seg([(30, 34), (14, 40)], _SAU, 3.4) + _seg([(34, 32), (20, 50)], _SAU, 3.4)
    + t(70, 14, "×2", 7, "bold"))
add("gqs_compression", "Saignement : compression directe de la plaie", GQS, 80, 50,
    f'<path d="M4 34 Q30 30 60 32 Q72 32 76 38 L74 44 Q60 42 30 44 Q12 46 4 44 Z" fill="{_SK}" stroke="CC" stroke-width="1.2"/>'
    '<path d="M34 36 Q38 33 42 36" stroke="#c62828" stroke-width="2.4" fill="none"/>'
    '<path d="M26 28 Q38 16 50 28 L48 34 H28 Z" fill="#90caf9" stroke="CC" stroke-width="1.2"/><path d="M30 26 L32 14 M36 22 L38 10 M42 22 L44 12" stroke="#64b5f6" stroke-width="3" stroke-linecap="round"/>'
    '<path d="M38 4 V10 M35 7 L38 10 L41 7" stroke="CC" stroke-width="1.4" fill="none"/>')
add("gqs_garrot", "Garrot (membre)", GQS, 80, 40,
    f'<path d="M4 14 Q40 10 74 16 V28 Q40 30 4 26 Z" fill="{_SK}" stroke="CC" stroke-width="1.2"/>'
    '<rect x="44" y="9" width="8" height="21" rx="1" fill="#424242" stroke="none"/><path d="M48 6 V34" stroke="#8d6e63" stroke-width="2.6"/>'
    '<path d="M64 20 Q66 23 64 25" stroke="#c62828" stroke-width="2" fill="none"/>')
add("gqs_brulure", "Brûlure : refroidir à l'eau 10 à 15 min", GQS, 70, 60,
    '<path d="M6 8 H34 V14 H24 V18 H16 V14 H6 Z" fill="#b0bec5" stroke="CC" stroke-width="1"/>'
    + "".join(f'<path d="M{x} 20 Q{x - 1} 30 {x} 38" stroke="#4fc3f7" stroke-width="1.8" fill="none"/>' for x in (17, 20, 23))
    + f'<path d="M4 46 Q30 40 50 42 Q60 42 66 48 L64 54 Q50 52 28 52 Q12 54 4 54 Z" fill="{_SK}" stroke="CC" stroke-width="1.2"/>'
    '<ellipse cx="22" cy="46" rx="6" ry="3" fill="#ef5350" fill-opacity="0.6" stroke="none"/>' + t(50, 26, "10 min", 7, "bold"))
add("gqs_etouffement", "Étouffement : claques dans le dos", GQS, 70, 60,
    '<path d="M4 56 H66" stroke="#9e9e9e" stroke-width="1.2"/>' + _head(20, 24, 5.5)
    + _seg([(26, 26), (40, 36)], _VIC, 8) + _seg([(40, 36), (42, 46), (40, 56)], "#37474f", 6) + _seg([(30, 30), (24, 40)], _VIC, 4)
    + _head(56, 12, 5.5) + _seg([(56, 18), (56, 38)], _SAU, 8) + _seg([(56, 38), (62, 56)], "#455a64", 6) + _seg([(55, 38), (50, 56)], "#455a64", 6) + _seg([(54, 22), (40, 30)], _SAU, 4)
    + '<path d="M36 22 L40 18 M40 24 L45 22 M34 27 L38 24" stroke="CC" stroke-width="1.2"/>' + t(50, 48, "×5", 6, "bold"))
add("gqs_couverture", "Couverture de survie", GQS, 60, 50,
    '<path d="M8 10 L44 6 L54 40 L16 46 Z" fill="#ffd54f" stroke="#b28704" stroke-width="1.2"/><path d="M8 10 L16 46" stroke="#e0e0e0" stroke-width="3"/>'
    '<path d="M18 14 L24 42 M30 12 L36 40 M40 10 L46 38" stroke="#ffecb3" stroke-width="1"/>')
add("gqs_gants", "Gants à usage unique", GQS, 50, 60,
    '<path d="M14 56 V36 L8 26 Q7 22 10 21 L16 30 V12 Q16 9 19 9 Q22 9 22 12 V28 V7 Q22 4 25 4 Q28 4 28 7 V28 V9 Q28 6 31 6 Q34 6 34 9 V30 V15 Q34 12 37 12 Q40 12 40 15 V40 Q40 48 36 56 Z" '
    'fill="#90caf9" stroke="#1565c0" stroke-width="1.2"/>')
add("gqs_air_frais", "Gaz inhalé : mettre la victime à l'air frais", GQS, 60, 60,
    '<rect x="6" y="6" width="30" height="44" fill="#e3f2fd" stroke="CC" stroke-width="1.6"/><path d="M21 6 V50 M6 28 H36" stroke="CC" stroke-width="1.2"/>'
    + "".join(f'<path d="M{40} {14 + i * 10} Q48 {10 + i * 10} 56 {14 + i * 10}" stroke="#4fc3f7" stroke-width="2.2" fill="none" stroke-linecap="round"/>' for i in range(3))
    + '<path d="M50 44 L56 50 L50 56" stroke="CC" stroke-width="1.8" fill="none"/><path d="M38 50 H56" stroke="CC" stroke-width="1.8"/>')

# ---------------------------------------------------------------- biologie de base
add("bio_cellule_animale", "Cellule animale", BIO, 80, 60,
    '<path d="M10 30 C8 12 30 4 46 8 C66 10 76 24 72 38 C68 54 42 58 26 52 C14 48 10 40 10 30 Z" fill="#fce4ec" stroke="#ad1457" stroke-width="1.6"/>'
    '<circle cx="40" cy="30" r="10" fill="#ce93d8" stroke="#6a1b9a" stroke-width="1.2"/><circle cx="42" cy="28" r="3" fill="#6a1b9a" stroke="none"/>'
    '<ellipse cx="22" cy="24" rx="6" ry="3" fill="#ffab91" stroke="#d84315" stroke-width="0.8" transform="rotate(-20 22 24)"/>'
    '<ellipse cx="60" cy="40" rx="6" ry="3" fill="#ffab91" stroke="#d84315" stroke-width="0.8" transform="rotate(25 60 40)"/>'
    '<circle cx="58" cy="20" r="2.4" fill="#fff59d" stroke="#f9a825" stroke-width="0.6"/><circle cx="24" cy="42" r="2" fill="#fff59d" stroke="#f9a825" stroke-width="0.6"/>')
add("bio_cellule_vegetale", "Cellule végétale", BIO, 80, 60,
    '<rect x="6" y="6" width="68" height="48" rx="6" fill="#dcedc8" stroke="#33691e" stroke-width="3"/><rect x="10" y="10" width="60" height="40" rx="4" fill="none" stroke="#7cb342" stroke-width="1"/>'
    '<rect x="26" y="16" width="34" height="26" rx="10" fill="#e1f5fe" stroke="#0288d1" stroke-width="1"/>'
    '<circle cx="18" cy="38" r="6" fill="#ce93d8" stroke="#6a1b9a" stroke-width="1"/>'
    + "".join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="2.2" fill="#43a047" stroke="#1b5e20" stroke-width="0.6"/>' for x, y in ((16, 16), (64, 46), (66, 14), (40, 46), (16, 26))))
add("bio_bacterie", "Bactérie", BIO, 70, 40,
    '<rect x="10" y="8" width="44" height="22" rx="11" fill="#c5e1a5" stroke="#558b2f" stroke-width="1.6"/>'
    '<path d="M18 18 Q26 12 34 20 T48 18" stroke="#33691e" stroke-width="1.2" fill="none"/>'
    '<path d="M54 19 Q60 14 62 22 T68 26" stroke="#558b2f" stroke-width="1.2" fill="none"/>'
    + "".join(f'<path d="M{x} 8 l-2 -4 M{x} 30 l-2 4" stroke="#558b2f" stroke-width="0.8"/>' for x in (16, 24, 32, 40, 48)))
add("bio_virus", "Virus", BIO, 50, 50,
    '<circle cx="25" cy="25" r="13" fill="#ef9a9a" stroke="#c62828" stroke-width="1.6"/>'
    + "".join(f'<path d="M{25 + 13 * math.cos(a):.1f} {25 + 13 * math.sin(a):.1f} L{25 + 19 * math.cos(a):.1f} {25 + 19 * math.sin(a):.1f}" stroke="#c62828" stroke-width="1.6"/>'
              f'<circle cx="{25 + 20 * math.cos(a):.1f}" cy="{25 + 20 * math.sin(a):.1f}" r="2.2" fill="#e53935" stroke="none"/>' for a in [i * math.pi / 5 for i in range(10)])
    + '<path d="M19 22 Q25 16 31 24 Q25 32 19 28" stroke="#b71c1c" stroke-width="1" fill="none"/>')
_dna = ""
for i in range(25):
    y = 4 + i * 2.2
    x1, x2 = 25 + 11 * math.sin(i * 0.5), 25 - 11 * math.sin(i * 0.5)
    if i % 2 == 0:
        _dna += f'<path d="M{x1:.1f} {y:.1f} H{x2:.1f}" stroke="{("#ef5350", "#42a5f5", "#66bb6a", "#ffca28")[i // 2 % 4]}" stroke-width="1.6"/>'
_s1 = "M" + " L".join(f"{25 + 11 * math.sin(i * 0.25):.1f} {4 + i * 1.1:.1f}" for i in range(50))
_s2 = "M" + " L".join(f"{25 - 11 * math.sin(i * 0.25):.1f} {4 + i * 1.1:.1f}" for i in range(50))
add("bio_adn", "ADN (double hélice)", BIO, 50, 60, _dna + f'<path d="{_s1}" stroke="#1565c0" stroke-width="2" fill="none"/><path d="{_s2}" stroke="#6a1b9a" stroke-width="2" fill="none"/>')
add("bio_chromosome", "Chromosome", BIO, 40, 60,
    '<path d="M8 6 Q14 2 18 8 L19 26 L18 30 L19 34 L18 52 Q14 58 8 54 Q6 30 8 6 Z" fill="#9575cd" stroke="#4527a0" stroke-width="1.2"/>'
    '<path d="M32 6 Q26 2 22 8 L21 26 L22 30 L21 34 L22 52 Q26 58 32 54 Q34 30 32 6 Z" fill="#9575cd" stroke="#4527a0" stroke-width="1.2"/>'
    '<circle cx="20" cy="30" r="3" fill="#4527a0" stroke="none"/><path d="M9 14 H17 M9 20 H17 M23 14 H31 M23 20 H31 M9 42 H17 M23 42 H31" stroke="#ede7f6" stroke-width="1.6"/>')
add("bio_neurone", "Neurone", BIO, 100, 50,
    '<path d="M20 25 L4 10 M20 25 L2 26 M20 25 L6 42 M20 25 L16 4 M20 25 L14 46" stroke="#7b1fa2" stroke-width="1.6" fill="none"/>'
    '<circle cx="20" cy="25" r="9" fill="#ce93d8" stroke="#7b1fa2" stroke-width="1.4"/><circle cx="20" cy="25" r="3" fill="#7b1fa2" stroke="none"/>'
    '<path d="M29 25 H82" stroke="#7b1fa2" stroke-width="2"/>'
    + "".join(f'<rect x="{34 + i * 12}" y="22" width="9" height="6" rx="3" fill="#fff9c4" stroke="#f9a825" stroke-width="0.8"/>' for i in range(4))
    + '<path d="M82 25 L94 16 M82 25 L96 25 M82 25 L94 34" stroke="#7b1fa2" stroke-width="1.6"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#7b1fa2" stroke="none"/>' for x, y in ((94, 16), (96, 25), (94, 34))))
add("bio_globules", "Globules rouges", BIO, 60, 40,
    "".join(f'<ellipse cx="{x}" cy="{y}" rx="12" ry="9" fill="#e53935" stroke="#b71c1c" stroke-width="1"/><ellipse cx="{x}" cy="{y}" rx="5" ry="3.5" fill="#c62828" stroke="none"/>' for x, y in ((16, 14), (40, 12), (30, 28))))
add("bio_coeur", "Cœur (schéma simplifié)", BIO, 60, 60,
    '<path d="M30 54 C10 42 4 30 8 20 C12 10 24 10 30 18 C36 10 48 10 52 20 C56 30 50 42 30 54 Z" fill="#e57373" stroke="#b71c1c" stroke-width="1.6"/>'
    '<path d="M22 14 V4 M30 16 V2 Q30 0 34 0 M38 14 V6" stroke="#1e88e5" stroke-width="3.4" fill="none"/><path d="M34 4 Q44 2 46 8" stroke="#e53935" stroke-width="3.4" fill="none"/>'
    '<path d="M30 18 V48" stroke="#b71c1c" stroke-width="1" stroke-dasharray="2 2"/>' + t(19, 34, "D", 7, "bold") + t(41, 34, "G", 7, "bold"))
add("bio_poumons", "Poumons", BIO, 60, 60,
    '<path d="M30 4 V22 M30 22 L22 28 M30 22 L38 28" stroke="#90a4ae" stroke-width="3.4" fill="none"/>'
    '<path d="M24 24 C14 22 6 34 6 46 C6 54 14 56 24 52 Z" fill="#f48fb1" stroke="#ad1457" stroke-width="1.4"/>'
    '<path d="M36 24 C46 22 54 34 54 46 C54 54 46 56 36 52 Z" fill="#f48fb1" stroke="#ad1457" stroke-width="1.4"/>'
    '<path d="M22 30 L14 38 M22 30 L16 46 M38 30 L46 38 M38 30 L44 46" stroke="#ad1457" stroke-width="1" fill="none"/>')
add("bio_digestif", "Appareil digestif (simplifié)", BIO, 60, 80,
    '<path d="M30 4 V24" stroke="#ef9a9a" stroke-width="4"/>'
    '<path d="M30 24 C40 20 50 26 46 36 C42 44 30 42 26 38" fill="#ef9a9a" stroke="#c62828" stroke-width="1.4"/>'
    '<path d="M12 46 H48 V72 H12 Z" fill="none" stroke="#8d6e63" stroke-width="5" stroke-linejoin="round"/>'
    '<path d="M18 52 Q24 50 26 56 T34 60 T42 54 M20 64 Q28 60 32 66 T42 66" stroke="#ffab91" stroke-width="3.4" fill="none"/>'
    '<path d="M14 30 C10 24 18 18 26 26 L24 34 Z" fill="#a1887f" stroke="#5d4037" stroke-width="1"/>')
add("bio_oeil", "Œil (coupe)", BIO, 70, 50,
    '<circle cx="32" cy="25" r="20" fill="#ffffff" stroke="CC" stroke-width="1.6"/><path d="M14 16 Q10 25 14 34" stroke="#ef9a9a" stroke-width="1"/>'
    '<path d="M50 14 Q56 25 50 36" fill="#e3f2fd" stroke="#1e88e5" stroke-width="1.2"/><ellipse cx="46" cy="25" rx="3" ry="7" fill="#ffffff" stroke="#6d4c41" stroke-width="1.2"/>'
    '<path d="M48 16 V19 M48 31 V34" stroke="#6d4c41" stroke-width="3"/><path d="M12 25 H2" stroke="#fdd835" stroke-width="4"/>'
    '<path d="M14 18 Q10 25 14 32" stroke="#e53935" stroke-width="2" fill="none"/>')
add("bio_plante", "Plante : racines, tige, feuilles, fleur", BIO, 60, 90,
    '<path d="M2 58 H58" stroke="#8d6e63" stroke-width="1.6"/><rect x="2" y="58" width="56" height="30" fill="#d7ccc8" stroke="none"/>'
    '<path d="M30 58 V16" stroke="#558b2f" stroke-width="3"/>'
    '<path d="M30 40 Q16 34 10 42 Q20 48 30 42 Z M30 30 Q44 22 52 30 Q42 38 30 32 Z" fill="#7cb342" stroke="#33691e" stroke-width="1"/>'
    + "".join(f'<ellipse cx="{30 + 7 * math.cos(a):.1f}" cy="{12 + 7 * math.sin(a):.1f}" rx="5" ry="3" transform="rotate({math.degrees(a):.0f} {30 + 7 * math.cos(a):.1f} {12 + 7 * math.sin(a):.1f})" fill="#f06292" stroke="#ad1457" stroke-width="0.6"/>' for a in [i * math.pi / 3 for i in range(6)])
    + '<circle cx="30" cy="12" r="3.4" fill="#fdd835" stroke="none"/>'
    '<path d="M30 58 L30 80 M30 64 L18 74 M30 64 L44 76 M24 70 L20 84 M38 72 L42 84" stroke="#6d4c41" stroke-width="1.6" fill="none"/>')
add("bio_fleur_coupe", "Fleur (coupe : pistil, étamines, pétales)", BIO, 70, 70,
    '<path d="M35 68 V44" stroke="#558b2f" stroke-width="3"/><path d="M20 46 Q35 54 50 46" fill="#7cb342" stroke="#33691e" stroke-width="1"/>'
    '<path d="M22 44 Q6 30 10 10 Q24 18 30 40 Z M48 44 Q64 30 60 10 Q46 18 40 40 Z" fill="#f8bbd0" stroke="#ad1457" stroke-width="1.2"/>'
    '<path d="M31 44 Q30 30 33 22 H37 Q40 30 39 44 Z" fill="#aed581" stroke="#33691e" stroke-width="1"/><ellipse cx="35" cy="20" rx="4" ry="2.4" fill="#689f38" stroke="none"/>'
    '<path d="M29 42 Q22 30 24 22 M41 42 Q48 30 46 22" stroke="#f9a825" stroke-width="1.2" fill="none"/><ellipse cx="24" cy="21" rx="2.4" ry="3.4" fill="#fbc02d" stroke="none"/><ellipse cx="46" cy="21" rx="2.4" ry="3.4" fill="#fbc02d" stroke="none"/>'
    '<ellipse cx="35" cy="40" rx="3.4" ry="2.6" fill="#ffffff" stroke="#33691e" stroke-width="0.6"/>')
add("bio_feuille", "Feuille (nervures)", BIO, 60, 50,
    '<path d="M4 25 Q20 2 50 8 Q58 22 50 40 Q20 48 4 25 Z" fill="#81c784" stroke="#2e7d32" stroke-width="1.4"/><path d="M4 25 L52 24 M54 24 H58" stroke="#2e7d32" stroke-width="1.6"/>'
    + "".join(f'<path d="M{x} 24.5 L{x + 8} {12 + (x - 14) / 10:.1f} M{x} 24.5 L{x + 8} {37 - (x - 14) / 10:.1f}" stroke="#2e7d32" stroke-width="0.8"/>' for x in (14, 24, 34)))
add("bio_graine", "Germination d'une graine", BIO, 50, 60,
    '<path d="M2 30 H48" stroke="#8d6e63" stroke-width="1.4"/><rect x="2" y="30" width="46" height="28" fill="#d7ccc8" stroke="none"/>'
    '<ellipse cx="25" cy="38" rx="9" ry="6" fill="#bcaaa4" stroke="#5d4037" stroke-width="1"/><path d="M25 32 V14" stroke="#7cb342" stroke-width="2"/>'
    '<path d="M25 18 Q14 10 12 16 Q18 22 25 18 Z M25 16 Q36 8 38 14 Q32 20 25 16 Z" fill="#9ccc65" stroke="#558b2f" stroke-width="0.8"/>'
    '<path d="M25 44 L23 54 M25 44 L30 52 M25 44 L18 50" stroke="#6d4c41" stroke-width="1" fill="none"/>')
add("bio_champignon", "Champignon", BIO, 50, 60,
    '<path d="M4 28 Q4 6 25 6 Q46 6 46 28 Z" fill="#e57373" stroke="#b71c1c" stroke-width="1.4"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#ffffff" stroke="none"/>' for x, y in ((14, 18), (26, 12), (36, 20), (22, 22)))
    + '<path d="M18 28 Q16 48 14 56 H36 Q34 48 32 28 Z" fill="#fff8e1" stroke="CC" stroke-width="1.2"/><path d="M18 34 H32" stroke="#bcaaa4" stroke-width="1.6"/>')
add("bio_microscope", "Microscope optique", BIO, 60, 80,
    '<rect x="10" y="70" width="40" height="7" rx="2" fill="#37474f" stroke="none"/><path d="M40 70 Q46 46 32 30" stroke="#455a64" stroke-width="6" fill="none"/>'
    '<rect x="16" y="50" width="28" height="4" fill="#607d8b" stroke="CC" stroke-width="0.6"/><rect x="22" y="47" width="16" height="3" fill="#b3e5fc" stroke="CC" stroke-width="0.4"/>'
    '<path d="M22 8 L30 40" stroke="#eceff1" stroke-width="8" stroke-linecap="round"/><path d="M22 8 L30 40" stroke="CC" stroke-width="8.8" stroke-opacity="0.2" stroke-linecap="round"/>'
    '<path d="M20 2 L24 2 L23 8 L21 8 Z" fill="#263238" stroke="none"/><rect x="26" y="40" width="8" height="6" fill="#263238" stroke="none"/>'
    '<circle cx="46" cy="56" r="4" fill="#90a4ae" stroke="CC" stroke-width="0.8"/><circle cx="30" cy="64" r="3" fill="#fff59d" stroke="CC" stroke-width="0.6"/>')
add("bio_lame", "Lame et lamelle (préparation)", BIO, 80, 30,
    '<rect x="4" y="8" width="72" height="16" rx="1" fill="#e3f2fd" stroke="CC" stroke-width="1.2"/><rect x="28" y="6" width="22" height="20" fill="#ffffff" fill-opacity="0.6" stroke="#90a4ae" stroke-width="0.8"/>'
    '<circle cx="39" cy="16" r="4" fill="#f48fb1" fill-opacity="0.7" stroke="none"/><rect x="6" y="10" width="14" height="12" fill="#eceff1" stroke="none"/>')
add("bio_petri", "Boîte de Petri (culture)", BIO, 60, 40,
    '<ellipse cx="30" cy="22" rx="26" ry="14" fill="#fffde7" stroke="CC" stroke-width="1.4"/><ellipse cx="30" cy="20" rx="26" ry="14" fill="none" stroke="#b0bec5" stroke-width="1"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffb74d" stroke="#e65100" stroke-width="0.5"/>' for x, y, r in ((20, 18, 3), (34, 24, 2.4), (40, 16, 2), (26, 28, 1.8), (16, 24, 1.6))))
add("bio_loupe", "Loupe", BIO, 50, 50,
    '<circle cx="20" cy="20" r="15" fill="#e3f2fd" fill-opacity="0.6" stroke="#455a64" stroke-width="3"/><path d="M31 31 L46 46" stroke="#5d4037" stroke-width="6" stroke-linecap="round"/>'
    '<path d="M12 14 Q16 10 20 10" stroke="#ffffff" stroke-width="2" fill="none"/>')

# ---------------------------------------------------------------- robotique : cartes et modules (vues)
_PCB_ARD, _PCB_RPI, _PCB_BLUE = "#00838f", "#2e7d32", "#1565c0"


def _pins(x, y, n, step=2.54, horiz=True, col="#212121", w=1.6):
    s = ""
    for i in range(n):
        xi, yi = (x + i * step, y) if horiz else (x, y + i * step)
        s += f'<rect x="{xi - w / 2:.2f}" y="{yi - w / 2:.2f}" width="{w}" height="{w}" fill="{col}" stroke="none"/>'
    return s


def _hole(x, y, r=1.8):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" stroke="#c0a060" stroke-width="0.8"/>'


add("rob_uno", "Carte Arduino Uno (vue)", ROB, 70, 54,
    f'<path d="M2 2 H64 L68 6 V50 L66 52 H2 Z" fill="{_PCB_ARD}" stroke="#004d40" stroke-width="1"/>'
    '<rect x="-4" y="8" width="16" height="12" fill="#bdbdbd" stroke="#616161" stroke-width="0.8"/><rect x="-2" y="36" width="14" height="10" fill="#212121" stroke="none"/>'
    '<rect x="24" y="3" width="42" height="4" fill="#212121" stroke="none"/>' + _pins(25.5, 5, 16, 2.54, col="#9e9e9e", w=1)
    + '<rect x="30" y="47" width="36" height="4" fill="#212121" stroke="none"/>' + _pins(31.5, 49, 14, 2.54, col="#9e9e9e", w=1)
    + '<rect x="36" y="30" width="26" height="7" rx="0.6" fill="#212121" stroke="none"/><rect x="28" y="16" width="7" height="7" fill="#263238" stroke="none"/>'
    '<rect x="16" y="22" width="6" height="3" rx="1.5" fill="#cfd8dc" stroke="none"/><circle cx="14" cy="5" r="2" fill="#eceff1" stroke="#9e9e9e" stroke-width="0.6"/>'
    + _W(t(48, 13, "DIGITAL", 3.2)) + _W(t(48, 44, "POWER    ANALOG", 3)) + _W(t(48, 26, "UNO", 5, "bold"))
    + _hole(14, 50) + _hole(64, 10) + _hole(64, 40))
add("rob_rpi", "Carte Raspberry Pi 4 / 5 (vue)", ROB, 90, 60,
    f'<rect x="2" y="2" width="84" height="56" rx="3" fill="{_PCB_RPI}" stroke="#1b5e20" stroke-width="1"/>'
    '<rect x="8" y="3.5" width="52" height="6" fill="#212121" stroke="none"/>' + _pins(9.5, 5, 20, 2.54, col="#ffd54f", w=1) + _pins(9.5, 8, 20, 2.54, col="#ffd54f", w=1)
    + '<rect x="70" y="4" width="18" height="12" fill="#cfd8dc" stroke="#78909c" stroke-width="0.6"/><rect x="70" y="20" width="18" height="12" fill="#cfd8dc" stroke="#78909c" stroke-width="0.6"/>'
    '<rect x="70" y="38" width="18" height="16" fill="#e0e0e0" stroke="#78909c" stroke-width="0.6"/><rect x="72" y="22" width="14" height="3" fill="#1e88e5" stroke="none"/>'
    '<rect x="22" y="20" width="16" height="16" fill="#bdbdbd" stroke="#757575" stroke-width="0.6"/><rect x="44" y="22" width="12" height="12" fill="#212121" stroke="none"/>'
    '<rect x="10" y="52" width="8" height="6" fill="#bdbdbd" stroke="none"/><rect x="26" y="52" width="7" height="6" fill="#bdbdbd" stroke="none"/><rect x="38" y="52" width="7" height="6" fill="#bdbdbd" stroke="none"/>'
    + _W(t(30, 46, "GPIO 40 broches", 3.6)) + _hole(6, 6) + _hole(62, 6) + _hole(6, 54) + _hole(62, 54))
add("rob_pico", "Carte Raspberry Pi Pico (vue)", ROB, 80, 30,
    f'<rect x="4" y="4" width="70" height="22" rx="1" fill="{_PCB_RPI}" stroke="#1b5e20" stroke-width="1"/><rect x="0" y="10" width="7" height="10" fill="#bdbdbd" stroke="none"/>'
    + _pins(8, 5.5, 20, 3.4, col="#ffd54f", w=1.6) + _pins(8, 24.5, 20, 3.4, col="#ffd54f", w=1.6)
    + '<rect x="32" y="10" width="10" height="10" fill="#212121" stroke="none"/><rect x="16" y="11" width="5" height="4" fill="#eceff1" stroke="none"/>')
add("rob_esp32", "Carte ESP32 (vue)", ROB, 50, 80,
    f'<rect x="4" y="4" width="42" height="72" rx="2" fill="#263238" stroke="CC" stroke-width="1"/>'
    '<rect x="11" y="4" width="28" height="30" fill="#b0bec5" stroke="#607d8b" stroke-width="0.6"/><path d="M14 6 H36 V10 H16 V14 H36" stroke="#455a64" stroke-width="1" fill="none"/>'
    '<rect x="14" y="16" width="22" height="16" fill="#cfd8dc" stroke="none"/>' + _W(t(25, 26, "ESP32", 5, "bold"))
    + _pins(6, 10, 26, 2.54, horiz=False, col="#ffd54f", w=1.4) + _pins(44, 10, 26, 2.54, horiz=False, col="#ffd54f", w=1.4)
    + '<rect x="19" y="72" width="12" height="6" fill="#bdbdbd" stroke="none"/><rect x="10" y="64" width="5" height="4" fill="#eceff1" stroke="none"/><rect x="35" y="64" width="5" height="4" fill="#eceff1" stroke="none"/>')
add("rob_microbit", "Carte micro:bit (vue)", ROB, 70, 56,
    '<path d="M4 4 H66 V44 H4 Z" fill="#212121" stroke="CC" stroke-width="1"/>'
    + "".join(f'<rect x="{25 + c * 4.6:.1f}" y="{12 + r * 5:.1f}" width="2" height="3" fill="{"#ff1744" if (r, c) in ((1, 1), (1, 3), (3, 0), (3, 4), (4, 1), (4, 2), (4, 3)) else "#5d4037"}" stroke="none"/>' for r in range(5) for c in range(5))
    + '<circle cx="13" cy="24" r="4.6" fill="#424242" stroke="#9e9e9e" stroke-width="0.8"/><circle cx="57" cy="24" r="4.6" fill="#424242" stroke="#9e9e9e" stroke-width="0.8"/>'
    + _W(t(13, 34, "A", 5, "bold")) + _W(t(57, 34, "B", 5, "bold"))
    + '<path d="M4 44 H66 V52 H4 Z" fill="#c8a43c" stroke="#8d6e00" stroke-width="0.6"/>'
    + "".join(f'<rect x="{x}" y="44" width="8" height="8" rx="2" fill="#e0c060" stroke="#8d6e00" stroke-width="0.6"/>' for x in (8, 24, 38, 54))
    + t(12, 50.5, "0", 3.4, "bold") + t(28, 50.5, "1", 3.4, "bold") + t(42, 50.5, "2", 3.4, "bold"))
add("rob_breadboard", "Plaque d'essai (breadboard)", ROB, 100, 50,
    '<rect x="2" y="2" width="96" height="46" rx="2" fill="#f5f5f5" stroke="CC" stroke-width="1.2"/>'
    '<path d="M6 6 H94 M6 44 H94" stroke="#e53935" stroke-width="0.8"/><path d="M6 10 H94 M6 40 H94" stroke="#1e88e5" stroke-width="0.8"/>'
    + "".join(f'<rect x="{7 + i * 3.6:.1f}" y="{y}" width="1.4" height="1.4" fill="#616161" stroke="none"/>' for i in range(24) for y in (7.3, 37.3))
    + '<rect x="4" y="24" width="92" height="2" fill="#e0e0e0" stroke="none"/>'
    + "".join(f'<rect x="{7 + i * 3.6:.1f}" y="{14 + j * 2.4:.1f}" width="1.4" height="1.4" fill="#757575" stroke="none"/>' for i in range(24) for j in range(4))
    + "".join(f'<rect x="{7 + i * 3.6:.1f}" y="{27.5 + j * 2.4:.1f}" width="1.4" height="1.4" fill="#757575" stroke="none"/>' for i in range(24) for j in range(4)))
add("rob_dupont", "Câbles de connexion (Dupont)", ROB, 70, 40,
    "".join(f'<path d="M6 {8 + i * 6} Q30 {2 + i * 9} 58 {10 + i * 5}" stroke="{c}" stroke-width="2" fill="none"/>'
            f'<rect x="2" y="{6 + i * 6}" width="6" height="4" fill="#212121" stroke="none"/><rect x="58" y="{8 + i * 5}" width="6" height="4" fill="#212121" stroke="none"/>'
            for i, c in enumerate(("#e53935", "#212121", "#fdd835", "#1e88e5", "#43a047"))))
add("rob_bouton", "Bouton poussoir (4 pattes)", ROB, 40, 40,
    '<rect x="8" y="8" width="24" height="24" fill="#424242" stroke="CC" stroke-width="1"/><circle cx="20" cy="20" r="6.4" fill="#212121" stroke="#9e9e9e" stroke-width="1"/>'
    '<path d="M10 8 V2 M30 8 V2 M10 32 V38 M30 32 V38" stroke="#9e9e9e" stroke-width="1.4"/>')
add("rob_potentiometre", "Potentiomètre rotatif", ROB, 40, 50,
    '<rect x="6" y="18" width="28" height="20" rx="2" fill="#1e88e5" stroke="CC" stroke-width="1"/><rect x="16" y="4" width="8" height="16" fill="#bdbdbd" stroke="#757575" stroke-width="0.8"/>'
    '<path d="M20 4 V12" stroke="#616161" stroke-width="1"/><path d="M12 38 V48 M20 38 V48 M28 38 V48" stroke="#9e9e9e" stroke-width="1.6"/>')
add("rob_ldr", "Photorésistance (LDR)", ROB, 30, 50,
    '<circle cx="15" cy="14" r="10" fill="#ffecb3" stroke="#bf8040" stroke-width="1"/><path d="M8 10 H22 M8 14 H22 M8 18 H22" stroke="#e65100" stroke-width="1" fill="none"/>'
    '<path d="M11 24 V48 M19 24 V48" stroke="#9e9e9e" stroke-width="1.4"/>')
add("rob_ultrason", "Capteur à ultrasons (HC-SR04)", ROB, 80, 46,
    f'<rect x="2" y="2" width="76" height="30" rx="2" fill="{_PCB_BLUE}" stroke="CC" stroke-width="1"/>'
    + "".join(f'<circle cx="{x}" cy="17" r="12" fill="#cfd8dc" stroke="#78909c" stroke-width="1.2"/><circle cx="{x}" cy="17" r="8" fill="#90a4ae" stroke="#607d8b" stroke-width="0.8"/>' for x in (18, 62))
    + '<rect x="34" y="6" width="12" height="5" rx="2" fill="#eceff1" stroke="none"/>'
    + "".join(f'<path d="M{34 + i * 4} 32 V44" stroke="#9e9e9e" stroke-width="1.4"/>' for i in range(4))
    + _W(t(18, 6, "T", 3.6, "bold")) + _W(t(62, 6, "R", 3.6, "bold")) + _W(t(40, 30, "Vcc Trig Echo Gnd", 2.6)))
add("rob_servo", "Servomoteur (type SG90)", ROB, 60, 50,
    '<rect x="6" y="14" width="40" height="22" rx="2" fill="#1e88e5" stroke="CC" stroke-width="1"/><rect x="2" y="20" width="48" height="5" fill="#1565c0" stroke="none"/>'
    '<circle cx="16" cy="12" r="6" fill="#1976d2" stroke="CC" stroke-width="0.8"/><path d="M16 12 L4 6 L4 2 L16 9 L28 4 L28 8 Z" fill="#fafafa" stroke="CC" stroke-width="0.8"/>'
    '<path d="M46 30 Q54 32 58 40" stroke="#ff9800" stroke-width="1.4" fill="none"/><path d="M46 32 Q53 35 56 42" stroke="#e53935" stroke-width="1.4" fill="none"/><path d="M46 34 Q52 38 54 44" stroke="#6d4c41" stroke-width="1.4" fill="none"/>')
add("rob_motoreducteur", "Motoréducteur avec roue", ROB, 80, 50,
    '<rect x="4" y="14" width="34" height="22" rx="3" fill="#fdd835" stroke="#b28704" stroke-width="1"/><rect x="38" y="18" width="16" height="14" rx="2" fill="#bdbdbd" stroke="#757575" stroke-width="1"/>'
    '<path d="M54 22 H58 M54 28 H58" stroke="#e53935" stroke-width="1.2"/>'
    '<circle cx="66" cy="25" r="13" fill="#263238" stroke="none"/><circle cx="66" cy="25" r="7" fill="#fdd835" stroke="#b28704" stroke-width="1"/><circle cx="66" cy="25" r="2" fill="#263238" stroke="none"/>'
    '<path d="M21 14 V30" stroke="#fbc02d" stroke-width="1"/>')
add("rob_relais", "Module relais 5 V", ROB, 60, 40,
    f'<rect x="2" y="2" width="56" height="36" rx="2" fill="{_PCB_BLUE}" stroke="CC" stroke-width="1"/><rect x="20" y="6" width="22" height="18" fill="#1e88e5" stroke="#0d47a1" stroke-width="0.8"/>'
    '<rect x="44" y="8" width="12" height="22" fill="#43a047" stroke="#1b5e20" stroke-width="0.8"/>' + "".join(f'<circle cx="50" cy="{12 + i * 7}" r="2" fill="#bdbdbd" stroke="none"/>' for i in range(3))
    + _pins(6, 14, 3, 5, horiz=False, col="#ffd54f", w=2) + _W(t(31, 18, "RELAIS", 3.2, "bold")) + '<circle cx="12" cy="32" r="1.6" fill="#ff1744" stroke="none"/>')
add("rob_pir", "Détecteur de mouvement infrarouge (PIR)", ROB, 50, 50,
    '<rect x="4" y="20" width="42" height="26" rx="2" fill="#2e7d32" stroke="CC" stroke-width="1"/>'
    '<path d="M8 26 Q8 4 25 4 Q42 4 42 26 Z" fill="#fafafa" stroke="#bdbdbd" stroke-width="1"/><path d="M14 10 L36 22 M36 10 L14 22 M25 4 V26" stroke="#e0e0e0" stroke-width="0.8"/>'
    '<circle cx="12" cy="38" r="3" fill="#ff9800" stroke="none"/><circle cx="38" cy="38" r="3" fill="#ff9800" stroke="none"/>')
add("rob_dht", "Capteur température et humidité (DHT11)", ROB, 40, 50,
    '<rect x="6" y="4" width="28" height="34" rx="2" fill="#4fc3f7" stroke="#0277bd" stroke-width="1"/>'
    + "".join(f'<rect x="{10 + c * 6}" y="{8 + r * 6}" width="4" height="3" fill="#0277bd" stroke="none"/>' for r in range(5) for c in range(4))
    + '<path d="M12 38 V48 M18 38 V48 M24 38 V48 M30 38 V48" stroke="#9e9e9e" stroke-width="1.4"/>')
add("rob_lcd", "Afficheur LCD 16×2", ROB, 90, 40,
    f'<rect x="2" y="2" width="86" height="36" rx="2" fill="{_PCB_RPI}" stroke="CC" stroke-width="1"/><rect x="8" y="8" width="74" height="24" fill="#212121" stroke="none"/>'
    '<rect x="11" y="11" width="68" height="18" fill="#1e88e5" stroke="none"/>' + _W(t(45, 19, "Bonjour !", 6, "bold")) + _W(t(45, 27, "T = 21 °C", 6))
    + _pins(10, 4.5, 16, 2.54, col="#ffd54f", w=1.2))
add("rob_oled", "Écran OLED 0,96\"", ROB, 50, 40,
    '<rect x="2" y="6" width="46" height="32" rx="2" fill="#1565c0" stroke="CC" stroke-width="1"/><rect x="6" y="12" width="38" height="20" fill="#000000" stroke="none"/>'
    '<path d="M10 22 H16 L18 16 L22 28 L25 20 H38" stroke="#4fc3f7" stroke-width="1.2" fill="none"/>' + _pins(19, 4, 4, 4, col="#ffd54f", w=1.8))
add("rob_buzzer", "Buzzer", ROB, 40, 50,
    '<circle cx="20" cy="18" r="14" fill="#212121" stroke="CC" stroke-width="1"/><circle cx="20" cy="18" r="2.4" fill="#616161" stroke="none"/>'
    '<path d="M16 32 V48 M24 32 V44" stroke="#9e9e9e" stroke-width="1.4"/>' + _W(t(20, 11, "+", 5, "bold")))
add("rob_feu", "Module feu tricolore (3 LED)", ROB, 70, 30,
    '<path d="M2 4 H52 V26 H2 Z" fill="#212121" stroke="CC" stroke-width="1"/><path d="M52 10 H62 V20 H52 Z" fill="#212121" stroke="none"/>'
    + "".join(f'<circle cx="{x}" cy="15" r="7" fill="{c}" stroke="#424242" stroke-width="0.8"/>' for x, c in ((12, "#e53935"), (27, "#fdd835"), (42, "#43a047")))
    + "".join(f'<path d="M62 {11 + i * 3} H68" stroke="#9e9e9e" stroke-width="1.2"/>' for i in range(3)))
add("rob_joystick", "Module joystick", ROB, 50, 50,
    '<rect x="2" y="2" width="46" height="46" rx="2" fill="#212121" stroke="CC" stroke-width="1"/><circle cx="25" cy="25" r="15" fill="#424242" stroke="#757575" stroke-width="1"/>'
    '<circle cx="25" cy="25" r="9" fill="#616161" stroke="#9e9e9e" stroke-width="1"/>' + _pins(6, 8, 5, 4, horiz=False, col="#ffd54f", w=1.6))
add("rob_humidite_sol", "Capteur d'humidité du sol", ROB, 30, 80,
    f'<path d="M4 4 H26 V60 L20 76 H10 L4 60 Z" fill="#212121" stroke="CC" stroke-width="1"/>'
    '<path d="M10 20 V70 M20 20 V70" stroke="#c8a43c" stroke-width="2.4"/>' + _pins(9, 8, 3, 6, col="#ffd54f", w=1.8))
add("rob_suiveur", "Capteur suiveur de ligne (infrarouge)", ROB, 50, 40,
    f'<rect x="2" y="2" width="46" height="24" rx="2" fill="{_PCB_BLUE}" stroke="CC" stroke-width="1"/>'
    '<circle cx="16" cy="14" r="4" fill="#212121" stroke="none"/><circle cx="28" cy="14" r="4" fill="#e3f2fd" stroke="#90a4ae" stroke-width="0.8"/>'
    '<path d="M2 34 H48" stroke="#212121" stroke-width="5"/>' + _pins(40, 8, 3, 4, horiz=False, col="#ffd54f", w=1.6))
add("rob_bluetooth", "Module Bluetooth", ROB, 60, 30,
    f'<rect x="2" y="2" width="48" height="26" rx="2" fill="{_PCB_BLUE}" stroke="CC" stroke-width="1"/><rect x="8" y="5" width="28" height="20" fill="#1e88e5" stroke="#0d47a1" stroke-width="0.6"/>'
    '<circle cx="22" cy="17" r="1.6" fill="#ffffff" stroke="none"/><path d="M18 13 Q22 9 26 13 M15 10 Q22 4 29 10" stroke="#ffffff" stroke-width="1.2" fill="none"/>' + _pins(52, 6, 6, 3.6, horiz=False, col="#ffd54f", w=1.6))
add("rob_pile9v", "Pile 9 V avec coupleur", ROB, 50, 60,
    '<rect x="6" y="14" width="30" height="44" rx="3" fill="#ff9800" stroke="CC" stroke-width="1"/><rect x="6" y="14" width="30" height="14" fill="#212121" stroke="none"/>'
    '<circle cx="14" cy="10" r="3" fill="#bdbdbd" stroke="CC" stroke-width="0.8"/><path d="M24 7 L30 7 L30 13 L24 13 Z" fill="#bdbdbd" stroke="CC" stroke-width="0.8"/>'
    + _W(t(21, 24, "9 V", 7, "bold")) + '<path d="M14 7 Q20 -2 44 6 M28 7 Q34 0 46 10" stroke="#e53935" stroke-width="1.4" fill="none"/>')
add("rob_robot", "Châssis de robot 2 roues", ROB, 90, 60,
    '<rect x="14" y="10" width="62" height="40" rx="8" fill="#eceff1" stroke="CC" stroke-width="1.4"/>'
    '<rect x="2" y="16" width="12" height="28" rx="3" fill="#263238" stroke="none"/><rect x="76" y="16" width="12" height="28" rx="3" fill="#263238" stroke="none"/>'
    f'<rect x="30" y="16" width="30" height="20" rx="1" fill="{_PCB_ARD}" stroke="#004d40" stroke-width="0.8"/><rect x="34" y="40" width="22" height="8" rx="2" fill="#ff9800" stroke="none"/>'
    '<circle cx="45" cy="4" r="3" fill="#90a4ae" stroke="CC" stroke-width="0.8"/>'
    + "".join(f'<circle cx="{x}" cy="12" r="4" fill="#cfd8dc" stroke="#607d8b" stroke-width="0.8"/>' for x in (36, 54)))

# ---------------------------------------------------------------- gestes qui sauvent : compléments (retours du 4/11)
_DK, _LT = "#1565c0", "#64b5f6"     # membres côté sol (foncé) / côté dessus (clair)
add("gqs_pls", "Position latérale de sécurité (PLS)", GQS, 100, 54,
    '<path d="M2 47 H98" stroke="#9e9e9e" stroke-width="1.4"/>'
    + _seg([(30, 41), (4, 42)], "#0d47a1", 5.5)                         # bras côté sol, tendu le long du sol
    + _seg([(60, 41), (96, 43)], "#263238", 7.5)                        # jambe côté sol, tendue
    + _seg([(26, 38), (61, 38)], "#64b5f6", 13)                         # tronc couché sur le côté
    + _seg([(60, 35), (76, 18), (88, 41)], "#455a64", 7.5)              # jambe du dessus pliée, genou en l'air
    + _seg([(34, 33), (42, 20), (25, 30)], "#1e88e5", 5.5)              # bras du dessus plié, main sous la joue
    + '<circle cx="17" cy="35" r="8" fill="#5d4037" stroke="none"/>'
    + '<ellipse cx="22" cy="31.5" rx="3.6" ry="2.4" fill="#f2c6a0" stroke="CC" stroke-width="0.6"/>'
    + '<path d="M11 41 Q10 45 12 46" stroke="#4fc3f7" stroke-width="1.6" fill="none"/>' + t(80, 10, "PLS", 9, "bold"))
_TORSE = ('<path d="M12 4 Q22 0 30 6 Q38 0 48 4 Q58 8 62 16 L58 30 L56 70 H4 L2 30 L-2 16 Q2 8 12 4 Z" fill="#f2c6a0" stroke="CC" stroke-width="1.4" transform="translate(4 0)"/>'
          '<path d="M26 4 Q34 10 42 4" stroke="#c8957a" stroke-width="1.2" fill="none"/>'
          '<path d="M14 28 Q24 34 32 28 M36 28 Q44 34 54 28" stroke="#c8957a" stroke-width="1" fill="none"/>'
          '<circle cx="22" cy="30" r="1.4" fill="#a1665e" stroke="none"/><circle cx="46" cy="30" r="1.4" fill="#a1665e" stroke="none"/>'
          '<path d="M34 36 V58" stroke="#d6a585" stroke-width="0.8"/><circle cx="34" cy="58" r="1.2" fill="#a1665e" stroke="none"/>'
          '<path d="M12 12 Q22 16 30 12 M38 12 Q46 16 56 12" stroke="#d6a585" stroke-width="0.8" fill="none"/>')
add("gqs_dae_pose", "Défibrillateur : position des électrodes sur le torse", GQS, 100, 72,
    _TORSE
    + '<rect x="10" y="14" width="13" height="17" rx="2" fill="#ffffff" stroke="CC" stroke-width="1" transform="rotate(-8 16 22)"/>'
    '<path d="M13 19 l3 3 l4 -5" stroke="' + _G + '" stroke-width="1.2" fill="none" transform="rotate(-8 16 22)"/>'
    '<rect x="48" y="38" width="13" height="17" rx="2" fill="#ffffff" stroke="CC" stroke-width="1" transform="rotate(28 54 46)"/>'
    '<path d="M51 43 l3 3 l4 -5" stroke="' + _G + '" stroke-width="1.2" fill="none" transform="rotate(28 54 46)"/>'
    '<path d="M18 31 Q30 52 74 54 M58 52 Q66 58 74 58" stroke="#424242" stroke-width="1.2" fill="none"/>'
    f'<rect x="72" y="42" width="26" height="26" rx="4" fill="{_G}" stroke="CC" stroke-width="1"/>'
    f'<g transform="translate(85 56) scale(0.8)"><path d="{_HEART}" fill="#ffffff"/></g>'
    f'<path d="M86 47 L82 55 H85.5 L83.5 61 L89 53 H85.5 Z" fill="{_G}" stroke="none"/>')
add("gqs_electrisation", "Électrisation : couper le courant (disjoncteur)", GQS, 60, 60,
    '<rect x="16" y="6" width="28" height="48" rx="3" fill="#eceff1" stroke="CC" stroke-width="1.4"/><rect x="24" y="22" width="12" height="16" rx="2" fill="#424242" stroke="none"/>'
    '<rect x="26" y="30" width="8" height="6" rx="1" fill="#e53935" stroke="none"/><path d="M30 14 V20 M27 17 L30 21 L33 17" stroke="CC" stroke-width="1.4" fill="none"/>'
    + t(30, 49, "0", 8, "bold") + '<path d="M46 8 L40 20 H46 L42 30 L52 16 H46 Z" fill="#fdd835" stroke="CC" stroke-width="0.8"/>'
    '<path d="M38 10 L54 30 M54 10 L38 30" stroke="#d32f2f" stroke-width="2"/>')
add("gqs_perche", "Électrisation : dégager avec un objet isolant (perche, bois sec)", GQS, 90, 60,
    '<path d="M4 56 H86" stroke="#9e9e9e" stroke-width="1.2"/>' + _head(60, 46, 5.5)
    + _seg([(67, 48), (86, 49)], _VIC, 8) + _seg([(54, 50), (42, 54)], _VIC, 3.4)
    + '<path d="M2 50 Q24 40 46 52" stroke="#212121" stroke-width="2" fill="none"/>'
    + _head(12, 10, 5) + _seg([(13, 16), (16, 36)], _SAU, 8) + _seg([(16, 36), (12, 54)], "#455a64", 6) + _seg([(16, 36), (22, 54)], "#455a64", 6)
    + _seg([(14, 20), (26, 26)], _SAU, 3.4) + '<path d="M24 22 L46 50" stroke="#8d6e63" stroke-width="3" stroke-linecap="round"/>'
    + '<path d="M70 6 L66 14 H70 L67 22 L75 12 H71 L74 6 Z" fill="#fdd835" stroke="CC" stroke-width="0.6"/>')

# ---------------------------------------------------------------- sécurité incendie
INC = "Sécurité incendie – équipements"
SINC = "Sécurité incendie – signalisation et évacuation"
_R, _V = "#d32f2f", "#2e8b57"


def _red(body):
    return f'<g stroke="none"><rect x="2" y="2" width="56" height="56" rx="4" fill="{_R}"/>' + body + '</g>'


def _runner(x, y, s=1.0, col="#ffffff"):
    """Personnage qui court (pictogramme d'évacuation), dessin original."""
    g = (f'<g transform="translate({x} {y}) scale({s})" stroke="none">'
         f'<circle cx="14" cy="4" r="4" fill="{col}"/>'
         f'<path d="M12 10 L8 24" stroke="{col}" stroke-width="5.4" stroke-linecap="round"/>'
         f'<path d="M11 12 L4 16 L0 13 M11 12 L18 15 L22 11" stroke="{col}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="M8 23 L14 29 L12 37 M8 23 L2 30 L-4 30" stroke="{col}" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return g


def _arrow(x, y, s=1.0, col="#ffffff", rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="none"><path d="M-9 -3 H2 V-8 L10 0 L2 8 V3 H-9 Z" fill="{col}"/></g>')


add("inc_detecteur_fumee", "Détecteur optique de fumée (plafond)", INC, 60, 40,
    '<path d="M2 6 H58" stroke="#9e9e9e" stroke-width="2"/><path d="M8 8 H52 L48 26 Q30 34 12 26 Z" fill="#fafafa" stroke="CC" stroke-width="1.4"/>'
    + "".join(f'<path d="M{x} 18 V24" stroke="#bdbdbd" stroke-width="1.6"/>' for x in range(16, 46, 4))
    + '<circle cx="30" cy="30" r="2" fill="#e53935" stroke="none"/><path d="M14 36 Q20 32 26 38 Q32 34 38 38" stroke="#90a4ae" stroke-width="1.4" fill="none"/>')
add("inc_detecteur_chaleur", "Détecteur de chaleur (thermovélocimétrique)", INC, 60, 40,
    '<path d="M2 6 H58" stroke="#9e9e9e" stroke-width="2"/><path d="M10 8 H50 L46 22 Q30 28 14 22 Z" fill="#fafafa" stroke="CC" stroke-width="1.4"/>'
    '<path d="M24 22 L30 30 L36 22" fill="#424242" stroke="CC" stroke-width="0.8"/><circle cx="30" cy="31" r="2" fill="#e53935" stroke="none"/>'
    '<path d="M44 26 Q48 32 44 38 M50 24 Q54 31 50 38" stroke="#ff7043" stroke-width="1.4" fill="none"/>')
add("inc_dm", "Déclencheur manuel d'alarme (boîtier rouge)", INC, 50, 50,
    f'<rect x="4" y="4" width="42" height="42" rx="4" fill="{_R}" stroke="CC" stroke-width="1.4"/><rect x="10" y="10" width="30" height="30" rx="2" fill="#ffffff" stroke="#b71c1c" stroke-width="1"/>'
    '<path d="M16 16 L34 34" stroke="#b0bec5" stroke-width="0.8"/><rect x="21" y="21" width="8" height="8" fill="#424242" stroke="none"/>'
    '<path d="M25 13 L22 19 H25 L23 25" stroke="#fdd835" stroke-width="0" fill="none"/>' + t(25, 37, "APPUYER", 4.2, "bold"))
add("inc_diffuseur_sonore", "Diffuseur sonore (sirène d'alarme)", INC, 60, 50,
    f'<path d="M10 14 H22 L36 4 V46 L22 36 H10 Z" fill="{_R}" stroke="CC" stroke-width="1.4"/>'
    + "".join(f'<path d="M{42 + i * 6} {16 - i * 3} Q{48 + i * 8} 25 {42 + i * 6} {34 + i * 3}" stroke="CC" stroke-width="1.8" fill="none"/>' for i in range(3)))
add("inc_diffuseur_lumineux", "Diffuseur lumineux (flash)", INC, 50, 50,
    '<rect x="10" y="30" width="30" height="16" rx="2" fill="#eceff1" stroke="CC" stroke-width="1.2"/><path d="M12 30 Q12 10 25 10 Q38 10 38 30 Z" fill="#ef5350" fill-opacity="0.85" stroke="CC" stroke-width="1.2"/>'
    + "".join(f'<path d="M{25 + 16 * math.cos(a):.1f} {22 - 16 * math.sin(a):.1f} L{25 + 22 * math.cos(a):.1f} {22 - 22 * math.sin(a):.1f}" stroke="#ff7043" stroke-width="2" stroke-linecap="round"/>' for a in [math.radians(d) for d in (10, 45, 90, 135, 170)]))
add("inc_baas", "Bloc autonome d'alarme sonore (BAAS)", INC, 70, 40,
    f'<rect x="4" y="6" width="62" height="28" rx="3" fill="#eceff1" stroke="CC" stroke-width="1.4"/><rect x="8" y="10" width="20" height="20" rx="2" fill="{_R}" stroke="none"/>'
    + "".join(f'<circle cx="{14 + c * 4}" cy="{14 + r * 4}" r="1" fill="#ffffff" stroke="none"/>' for r in range(4) for c in range(3))
    + t(47, 18, "BAAS", 7, "bold") + '<circle cx="40" cy="27" r="1.8" fill="#43a047" stroke="none"/>' + t(52, 29, "alarme", 4.6))
add("inc_baes", "Bloc autonome d'éclairage de sécurité (BAES)", INC, 80, 40,
    '<rect x="4" y="4" width="72" height="32" rx="3" fill="#fafafa" stroke="CC" stroke-width="1.4"/>'
    f'<rect x="10" y="9" width="60" height="22" fill="{_V}" stroke="none"/>' + _runner(16, 10, 0.5) + _arrow(58, 20, 1.0)
    + '<path d="M30 12 H42 V28 H30" stroke="#ffffff" stroke-width="1.6" fill="none"/><circle cx="72" cy="32" r="1.6" fill="#43a047" stroke="none"/>')
add("inc_extincteur_eau", "Extincteur à eau pulvérisée", INC, 40, 80,
    f'<rect x="8" y="16" width="24" height="60" rx="10" fill="{_R}" stroke="CC" stroke-width="1.4"/><rect x="10" y="40" width="20" height="18" rx="1" fill="#ffffff" stroke="none"/>'
    + t(20, 48, "EAU", 5.2, "bold") + t(20, 55, "+ additif", 3.8)
    + '<rect x="15" y="8" width="10" height="9" fill="#424242" stroke="none"/><path d="M14 8 L30 4 M25 12 Q36 14 36 30 V44" stroke="CC" stroke-width="2.2" fill="none"/>'
    '<path d="M20 8 V2 H26" stroke="CC" stroke-width="1.6" fill="none"/>')
add("inc_extincteur_co2", "Extincteur CO₂ (feux électriques)", INC, 40, 80,
    f'<rect x="10" y="16" width="20" height="60" rx="8" fill="{_R}" stroke="CC" stroke-width="1.4"/><rect x="10" y="20" width="20" height="8" fill="#212121" stroke="none"/>'
    '<rect x="12" y="42" width="16" height="14" rx="1" fill="#ffffff" stroke="none"/>' + t(20, 52, "CO₂", 5.2, "bold")
    + '<rect x="15" y="8" width="10" height="9" fill="#424242" stroke="none"/><path d="M25 12 Q34 14 34 24 L38 36 L32 38 L30 26" stroke="CC" stroke-width="1.6" fill="#212121"/>'
    '<path d="M20 8 V2 H26" stroke="CC" stroke-width="1.6" fill="none"/>')
add("inc_ria", "Robinet d'incendie armé (RIA)", INC, 70, 70,
    f'<rect x="4" y="4" width="62" height="62" rx="3" fill="#ffebee" stroke="{_R}" stroke-width="2"/>'
    + "".join(f'<circle cx="35" cy="35" r="{r}" fill="none" stroke="{_R}" stroke-width="4"/>' for r in (24, 18, 12))
    + '<circle cx="35" cy="35" r="5" fill="#424242" stroke="none"/><path d="M59 35 Q66 50 56 62 L50 60" stroke="CC" stroke-width="2.4" fill="none"/>'
    '<rect x="46" y="57" width="8" height="6" fill="#424242" stroke="none"/>' + t(16, 12, "RIA", 6, "bold"))
add("inc_porte_cf", "Porte coupe-feu (avec ferme-porte)", INC, 60, 90,
    '<rect x="6" y="4" width="48" height="84" fill="#eceff1" stroke="CC" stroke-width="1.6"/><rect x="10" y="10" width="40" height="76" fill="#cfd8dc" stroke="CC" stroke-width="1"/>'
    '<path d="M14 12 H40 L46 16" stroke="#424242" stroke-width="2.6" fill="none"/><rect x="36" y="10" width="10" height="4" fill="#616161" stroke="none"/>'
    '<path d="M42 50 H48" stroke="#616161" stroke-width="3" stroke-linecap="round"/>'
    f'<rect x="16" y="28" width="28" height="14" rx="1" fill="{_R}" stroke="none"/>' + _W(t(30, 34, "PORTE COUPE-FEU", 2.9, "bold")) + _W(t(30, 39.5, "maintenir fermée", 2.8)))
add("inc_ventouse", "Ventouse électromagnétique de porte (maintien ouvert)", INC, 70, 60,
    '<rect x="2" y="2" width="12" height="56" fill="#bcaaa4" stroke="CC" stroke-width="1"/>'
    '<rect x="14" y="20" width="16" height="20" rx="2" fill="#9e9e9e" stroke="CC" stroke-width="1"/><circle cx="22" cy="30" r="5" fill="#616161" stroke="#424242" stroke-width="0.8"/>'
    '<rect x="34" y="22" width="4" height="16" fill="#bdbdbd" stroke="CC" stroke-width="0.8"/><path d="M38 24 H44 M38 36 H44" stroke="CC" stroke-width="1"/>'
    '<rect x="44" y="4" width="8" height="52" fill="#cfd8dc" stroke="CC" stroke-width="1"/>'
    '<path d="M30 26 H33 M30 34 H33" stroke="#e53935" stroke-width="1" stroke-dasharray="1 1"/>' + t(28, 56, "24 V", 5) + '<path d="M8 40 Q8 50 20 50" stroke="#e53935" stroke-width="1" fill="none"/>')
add("inc_cmsi", "Centrale incendie / CMSI (tableau de signalisation)", INC, 80, 60,
    '<rect x="4" y="4" width="72" height="52" rx="3" fill="#eceff1" stroke="CC" stroke-width="1.6"/>'
    f'<rect x="4" y="4" width="72" height="10" rx="3" fill="{_R}" stroke="none"/>' + _W(t(40, 11, "SÉCURITÉ INCENDIE", 4.8, "bold"))
    + '<rect x="10" y="18" width="34" height="14" fill="#263238" stroke="none"/>' + _W(t(27, 27, "ZONE 2 : FEU", 4.2, "bold"))
    + "".join(f'<circle cx="{52 + (i % 3) * 8}" cy="{21 + (i // 3) * 8}" r="2.4" fill="{c}" stroke="none"/>' for i, c in enumerate(("#e53935", "#fdd835", "#43a047", "#e53935", "#fdd835", "#43a047")))
    + "".join(f'<rect x="{10 + i * 13}" y="38" width="10" height="7" rx="1.5" fill="#90a4ae" stroke="CC" stroke-width="0.6"/>' for i in range(5))
    + t(14, 51, "Arrêt", 3.4) + t(27, 51, "Réarm.", 3.4) + t(40, 51, "Évac.", 3.4) + t(53, 51, "Test", 3.4) + t(66, 51, "Acq.", 3.4))
add("inc_uga", "Unité de gestion d'alarme (UGA)", INC, 70, 50,
    '<rect x="4" y="4" width="62" height="42" rx="3" fill="#fafafa" stroke="CC" stroke-width="1.6"/>' + t(35, 14, "UGA", 8, "bold")
    + '<circle cx="18" cy="28" r="4" fill="#e53935" stroke="CC" stroke-width="0.8"/><circle cx="32" cy="28" r="4" fill="#fdd835" stroke="CC" stroke-width="0.8"/><circle cx="46" cy="28" r="4" fill="#43a047" stroke="CC" stroke-width="0.8"/>'
    + '<rect x="14" y="36" width="42" height="6" rx="1.5" fill="#90a4ae" stroke="none"/>')
add("inc_desenfumage", "Commande manuelle de désenfumage", INC, 50, 50,
    '<rect x="4" y="4" width="42" height="42" rx="4" fill="#ff9800" stroke="CC" stroke-width="1.4"/><rect x="10" y="10" width="30" height="30" rx="2" fill="#ffffff" stroke="#e65100" stroke-width="1"/>'
    + "".join(f'<path d="M{16 + i * 6} 34 Q{12 + i * 6} 26 {18 + i * 6} 20 Q{22 + i * 6} 14 {18 + i * 6} 12" stroke="#757575" stroke-width="1.6" fill="none"/>' for i in range(3))
    + t(25, 44.5, "DÉSENFUMAGE", 3.4, "bold"))

add("sinc_extincteur", "Extincteur (panneau)", SINC, 60, 60, _red(
    '<rect x="20" y="22" width="14" height="30" rx="6" fill="#ffffff"/><rect x="23" y="16" width="8" height="7" fill="#ffffff"/><path d="M31 18 Q42 18 42 32 L46 40" stroke="#ffffff" stroke-width="2.4" fill="none"/>'
    '<path d="M44 8 Q50 14 46 20 Q42 14 44 8 Z" fill="#ffffff"/>'))
add("sinc_ria", "Robinet d'incendie armé (panneau)", SINC, 60, 60, _red(
    "".join(f'<circle cx="26" cy="30" r="{r}" fill="none" stroke="#ffffff" stroke-width="3.4"/>' for r in (18, 12)) + '<circle cx="26" cy="30" r="4" fill="#ffffff"/>'
    '<path d="M44 30 Q52 40 46 50 L42 48" stroke="#ffffff" stroke-width="2.4" fill="none"/><path d="M48 6 Q54 12 50 18 Q46 12 48 6 Z" fill="#ffffff"/>'))
add("sinc_declencheur", "Déclencheur manuel d'alarme incendie (panneau)", SINC, 60, 60, _red(
    '<rect x="14" y="14" width="22" height="22" rx="2" fill="none" stroke="#ffffff" stroke-width="2.4"/><rect x="21" y="21" width="8" height="8" fill="#ffffff"/>'
    '<path d="M40 50 Q36 40 40 34 L46 30 Q50 30 50 34 L48 42 Q54 44 52 50 Z" fill="#ffffff"/><path d="M44 30 L36 26" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>'
    '<path d="M48 8 Q54 14 50 20 Q46 14 48 8 Z" fill="#ffffff"/>'))
add("sinc_telephone", "Téléphone à utiliser en cas d'incendie (panneau)", SINC, 60, 60, _red(
    '<path d="M14 22 Q14 16 20 16 L24 22 L20 26 Q24 34 32 38 L36 34 L42 38 Q42 44 36 44 Q16 40 14 22 Z" fill="#ffffff"/>'
    '<path d="M46 8 Q52 14 48 20 Q44 14 46 8 Z" fill="#ffffff"/>'))
add("sinc_alarme", "Alarme incendie – sirène (panneau)", SINC, 60, 60, _red(
    '<path d="M12 24 H20 L32 14 V46 L20 36 H12 Z" fill="#ffffff"/>'
    + "".join(f'<path d="M{36 + i * 5} {22 - i * 3} Q{41 + i * 7} 30 {36 + i * 5} {38 + i * 3}" stroke="#ffffff" stroke-width="2.4" fill="none"/>' for i in range(3))))
add("sinc_sortie", "Sortie de secours (panneau)", SINC, 90, 50,
    f'<rect x="2" y="2" width="86" height="46" rx="3" fill="{_V}" stroke="none"/>' + _runner(12, 7, 0.95) + '<path d="M44 8 H62 V42 H44" stroke="#ffffff" stroke-width="2.6" fill="none"/>'
    + '<rect x="47" y="11" width="12" height="28" fill="none" stroke="#ffffff" stroke-width="1"/>' + _arrow(76, 25, 1.3))
add("sinc_fleche", "Flèche directionnelle d'évacuation", SINC, 50, 50, f'<rect x="2" y="2" width="46" height="46" rx="3" fill="{_V}" stroke="none"/>' + _arrow(25, 25, 1.9))
add("sinc_escalier", "Évacuation par l'escalier (panneau)", SINC, 60, 60,
    f'<rect x="2" y="2" width="56" height="56" rx="3" fill="{_V}" stroke="none"/><path d="M8 50 H20 V42 H30 V34 H40 V26 H52" stroke="#ffffff" stroke-width="3" fill="none"/>' + _runner(14, 6, 0.75))
add("sinc_rassemblement", "Point de rassemblement (panneau)", SINC, 60, 60,
    f'<rect x="2" y="2" width="56" height="56" rx="3" fill="{_V}" stroke="none"/>'
    + "".join(f'<g transform="translate({x} 22)"><circle cx="0" cy="0" r="3.2" fill="#ffffff"/><path d="M0 5 V16 M-3 24 L0 16 L3 24 M-5 10 H5" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round" fill="none"/></g>' for x in (20, 30, 40))
    + "".join(_arrow(30 + 22 * math.cos(math.radians(a)), 30 + 22 * math.sin(math.radians(a)), 0.55, "#ffffff", a + 180) for a in (45, 135, 225, 315)))
add("sinc_ascenseur", "Ne pas utiliser l'ascenseur en cas d'incendie", SINC, 60, 60,
    '<circle cx="30" cy="30" r="26" fill="#ffffff" stroke="#d32f2f" stroke-width="5"/>'
    '<rect x="18" y="14" width="24" height="32" fill="none" stroke="CC" stroke-width="2.4"/><path d="M30 14 V46" stroke="CC" stroke-width="1.6"/>'
    '<path d="M22 22 L25 18 L28 22 M32 18 L35 22 L38 18" stroke="CC" stroke-width="1.6" fill="none"/><path d="M12 12 L48 48" stroke="#d32f2f" stroke-width="5"/>')
add("sinc_ne_pas_encombrer", "Porte coupe-feu – ne pas encombrer, maintenir fermée", SINC, 80, 40,
    '<rect x="2" y="2" width="76" height="36" rx="3" fill="#ffffff" stroke="#1565c0" stroke-width="2.4"/>'
    '<circle cx="18" cy="20" r="12" fill="#1565c0" stroke="none"/><path d="M12 12 H22 V28 H12 Z" stroke="#ffffff" stroke-width="1.6" fill="none"/><path d="M22 14 L26 20 L22 26" stroke="#ffffff" stroke-width="1.6" fill="none"/>'
    + t(52, 16, "PORTE COUPE-FEU", 5.2, "bold") + t(52, 24, "à maintenir fermée", 4.6) + t(52, 31, "ne pas encombrer", 4.6))

# ---------------------------------------------------------------- retours du 4/11 (2)
add("gqs_heimlich", "Étouffement : compressions abdominales (méthode de Heimlich)", GQS, 70, 70,
    '<path d="M4 66 H66" stroke="#9e9e9e" stroke-width="1.2"/>'
    # sauveteur derrière la victime : tronc et jambes écartées, en appui
    + _head(44, 8, 6) + _seg([(44, 15), (45, 40)], _SAU, 9)
    + _seg([(44, 40), (52, 52), (56, 65)], "#455a64", 6) + _seg([(46, 40), (40, 52), (42, 65)], "#455a64", 6)
    # victime devant, légèrement penchée
    + _head(28, 13, 6) + _seg([(29, 20), (31, 42)], _VIC, 11) + _seg([(29, 42), (26, 64)], "#37474f", 6) + _seg([(33, 42), (34, 64)], "#37474f", 6)
    # bras du sauveteur autour de l'abdomen, poing sous le sternum
    + _seg([(45, 22), (22, 30), (30, 34)], _SAU, 4.4) + _seg([(45, 24), (40, 34), (31, 34)], _SAU, 4.4)
    + '<circle cx="30" cy="34" r="3.6" fill="' + _SK + '" stroke="CC" stroke-width="0.8"/>'
    + '<path d="M16 41 L25 35 M21 34 L25 35 L23 39" stroke="CC" stroke-width="1.4" fill="none"/>' + t(62, 58, "×5", 7, "bold"))

_LEDC = {"Rouge": ("#ef5350", "#b71c1c"), "Verte": ("#66bb6a", "#1b5e20"), "Orange": ("#ffa726", "#e65100"),
         "Jaune": ("#ffee58", "#f9a825"), "Bleue": ("#42a5f5", "#0d47a1"), "Transparente": ("#f5f5f5", "#9e9e9e")}


def _led(p):
    f, s = _LEDC.get(p.get("couleur"), _LEDC["Rouge"])
    clair = p.get("couleur") == "Transparente"
    body = (f'<path d="M7 28 V12 Q7 4 15 4 Q23 4 23 12 V28 Z" fill="{f}" fill-opacity="{0.55 if clair else 0.85}" stroke="{s}" stroke-width="1"/>'
            f'<rect x="5" y="28" width="20" height="3" fill="{f}" stroke="{s}" stroke-width="0.8"/>'
            '<path d="M11 31 V56 M19 31 V50" stroke="#9e9e9e" stroke-width="1.4"/>'
            '<path d="M11 28 V18 L15 14 M19 28 V20 H15" stroke="#9e9e9e" stroke-width="0.8" fill="none" stroke-opacity="0.8"/>'
            '<path d="M10 9 Q11 6 14 6" stroke="#ffffff" stroke-width="1.4" fill="none"/>'
            + t(8, 56, "+", 6, "bold") + t(24, 52, "−", 6, "bold"))
    return 30, 60, body


add("rob_led", "LED 5 mm (anode +, cathode −)", ROB, params=[("couleur", "Couleur", "Rouge", list(_LEDC))], func=_led)

_CC = [("noir", "#212121"), ("marron", "#795548"), ("rouge", "#e53935"), ("orange", "#fb8c00"), ("jaune", "#fdd835"),
       ("vert", "#43a047"), ("bleu", "#1e88e5"), ("violet", "#8e24aa"), ("gris", "#9e9e9e"), ("blanc", "#fafafa")]
_OR, _ARG = "#c8a43c", "#cfd8dc"
_VALS = ["10 Ω", "47 Ω", "100 Ω", "150 Ω", "220 Ω", "330 Ω", "470 Ω", "680 Ω", "1 kΩ", "1,5 kΩ", "2,2 kΩ", "3,3 kΩ",
         "4,7 kΩ", "6,8 kΩ", "10 kΩ", "22 kΩ", "47 kΩ", "100 kΩ", "220 kΩ", "470 kΩ", "1 MΩ"]


def _bands(val):
    num = float(val.split()[0].replace(",", "."))
    unit = val.split()[1]
    ohms = num * {"Ω": 1, "kΩ": 1e3, "MΩ": 1e6}[unit]
    e = int(math.floor(math.log10(ohms))) - 1
    d = int(round(ohms / 10 ** e))
    return [_CC[d // 10][1], _CC[d % 10][1], _CC[e][1] if e >= 0 else _OR]


def _resistance(p):
    b = _bands(p.get("valeur", "220 Ω")) + [_OR if p.get("tolerance", "± 5 % (or)") == "± 5 % (or)" else (_ARG if "10" in p["tolerance"] else _CC[1][1])]
    body = ('<path d="M2 12 H14 M56 12 H68" stroke="#9e9e9e" stroke-width="1.4"/>'
            '<rect x="14" y="5" width="42" height="14" rx="6" fill="#e6d3b3" stroke="#8d6e63" stroke-width="0.8"/>'
            + "".join(f'<rect x="{x}" y="5" width="3.4" height="14" fill="{c}" stroke="#5d4037" stroke-width="0.3"/>' for x, c in zip((20, 26, 32, 46), b)))
    if p.get("afficher", "Oui") == "Oui":
        body += t(35, 28, p.get("valeur", ""), 6, "bold")
    return 70, 32, body


add("rob_resistance", "Résistance (anneaux de couleur selon la valeur)", ROB,
    params=[("valeur", "Valeur", "220 Ω", _VALS), ("tolerance", "Tolérance", "± 5 % (or)", ["± 5 % (or)", "± 10 % (argent)", "± 1 % (marron)"]),
            ("afficher", "Afficher la valeur", "Oui", ["Oui", "Non"])], func=_resistance)


def _code_couleurs():
    rows = [("Noir", 0, "× 1", ""), ("Marron", 1, "× 10", "± 1 %"), ("Rouge", 2, "× 100", "± 2 %"), ("Orange", 3, "× 1 k", ""),
            ("Jaune", 4, "× 10 k", ""), ("Vert", 5, "× 100 k", "± 0,5 %"), ("Bleu", 6, "× 1 M", "± 0,25 %"), ("Violet", 7, "× 10 M", "± 0,1 %"),
            ("Gris", 8, "", "± 0,05 %"), ("Blanc", 9, "", ""), ("Or", "", "× 0,1", "± 5 %"), ("Argent", "", "× 0,01", "± 10 %")]
    cols = [(4, 36, "Couleur"), (40, 26, "1er chiffre"), (66, 26, "2e chiffre"), (92, 30, "Multiplicateur"), (122, 34, "Tolérance")]
    W, H, rh = 160, 16 + len(rows) * 9 + 20, 9
    body = '<rect x="2" y="2" width="156" height="%d" rx="2" fill="#ffffff" stroke="CC" stroke-width="1"/>' % (H - 4)
    body += '<rect x="2" y="2" width="156" height="12" fill="#dce8f5" stroke="none"/>'
    for x, w, h in cols:
        body += t(x + w / 2, 10, h, 4.2, "bold")
    sw = [c for _, c in _CC] + [_OR, _ARG]
    for i, (name, dig, mul, tol) in enumerate(rows):
        y = 14 + i * rh
        body += f'<rect x="4" y="{y + 1}" width="10" height="{rh - 2}" fill="{sw[i]}" stroke="#757575" stroke-width="0.4"/>'
        body += t(26, y + 6.4, name, 4.4)
        for x, w, v in ((40, 26, dig), (66, 26, dig), (92, 30, mul), (122, 34, tol)):
            body += t(x + w / 2, y + 6.4, str(v), 4.4)
        body += f'<path d="M2 {y + rh} H158" stroke="#cfd8dc" stroke-width="0.4"/>'
    yb = 14 + len(rows) * rh + 4
    body += ('<path d="M30 %d H44 M90 %d H104" stroke="#9e9e9e" stroke-width="1"/><rect x="44" y="%d" width="46" height="10" rx="4" fill="#e6d3b3" stroke="#8d6e63" stroke-width="0.6"/>' % (yb + 5, yb + 5, yb)
             + "".join(f'<rect x="{x}" y="{yb}" width="3" height="10" fill="{c}" stroke="none"/>' for x, c in ((50, _CC[2][1]), (56, _CC[2][1]), (62, _CC[1][1]), (80, _OR)))
             + t(132, yb + 7, "= 220 Ω ± 5 %", 4.6, "bold"))
    return W, H, body


_w, _h, _b = _code_couleurs()
add("rob_code_couleurs", "Tableau du code des couleurs des résistances", ROB, _w, _h, _b)

_GP = [("3V3", "p3"), ("5V", "p5"), ("GPIO2 SDA", "i2c"), ("5V", "p5"), ("GPIO3 SCL", "i2c"), ("GND", "g"), ("GPIO4", "io"), ("GPIO14 TXD", "uart"),
       ("GND", "g"), ("GPIO15 RXD", "uart"), ("GPIO17", "io"), ("GPIO18 PWM", "io"), ("GPIO27", "io"), ("GND", "g"), ("GPIO22", "io"), ("GPIO23", "io"),
       ("3V3", "p3"), ("GPIO24", "io"), ("GPIO10 MOSI", "spi"), ("GND", "g"), ("GPIO9 MISO", "spi"), ("GPIO25", "io"), ("GPIO11 SCLK", "spi"), ("GPIO8 CE0", "spi"),
       ("GND", "g"), ("GPIO7 CE1", "spi"), ("ID_SD", "id"), ("ID_SC", "id"), ("GPIO5", "io"), ("GND", "g"), ("GPIO6", "io"), ("GPIO12 PWM", "io"),
       ("GPIO13 PWM", "io"), ("GND", "g"), ("GPIO19", "io"), ("GPIO16", "io"), ("GPIO26", "io"), ("GPIO20", "io"), ("GND", "g"), ("GPIO21", "io")]
_GPC = {"p3": ("#ff9800", "#000000"), "p5": ("#e53935", "#ffffff"), "g": ("#212121", "#ffffff"), "io": ("#43a047", "#ffffff"),
        "i2c": ("#1e88e5", "#ffffff"), "spi": ("#8e24aa", "#ffffff"), "uart": ("#fdd835", "#000000"), "id": ("#bdbdbd", "#000000")}


def _gpio():
    W, rh = 150, 8
    H = 20 * rh + 36
    body = f'<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="3" fill="#ffffff" stroke="CC" stroke-width="1"/>'
    body += t(W / 2, 11, "Raspberry Pi – connecteur GPIO 40 broches", 5.2, "bold")
    body += '<rect x="58" y="16" width="34" height="%d" rx="1.5" fill="#263238" stroke="none"/>' % (20 * rh + 2)
    for i, (lab, k) in enumerate(_GP):
        r, c = i // 2, i % 2
        y = 17 + r * rh
        bg, fg = _GPC[k]
        cx = 70 if c == 0 else 80
        body += f'<circle cx="{cx}" cy="{y + rh / 2}" r="2.6" fill="{bg}" stroke="#ffffff" stroke-width="0.4"/>'
        x = 4 if c == 0 else 94
        body += f'<rect x="{x}" y="{y + 0.6}" width="52" height="{rh - 1.2}" rx="1.5" fill="{bg}" stroke="none"/>'
        num = str(i + 1)
        if c == 0:
            body += f'<text x="{x + 50}" y="{y + 5.6}" font-size="4.4" text-anchor="end" fill="{fg}" stroke="none" font-family="DejaVu Sans">{lab}</text>'
            body += f'<text x="{cx - 4}" y="{y + 5.6}" font-size="3.6" text-anchor="end" fill="#ffffff" stroke="none" font-family="DejaVu Sans" opacity="0">{num}</text>'
        else:
            body += f'<text x="{x + 2}" y="{y + 5.6}" font-size="4.4" fill="{fg}" stroke="none" font-family="DejaVu Sans">{lab}</text>'
        body += f'<text x="{60 if c == 0 else 90}" y="{y + 5.4}" font-size="3.4" text-anchor="{"end" if c == 0 else "start"}" fill="#455a64" stroke="none" font-family="DejaVu Sans"></text>'
        body += f'<text x="{cx + (-4 if c == 0 else 4)}" y="{y + 5.4}" font-size="3.2" text-anchor="{"end" if c == 0 else "start"}" fill="#ffffff" stroke="none" font-family="DejaVu Sans" font-weight="bold">{num}</text>'
    ly = 17 + 20 * rh + 6
    for j, (k, lab) in enumerate((("p3", "3,3 V"), ("p5", "5 V"), ("g", "GND"), ("io", "GPIO"), ("i2c", "I²C"), ("spi", "SPI"), ("uart", "UART"))):
        x = 8 + j * 20
        body += f'<rect x="{x}" y="{ly}" width="5" height="5" fill="{_GPC[k][0]}" stroke="#757575" stroke-width="0.3"/>' + f'<text x="{x + 6.5}" y="{ly + 4.4}" font-size="4.2" fill="CC" stroke="none" font-family="DejaVu Sans">{lab}</text>'
    return W, H, body


_w, _h, _b = _gpio()
add("rob_gpio_brochage", "Brochage du connecteur GPIO Raspberry Pi (40 broches)", ROB, _w, _h, _b)
add("rob_sensehat", "Carte d'extension Sense HAT (matrice 8×8, joystick, capteurs)", ROB, 90, 60,
    f'<rect x="2" y="2" width="86" height="56" rx="3" fill="{_PCB_RPI}" stroke="#1b5e20" stroke-width="1"/>'
    '<rect x="8" y="3.5" width="52" height="6" fill="#212121" stroke="none"/>'
    '<rect x="12" y="14" width="40" height="40" rx="1" fill="#212121" stroke="none"/>'
    + "".join(f'<rect x="{14 + c * 4.8:.1f}" y="{16 + r * 4.8:.1f}" width="3.6" height="3.6" rx="0.6" fill="{("#e53935", "#fb8c00", "#fdd835", "#43a047", "#1e88e5", "#8e24aa", "#ec407a", "#26c6da")[(r + c) % 8]}" stroke="none"/>' for r in range(8) for c in range(8))
    + '<rect x="62" y="38" width="12" height="12" rx="1" fill="#424242" stroke="none"/><circle cx="68" cy="44" r="3.4" fill="#212121" stroke="#9e9e9e" stroke-width="0.6"/>'
    '<rect x="62" y="16" width="6" height="6" fill="#263238" stroke="none"/><rect x="72" y="16" width="6" height="6" fill="#263238" stroke="none"/><rect x="62" y="26" width="6" height="6" fill="#263238" stroke="none"/>'
    + _W(t(76, 56, "joystick", 3)) + _hole(6, 6) + _hole(84, 6) + _hole(6, 54) + _hole(84, 54))
add("rob_dht22", "Capteur température et humidité (DHT22 / AM2302)", ROB, 40, 60,
    '<rect x="6" y="4" width="28" height="40" rx="2" fill="#fafafa" stroke="#9e9e9e" stroke-width="1"/>'
    + "".join(f'<rect x="{10 + c * 6}" y="{8 + r * 6}" width="4" height="3" fill="#bdbdbd" stroke="none"/>' for r in range(5) for c in range(4))
    + '<path d="M12 44 V58 M18 44 V58 M24 44 V58 M30 44 V58" stroke="#9e9e9e" stroke-width="1.4"/>' + t(20, 41, "DHT22", 4, "bold"))

# ---------------------------------------------------------------- retours du 4/11 (3) : arrêt d'urgence, main nue barrée
def _main_plate(fill="#ffffff", stroke="CC", sw=1.2):
    """Main ouverte vue de côté, paume vers le bas, doigts tendus vers la gauche (dessin original)."""
    return (f'<path d="M60 2 L46 4 C38 5 30 7 22 10 L8 15 C4 16.5 4 20 8 20 L22 17.5 '
            f'L10 22 C6 23.5 6.5 27 10.5 26.5 L24 23 L14 27.5 C10 29 11 32.5 15 31.5 L28 27.5 '
            f'C30 29 32 30 36 29 L44 26 C50 25 56 24 60 20 Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<path d="M36 29 C34 32 33 35 35 36 C37 37 39 34 41 30" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')


def _main_ouverte(fill, stroke="CC", sw=1.2):
    """Main nue ouverte vue de face, doigts écartés, pouce sur le côté (dessin original)."""
    f = f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
    return (f'<rect x="-2.7" y="-12" width="5.4" height="14" rx="2.7" {f} transform="translate(-8 6) rotate(-40)"/>'
            + "".join(f'<rect x="{x - 2.4}" y="{-2 - l}" width="4.8" height="{l + 6}" rx="2.4" {f} transform="rotate({a} {x} -2)"/>'
                      for x, l, a in ((-6.6, 10, -8), (-2.2, 13, -2), (2.2, 12.5, 2), (6.6, 9.5, 8)))
            + f'<path d="M-9 -1 H9 V10 Q9 19 0 19 Q-9 19 -9 10 Z" {f}/>'
            + f'<rect x="-8.3" y="-2" width="16.6" height="3" fill="{fill}" stroke="none"/>')


add("gqs_arret_urgence", "Électrisation : appuyer sur l'arrêt d'urgence (coup de poing)", GQS, 80, 80,
    # boîtier jaune en perspective, socle noir
    '<path d="M12 50 L40 40 L70 50 L42 62 Z" fill="#fdd835" stroke="CC" stroke-width="1.2"/>'
    '<path d="M12 50 V62 L42 74 V62 Z" fill="#f9a825" stroke="CC" stroke-width="1.2"/><path d="M42 62 V74 L70 62 V50 Z" fill="#fbc02d" stroke="CC" stroke-width="1.2"/>'
    '<path d="M12 58 L42 70 L70 58" stroke="#424242" stroke-width="5" fill="none"/>'
    # champignon rouge
    '<ellipse cx="41" cy="50" rx="9" ry="3.6" fill="#212121" stroke="none"/><path d="M36 50 V45 H46 V50" fill="#212121" stroke="none"/>'
    '<path d="M27 45 C27 34 55 34 55 45 C55 49 27 49 27 45 Z" fill="#e53935" stroke="CC" stroke-width="1.2"/>'
    '<ellipse cx="41" cy="40" rx="11" ry="3.6" fill="#ef5350" stroke="none"/>'
    # main qui frappe, avec flèche de mouvement
    '<g transform="translate(30 2) scale(0.78)">' + _main_plate("#f2c6a0") + '</g>'
    '<path d="M64 26 V36 M60 32 L64 37 L68 32" stroke="' + _SAU + '" stroke-width="1.8" fill="none"/>'
    '<path d="M30 30 L26 28 M31 34 L26 34" stroke="CC" stroke-width="1.2"/>')
add("gqs_arret_urgence_panneau", "Bouton d'arrêt d'urgence (panneau)", GQS, 60, 76,
    '<g stroke="none"><rect x="2" y="2" width="56" height="52" rx="2" fill="#c62828"/><rect x="2" y="57" width="56" height="17" rx="3" fill="#c62828"/></g>'
    '<g transform="translate(20 6) scale(0.62)">' + _main_plate("#ffffff", "#ffffff", 0.6) + '</g>'
    '<path d="M22 34 C22 28 38 28 38 34 Z" fill="#ffffff" stroke="none"/><rect x="28" y="34" width="4" height="8" fill="#ffffff" stroke="none"/>'
    '<path d="M8 44 H25 V41 H35 V44 H52" stroke="#ffffff" stroke-width="1.6" fill="none"/>'
    + _W(t(30, 64, "Bouton d'arrêt", 5.4, "bold")) + _W(t(30, 71, "d'urgence", 5.4, "bold")))
add("gqs_ne_pas_toucher", "Électrisation : ne pas toucher la victime à mains nues", GQS, 60, 60,
    '<circle cx="30" cy="30" r="26" fill="#ffffff" stroke="#d32f2f" stroke-width="5"/>'
    '<g transform="translate(30 33) scale(1.15)">' + _main_ouverte("#f2c6a0") + '</g>'
    '<path d="M48 8 L43 18 H48 L44 27 L53 15 H48 L51 8 Z" fill="#fdd835" stroke="CC" stroke-width="0.6"/>'
    '<path d="M12 12 L48 48" stroke="#d32f2f" stroke-width="5"/>')
add("gqs_ne_pas_toucher_victime", "Électrisation : ne pas toucher la victime à mains nues (avec la victime)", GQS, 100, 64,
    '<path d="M2 60 H98" stroke="#9e9e9e" stroke-width="1.2"/>'
    # victime au sol, câble et éclair
    + _head(52, 51, 5.5) + _seg([(59, 53), (82, 53)], _VIC, 8) + _seg([(82, 54), (97, 55)], "#37474f", 6) + _seg([(48, 55), (38, 58)], _VIC, 3.4)
    + '<path d="M78 30 Q68 37 56 39 Q42 41 39 56" stroke="#212121" stroke-width="1.8" fill="none"/>'
    + '<path d="M36 52 L33 49 M41 51 L44 48 M38 50 V46" stroke="#fdd835" stroke-width="1.4"/>'
    + '<path d="M80 6 L74 18 H80 L76 28 L87 14 H81 L84 6 Z" fill="#fdd835" stroke="CC" stroke-width="0.7"/>'
    # main nue barrée qui s'approche
    + '<circle cx="26" cy="26" r="21" fill="#ffffff" stroke="#d32f2f" stroke-width="4.4"/>'
    + '<g transform="translate(26 28) scale(0.95)">' + _main_ouverte("#f2c6a0") + '</g>'
    + '<path d="M11 11 L41 41" stroke="#d32f2f" stroke-width="4.4"/>')

# ================================================================ équipements industriels (électrotechnique), habitat
IND = "Équipements industriels – électrotechnique"
HAB = "Habitat – GTL, chauffage, éclairage"
_ACIER, _JAUNE_IND, _EAU = "#90a4ae", "#fbc02d", "#4fc3f7"


def _barriere(p):
    ang = {"Fermée (bas)": 0, "Mi-course (milieu)": -45, "Ouverte (haut)": -88}.get(p.get("position"), 0)
    arm = '<rect x="0" y="-3" width="62" height="6" rx="2" fill="#ffffff" stroke="CC" stroke-width="1"/>'
    arm += "".join(f'<rect x="{x}" y="-3" width="7" height="6" fill="#e53935" stroke="none"/>' for x in range(8, 62, 14))
    body = ('<path d="M2 97 H98" stroke="#9e9e9e" stroke-width="1.2"/>'
            '<path d="M86 97 V72 M82 72 H90" stroke="CC" stroke-width="2"/>'
            f'<g transform="translate(14 68) rotate({ang})">{arm}</g>'
            f'<rect x="4" y="64" width="20" height="33" rx="2" fill="{_JAUNE_IND}" stroke="CC" stroke-width="1.2"/>'
            '<circle cx="14" cy="68" r="3" fill="#424242" stroke="CC" stroke-width="0.8"/><rect x="8" y="78" width="12" height="8" rx="1" fill="#424242" stroke="none"/>'
            + t(14, 84, "M", 5, "bold").replace('fill="CC"', 'fill="#ffffff"'))
    return 100, 100, body


add("ind_barriere", "Barrière levante motorisée (position réglable)", IND,
    params=[("position", "Position", "Fermée (bas)", ["Fermée (bas)", "Mi-course (milieu)", "Ouverte (haut)"])], func=_barriere)


def _ventilateur(p):
    on = p.get("etat") == "En marche"
    body = '<circle cx="30" cy="28" r="24" fill="#eceff1" stroke="CC" stroke-width="1.6"/>'
    body += "".join(f'<g transform="rotate({a} 30 28)"><path d="M30 28 C26 18 28 8 34 6 C40 10 38 20 30 28 Z" fill="#1e88e5" stroke="CC" stroke-width="0.8"/></g>' for a in (0, 120, 240))
    body += '<circle cx="30" cy="28" r="4" fill="#424242" stroke="none"/>'
    body += "".join(f'<circle cx="30" cy="28" r="{r}" fill="none" stroke="#9e9e9e" stroke-width="0.6"/>' for r in (10, 16, 22))
    body += '<path d="M30 52 V62 M20 64 H40" stroke="CC" stroke-width="3"/>'
    if on:
        body += '<path d="M8 12 A26 26 0 0 1 20 4 M52 44 A26 26 0 0 1 40 52" stroke="#43a047" stroke-width="2" fill="none"/>'
    return 60, 66, body


add("ind_ventilateur", "Ventilateur industriel", IND, params=[("etat", "État", "Arrêté", ["Arrêté", "En marche"])], func=_ventilateur)


def _tapis(p):
    sens = 1 if p.get("sens", "→ vers la droite").startswith("→") else -1
    body = ('<rect x="10" y="22" width="90" height="10" rx="5" fill="#37474f" stroke="CC" stroke-width="1"/>'
            '<circle cx="15" cy="27" r="5" fill="#90a4ae" stroke="CC" stroke-width="0.8"/><circle cx="95" cy="27" r="5" fill="#90a4ae" stroke="CC" stroke-width="0.8"/>'
            '<path d="M20 32 V44 M90 32 V44 M16 44 H24 M86 44 H94" stroke="CC" stroke-width="2"/>'
            f'<circle cx="{95 if sens > 0 else 15}" cy="38" r="5" fill="#ffffff" stroke="CC" stroke-width="1"/>' + t(95 if sens > 0 else 15, 40, "M", 5, "bold")
            + _box(30, 4, 16, 18) + _box(60, 6, 14, 16))
    ax = 55
    body += (f'<path d="M{ax - 10 * sens} 15 H{ax + 8 * sens}" stroke="#e53935" stroke-width="1.8"/>'
             f'<path d="M{ax + 8 * sens} 11 L{ax + 13 * sens} 15 L{ax + 8 * sens} 19 Z" fill="#e53935" stroke="none"/>')
    return 110, 46, body


add("ind_tapis", "Tapis roulant (convoyeur à bande)", IND, params=[("sens", "Sens", "→ vers la droite", ["→ vers la droite", "← vers la gauche"])], func=_tapis)


def _malaxeur(p):
    on = p.get("etat") == "En marche"
    body = ('<rect x="20" y="2" width="20" height="14" rx="2" fill="#1e88e5" stroke="CC" stroke-width="1"/>' + _W(t(30, 12, "M", 6, "bold"))
            + '<path d="M30 16 V64" stroke="#616161" stroke-width="2.4"/>'
            '<path d="M6 22 H54 V58 L40 72 H20 L6 58 Z" fill="#eceff1" stroke="CC" stroke-width="1.6"/>'
            '<path d="M8 36 H52 V58 L40 70 H20 L8 58 Z" fill="#bcaaa4" fill-opacity="0.85" stroke="none"/>'
            '<path d="M18 48 L30 44 L42 48 M18 60 L30 56 L42 60" stroke="#424242" stroke-width="2.4" fill="none"/>'
            '<path d="M26 72 V78 H34 V72" stroke="CC" stroke-width="1.4" fill="none"/>')
    if on:
        body += '<path d="M14 30 A18 6 0 0 0 46 30" stroke="#43a047" stroke-width="1.8" fill="none"/><path d="M44 27 L47 31 L42 32" stroke="#43a047" stroke-width="1.6" fill="none"/>'
    return 60, 80, body


add("ind_malaxeur", "Malaxeur (cuve avec agitateur)", IND, params=[("etat", "État", "Arrêté", ["Arrêté", "En marche"])], func=_malaxeur)


def _monte_charge(p):
    x = {"Gauche": 24, "Milieu": 60, "Droite": 96}.get(p.get("horizontal"), 24)
    yb = {"Haut": 26, "Milieu": 48, "Bas": 70}.get(p.get("hauteur"), 70)
    body = ('<path d="M2 96 H118" stroke="#9e9e9e" stroke-width="1.2"/>'
            f'<path d="M8 10 V96 M112 10 V96" stroke="{_JAUNE_IND}" stroke-width="5"/>'
            f'<rect x="4" y="6" width="112" height="7" fill="{_JAUNE_IND}" stroke="CC" stroke-width="1"/>'
            f'<rect x="{x - 9}" y="13" width="18" height="8" rx="1.5" fill="#455a64" stroke="CC" stroke-width="0.8"/>'
            f'<circle cx="{x - 5}" cy="13" r="2" fill="#212121" stroke="none"/><circle cx="{x + 5}" cy="13" r="2" fill="#212121" stroke="none"/>'
            f'<path d="M{x} 21 V{yb - 6}" stroke="#424242" stroke-width="1.2"/><path d="M{x - 3} {yb - 7} Q{x} {yb - 1} {x + 3} {yb - 7}" stroke="#424242" stroke-width="1.6" fill="none"/>'
            f'<path d="M{x} {yb - 4} L{x - 10} {yb} M{x} {yb - 4} L{x + 10} {yb}" stroke="#616161" stroke-width="0.8"/>'
            + _box(x - 11, yb, 22, 22)
            + '<path d="M40 2 H50 M45 0 L50 2 L45 4 M80 2 H70 M75 0 L70 2 L75 4" stroke="#e53935" stroke-width="1.2" fill="none"/>')
    return 120, 98, body


add("ind_monte_charge", "Monte-charge à déplacement horizontal (pont roulant)", IND,
    params=[("horizontal", "Position horizontale", "Gauche", ["Gauche", "Milieu", "Droite"]), ("hauteur", "Hauteur de la charge", "Bas", ["Haut", "Milieu", "Bas"])],
    func=_monte_charge)


def _ascenseur(p):
    lvl = {"Rez-de-chaussée": 0, "1er étage": 1, "2e étage": 2}.get(p.get("etage"), 0)
    floors = [96, 64, 32]
    body = ('<rect x="14" y="2" width="40" height="96" fill="#fafafa" stroke="CC" stroke-width="1.4"/>'
            '<rect x="22" y="2" width="16" height="8" fill="#455a64" stroke="none"/><circle cx="30" cy="10" r="4" fill="#90a4ae" stroke="CC" stroke-width="0.8"/>'
            + _W(t(30, 8, "M", 5, "bold")))
    for i, y in enumerate(floors):
        body += f'<path d="M2 {y} H14 M54 {y} H66" stroke="CC" stroke-width="2"/>' + t(8, y - 4, ("RDC", "1er", "2e")[i], 4.6, "bold")
        on = i == lvl
        body += f'<rect x="54" y="{y - 14}" width="5" height="5" fill="{"#43a047" if on else "#cfd8dc"}" stroke="CC" stroke-width="0.6"/>'
    yc = floors[lvl]
    body += (f'<path d="M26 14 V{yc - 26}" stroke="#424242" stroke-width="1"/><path d="M34 14 V60" stroke="#424242" stroke-width="1"/>'
             '<rect x="44" y="50" width="7" height="12" fill="#616161" stroke="none"/><path d="M34 14 Q42 10 47 14 V50" stroke="#424242" stroke-width="1" fill="none"/>'
             f'<rect x="17" y="{yc - 26}" width="24" height="26" rx="1" fill="#bbdefb" stroke="CC" stroke-width="1.2"/>'
             f'<path d="M29 {yc - 22} V{yc}" stroke="#64b5f6" stroke-width="0.8"/>' + _head(29, yc - 17, 2.4) + _seg([(29, yc - 14), (29, yc - 6)], "#455a64", 2.4))
    return 68, 100, body


add("ind_ascenseur", "Ascenseur 3 niveaux (cabine et capteurs d'étage)", IND,
    params=[("etage", "Position de la cabine", "Rez-de-chaussée", ["Rez-de-chaussée", "1er étage", "2e étage"])], func=_ascenseur)

_NIV = {"Vide": 0.04, "Bas": 0.28, "Milieu": 0.58, "Haut": 0.88, "Plein": 0.97}
_NIV_L = list(_NIV)


def _cuve(x, y, w, h, niveau, sensors=True):
    f = _NIV.get(niveau, 0.5)
    hw = h * f
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#ffffff" stroke="CC" stroke-width="1.4"/>'
         f'<rect x="{x + 1}" y="{y + h - hw:.1f}" width="{w - 2}" height="{hw - 1:.1f}" fill="{_EAU}" fill-opacity="0.8" stroke="none"/>'
         f'<path d="M{x + 1} {y + h - hw:.1f} H{x + w - 1}" stroke="#0288d1" stroke-width="0.8"/>')
    if sensors:
        for lab, fr in (("H", 0.8), ("M", 0.5), ("B", 0.2)):
            yy = y + h - h * fr
            wet = f >= fr
            s += (f'<path d="M{x + w} {yy:.1f} H{x + w + 6}" stroke="CC" stroke-width="1"/>'
                  f'<circle cx="{x + w + 9}" cy="{yy:.1f}" r="2.6" fill="{"#43a047" if wet else "#e0e0e0"}" stroke="CC" stroke-width="0.6"/>'
                  + t(x + w + 15, yy + 1.8, lab, 4.6, "bold"))
    return s


def _reservoir(p):
    return 60, 70, _cuve(6, 6, 34, 58, p.get("niveau", "Milieu"))


add("ind_reservoir", "Réservoir avec capteurs de niveau haut, milieu, bas", IND,
    params=[("niveau", "Niveau d'eau", "Milieu", _NIV_L)], func=_reservoir)


def _chateau(p):
    body = (_cuve(14, 4, 40, 34, p.get("niveau", "Milieu"))
            + '<path d="M18 38 L12 96 M50 38 L56 96 M16 60 H52 M14 80 H54 M17 50 L51 70 M51 50 L17 70" stroke="#78909c" stroke-width="1.6" fill="none"/>'
            '<path d="M34 38 V96" stroke="#1e88e5" stroke-width="2.4"/><path d="M4 96 H70" stroke="#9e9e9e" stroke-width="1.2"/>')
    return 72, 98, body


add("ind_chateau_eau", "Château d'eau (niveau réglable, capteurs H M B)", IND,
    params=[("niveau", "Niveau d'eau", "Milieu", _NIV_L)], func=_chateau)


def _puits(p):
    f = _NIV.get(p.get("niveau", "Milieu"), 0.5)
    body = ('<rect x="0" y="16" width="60" height="70" fill="#d7ccc8" stroke="none"/><path d="M0 16 H60" stroke="#6d4c41" stroke-width="1.4"/>'
            '<rect x="20" y="10" width="20" height="76" fill="#ffffff" stroke="CC" stroke-width="1.4"/>'
            f'<rect x="21" y="{86 - 66 * f:.1f}" width="18" height="{66 * f - 1:.1f}" fill="{_EAU}" fill-opacity="0.85" stroke="none"/>')
    for lab, fr in (("H", 0.8), ("M", 0.5), ("B", 0.2)):
        yy = 86 - 66 * fr
        body += (f'<path d="M40 {yy:.1f} H46" stroke="CC" stroke-width="1"/><circle cx="49" cy="{yy:.1f}" r="2.6" fill="{"#43a047" if f >= fr else "#e0e0e0"}" stroke="CC" stroke-width="0.6"/>'
                 + t(55, yy + 1.8, lab, 4.6, "bold"))
    body += '<rect x="26" y="74" width="8" height="10" rx="2" fill="#455a64" stroke="none"/><path d="M30 74 V4 H58" stroke="#1e88e5" stroke-width="2.2" fill="none"/>'
    return 60, 88, body


add("ind_puits", "Puits avec pompe immergée et capteurs de niveau", IND,
    params=[("niveau", "Niveau d'eau", "Milieu", _NIV_L)], func=_puits)


def _pompe(p):
    on = p.get("etat") == "En marche"
    col = "#43a047" if on else "#ffffff"
    return 50, 40, (f'<path d="M0 26 H10 M40 10 H50" stroke="#1e88e5" stroke-width="3"/>'
                    f'<circle cx="24" cy="22" r="14" fill="{col}" stroke="CC" stroke-width="1.6"/><path d="M14 12 L38 10 L34 20" stroke="CC" stroke-width="1.2" fill="none"/>'
                    '<path d="M18 30 L24 16 L30 30 Z" fill="CC" stroke="none"/><path d="M14 36 H34" stroke="CC" stroke-width="2"/>')


add("ind_pompe", "Pompe centrifuge (arrêt / marche)", IND, params=[("etat", "État", "Arrêtée", ["Arrêtée", "En marche"])], func=_pompe)


def _pompage(p):
    nr, npu = p.get("reservoir", "Bas"), p.get("puits", "Haut")
    on = p.get("pompe") == "En marche"
    _, _, puits = _puits({"niveau": npu})
    _, _, ch = _chateau({"niveau": nr})
    body = (f'<g transform="translate(0 30)">{puits}</g><g transform="translate(108 20)">{ch}</g>'
            '<path d="M58 34 H62 V40 H66 M116 24 H120 V14 H142 V24" stroke="#1e88e5" stroke-width="2.2" fill="none"/>'
            f'<g transform="translate(66 14)">' + _pompe({"etat": "En marche" if on else "Arrêtée"})[2] + '</g>'
            '<rect x="66" y="66" width="34" height="18" rx="2" fill="#eceff1" stroke="CC" stroke-width="1"/>' + t(83, 73, "Automate", 4.4, "bold")
            + t(83, 80, "H / M / B", 4.2) + '<path d="M83 66 V54" stroke="#9e9e9e" stroke-width="0.8" stroke-dasharray="2 1.4"/>')
    return 190, 120, body


add("ind_pompage", "Système de pompage complet : puits, pompe, château d'eau", IND,
    params=[("puits", "Niveau du puits", "Haut", _NIV_L), ("reservoir", "Niveau du château d'eau", "Bas", _NIV_L),
            ("pompe", "Pompe", "En marche", ["Arrêtée", "En marche"])], func=_pompage)
add("ind_flotteur", "Capteur de niveau à flotteur (poire)", IND, 40, 60,
    '<path d="M20 2 V20" stroke="#424242" stroke-width="2"/><path d="M20 20 Q6 30 10 44 Q20 56 30 44 Q34 30 20 20 Z" fill="#fbc02d" stroke="CC" stroke-width="1.2"/>'
    f'<path d="M0 40 Q10 36 20 40 T40 40" stroke="{_EAU}" stroke-width="2" fill="none"/>')


def _four(p):
    on = p.get("etat") == "En chauffe"
    glow = "#ff7043" if on else "#9e9e9e"
    body = ('<rect x="4" y="14" width="66" height="60" rx="3" fill="#cfd8dc" stroke="CC" stroke-width="1.6"/><rect x="58" y="2" width="8" height="12" fill="#90a4ae" stroke="CC" stroke-width="1"/>'
            '<rect x="10" y="22" width="40" height="44" rx="2" fill="#455a64" stroke="CC" stroke-width="1.2"/>'
            f'<rect x="15" y="27" width="30" height="20" fill="{"#ffccbc" if on else "#263238"}" stroke="#212121" stroke-width="1"/>'
            + "".join(f'<path d="M17 {30 + i * 5} Q22 {28 + i * 5} 27 {30 + i * 5} T37 {30 + i * 5} T43 {30 + i * 5}" stroke="{glow}" stroke-width="1.4" fill="none"/>' for i in range(3))
            + '<path d="M46 54 H50" stroke="#212121" stroke-width="3" stroke-linecap="round"/>'
            '<rect x="54" y="22" width="12" height="8" fill="#212121" stroke="none"/>' + t(60, 28, "850", 4.4, "bold").replace('fill="CC"', 'fill="#76ff03"')
            + f'<circle cx="60" cy="38" r="3" fill="{"#43a047" if on else "#e0e0e0"}" stroke="CC" stroke-width="0.6"/><circle cx="60" cy="48" r="3" fill="#e53935" stroke="CC" stroke-width="0.6"/>'
            '<path d="M8 74 V80 M66 74 V80" stroke="CC" stroke-width="2"/>')
    if on:
        body += '<path d="M60 0 Q58 -4 62 -6" stroke="#bdbdbd" stroke-width="1" fill="none"/>'
    return 74, 82, body


add("ind_four", "Four industriel à résistances", IND, params=[("etat", "État", "Arrêté", ["Arrêté", "En chauffe"])], func=_four)

# ---------------------------------------------------------------- habitat : GTL, chauffage, éclairage
def _module(x, y, w=6, h=14, col="#ffffff", lev="#424242"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" stroke="CC" stroke-width="0.5"/>'
            f'<rect x="{x + w / 2 - 1.2}" y="{y + h / 2 - 3}" width="2.4" height="5" fill="{lev}" stroke="none"/>')


def _gtl_vue():
    """GTL : goulotte du sol au plafond, tableau et coffret de communication posés dessus."""
    fils = ("#1e88e5", "#795548", "#212121", "#fdd835", "#43a047")
    s = ('<path d="M0 2 H70" stroke="#9e9e9e" stroke-width="2"/><path d="M0 198 H70" stroke="#9e9e9e" stroke-width="2"/>'
         + t(8, 9, "plafond", 3.4) + t(8, 196, "sol", 3.4)
         # goulotte pleine hauteur (couvercle)
         + '<rect x="21" y="3" width="28" height="194" fill="#fafafa" stroke="CC" stroke-width="1.2"/>'
         '<path d="M24 3 V197 M46 3 V197" stroke="#e0e0e0" stroke-width="0.8"/>')
    # couvercle retiré en haut et en bas : on voit les câbles dans la goulotte
    for y0, y1 in ((6, 40), (150, 194)):
        s += f'<rect x="23" y="{y0}" width="24" height="{y1 - y0}" fill="#eceff1" stroke="#9e9e9e" stroke-width="0.6"/>'
        s += "".join(f'<path d="M{26 + i * 4.4:.1f} {y0} V{y1}" stroke="{c}" stroke-width="1.8"/>' for i, c in enumerate(fils))
        s += f'<path d="M23 {y0} H47 M23 {y1} H47" stroke="#757575" stroke-width="0.8" stroke-dasharray="2 1.4"/>'
    # tableau de répartition (2 rangées) posé sur la goulotte
    s += ('<rect x="4" y="44" width="62" height="66" rx="2" fill="#ffffff" stroke="CC" stroke-width="1.4"/>'
          '<path d="M7 50 H63 M7 78 H63" stroke="#9e9e9e" stroke-width="1"/>'
          '<rect x="7" y="53" width="13" height="20" fill="#ffffff" stroke="CC" stroke-width="0.6"/><rect x="10" y="58" width="7" height="6" fill="#e53935" stroke="none"/>'
          + t(13.5, 71, "AGCP", 2.8, "bold")
          + "".join(_module(22 + i * 5.8, 55, 5, 14) for i in range(7))
          + '<rect x="7" y="81" width="11" height="18" fill="#e3f2fd" stroke="CC" stroke-width="0.6"/>' + t(12.5, 97, "ID", 3, "bold")
          + "".join(_module(20 + i * 5.8, 83, 5, 14) for i in range(7))
          + t(35, 106, "tableau de répartition", 3.4)
          # bornier de terre
          + '<rect x="8" y="112" width="30" height="5" rx="1" fill="#c8e6c9" stroke="CC" stroke-width="0.6"/>'
          + "".join(f'<circle cx="{11 + i * 4.5}" cy="114.5" r="1" fill="#2e7d32" stroke="none"/>' for i in range(6)) + t(52, 116, "terre", 3.4, "bold")
          # coffret de communication
          + '<rect x="6" y="120" width="58" height="28" rx="2" fill="#eceff1" stroke="CC" stroke-width="1.2"/>'
          + '<rect x="9" y="123" width="12" height="9" rx="1" fill="#ffffff" stroke="CC" stroke-width="0.6"/>' + t(15, 129.4, "DTI", 3.2, "bold")
          + '<rect x="24" y="123" width="37" height="9" rx="1" fill="#ffffff" stroke="CC" stroke-width="0.6"/>'
          + "".join(f'<rect x="{26.5 + i * 5.6:.1f}" y="125.5" width="3.8" height="4" fill="#1e88e5" stroke="none"/>' for i in range(6))
          + '<rect x="9" y="135" width="26" height="10" rx="2" fill="#ffffff" stroke="CC" stroke-width="0.6"/>' + t(22, 141.6, "box Internet", 3, "bold")
          + '<rect x="38" y="135" width="23" height="10" rx="1" fill="#ffffff" stroke="CC" stroke-width="0.6"/>' + t(49.5, 141.6, "prises", 3)
          )
    return s


add("hab_gtl", "Gaine technique logement (GTL) avec goulotte du sol au plafond", HAB, 70, 200, _gtl_vue())
add("hab_radiateur_inertie", "Radiateur à inertie", HAB, 100, 56,
    '<rect x="4" y="6" width="92" height="44" rx="5" fill="#fafafa" stroke="CC" stroke-width="1.6"/>'
    + "".join(f'<path d="M{10 + i * 6} 10 V44" stroke="#e0e0e0" stroke-width="2.4"/>' for i in range(11))
    + '<rect x="76" y="12" width="14" height="20" rx="2" fill="#eceff1" stroke="CC" stroke-width="0.8"/><rect x="78" y="14" width="10" height="7" fill="#263238" stroke="none"/>'
    + _W(t(83, 20, "19°", 4.4, "bold")) + '<circle cx="83" cy="27" r="2.4" fill="#ffffff" stroke="CC" stroke-width="0.6"/>'
    + '<path d="M14 50 V54 M86 50 V54" stroke="CC" stroke-width="2"/>' + t(40, 30, "inertie", 6))
add("hab_radiant", "Panneau rayonnant (radiant)", HAB, 100, 56,
    '<rect x="4" y="6" width="80" height="44" rx="3" fill="#eceff1" stroke="CC" stroke-width="1.6"/>'
    + "".join(f'<path d="M10 {14 + i * 7} H78" stroke="#ff7043" stroke-width="3" stroke-linecap="round"/><path d="M10 {14 + i * 7} H78" stroke="#ffccbc" stroke-width="1"/>' for i in range(5))
    + "".join(f'<path d="M{8 + i * 6} 10 V46" stroke="#b0bec5" stroke-width="0.6"/>' for i in range(13))
    + "".join(f'<path d="M88 {14 + i * 10} Q92 {17 + i * 10} 88 {20 + i * 10} Q92 {23 + i * 10} 96 {22 + i * 10}" stroke="#ff7043" stroke-width="1.2" fill="none"/>' for i in range(3)))
add("hab_convecteur", "Convecteur électrique", HAB, 100, 60,
    '<rect x="4" y="14" width="92" height="38" rx="3" fill="#fafafa" stroke="CC" stroke-width="1.6"/>'
    + "".join(f'<path d="M{10 + i * 4} 17 V23" stroke="#757575" stroke-width="1.6"/>' for i in range(20))
    + "".join(f'<path d="M{10 + i * 4} 46 V50" stroke="#757575" stroke-width="1.2"/>' for i in range(20))
    + "".join(f'<path d="M{20 + i * 20} 12 Q{16 + i * 20} 6 {20 + i * 20} 2 M{17 + i * 20} 5 L{20 + i * 20} 1 L{23 + i * 20} 5" stroke="#ef5350" stroke-width="1.2" fill="none"/>' for i in range(4))
    + '<rect x="80" y="28" width="10" height="12" rx="1" fill="#eceff1" stroke="CC" stroke-width="0.6"/><circle cx="85" cy="34" r="2.6" fill="#ffffff" stroke="CC" stroke-width="0.6"/>'
    + '<path d="M50 56 Q46 62 50 66" stroke="#4fc3f7" stroke-width="1" fill="none"/>')
add("hab_plancher", "Plancher chauffant (coupe)", HAB, 110, 50,
    '<rect x="2" y="8" width="106" height="6" fill="#d7ccc8" stroke="CC" stroke-width="0.8"/>' + t(55, 6, "carrelage", 4)
    + '<rect x="2" y="14" width="106" height="14" fill="#bdbdbd" stroke="CC" stroke-width="0.8"/>'
    + "".join(f'<circle cx="{10 + i * 12}" cy="21" r="3.2" fill="#ff7043" stroke="#bf360c" stroke-width="0.8"/>' for i in range(9))
    + '<rect x="2" y="28" width="106" height="8" fill="#fff59d" stroke="CC" stroke-width="0.8"/>'
    + "".join(f'<path d="M{4 + i * 6} 29 L{7 + i * 6} 35" stroke="#f9a825" stroke-width="0.6"/>' for i in range(17))
    + '<rect x="2" y="36" width="106" height="12" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>'
    + _W(t(20, 24, "chape", 4)) + t(96, 34, "isolant", 4) + _W(t(55, 44, "dalle béton", 4))
    + "".join(f'<path d="M{20 + i * 24} 6 V0 M{17 + i * 24} 3 L{20 + i * 24} 0 L{23 + i * 24} 3" stroke="#ef5350" stroke-width="1" fill="none"/>' for i in range(0)))
add("hab_spot", "Spot encastré (plafond)", HAB, 60, 50,
    '<path d="M2 8 H58" stroke="#9e9e9e" stroke-width="3"/><path d="M18 8 H42 L38 16 H22 Z" fill="#eceff1" stroke="CC" stroke-width="1.2"/>'
    '<ellipse cx="30" cy="16" rx="8" ry="2.4" fill="#fff59d" stroke="CC" stroke-width="0.8"/>'
    '<path d="M22 17 L8 48 H52 L38 17 Z" fill="#fff59d" fill-opacity="0.35" stroke="none"/>')
add("hab_tube_fluo", "Tube fluorescent (néon) T8", HAB, 120, 20,
    '<rect x="8" y="5" width="104" height="10" rx="5" fill="#fafafa" stroke="CC" stroke-width="1.2"/>'
    '<rect x="6" y="5" width="8" height="10" rx="1" fill="#bdbdbd" stroke="CC" stroke-width="0.8"/><rect x="106" y="5" width="8" height="10" rx="1" fill="#bdbdbd" stroke="CC" stroke-width="0.8"/>'
    '<path d="M2 8 H6 M2 12 H6 M114 8 H118 M114 12 H118" stroke="CC" stroke-width="1.2"/>')
add("hab_reglette", "Réglette / rampe néon (avec tube)", HAB, 120, 30,
    '<path d="M4 6 H116 L112 20 H8 Z" fill="#eceff1" stroke="CC" stroke-width="1.4"/>'
    '<rect x="12" y="18" width="96" height="8" rx="4" fill="#ffffff" stroke="CC" stroke-width="1"/>'
    '<rect x="8" y="17" width="6" height="10" fill="#9e9e9e" stroke="CC" stroke-width="0.6"/><rect x="106" y="17" width="6" height="10" fill="#9e9e9e" stroke="CC" stroke-width="0.6"/>')
add("hab_dalle_led", "Dalle LED carrée 60 × 60 (plafond)", HAB, 60, 60,
    '<rect x="2" y="2" width="56" height="56" fill="#cfd8dc" stroke="CC" stroke-width="1.4"/><rect x="6" y="6" width="48" height="48" fill="#fffde7" stroke="#bdbdbd" stroke-width="0.8"/>'
    + "".join(f'<path d="M{6 + i * 8} 6 V54 M6 {6 + i * 8} H54" stroke="#fff59d" stroke-width="0.6"/>' for i in range(1, 6)) + t(30, 33, "LED", 7, "bold"))
add("hab_neon_rond", "Tube fluorescent circulaire (néon rond)", HAB, 60, 60,
    '<circle cx="30" cy="30" r="24" fill="none" stroke="CC" stroke-width="7.4"/><circle cx="30" cy="30" r="24" fill="none" stroke="#fafafa" stroke-width="5"/>'
    '<rect x="22" y="2" width="16" height="8" rx="1" fill="#bdbdbd" stroke="CC" stroke-width="0.8"/>')
add("hab_douille", "Douille E27 (culot à vis) avec bornes", HAB, 40, 60,
    '<path d="M8 4 H32 V14 H8 Z" fill="#eceff1" stroke="CC" stroke-width="1.2"/><circle cx="15" cy="9" r="2" fill="#ffd54f" stroke="CC" stroke-width="0.6"/><circle cx="25" cy="9" r="2" fill="#ffd54f" stroke="CC" stroke-width="0.6"/>'
    '<path d="M6 14 H34 V48 Q34 56 20 56 Q6 56 6 48 Z" fill="#fafafa" stroke="CC" stroke-width="1.4"/>'
    '<rect x="11" y="20" width="18" height="30" rx="3" fill="#cfd8dc" stroke="CC" stroke-width="0.8"/>'
    + "".join(f'<path d="M11 {24 + i * 6} L29 {21 + i * 6}" stroke="#90a4ae" stroke-width="1.2"/>' for i in range(5))
    + '<path d="M15 4 V0 M25 4 V0" stroke="#1e88e5" stroke-width="1.6"/><path d="M25 0 V-2" stroke="#8d6e63" stroke-width="1.6"/>')
add("hab_inter_etanche", "Interrupteur étanche en saillie (IP55)", HAB, 50, 60,
    '<rect x="4" y="4" width="42" height="42" rx="5" fill="#9e9e9e" stroke="CC" stroke-width="1.4"/><rect x="10" y="10" width="30" height="30" rx="4" fill="#bdbdbd" stroke="#757575" stroke-width="1"/>'
    '<rect x="18" y="14" width="14" height="22" rx="3" fill="#e0e0e0" stroke="CC" stroke-width="1"/><path d="M18 25 H32" stroke="#9e9e9e" stroke-width="0.8"/>'
    '<path d="M20 46 V54 H30 V46" fill="#757575" stroke="CC" stroke-width="1"/><path d="M22 54 V58 M28 54 V58" stroke="CC" stroke-width="1"/>')
add("hab_prise_etanche", "Prise étanche en saillie avec clapet (IP55)", HAB, 50, 70,
    '<rect x="4" y="16" width="42" height="42" rx="5" fill="#9e9e9e" stroke="CC" stroke-width="1.4"/><circle cx="25" cy="37" r="14" fill="#e0e0e0" stroke="#757575" stroke-width="1"/>'
    '<circle cx="20" cy="37" r="2" fill="#424242" stroke="none"/><circle cx="30" cy="37" r="2" fill="#424242" stroke="none"/><rect x="23.5" y="25" width="3" height="4" fill="#bdbdbd" stroke="CC" stroke-width="0.4"/>'
    '<path d="M8 16 L12 2 H38 L42 16" fill="#bdbdbd" fill-opacity="0.9" stroke="CC" stroke-width="1.2"/>'
    '<path d="M20 58 V66 H30 V58" fill="#757575" stroke="CC" stroke-width="1"/>')

# ---------------------------------------------------------------- retours du 5/11 : voiture, détection, fins de course, éclairage EXIT
def _voiture(p):
    col = {"Rouge": "#e53935", "Bleue": "#1e88e5", "Grise": "#90a4ae", "Blanche": "#fafafa"}.get(p.get("couleur"), "#1e88e5")
    body = (f'<path d="M6 34 V26 Q6 22 12 21 L28 18 L40 8 Q44 6 50 6 H74 Q80 6 84 12 L92 20 Q104 21 106 26 V34 Q106 36 102 36 H8 Q6 36 6 34 Z" fill="{col}" stroke="CC" stroke-width="1.4"/>'
            '<path d="M42 10 Q45 8 50 8 H60 V19 H31 Z" fill="#b3e5fc" stroke="CC" stroke-width="1"/><path d="M63 8 H73 Q78 8 81 12 L88 19 H63 Z" fill="#b3e5fc" stroke="CC" stroke-width="1"/>'
            '<path d="M61 19 V34" stroke="CC" stroke-width="0.8"/><path d="M52 22 H58 M70 22 H76" stroke="CC" stroke-width="1.4"/>'
            '<rect x="100" y="23" width="6" height="4" rx="1" fill="#fff59d" stroke="none"/><rect x="6" y="24" width="4" height="4" rx="1" fill="#ef5350" stroke="none"/>'
            + "".join(f'<circle cx="{x}" cy="36" r="8" fill="#263238" stroke="none"/><circle cx="{x}" cy="36" r="3.4" fill="#b0bec5" stroke="none"/>' for x in (26, 86)))
    return 112, 46, body


add("ind_voiture", "Voiture (vue de côté)", IND, params=[("couleur", "Couleur", "Bleue", ["Bleue", "Rouge", "Grise", "Blanche"])], func=_voiture)


def _boucle(p):
    det = p.get("etat") == "Véhicule détecté"
    body = ('<path d="M2 30 L28 10 H118 L92 30 Z" fill="#78909c" stroke="CC" stroke-width="1"/>'
            '<path d="M24 26 L42 13 H96 L78 26 Z" fill="none" stroke="#212121" stroke-width="2.2" stroke-dasharray="1 0"/>'
            '<path d="M27 25 L43 14.4 H93 L77 25 Z" fill="none" stroke="#424242" stroke-width="0.8"/>'
            '<path d="M24 26 Q16 34 14 44" stroke="#212121" stroke-width="1.6" fill="none"/>'
            f'<rect x="2" y="44" width="30" height="16" rx="2" fill="#eceff1" stroke="CC" stroke-width="1"/>'
            f'<circle cx="26" cy="52" r="2.6" fill="{"#43a047" if det else "#e0e0e0"}" stroke="CC" stroke-width="0.6"/>' + t(13, 54, "boucle", 4))
    if det:
        body += '<path d="M60 4 Q66 8 60 12 M56 2 Q66 8 56 14" stroke="#e53935" stroke-width="1" fill="none"/>'
    return 120, 62, body


add("ind_boucle", "Boucle de détection magnétique au sol avec détecteur", IND,
    params=[("etat", "État", "Libre", ["Libre", "Véhicule détecté"])], func=_boucle)


def _barrage(p):
    coupe = p.get("faisceau") == "Interrompu"
    body = ('<rect x="2" y="14" width="18" height="24" rx="2" fill="#37474f" stroke="CC" stroke-width="1"/><circle cx="16" cy="22" r="2.6" fill="#e53935" stroke="none"/><circle cx="16" cy="31" r="2.6" fill="#90caf9" stroke="none"/>'
            f'<circle cx="6" cy="18" r="1.6" fill="{"#e53935" if coupe else "#43a047"}" stroke="none"/>'
            '<path d="M11 38 V50 M5 50 H17" stroke="CC" stroke-width="2"/>'
            '<rect x="102" y="16" width="14" height="20" rx="2" fill="#e53935" stroke="CC" stroke-width="1"/>'
            + "".join(f'<path d="M104 {18 + i * 4} L114 {22 + i * 4} M114 {18 + i * 4} L104 {22 + i * 4}" stroke="#ffcdd2" stroke-width="0.6"/>' for i in range(4))
            + '<path d="M109 36 V50 M103 50 H115" stroke="CC" stroke-width="2"/>')
    if coupe:
        body += ('<path d="M20 22 H52" stroke="#e53935" stroke-width="1.4" stroke-dasharray="3 2"/>'
                 '<rect x="52" y="8" width="16" height="40" rx="2" fill="#9e9e9e" fill-opacity="0.7" stroke="CC" stroke-width="0.8"/>' + t(60, 58, "objet", 4.4))
    else:
        body += '<path d="M20 22 H102 M102 30 H20" stroke="#e53935" stroke-width="1.4" stroke-dasharray="3 2"/><path d="M26 28 L20 30 L26 32" stroke="#e53935" stroke-width="1.2" fill="none"/>'
    return 120, 60, body


add("ind_barrage_optique", "Détecteur de passage optique (cellule et miroir réflecteur)", IND,
    params=[("faisceau", "Faisceau", "Libre", ["Libre", "Interrompu"])], func=_barrage)


def _fin_course(p):
    act = p.get("etat") == "Actionné"
    ang = -10 if act else -45
    body = ('<rect x="6" y="20" width="30" height="34" rx="2" fill="#fbc02d" stroke="CC" stroke-width="1.2"/>'
            '<rect x="10" y="44" width="22" height="7" rx="1" fill="#424242" stroke="none"/>' + _W(t(21, 49.5, "NO NF", 3.6, "bold"))
            + f'<g transform="translate(21 24) rotate({ang})"><rect x="-2" y="-2" width="26" height="4" rx="2" fill="#616161" stroke="CC" stroke-width="0.6"/>'
            '<circle cx="24" cy="0" r="5" fill="#212121" stroke="CC" stroke-width="0.6"/><circle cx="24" cy="0" r="1.6" fill="#9e9e9e" stroke="none"/></g>'
            '<circle cx="21" cy="24" r="3" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>'
            f'<circle cx="31" cy="30" r="2" fill="{"#43a047" if act else "#e0e0e0"}" stroke="CC" stroke-width="0.5"/>')
    if act:
        body += '<path d="M40 6 H60 L56 18 H44 Z" fill="#90a4ae" stroke="CC" stroke-width="1"/><path d="M62 12 H52" stroke="#e53935" stroke-width="1.4"/><path d="M54 9 L50 12 L54 15" stroke="#e53935" stroke-width="1.2" fill="none"/>'
    return 64, 58, body


add("ind_fin_course", "Capteur fin de course mécanique à galet", IND,
    params=[("etat", "État", "Repos", ["Repos", "Actionné"])], func=_fin_course)


def _ils(p):
    proche = p.get("aimant") == "Aimant proche"
    body = ('<rect x="4" y="24" width="50" height="14" rx="3" fill="#eceff1" stroke="CC" stroke-width="1.2"/>'
            '<rect x="12" y="28" width="34" height="6" rx="3" fill="#e3f2fd" stroke="#90a4ae" stroke-width="0.6"/>'
            f'<path d="M14 31 H27 M44 31 H{30 if proche else 32}" stroke="#616161" stroke-width="1"/>'
            f'<path d="M27 31 L{30 if proche else 31} {31 if proche else 29}" stroke="#616161" stroke-width="1"/>'
            '<path d="M4 31 H-2 M54 31 H60" stroke="CC" stroke-width="1.2"/>'
            f'<circle cx="50" cy="28" r="1.8" fill="{"#43a047" if proche else "#e0e0e0"}" stroke="none"/>')
    y = 8 if proche else 0
    body += (f'<rect x="18" y="{y}" width="11" height="10" fill="#e53935" stroke="CC" stroke-width="0.8"/><rect x="29" y="{y}" width="11" height="10" fill="#1e88e5" stroke="CC" stroke-width="0.8"/>'
             + _W(t(23.5, y + 7.5, "N", 5, "bold")) + _W(t(34.5, y + 7.5, "S", 5, "bold")))
    return 60, 42, body


add("ind_capteur_magnetique", "Capteur magnétique (ILS) avec aimant", IND,
    params=[("aimant", "Aimant", "Aimant éloigné", ["Aimant éloigné", "Aimant proche"])], func=_ils)


def _exit(p):
    txt = p.get("texte", "SORTIE")
    d = p.get("fleche", "→ Droite")
    body = ('<rect x="2" y="2" width="96" height="40" rx="3" fill="#fafafa" stroke="CC" stroke-width="1.4"/>'
            '<rect x="6" y="6" width="88" height="32" rx="1.5" fill="#2e8b57" stroke="none"/>'
            '<path d="M6 6 H94 V12 H6 Z" fill="#ffffff" fill-opacity="0.18" stroke="none"/>')
    rot = {"→ Droite": 0, "← Gauche": 180, "↑ Haut": -90, "↓ Bas": 90}.get(d, 0)
    ax = 80 if rot in (0, -90, 90) else 20
    tx = 40 if ax == 80 else 60
    long_ = len(txt) > 6
    if long_:
        tx = 36 if ax == 80 else 64
    body += _arrow(ax, 22, 1.25, "#ffffff", rot) + _W(t(tx, 25 if long_ else 25.5, txt, 5.2 if long_ else 9, "bold"))
    body += '<circle cx="92" cy="40" r="1.4" fill="#43a047" stroke="none"/>'
    return 100, 44, body


add("inc_exit", "Bloc d'éclairage de sécurité lumineux « SORTIE / EXIT » avec flèche", INC,
    params=[("texte", "Texte", "SORTIE", ["SORTIE", "EXIT", "SORTIE DE SECOURS"]), ("fleche", "Flèche", "→ Droite", ["→ Droite", "← Gauche", "↑ Haut", "↓ Bas"])],
    func=_exit)

# ---------------------------------------------------------------- retours du 5/11 (2) : capteur cylindrique, vérins, bornes de recharge, voiture face/arrière
def _prox(p):
    on = p.get("etat") == "Objet détecté"
    body = ('<path d="M0 22 Q10 22 18 22" stroke="#263238" stroke-width="7" fill="none"/>'
            '<rect x="16" y="17" width="8" height="10" rx="1" fill="#6d4c41" stroke="none"/>'
            '<rect x="24" y="12" width="56" height="20" rx="2" fill="#cfd8dc" stroke="CC" stroke-width="1"/>'
            + "".join(f'<path d="M{27 + i * 3} 12 L{26 + i * 3} 32" stroke="#90a4ae" stroke-width="0.8"/>' for i in range(17))
            + '<path d="M58 8 H66 V36 H58 Z" fill="#b0bec5" stroke="CC" stroke-width="1"/><path d="M58 15 H66 M58 29 H66" stroke="#78909c" stroke-width="0.6"/>'
            '<rect x="80" y="13" width="8" height="18" rx="2" fill="#4fc3f7" stroke="CC" stroke-width="1"/>'
            f'<circle cx="30" cy="22" r="2.2" fill="{"#ff9800" if on else "#8d6e63"}" stroke="none"/>')
    if on:
        body += '<rect x="94" y="8" width="6" height="28" fill="#78909c" stroke="CC" stroke-width="0.8"/><path d="M89 16 Q92 22 89 28" stroke="#4fc3f7" stroke-width="1" fill="none"/>'
    return 102, 44, body


add("ind_capteur_cylindrique", "Capteur de proximité cylindrique M18 (inductif, face bleue)", IND,
    params=[("etat", "État", "Aucun objet", ["Aucun objet", "Objet détecté"])], func=_prox)


def _verin(p, double=True):
    pos = {"Tige rentrée": 0.0, "Mi-course": 0.5, "Tige sortie": 1.0}.get(p.get("position"), 0.0)
    L = 34 * pos
    body = ('<rect x="10" y="12" width="70" height="20" rx="1" fill="#cfd8dc" stroke="CC" stroke-width="1.2"/>'
            '<path d="M10 15 H80 M10 29 H80" stroke="#90a4ae" stroke-width="0.6"/>'
            '<rect x="4" y="10" width="8" height="24" rx="1" fill="#90a4ae" stroke="CC" stroke-width="1"/><rect x="78" y="10" width="8" height="24" rx="1" fill="#90a4ae" stroke="CC" stroke-width="1"/>'
            f'<rect x="86" y="19.5" width="{8 + L:.1f}" height="5" fill="#eceff1" stroke="CC" stroke-width="0.8"/>'
            f'<rect x="{92 + L:.1f}" y="17" width="6" height="10" rx="1" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>')
    # piston visible en transparence
    xp = 14 + 56 * pos
    body += f'<rect x="{xp:.1f}" y="13" width="6" height="18" fill="#78909c" fill-opacity="0.45" stroke="none"/>'
    # raccords
    body += '<path d="M8 10 V4 M5 4 H11" stroke="#1e88e5" stroke-width="2.4"/>'
    if double:
        body += '<path d="M82 10 V4 M79 4 H85" stroke="#1e88e5" stroke-width="2.4"/>'
    else:
        body += ('<circle cx="82" cy="8" r="1.4" fill="#424242" stroke="none"/>'
                 + f'<path d="M{xp + 6:.1f} 22 ' + " ".join(f"L{xp + 6 + (78 - xp - 6) * (i + .5) / 8:.1f} {18 if i % 2 else 26}" for i in range(8)) + ' L78 22" stroke="#616161" stroke-width="0.8" fill="none"/>')
    # petits capteurs de position dans la rainure
    for x, act in ((16, pos == 0.0), (68, pos == 1.0)):
        body += (f'<rect x="{x}" y="30" width="10" height="5" rx="1" fill="#424242" stroke="CC" stroke-width="0.6"/>'
                 f'<circle cx="{x + 8}" cy="32.5" r="1.3" fill="{"#ff9800" if act else "#757575"}" stroke="none"/>'
                 f'<path d="M{x} 33 Q{x - 4} 38 {x - 2} 44" stroke="#212121" stroke-width="1" fill="none"/>')
    return 136, 46, body


_VPOS = ("position", "Position de la tige", "Tige rentrée", ["Tige rentrée", "Mi-course", "Tige sortie"])
add("ind_verin_double", "Vérin double effet avec capteurs de position", IND, params=[_VPOS], func=lambda p: _verin(p, True))
add("ind_verin_simple", "Vérin simple effet (rappel par ressort) avec capteurs de position", IND, params=[_VPOS], func=lambda p: _verin(p, False))


def _etat_borne(p):
    return {"Libre": "#43a047", "En charge": "#1e88e5", "Défaut": "#e53935"}.get(p.get("etat"), "#43a047")


def _wallbox(p):
    c = _etat_borne(p)
    body = ('<rect x="2" y="2" width="4" height="86" fill="#d7ccc8" stroke="none"/>'
            '<rect x="8" y="8" width="40" height="56" rx="8" fill="#fafafa" stroke="CC" stroke-width="1.4"/>'
            '<rect x="14" y="16" width="28" height="12" rx="2" fill="#263238" stroke="none"/>' + _W(t(28, 24.5, "7,4 kW", 5, "bold"))
            + f'<rect x="20" y="34" width="16" height="3" rx="1.5" fill="{c}" stroke="none"/>'
            '<circle cx="28" cy="50" r="6" fill="#424242" stroke="CC" stroke-width="0.8"/>'
            '<path d="M28 64 Q28 80 40 84 Q56 88 54 70 V60" stroke="#212121" stroke-width="3" fill="none"/><rect x="50" y="52" width="8" height="10" rx="2" fill="#424242" stroke="none"/>')
    return 62, 90, body


def _borne_ext(p):
    c = _etat_borne(p)
    body = ('<path d="M4 108 H76" stroke="#9e9e9e" stroke-width="1.4"/><rect x="22" y="100" width="36" height="8" fill="#9e9e9e" stroke="none"/>'
            '<rect x="20" y="6" width="40" height="94" rx="6" fill="#eceff1" stroke="CC" stroke-width="1.4"/>'
            f'<rect x="20" y="6" width="40" height="14" rx="6" fill="{c}" stroke="none"/><rect x="20" y="14" width="40" height="6" fill="{c}" stroke="none"/>'
            '<path d="M38 9 L34 15 H38 L36 19 L42 13 H38 Z" fill="#ffffff" stroke="none"/>'
            '<rect x="26" y="26" width="28" height="14" rx="1.5" fill="#263238" stroke="none"/>' + _W(t(40, 35, "22 kW", 5, "bold"))
            + '<circle cx="31" cy="54" r="6" fill="#424242" stroke="CC" stroke-width="0.8"/><circle cx="49" cy="54" r="6" fill="#424242" stroke="CC" stroke-width="0.8"/>'
            '<rect x="28" y="66" width="24" height="8" rx="2" fill="#cfd8dc" stroke="CC" stroke-width="0.6"/>' + t(40, 72, "badge", 4)
            + '<path d="M60 52 Q74 60 70 84 L66 90" stroke="#212121" stroke-width="3" fill="none"/>')
    return 80, 110, body


_ETAT_B = [("etat", "État", "Libre", ["Libre", "En charge", "Défaut"])]
add("hab_borne_murale", "Borne de recharge murale (intérieure, wallbox)", HAB, params=_ETAT_B, func=_wallbox)
add("hab_borne_exterieure", "Borne de recharge sur pied (extérieure, 2 prises)", HAB, params=_ETAT_B, func=_borne_ext)

_COUL_V = {"Bleue": "#1e88e5", "Rouge": "#e53935", "Grise": "#90a4ae", "Blanche": "#fafafa"}


def _voiture_face(p):
    col = _COUL_V.get(p.get("couleur"), "#1e88e5")
    body = (f'<path d="M18 22 L26 8 Q28 4 34 4 H66 Q72 4 74 8 L82 22 Z" fill="{col}" stroke="CC" stroke-width="1.2"/>'
            '<path d="M24 21 L30 9 Q31 7 35 7 H65 Q69 7 70 9 L76 21 Z" fill="#b3e5fc" stroke="CC" stroke-width="1"/>'
            f'<path d="M8 26 Q8 22 18 21 H82 Q92 22 92 26 V48 H8 Z" fill="{col}" stroke="CC" stroke-width="1.4"/>'
            '<rect x="2" y="22" width="8" height="5" rx="1.5" fill="' + col + '" stroke="CC" stroke-width="0.8"/><rect x="90" y="22" width="8" height="5" rx="1.5" fill="' + col + '" stroke="CC" stroke-width="0.8"/>'
            '<path d="M12 28 H28 L26 34 H12 Z M88 28 H72 L74 34 H88 Z" fill="#fff9c4" stroke="CC" stroke-width="0.8"/>'
            '<rect x="34" y="32" width="32" height="8" rx="2" fill="#37474f" stroke="none"/><path d="M38 34 H62 M38 36.5 H62" stroke="#78909c" stroke-width="0.6"/>'
            '<rect x="40" y="42" width="20" height="5" rx="0.6" fill="#ffffff" stroke="CC" stroke-width="0.6"/>'
            '<rect x="10" y="48" width="12" height="8" rx="2" fill="#263238" stroke="none"/><rect x="78" y="48" width="12" height="8" rx="2" fill="#263238" stroke="none"/>')
    return 100, 58, body


def _voiture_arriere(p):
    col = _COUL_V.get(p.get("couleur"), "#1e88e5")
    body = (f'<path d="M18 22 L26 8 Q28 4 34 4 H66 Q72 4 74 8 L82 22 Z" fill="{col}" stroke="CC" stroke-width="1.2"/>'
            '<path d="M26 20 L31 10 Q32 8 36 8 H64 Q68 8 69 10 L74 20 Z" fill="#b3e5fc" stroke="CC" stroke-width="1"/>'
            f'<path d="M8 26 Q8 22 18 21 H82 Q92 22 92 26 V48 H8 Z" fill="{col}" stroke="CC" stroke-width="1.4"/>'
            '<path d="M10 26 H26 V34 H10 Z M90 26 H74 V34 H90 Z" fill="#e53935" stroke="CC" stroke-width="0.8"/>'
            '<path d="M10 30 H26 M74 30 H90" stroke="#ffcdd2" stroke-width="0.8"/>'
            '<rect x="38" y="30" width="24" height="6" rx="0.6" fill="#ffffff" stroke="CC" stroke-width="0.6"/>'
            '<path d="M8 42 H92" stroke="#37474f" stroke-width="3"/><rect x="64" y="44" width="6" height="3" rx="1" fill="#616161" stroke="none"/>'
            '<rect x="10" y="48" width="12" height="8" rx="2" fill="#263238" stroke="none"/><rect x="78" y="48" width="12" height="8" rx="2" fill="#263238" stroke="none"/>')
    return 100, 58, body


_CV = [("couleur", "Couleur", "Bleue", list(_COUL_V))]
add("ind_voiture_face", "Voiture (vue de face)", IND, params=_CV, func=_voiture_face)
add("ind_voiture_arriere", "Voiture (vue de l'arrière)", IND, params=_CV, func=_voiture_arriere)

# ---------------------------------------------------------------- retours du 5/11 (3) : bras manipulateur, moteur et plaque à bornes
def _bras(p):
    pos = p.get("position", "Repos")
    ferme = p.get("pince") == "Fermée"
    a1, a2 = {"Repos": (-100, -10), "Saisie (en bas)": (-48, 62), "Dépose (en haut)": (-72, 4)}.get(pos, (-100, -10))
    sx, sy = 34, 70
    ex, ey = sx + 36 * math.cos(math.radians(a1)), sy + 36 * math.sin(math.radians(a1))
    wx, wy = ex + 32 * math.cos(math.radians(a2)), ey + 32 * math.sin(math.radians(a2))
    gap = 3.2 if ferme else 8
    body = ('<path d="M2 94 H118" stroke="#9e9e9e" stroke-width="1.4"/>'
            '<rect x="20" y="84" width="28" height="10" rx="2" fill="#455a64" stroke="CC" stroke-width="1"/>'
            '<path d="M24 84 L28 72 H40 L44 84 Z" fill="#ff7043" stroke="CC" stroke-width="1"/>'
            f'<path d="M{sx} {sy} L{ex:.1f} {ey:.1f}" stroke="CC" stroke-width="11.4" stroke-linecap="round"/><path d="M{sx} {sy} L{ex:.1f} {ey:.1f}" stroke="#ff7043" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M{ex:.1f} {ey:.1f} L{wx:.1f} {wy:.1f}" stroke="CC" stroke-width="8.4" stroke-linecap="round"/><path d="M{ex:.1f} {ey:.1f} L{wx:.1f} {wy:.1f}" stroke="#ff8a65" stroke-width="6.4" stroke-linecap="round"/>'
            f'<circle cx="{sx}" cy="{sy}" r="5" fill="#37474f" stroke="CC" stroke-width="0.8"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="#37474f" stroke="CC" stroke-width="0.8"/>'
            f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="3.2" fill="#37474f" stroke="CC" stroke-width="0.8"/>'
            f'<rect x="{wx - 5:.1f}" y="{wy + 2:.1f}" width="10" height="5" rx="1" fill="#607d8b" stroke="CC" stroke-width="0.8"/>'
            f'<path d="M{wx - gap - 1:.1f} {wy + 7:.1f} H{wx + gap + 1:.1f}" stroke="#424242" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M{wx - gap:.1f} {wy + 7:.1f} V{wy + 15:.1f} M{wx + gap:.1f} {wy + 7:.1f} V{wy + 15:.1f}" stroke="#424242" stroke-width="2" stroke-linecap="round"/>')
    if ferme and pos != "Repos":
        body += _box(wx - 3, wy + 9, 6, 7)
    elif pos == "Saisie (en bas)":
        body += _box(wx - 6, 82, 12, 12)
    else:
        body += _box(88, 80, 14, 14)
    return 120, 96, body


add("ind_bras_manipulateur", "Bras manipulateur (robot à pince)", IND,
    params=[("position", "Position", "Repos", ["Repos", "Saisie (en bas)", "Dépose (en haut)"]), ("pince", "Pince", "Ouverte", ["Ouverte", "Fermée"])],
    func=_bras)


def _moteur_vue(p):
    body = ('<rect x="20" y="22" width="60" height="40" rx="4" fill="#1e88e5" stroke="CC" stroke-width="1.4"/>'
            + "".join(f'<path d="M{24 + i * 5} 22 V62" stroke="#1565c0" stroke-width="1.6"/>' for i in range(11))
            + '<path d="M6 26 Q4 42 6 58 H20 V26 Z" fill="#1976d2" stroke="CC" stroke-width="1.2"/>'
            + "".join(f'<path d="M8 {30 + i * 5} H18" stroke="#0d47a1" stroke-width="1"/>' for i in range(6))
            + '<rect x="80" y="32" width="6" height="20" fill="#1976d2" stroke="CC" stroke-width="1"/><rect x="86" y="39" width="14" height="6" fill="#cfd8dc" stroke="CC" stroke-width="0.8"/>'
            '<rect x="92" y="40.5" width="4" height="2" fill="#9e9e9e" stroke="none"/>'
            '<rect x="40" y="8" width="24" height="14" rx="1.5" fill="#1976d2" stroke="CC" stroke-width="1.2"/><circle cx="44" cy="12" r="0.8" fill="#bbdefb" stroke="none"/><circle cx="60" cy="12" r="0.8" fill="#bbdefb" stroke="none"/>'
            '<path d="M64 14 H70" stroke="#424242" stroke-width="3"/>'
            '<rect x="28" y="52" width="16" height="9" rx="0.8" fill="#eceff1" stroke="CC" stroke-width="0.6"/>' + t(36, 57, "3~ 400 V", 2.6, "bold")
            + t(36, 60, "1,5 kW", 2.4)
            + '<path d="M22 62 L18 70 H34 L30 62 M70 62 L66 70 H82 L78 62" fill="#1565c0" stroke="CC" stroke-width="1"/>')
    return 102, 72, body


add("ind_moteur_asynchrone", "Moteur asynchrone triphasé (vue, boîte à bornes et plaque signalétique)", IND, 102, 72, _moteur_vue({})[2])


def _plaque_bornes(p):
    cpl = p.get("couplage", "Étoile")
    xs = (14, 40, 66)
    body = ('<rect x="2" y="16" width="76" height="60" rx="3" fill="#eceff1" stroke="CC" stroke-width="1.4"/>'
            '<rect x="6" y="20" width="68" height="52" rx="2" fill="#fafafa" stroke="#b0bec5" stroke-width="0.8"/>')
    for i, x in enumerate(xs):
        body += f'<path d="M{x} 0 V28" stroke="CC" stroke-width="1.2"/>' + t(x + 6, 6, f"L{i + 1}", 5, "bold")
    for x, n in zip(xs, ("U1", "V1", "W1")):
        body += f'<circle cx="{x}" cy="32" r="4.4" fill="#ffd54f" stroke="CC" stroke-width="1"/><circle cx="{x}" cy="32" r="1.4" fill="#8d6e00" stroke="none"/>' + t(x, 44, n, 4.6, "bold")
    for x, n in zip(xs, ("W2", "U2", "V2")):
        body += f'<circle cx="{x}" cy="60" r="4.4" fill="#ffd54f" stroke="CC" stroke-width="1"/><circle cx="{x}" cy="60" r="1.4" fill="#8d6e00" stroke="none"/>' + t(x, 72, n, 4.6, "bold")
    if cpl == "Étoile":
        body += '<rect x="10" y="57" width="60" height="6" rx="2" fill="#bdbdbd" fill-opacity="0.85" stroke="CC" stroke-width="0.8"/>'
        body += f'<rect x="10" y="57" width="34" height="6" rx="2" fill="none" stroke="CC" stroke-width="0.6"/>'
    elif cpl == "Triangle":
        for x in xs:
            body += f'<rect x="{x - 3}" y="29" width="6" height="34" rx="2" fill="#bdbdbd" fill-opacity="0.85" stroke="CC" stroke-width="0.8"/>'
    body += t(40, 84, {"Étoile": "couplage étoile (Y)", "Triangle": "couplage triangle (Δ)"}.get(cpl, "sans barrettes"), 5, "bold")
    return 80, 88, body


add("ind_plaque_bornes", "Plaque à bornes de moteur triphasé (couplage étoile / triangle)", IND,
    params=[("couplage", "Couplage", "Étoile", ["Étoile", "Triangle", "Sans barrettes"])], func=_plaque_bornes,
    pins=[(14, 0), (40, 0), (66, 0)], pin_names="L1 L2 L3")

# ================================================================ bac pro Métiers de la sécurité
MSP = "Métiers de la sécurité – sapeurs-pompiers"
MSS = "Métiers de la sécurité – sûreté et surveillance"

add("ms_casque_pompier", "Casque de sapeur-pompier avec visière", MSP, 70, 56,
    '<path d="M10 36 C8 16 22 4 38 4 C54 4 64 16 62 34 Z" fill="#eceff1" stroke="CC" stroke-width="1.6"/>'
    '<path d="M20 10 C30 2 50 4 60 18" stroke="#ffffff" stroke-width="3" fill="none"/><path d="M14 30 C26 34 50 34 62 28" stroke="#fdd835" stroke-width="3" fill="none"/>'
    '<path d="M8 36 C10 50 24 54 38 54 C50 54 58 48 60 38 C46 42 24 42 8 36 Z" fill="#ffd54f" fill-opacity="0.55" stroke="#f9a825" stroke-width="1.2"/>'
    '<path d="M4 37 C20 43 46 44 66 34" stroke="#424242" stroke-width="2.4" fill="none"/>')
add("ms_lance", "Lance à incendie", MSP, 90, 30,
    '<path d="M2 15 H30" stroke="#e53935" stroke-width="8" stroke-linecap="round"/><rect x="28" y="9" width="10" height="12" rx="1.5" fill="#9e9e9e" stroke="CC" stroke-width="1"/>'
    '<path d="M38 10 H60 L72 13 V17 L60 20 H38 Z" fill="#bdbdbd" stroke="CC" stroke-width="1"/><rect x="46" y="18" width="6" height="10" rx="1" fill="#e53935" stroke="CC" stroke-width="0.8"/>'
    + "".join(f'<path d="M72 15 L{86} {6 + i * 6}" stroke="#4fc3f7" stroke-width="1.4"/>' for i in range(4)))
add("ms_tuyau", "Tuyau d'incendie en écheveau", MSP, 60, 50,
    "".join(f'<circle cx="30" cy="25" r="{r}" fill="none" stroke="#fafafa" stroke-width="5"/><circle cx="30" cy="25" r="{r}" fill="none" stroke="CC" stroke-width="0.8"/>' for r in (21, 15, 9))
    + '<rect x="46" y="38" width="10" height="8" rx="1" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>')
add("ms_ari", "Appareil respiratoire isolant (ARI)", MSP, 70, 70,
    '<rect x="8" y="10" width="20" height="54" rx="10" fill="#fdd835" stroke="CC" stroke-width="1.4"/><rect x="12" y="4" width="12" height="8" rx="2" fill="#424242" stroke="none"/>'
    '<path d="M18 6 Q30 0 40 14 Q46 22 46 30" stroke="#212121" stroke-width="2" fill="none"/>'
    '<ellipse cx="50" cy="40" rx="14" ry="18" fill="#cfd8dc" stroke="CC" stroke-width="1.4"/><ellipse cx="50" cy="36" rx="9" ry="9" fill="#b3e5fc" stroke="CC" stroke-width="1"/>'
    '<circle cx="50" cy="52" r="4" fill="#424242" stroke="none"/>')
add("ms_poteau", "Poteau d'incendie", MSP, 40, 80,
    '<path d="M4 76 H36" stroke="#9e9e9e" stroke-width="1.4"/><rect x="10" y="16" width="20" height="60" rx="2" fill="#e53935" stroke="CC" stroke-width="1.4"/>'
    '<path d="M8 16 Q20 2 32 16 Z" fill="#c62828" stroke="CC" stroke-width="1.2"/><rect x="16" y="2" width="8" height="6" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>'
    '<rect x="2" y="30" width="10" height="10" rx="2" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/><rect x="28" y="30" width="10" height="10" rx="2" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>'
    '<rect x="14" y="44" width="12" height="12" rx="6" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>')
add("ms_bouche", "Bouche d'incendie (regard au sol)", MSP, 60, 40,
    '<path d="M2 20 L14 6 H58 L46 20 Z" fill="#9e9e9e" stroke="CC" stroke-width="1"/><path d="M14 18 L22 9 H46 L38 18 Z" fill="#e53935" stroke="CC" stroke-width="1"/>'
    + t(30, 16, "B.I.", 4.4, "bold").replace('fill="CC"', 'fill="#ffffff"') + '<path d="M2 20 V26 H46 V20 M46 26 L58 12 V6" fill="#757575" stroke="CC" stroke-width="1"/>')
add("ms_colonne_seche", "Colonne sèche (prise en façade)", MSP, 50, 60,
    '<rect x="4" y="4" width="42" height="52" rx="2" fill="#fafafa" stroke="#e53935" stroke-width="2"/>' + t(25, 14, "COLONNE", 5, "bold") + t(25, 20, "SÈCHE", 5, "bold")
    + '<circle cx="17" cy="38" r="8" fill="#9e9e9e" stroke="CC" stroke-width="1"/><circle cx="33" cy="38" r="8" fill="#9e9e9e" stroke="CC" stroke-width="1"/>'
    '<circle cx="17" cy="38" r="3" fill="#616161" stroke="none"/><circle cx="33" cy="38" r="3" fill="#616161" stroke="none"/>')
add("ms_camion_pompier", "Camion de sapeurs-pompiers (fourgon)", MSP, 120, 56,
    '<path d="M4 44 V18 Q4 14 8 14 H84 V44 Z" fill="#e53935" stroke="CC" stroke-width="1.4"/>'
    '<path d="M84 44 V20 H102 L114 32 V44 Z" fill="#e53935" stroke="CC" stroke-width="1.4"/><path d="M88 23 H100 L108 31 H88 Z" fill="#b3e5fc" stroke="none"/>'
    '<rect x="4" y="34" width="110" height="4" fill="#fafafa" stroke="none"/>'
    '<path d="M10 10 H78" stroke="#9e9e9e" stroke-width="2.4"/>' + "".join(f'<path d="M{14 + i * 8} 7 V13" stroke="#9e9e9e" stroke-width="1.2"/>' for i in range(8))
    + '<rect x="90" y="16" width="12" height="4" rx="1.5" fill="#1e88e5" stroke="none"/>'
    + "".join(f'<circle cx="{x}" cy="46" r="7" fill="#263238" stroke="none"/><circle cx="{x}" cy="46" r="2.8" fill="#b0bec5" stroke="none"/>' for x in (20, 70, 100)))


def _triangle_feu():
    body = ('<path d="M40 6 L76 66 H4 Z" fill="none" stroke="CC" stroke-width="2"/>'
            '<path d="M40 6 L4 66" stroke="#ff7043" stroke-width="5"/><path d="M40 6 L76 66" stroke="#4fc3f7" stroke-width="5"/><path d="M4 66 H76" stroke="#8d6e63" stroke-width="5"/>'
            '<path d="M40 30 Q48 40 46 50 Q50 48 50 44 Q56 52 50 60 H30 Q24 52 30 44 Q30 48 34 50 Q32 40 40 30 Z" fill="#ff7043" stroke="#e64a19" stroke-width="0.8"/>'
            + t(16, 34, "Chaleur", 5.4, "bold") + t(66, 34, "Comburant", 5.4, "bold") + t(66, 40, "(oxygène)", 4.4) + t(40, 76, "Combustible", 5.4, "bold"))
    return 80, 80, body


_w, _h, _b = _triangle_feu()
add("ms_triangle_feu", "Triangle du feu", MSP, _w, _h, _b)


def _classe_feu(p):
    c = p.get("classe", "A")
    desc = {"A": "solides (bois, papier)", "B": "liquides (essence)", "C": "gaz (butane)", "D": "métaux", "F": "huiles de cuisson"}.get(c, "")
    body = ('<rect x="2" y="2" width="56" height="56" rx="6" fill="#ffffff" stroke="CC" stroke-width="2"/>'
            + t(30, 32, c, 22, "bold")
            + '<path d="M44 8 Q50 14 46 20 Q42 14 44 8 Z" fill="#ff7043" stroke="none"/>' + t(30, 50, desc, 4.2))
    return 60, 60, body


add("ms_classe_feu", "Classe de feu (A, B, C, D, F)", MSP, params=[("classe", "Classe", "A", ["A", "B", "C", "D", "F"])], func=_classe_feu)

# ---------------------------------------------------------------- sûreté et surveillance
add("ms_agent", "Agent de sécurité", MSS, 40, 80,
    _head(20, 10, 7) + '<path d="M12 6 Q20 0 28 6 V8 H12 Z" fill="#263238" stroke="none"/>'
    + '<path d="M8 22 Q20 16 32 22 L34 50 H6 Z" fill="#263238" stroke="CC" stroke-width="1"/>'
    + '<rect x="9" y="26" width="9" height="5" rx="1" fill="#fdd835" stroke="none"/>' + _W(t(13.5, 30, "SÉCU", 2.6, "bold"))
    + _seg([(14, 50), (13, 76)], "#37474f", 7) + _seg([(26, 50), (27, 76)], "#37474f", 7)
    + _seg([(8, 24), (4, 46)], "#263238", 5) + _seg([(32, 24), (36, 46)], "#263238", 5)
    + '<rect x="30" y="30" width="5" height="8" rx="1" fill="#424242" stroke="none"/>')
add("ms_talkie", "Talkie-walkie", MSS, 30, 70,
    '<rect x="22" y="2" width="4" height="20" rx="2" fill="#424242" stroke="none"/><rect x="4" y="18" width="22" height="48" rx="4" fill="#263238" stroke="CC" stroke-width="1"/>'
    '<rect x="8" y="22" width="14" height="10" rx="1" fill="#a5d6a7" stroke="none"/>' + t(15, 29, "CH 3", 3.8, "bold")
    + "".join(f'<path d="M8 {38 + i * 3} H22" stroke="#546e7a" stroke-width="1"/>' for i in range(5)) + '<circle cx="15" cy="58" r="3" fill="#e53935" stroke="none"/>')
add("ms_lampe", "Lampe torche", MSS, 80, 30,
    '<rect x="4" y="9" width="44" height="12" rx="3" fill="#37474f" stroke="CC" stroke-width="1"/><path d="M48 7 H58 V23 H48 Z" fill="#455a64" stroke="CC" stroke-width="1"/>'
    '<ellipse cx="58" cy="15" rx="2" ry="8" fill="#fff59d" stroke="CC" stroke-width="0.8"/><path d="M60 8 L78 2 V28 L60 22 Z" fill="#fff59d" fill-opacity="0.5" stroke="none"/>'
    '<rect x="22" y="6" width="6" height="4" rx="1" fill="#e53935" stroke="none"/>')
add("ms_main_courante", "Main courante (registre)", MSS, 60, 60,
    '<rect x="6" y="4" width="48" height="52" rx="2" fill="#1565c0" stroke="CC" stroke-width="1.2"/><rect x="10" y="8" width="40" height="44" fill="#ffffff" stroke="none"/>'
    + t(30, 16, "MAIN COURANTE", 4.2, "bold") + "".join(f'<path d="M12 {22 + i * 6} H{48 - (i % 2) * 8}" stroke="#90a4ae" stroke-width="1"/>' for i in range(5))
    + '<path d="M40 50 L54 36 L57 39 L43 53 Z" fill="#fdd835" stroke="CC" stroke-width="0.8"/>')
add("ms_ronde", "Contrôleur de ronde et point de pointage", MSS, 70, 50,
    '<rect x="4" y="10" width="16" height="36" rx="5" fill="#424242" stroke="CC" stroke-width="1"/><rect x="7" y="16" width="10" height="8" rx="1" fill="#a5d6a7" stroke="none"/>'
    '<circle cx="12" cy="40" r="3" fill="#90a4ae" stroke="none"/>'
    '<rect x="44" y="16" width="20" height="20" rx="3" fill="#eceff1" stroke="CC" stroke-width="1"/><circle cx="54" cy="26" r="5" fill="#1e88e5" stroke="CC" stroke-width="0.8"/>'
    '<path d="M24 22 Q34 18 40 24 M26 28 Q34 24 38 30" stroke="#43a047" stroke-width="1.2" fill="none"/>')
add("ms_portique", "Portique de détection de métaux", MSS, 60, 90,
    '<path d="M2 88 H58" stroke="#9e9e9e" stroke-width="1.4"/><rect x="6" y="8" width="10" height="80" rx="2" fill="#cfd8dc" stroke="CC" stroke-width="1.2"/>'
    '<rect x="44" y="8" width="10" height="80" rx="2" fill="#cfd8dc" stroke="CC" stroke-width="1.2"/><rect x="4" y="2" width="52" height="10" rx="2" fill="#90a4ae" stroke="CC" stroke-width="1.2"/>'
    + "".join(f'<circle cx="{x}" cy="7" r="1.6" fill="{c}" stroke="none"/>' for x, c in ((20, "#43a047"), (30, "#fdd835"), (40, "#e53935")))
    + "".join(f'<path d="M8 {20 + i * 12} H14 M46 {20 + i * 12} H52" stroke="#78909c" stroke-width="1"/>' for i in range(6)))
add("ms_raquette", "Détecteur de métaux manuel (raquette)", MSS, 80, 30,
    '<rect x="4" y="11" width="26" height="8" rx="4" fill="#212121" stroke="CC" stroke-width="1"/>'
    '<path d="M30 9 H66 Q76 9 76 15 Q76 21 66 21 H30 Z" fill="#424242" stroke="CC" stroke-width="1"/><path d="M36 12 H66 Q72 12 72 15 Q72 18 66 18 H36 Z" fill="none" stroke="#fdd835" stroke-width="1"/>'
    '<circle cx="24" cy="15" r="2" fill="#43a047" stroke="none"/>')
add("ms_tourniquet", "Tourniquet de contrôle d'accès", MSS, 60, 70,
    '<path d="M2 68 H58" stroke="#9e9e9e" stroke-width="1.4"/><rect x="8" y="20" width="20" height="48" rx="3" fill="#cfd8dc" stroke="CC" stroke-width="1.2"/>'
    '<rect x="11" y="24" width="14" height="8" rx="1" fill="#263238" stroke="none"/><circle cx="18" cy="28" r="2" fill="#43a047" stroke="none"/>'
    '<circle cx="28" cy="40" r="4" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/><path d="M28 40 H56 M28 40 L44 26 M28 40 L44 54" stroke="#9e9e9e" stroke-width="3" stroke-linecap="round"/>')
add("ms_badge", "Lecteur de badge et badge", MSS, 60, 50,
    '<rect x="4" y="4" width="24" height="40" rx="3" fill="#37474f" stroke="CC" stroke-width="1"/><circle cx="16" cy="20" r="6" fill="none" stroke="#90a4ae" stroke-width="1"/>'
    '<path d="M12 20 Q16 15 20 20 M10 20 Q16 12 22 20" stroke="#90a4ae" stroke-width="0.8" fill="none"/><circle cx="16" cy="36" r="2" fill="#43a047" stroke="none"/>'
    '<rect x="34" y="14" width="22" height="32" rx="2" fill="#ffffff" stroke="CC" stroke-width="1" transform="rotate(12 45 30)"/>'
    '<rect x="38" y="18" width="10" height="10" fill="#cfd8dc" stroke="none" transform="rotate(12 45 30)"/><path d="M38 34 H52 M38 38 H50" stroke="#90a4ae" stroke-width="1" transform="rotate(12 45 30)"/>')
add("ms_camera_dome", "Caméra de vidéosurveillance dôme", MSS, 60, 40,
    '<path d="M2 6 H58" stroke="#9e9e9e" stroke-width="2"/><rect x="10" y="6" width="40" height="8" fill="#eceff1" stroke="CC" stroke-width="1"/>'
    '<path d="M14 14 A16 16 0 0 0 46 14 Z" fill="#37474f" fill-opacity="0.85" stroke="CC" stroke-width="1"/><circle cx="30" cy="22" r="4" fill="#212121" stroke="#90a4ae" stroke-width="0.8"/>')
add("ms_camera_bullet", "Caméra de vidéosurveillance tube (bullet)", MSS, 70, 50,
    '<rect x="2" y="30" width="6" height="18" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/><path d="M8 38 H20 L28 26" stroke="#9e9e9e" stroke-width="3" fill="none"/>'
    '<rect x="22" y="10" width="44" height="18" rx="4" fill="#fafafa" stroke="CC" stroke-width="1.2" transform="rotate(10 44 19)"/>'
    '<path d="M24 8 H68" stroke="#cfd8dc" stroke-width="3" transform="rotate(10 44 19)"/><circle cx="64" cy="26" r="4" fill="#212121" stroke="#90a4ae" stroke-width="0.8"/>')
add("ms_pc_securite", "Poste central de sécurité (écrans de contrôle)", MSS, 90, 60,
    '<rect x="2" y="44" width="86" height="14" rx="2" fill="#8d6e63" stroke="CC" stroke-width="1"/>'
    + "".join(f'<rect x="{6 + c * 28}" y="{4 + r * 20}" width="24" height="17" rx="1" fill="#263238" stroke="CC" stroke-width="0.8"/>'
              f'<rect x="{8 + c * 28}" y="{6 + r * 20}" width="20" height="13" fill="{("#4fc3f7", "#81c784", "#ffb74d", "#90caf9", "#a5d6a7", "#ce93d8")[r * 3 + c]}" fill-opacity="0.6" stroke="none"/>' for r in range(2) for c in range(3))
    + '<rect x="30" y="48" width="30" height="6" rx="1" fill="#424242" stroke="none"/>')
add("ms_barriere_vauban", "Barrière de sécurité (type Vauban)", MSS, 90, 50,
    '<path d="M4 6 H86 V36 H4 Z" fill="none" stroke="#90a4ae" stroke-width="2.4"/>'
    + "".join(f'<path d="M{8 + i * 4} 6 V36" stroke="#b0bec5" stroke-width="1"/>' for i in range(20))
    + '<path d="M6 36 L2 48 M6 36 L14 48 M84 36 L76 48 M84 36 L88 48" stroke="#90a4ae" stroke-width="2"/>')
add("ms_gilet", "Gilet haute visibilité", MSS, 60, 60,
    '<path d="M16 4 L24 4 L30 14 L36 4 L44 4 L52 14 V56 H8 V14 Z" fill="#ffeb3b" stroke="CC" stroke-width="1.2"/>'
    '<path d="M8 34 H52 M8 42 H52" stroke="#b0bec5" stroke-width="3"/><path d="M30 14 V56" stroke="#fbc02d" stroke-width="1"/>')
add("ms_sifflet", "Sifflet", MSS, 50, 30,
    '<path d="M4 10 H28 Q44 10 44 20 Q44 28 34 28 Q24 28 24 20 V16 H4 Z" fill="#9e9e9e" stroke="CC" stroke-width="1.2"/><rect x="14" y="10" width="6" height="3" fill="#424242" stroke="none"/>'
    '<path d="M46 8 L50 4 M46 14 L50 14" stroke="CC" stroke-width="1"/>')

# ---------------------------------------------------------------- police et maintien de l'ordre
MSO = "Métiers de la sécurité – police et maintien de l'ordre"


def _voiture_police(p):
    gyro = p.get("gyrophare") == "Allumé"
    body = ('<path d="M6 34 V26 Q6 22 12 21 L28 18 L40 8 Q44 6 50 6 H74 Q80 6 84 12 L92 20 Q104 21 106 26 V34 Q106 36 102 36 H8 Q6 36 6 34 Z" fill="#fafafa" stroke="CC" stroke-width="1.4"/>'
            '<path d="M6 26 H106 V31 H6 Z" fill="#1565c0" stroke="none"/><path d="M6 31 H106" stroke="#e53935" stroke-width="1.6"/>'
            '<path d="M42 10 Q45 8 50 8 H60 V19 H31 Z" fill="#b3e5fc" stroke="CC" stroke-width="1"/><path d="M63 8 H73 Q78 8 81 12 L88 19 H63 Z" fill="#b3e5fc" stroke="CC" stroke-width="1"/>'
            '<path d="M61 19 V34" stroke="CC" stroke-width="0.8"/>'
            '<rect x="48" y="1" width="22" height="5" rx="2" fill="#1e88e5" stroke="CC" stroke-width="0.8"/><rect x="59" y="1" width="11" height="5" rx="2" fill="#e53935" stroke="none"/>'
            + _W(t(40, 30.2, p.get("texte", "SÉCURITÉ") or "", _fs(p.get("texte", "SÉCURITÉ") or "", 4.6, 8), "bold"))
            + "".join(f'<circle cx="{x}" cy="36" r="8" fill="#263238" stroke="none"/><circle cx="{x}" cy="36" r="3.4" fill="#b0bec5" stroke="none"/>' for x in (26, 86)))
    if gyro:
        body += '<path d="M46 0 L40 -4 M72 0 L78 -4 M59 -1 V-5" stroke="#1e88e5" stroke-width="1.2"/>'
    return 112, 46, body


add("mso_voiture_police", "Véhicule d'intervention (sécurité, police)", MSO,
    params=[("gyrophare", "Gyrophare", "Éteint", ["Éteint", "Allumé"]), ("texte", "Texte", "SÉCURITÉ", None)], func=_voiture_police)
add("mso_pie", "Pistolet à impulsion électrique (type Taser)", MSO, 80, 50,
    '<path d="M6 10 H58 Q64 10 64 16 V22 H34 L30 44 Q29 48 24 48 H16 Q12 48 13 44 L18 22 H6 Z" fill="#fdd835" stroke="CC" stroke-width="1.4"/>'
    '<rect x="58" y="10" width="12" height="12" rx="1.5" fill="#212121" stroke="CC" stroke-width="1"/><path d="M34 22 Q36 32 28 32" stroke="CC" stroke-width="1.4" fill="none"/>'
    '<path d="M72 13 L78 11 M72 19 L78 21" stroke="#4fc3f7" stroke-width="1.2"/><rect x="10" y="13" width="10" height="5" rx="1" fill="#212121" stroke="none"/>')
add("mso_casque", "Casque de maintien de l'ordre à visière", MSO, 70, 60,
    '<path d="M10 38 C8 16 22 4 36 4 C52 4 62 16 62 36 Z" fill="#37474f" stroke="CC" stroke-width="1.6"/>'
    '<path d="M18 12 C28 4 46 4 56 16" stroke="#546e7a" stroke-width="3" fill="none"/>'
    '<path d="M8 22 C10 16 20 14 36 14 C50 14 58 18 60 24 L60 46 C56 54 44 58 34 58 C22 58 12 54 8 46 Z" fill="#b3e5fc" fill-opacity="0.45" stroke="#455a64" stroke-width="1.4"/>'
    '<path d="M16 26 L18 46 M24 26 L26 48" stroke="#ffffff" stroke-width="1.4" stroke-opacity="0.8"/><path d="M60 46 V52 H66" stroke="#263238" stroke-width="3" fill="none"/>')
def _fs(txt, base, ref):
    """Taille de police réduite si le texte est plus long que la référence."""
    return round(base * min(1.0, ref / max(1, len(txt))), 2)


_TXT = ("texte", "Texte", "SÉCURITÉ", None)


def _gilet_pb(p):
    txt = p.get("texte", "SÉCURITÉ") or ""
    return 60, 60, ('<path d="M14 4 L22 4 L30 12 L38 4 L46 4 L52 14 V56 H8 V14 Z" fill="#263238" stroke="CC" stroke-width="1.2"/>'
                    '<rect x="12" y="30" width="36" height="9" fill="#ffffff" stroke="none"/>' + t(30, 37, txt, _fs(txt, 5.4, 7), "bold")
                    + '<path d="M8 46 H52" stroke="#37474f" stroke-width="1"/><rect x="14" y="16" width="8" height="8" rx="1" fill="#37474f" stroke="none"/><rect x="38" y="16" width="8" height="8" rx="1" fill="#37474f" stroke="none"/>')


def _bouclier(p):
    txt = p.get("texte", "SÉCURITÉ") or ""
    return 50, 90, ('<rect x="4" y="4" width="42" height="82" rx="6" fill="#b3e5fc" fill-opacity="0.45" stroke="#455a64" stroke-width="2"/>'
                    '<rect x="10" y="10" width="30" height="20" rx="2" fill="none" stroke="#78909c" stroke-width="0.8"/>' + t(25, 50, txt, _fs(txt, 5.6, 7), "bold")
                    + '<path d="M12 60 L14 80 M20 60 L22 80" stroke="#ffffff" stroke-width="1.4" stroke-opacity="0.7"/>')


add("mso_gilet", "Gilet pare-balles", MSO, params=[_TXT], func=_gilet_pb)
add("mso_bouclier", "Bouclier de protection transparent", MSO, params=[_TXT], func=_bouclier)
add("mso_protections", "Protections de jambes et d'avant-bras", MSO, 70, 70,
    '<path d="M8 8 Q16 4 24 8 V58 Q16 64 8 58 Z" fill="#37474f" stroke="CC" stroke-width="1.2"/><path d="M8 26 H24 M8 44 H24" stroke="#546e7a" stroke-width="1.2"/>'
    '<ellipse cx="16" cy="32" rx="6" ry="5" fill="#455a64" stroke="CC" stroke-width="0.8"/>'
    '<path d="M40 14 Q50 10 60 14 V44 Q50 48 40 44 Z" fill="#37474f" stroke="CC" stroke-width="1.2"/><path d="M40 26 H60 M40 36 H60" stroke="#546e7a" stroke-width="1.2"/>')
add("mso_baton", "Bâton de défense à poignée latérale (tonfa)", MSO, 80, 40,
    '<rect x="4" y="16" width="72" height="8" rx="4" fill="#212121" stroke="CC" stroke-width="1"/><rect x="18" y="22" width="7" height="16" rx="3" fill="#212121" stroke="CC" stroke-width="1"/>'
    '<path d="M60 18 V22" stroke="#424242" stroke-width="1"/>')
add("mso_menottes", "Menottes", MSO, 70, 40,
    '<circle cx="18" cy="22" r="13" fill="none" stroke="#9e9e9e" stroke-width="4"/><circle cx="52" cy="22" r="13" fill="none" stroke="#9e9e9e" stroke-width="4"/>'
    '<path d="M31 22 H39" stroke="#9e9e9e" stroke-width="3"/><rect x="30" y="18" width="4" height="8" fill="#757575" stroke="none"/><rect x="36" y="18" width="4" height="8" fill="#757575" stroke="none"/>')
add("mso_masque_gaz", "Masque de protection respiratoire (masque à gaz)", MSO, 60, 60,
    '<path d="M10 20 Q10 6 30 6 Q50 6 50 20 V36 Q50 50 30 54 Q10 50 10 36 Z" fill="#424242" stroke="CC" stroke-width="1.4"/>'
    '<ellipse cx="22" cy="22" rx="7" ry="6" fill="#b3e5fc" stroke="CC" stroke-width="1"/><ellipse cx="38" cy="22" rx="7" ry="6" fill="#b3e5fc" stroke="CC" stroke-width="1"/>'
    '<circle cx="30" cy="44" r="9" fill="#616161" stroke="CC" stroke-width="1"/>' + "".join(f'<circle cx="{30 + 4 * math.cos(a):.1f}" cy="{44 + 4 * math.sin(a):.1f}" r="1" fill="#212121" stroke="none"/>' for a in [i * math.pi / 3 for i in range(6)]))


def _tenue_crs(p):
    masque = p.get("masque") == "Avec masque à gaz"
    bouclier = p.get("bouclier", "Avec bouclier") == "Avec bouclier"
    txt = p.get("texte", "SÉCURITÉ") or ""
    N, D = "#263238", "#37474f"
    body = (
        # jambes, protections de tibias, rangers
        f'<path d="M28 76 L26 112 H34 L36 80 Z M42 76 L44 112 H36 L36 80 Z" fill="{N}" stroke="CC" stroke-width="1"/>'
        f'<path d="M25 88 Q30 86 34 88 L33 108 H26 Z M36 88 Q40 86 45 88 L44 108 H37 Z" fill="{D}" stroke="CC" stroke-width="0.8"/>'
        '<ellipse cx="30" cy="92" rx="3.4" ry="3" fill="#455a64" stroke="none"/><ellipse cx="40" cy="92" rx="3.4" ry="3" fill="#455a64" stroke="none"/>'
        '<path d="M24 110 H35 V116 H21 Q21 112 24 110 Z M35 110 H46 Q49 112 49 116 H35 Z" fill="#000000" stroke="CC" stroke-width="0.8"/>'
        # ceinturon
        f'<rect x="24" y="72" width="22" height="6" fill="{N}" stroke="CC" stroke-width="0.8"/><rect x="33" y="73" width="4" height="4" fill="#9e9e9e" stroke="none"/>'
        # tronc : gilet pare-balles
        f'<path d="M22 38 Q35 32 48 38 L47 74 H23 Z" fill="{N}" stroke="CC" stroke-width="1.2"/>'
        '<rect x="24" y="52" width="22" height="7" fill="#ffffff" stroke="none"/>' + t(35, 57.6, txt, _fs(txt, 4.4, 6), "bold")
        + f'<rect x="25" y="42" width="7" height="7" rx="1" fill="{D}" stroke="none"/><rect x="38" y="42" width="7" height="7" rx="1" fill="{D}" stroke="none"/>'
        # épaulières et bras avec protections d'avant-bras
        f'<ellipse cx="20" cy="41" rx="6" ry="5" fill="{D}" stroke="CC" stroke-width="1"/><ellipse cx="50" cy="41" rx="6" ry="5" fill="{D}" stroke="CC" stroke-width="1"/>'
        + _seg([(18, 44), (14, 58), (18, 70)], N, 7) + _seg([(52, 44), (56, 58), (54, 70)], N, 7)
        + f'<path d="M12 58 L16 70 L21 68 L18 57 Z M54 57 L51 68 L56 70 L59 58 Z" fill="{D}" stroke="CC" stroke-width="0.8"/>'
        '<circle cx="18" cy="71" r="3" fill="#000000" stroke="none"/><circle cx="54" cy="71" r="3" fill="#000000" stroke="none"/>'
        # bâton de défense dans la main droite (côté droit de l'image)
        '<path d="M54 71 L64 100" stroke="#000000" stroke-width="3" stroke-linecap="round"/><path d="M56 76 L61 74" stroke="#000000" stroke-width="2.4" stroke-linecap="round"/>'
        # cou et tête
        f'<rect x="31" y="30" width="8" height="6" fill="{N}" stroke="none"/>'
        f'<path d="M23 20 C22 6 30 2 35 2 C41 2 48 6 47 20 Z" fill="{D}" stroke="CC" stroke-width="1.2"/>'
        f'<path d="M23 26 Q22 20 24 16 H46 Q48 20 47 26 Q46 34 35 34 Q24 34 23 26 Z" fill="#f2c6a0" stroke="CC" stroke-width="0.8"/>')
    if masque:
        body += ('<path d="M24 18 H46 V26 Q46 34 35 35 Q24 34 24 26 Z" fill="#424242" stroke="CC" stroke-width="0.8"/>'
                 '<ellipse cx="30" cy="22" rx="3.4" ry="2.8" fill="#b3e5fc" stroke="none"/><ellipse cx="40" cy="22" rx="3.4" ry="2.8" fill="#b3e5fc" stroke="none"/>'
                 '<circle cx="35" cy="30" r="4" fill="#616161" stroke="CC" stroke-width="0.6"/>')
    else:
        body += '<circle cx="31" cy="23" r="1" fill="#3e2723" stroke="none"/><circle cx="39" cy="23" r="1" fill="#3e2723" stroke="none"/><path d="M32 29 H38" stroke="#8d6e63" stroke-width="0.8"/>'
    # visière du casque
    body += ('<path d="M22 14 Q35 10 48 14 L48 30 Q35 38 22 30 Z" fill="#b3e5fc" fill-opacity="0.35" stroke="#455a64" stroke-width="1"/>'
             '<path d="M26 16 L27 28" stroke="#ffffff" stroke-width="1" stroke-opacity="0.8"/>')
    if bouclier:
        body += ('<rect x="2" y="44" width="24" height="56" rx="4" fill="#b3e5fc" fill-opacity="0.4" stroke="#455a64" stroke-width="1.4"/>'
                 + t(14, 70, txt, _fs(txt, 3.6, 6), "bold") + '<path d="M6 76 L7 94" stroke="#ffffff" stroke-width="1.2" stroke-opacity="0.8"/>')
    return 70, 118, body


add("mso_tenue_complete", "Tenue complète de maintien de l'ordre (CRS)", MSO,
    params=[("masque", "Masque", "Sans masque", ["Sans masque", "Avec masque à gaz"]),
            ("bouclier", "Bouclier", "Avec bouclier", ["Avec bouclier", "Sans bouclier"]),
            ("texte", "Texte du gilet et du bouclier", "SÉCURITÉ", None)], func=_tenue_crs)
