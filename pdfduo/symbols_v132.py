"""Bibliothèques 1.3.2 : métiers de bouche (cuisine), service en salle, couture,
structure d'un réseau (schéma technologique). Dessins originaux, sans marque ni logo."""
from .symbols import add, t

CUI = "Métiers de bouche – cuisine"
SAL = "Service et restauration – salle"
COU = "Couture – textile"
RST = "Réseau – structure (schéma technologique)"

_O = 'stroke="CC" stroke-width="1.2"'
_INOX, _INOX2, _BOIS, _NOIR = "#cfd8dc", "#90a4ae", "#c8a26b", "#37474f"

# ======================================================================= cuisine
add("cui_couteau_chef", "Couteau de chef (éminceur)", CUI, 100, 30,
    f'<path d="M40 10 H94 Q98 10 96 14 Q80 24 40 22 Z" fill="{_INOX}" {_O}/>'
    f'<rect x="6" y="11" width="34" height="10" rx="3" fill="{_NOIR}" stroke="none"/>'
    '<circle cx="15" cy="16" r="1.4" fill="#cfd8dc" stroke="none"/><circle cx="29" cy="16" r="1.4" fill="#cfd8dc" stroke="none"/>')
add("cui_couteau_office", "Couteau d'office", CUI, 70, 24,
    f'<path d="M32 9 H64 Q67 10 64 13 Q52 18 32 16 Z" fill="{_INOX}" {_O}/>'
    f'<rect x="6" y="8" width="26" height="9" rx="3" fill="{_NOIR}" stroke="none"/>')
add("cui_fusil", "Fusil à aiguiser", CUI, 100, 24,
    f'<rect x="38" y="10" width="58" height="4" rx="2" fill="{_INOX2}" {_O}/>'
    f'<path d="M30 6 V18" stroke="{_INOX2}" stroke-width="3"/>'
    f'<rect x="6" y="7" width="24" height="10" rx="4" fill="{_NOIR}" stroke="none"/>')
_HACCP = {"Rouge – viande crue": "#e53935", "Bleu – poisson cru": "#1e88e5", "Vert – fruits et légumes": "#43a047",
          "Jaune – volaille crue": "#fdd835", "Blanc – pain, produits laitiers": "#fafafa", "Marron – viande cuite": "#8d6e63"}


def _planche(p):
    c = _HACCP.get(p.get("couleur"), "#43a047")
    return 90, 50, (f'<rect x="4" y="6" width="74" height="40" rx="5" fill="{c}" {_O}/>'
                    f'<path d="M78 20 H82 Q86 20 86 26 Q86 32 82 32 H78" fill="{c}" {_O}/>'
                    '<rect x="10" y="12" width="62" height="28" rx="3" fill="none" stroke="#000000" stroke-opacity="0.15" stroke-width="1"/>')


add("cui_planche", "Planche à découper (couleurs HACCP)", CUI,
    params=[("couleur", "Couleur", "Vert – fruits et légumes", list(_HACCP))], func=_planche)
add("cui_casserole", "Casserole", CUI, 90, 50,
    f'<path d="M10 14 H58 V40 Q58 46 52 46 H16 Q10 46 10 40 Z" fill="{_INOX}" {_O}/>'
    f'<path d="M8 14 H60" stroke="CC" stroke-width="2"/><rect x="58" y="16" width="30" height="6" rx="3" fill="{_NOIR}" stroke="none"/>')
add("cui_poele", "Poêle", CUI, 100, 40,
    f'<path d="M6 14 H60 L56 30 Q55 34 50 34 H16 Q11 34 10 30 Z" fill="{_NOIR}" {_O}/>'
    f'<rect x="60" y="15" width="36" height="6" rx="3" fill="{_BOIS}" stroke="none" transform="rotate(-8 60 18)"/>')
add("cui_marmite", "Marmite (faitout) avec couvercle", CUI, 80, 60,
    f'<path d="M14 22 H66 V50 Q66 56 60 56 H20 Q14 56 14 50 Z" fill="{_INOX}" {_O}/>'
    f'<path d="M12 22 Q40 8 68 22 Z" fill="{_INOX2}" {_O}/><rect x="36" y="9" width="8" height="5" rx="2" fill="{_NOIR}" stroke="none"/>'
    f'<path d="M14 30 H6 V36 H14 M66 30 H74 V36 H66" fill="none" stroke="CC" stroke-width="1.6"/>')
add("cui_fouet", "Fouet", CUI, 90, 40,
    f'<rect x="4" y="16" width="30" height="8" rx="4" fill="{_NOIR}" stroke="none"/>'
    + "".join(f'<path d="M34 20 Q60 {20 - k} 86 20 Q60 {20 + k} 34 20" fill="none" stroke="{_INOX2}" stroke-width="1.2"/>' for k in (4, 9, 14)))
add("cui_maryse", "Maryse (spatule souple)", CUI, 90, 30,
    f'<rect x="4" y="13" width="54" height="5" rx="2" fill="{_BOIS}" stroke="none"/>'
    '<path d="M58 8 H80 Q88 8 88 15 Q88 22 80 22 H58 Z" fill="#ef5350" stroke="CC" stroke-width="1"/>')
add("cui_louche", "Louche", CUI, 90, 40,
    f'<path d="M6 10 Q4 6 8 6 L58 18" fill="none" stroke="{_INOX2}" stroke-width="3" stroke-linecap="round"/>'
    f'<path d="M56 16 H86 Q86 36 71 36 Q56 36 56 16 Z" fill="{_INOX}" {_O}/>')
add("cui_ecumoire", "Écumoire", CUI, 90, 40,
    f'<path d="M6 20 H54" stroke="{_INOX2}" stroke-width="3" stroke-linecap="round"/>'
    f'<circle cx="70" cy="20" r="16" fill="{_INOX}" {_O}/>'
    + "".join(f'<circle cx="{70 + dx}" cy="{20 + dy}" r="1.6" fill="#ffffff" stroke="CC" stroke-width="0.5"/>'
              for dx in (-8, 0, 8) for dy in (-8, 0, 8)))
add("cui_chinois", "Chinois (passoire conique)", CUI, 70, 70,
    f'<path d="M12 10 H58 L35 64 Z" fill="{_INOX}" {_O}/>'
    + "".join(f'<path d="M{14 + 3 * k} {12 + 7 * k} H{56 - 3 * k}" stroke="{_INOX2}" stroke-width="0.6"/>' for k in range(7))
    + f'<path d="M58 12 H68" stroke="{_NOIR}" stroke-width="4" stroke-linecap="round"/>')
add("cui_rouleau", "Rouleau à pâtisserie", CUI, 100, 24,
    f'<rect x="20" y="5" width="60" height="14" rx="4" fill="{_BOIS}" {_O}/>'
    f'<rect x="4" y="9" width="16" height="6" rx="3" fill="{_BOIS}" {_O}/><rect x="80" y="9" width="16" height="6" rx="3" fill="{_BOIS}" {_O}/>')
add("cui_poche_douille", "Poche à douille", CUI, 70, 60,
    f'<path d="M6 8 L46 8 L58 46 L52 52 Z" fill="#fff8e1" {_O}/>'
    f'<path d="M54 46 L64 56 L58 58 L50 50 Z" fill="{_INOX2}" stroke="CC" stroke-width="1"/>'
    '<path d="M10 12 L46 12" stroke="#ffcc80" stroke-width="3"/>')
add("cui_balance", "Balance de cuisine", CUI, 70, 50,
    f'<rect x="6" y="24" width="58" height="20" rx="4" fill="#eceff1" {_O}/>'
    f'<ellipse cx="35" cy="20" rx="26" ry="5" fill="{_INOX}" {_O}/>'
    '<rect x="22" y="30" width="26" height="9" rx="1" fill="#c5e1a5" stroke="none"/>' + t(35, 37, "500 g", 6, "bold"))
add("cui_thermo_sonde", "Thermomètre à sonde (contrôle des températures)", CUI, 80, 40,
    f'<rect x="4" y="8" width="30" height="24" rx="5" fill="#eceff1" {_O}/>'
    '<rect x="8" y="12" width="22" height="10" rx="1" fill="#c5e1a5" stroke="none"/>' + t(19, 20, "63 °C", 5.5, "bold")
    + f'<path d="M34 20 H78" stroke="{_INOX2}" stroke-width="2"/><path d="M76 18 L79 20 L76 22" fill="{_INOX2}" stroke="none"/>')
add("cui_bac_gn", "Bac gastronorme", CUI, 90, 40,
    f'<path d="M6 8 H84 L78 34 H12 Z" fill="{_INOX}" {_O}/><path d="M4 8 H86" stroke="CC" stroke-width="2"/>'
    + t(45, 24, "GN 1/1", 7, "bold"))
add("cui_piano", "Piano de cuisson (fourneau, 4 feux)", CUI, 100, 70,
    f'<rect x="4" y="18" width="92" height="48" rx="2" fill="{_INOX}" {_O}/>'
    f'<rect x="4" y="8" width="92" height="10" fill="{_INOX2}" {_O}/>'
    + "".join(f'<circle cx="{x}" cy="13" r="3" fill="{_NOIR}" stroke="none"/>' for x in (20, 40, 60, 80))
    + f'<rect x="12" y="28" width="76" height="30" rx="2" fill="{_NOIR}" stroke="none"/>'
    '<rect x="16" y="32" width="68" height="4" rx="2" fill="#78909c" stroke="none"/>')
add("cui_four_mixte", "Four mixte (vapeur et chaleur sèche)", CUI, 80, 80,
    f'<rect x="4" y="6" width="72" height="70" rx="3" fill="{_INOX}" {_O}/>'
    f'<rect x="10" y="12" width="46" height="56" rx="3" fill="{_NOIR}" stroke="none"/>'
    + "".join(f'<path d="M14 {22 + 10 * k} H52" stroke="#78909c" stroke-width="1"/>' for k in range(5))
    + '<rect x="61" y="14" width="11" height="10" rx="1" fill="#80deea" stroke="none"/>'
    '<circle cx="66.5" cy="36" r="4" fill="#78909c" stroke="none"/><path d="M58 40 V58" stroke="#78909c" stroke-width="2.4"/>')
add("cui_cellule_froid", "Cellule de refroidissement rapide", CUI, 70, 90,
    f'<rect x="4" y="4" width="62" height="82" rx="3" fill="{_INOX}" {_O}/>'
    '<rect x="10" y="10" width="50" height="12" rx="1" fill="#263238" stroke="none"/>'
    '<text x="35" y="19" font-size="7" font-family="DejaVu Sans Mono, monospace" text-anchor="middle" fill="#80deea" stroke="none">+3 °C</text>'
    '<path d="M58 30 V76" stroke="#78909c" stroke-width="3" stroke-linecap="round"/>'
    '<path d="M24 46 V66 M16 50 L32 62 M32 50 L16 62" stroke="#1e88e5" stroke-width="1.8" stroke-linecap="round"/>')
add("cui_plonge", "Plonge (bac de lavage et douchette)", CUI, 90, 70,
    f'<rect x="4" y="34" width="82" height="32" fill="{_INOX}" {_O}/>'
    f'<rect x="10" y="38" width="32" height="18" rx="2" fill="#b0bec5" stroke="none"/><rect x="48" y="38" width="32" height="18" rx="2" fill="#b0bec5" stroke="none"/>'
    f'<path d="M26 34 V8 Q26 4 30 4 H36" fill="none" stroke="{_INOX2}" stroke-width="3"/>'
    f'<path d="M36 4 Q46 6 44 18" fill="none" stroke="{_NOIR}" stroke-width="1.4"/><rect x="40" y="18" width="8" height="8" rx="2" fill="{_INOX2}" stroke="none"/>')
add("cui_toque", "Toque de cuisinier", CUI, 60, 60,
    '<path d="M14 36 Q4 30 8 18 Q12 8 22 12 Q26 2 34 6 Q44 2 48 12 Q58 12 54 26 Q52 32 46 36 Z" fill="#ffffff" stroke="CC" stroke-width="1.2"/>'
    '<rect x="14" y="36" width="32" height="16" fill="#ffffff" stroke="CC" stroke-width="1.2"/>'
    '<path d="M22 36 V52 M30 36 V52 M38 36 V52" stroke="#e0e0e0" stroke-width="1"/>')
add("cui_veste", "Veste de cuisinier", CUI, 70, 70,
    '<path d="M22 6 L12 10 L4 34 L12 37 L16 26 V64 H54 V26 L58 37 L66 34 L58 10 L48 6 Q35 14 22 6 Z" fill="#ffffff" stroke="CC" stroke-width="1.2"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="CC" stroke="none"/>' for x in (28, 42) for y in (22, 34, 46, 58))
    + '<path d="M22 6 Q35 18 48 6" fill="none" stroke="CC" stroke-width="1"/>')
add("cui_tablier", "Tablier de cuisine", CUI, 60, 70,
    '<path d="M18 4 H42 V18 L50 22 V64 H10 V22 L18 18 Z" fill="#ffffff" stroke="CC" stroke-width="1.2"/>'
    '<path d="M18 4 Q30 -6 42 4" fill="none" stroke="CC" stroke-width="1.2"/><path d="M10 26 H2 M50 26 H58" stroke="CC" stroke-width="1.6"/>'
    '<rect x="20" y="36" width="20" height="12" fill="none" stroke="#bdbdbd" stroke-width="1"/>')

# ======================================================================= service en salle
add("sal_assiette", "Assiette plate (vue de dessus)", SAL, 60, 60,
    f'<circle cx="30" cy="30" r="26" fill="#ffffff" {_O}/><circle cx="30" cy="30" r="17" fill="none" stroke="#bdbdbd" stroke-width="1"/>')
add("sal_assiette_creuse", "Assiette creuse (vue de côté)", SAL, 70, 30,
    f'<path d="M4 8 H66 Q60 24 35 24 Q10 24 4 8 Z" fill="#ffffff" {_O}/><path d="M24 24 L22 28 H48 L46 24" fill="#ffffff" {_O}/>')
add("sal_fourchette", "Fourchette", SAL, 20, 80,
    f'<path d="M4 4 V22 Q4 30 10 30 Q16 30 16 22 V4 M8 4 V20 M12 4 V20" fill="none" stroke="{_INOX2}" stroke-width="1.6"/>'
    f'<rect x="8" y="30" width="4" height="46" rx="2" fill="{_INOX2}" stroke="none"/>')
add("sal_couteau", "Couteau de table", SAL, 20, 80,
    f'<path d="M8 4 Q15 8 14 34 H8 Z" fill="{_INOX}" {_O}/><rect x="7" y="34" width="6" height="42" rx="3" fill="{_INOX2}" stroke="none"/>')
add("sal_cuillere", "Cuillère", SAL, 20, 80,
    f'<ellipse cx="10" cy="14" rx="7" ry="11" fill="{_INOX}" {_O}/><rect x="8" y="24" width="4" height="52" rx="2" fill="{_INOX2}" stroke="none"/>')
add("sal_couvert_dresse", "Couvert dressé (vue de dessus)", SAL, 120, 80,
    f'<rect x="2" y="2" width="116" height="76" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>'
    f'<circle cx="60" cy="44" r="24" fill="#ffffff" {_O}/><circle cx="60" cy="44" r="15" fill="none" stroke="#bdbdbd" stroke-width="1"/>'
    f'<path d="M28 22 V64 M24 22 V30 Q24 34 28 34 Q32 34 32 30 V22" fill="none" stroke="{_INOX2}" stroke-width="1.6"/>'
    f'<path d="M92 22 Q97 26 96 40 H92 Z" fill="{_INOX}" stroke="CC" stroke-width="0.8"/><path d="M94 40 V66" stroke="{_INOX2}" stroke-width="2.4"/>'
    f'<ellipse cx="104" cy="28" rx="3.5" ry="6" fill="{_INOX}" stroke="CC" stroke-width="0.8"/><path d="M104 34 V66" stroke="{_INOX2}" stroke-width="2"/>'
    '<circle cx="96" cy="10" r="6" fill="#e3f2fd" stroke="CC" stroke-width="1"/><circle cx="108" cy="12" r="5" fill="#f3e5f5" stroke="CC" stroke-width="1"/>'
    '<path d="M50 6 H70 L66 14 H54 Z" fill="#ffffff" stroke="CC" stroke-width="0.8"/>')
add("sal_verre_eau", "Verre à eau", SAL, 40, 60,
    f'<path d="M8 6 H32 L28 54 H12 Z" fill="#e3f2fd" {_O}/><path d="M10 24 H30 L28 52 H12 Z" fill="#90caf9" stroke="none" opacity="0.6"/>')
add("sal_verre_vin", "Verre à vin (à pied)", SAL, 40, 70,
    f'<path d="M8 4 H32 Q34 30 20 36 Q6 30 8 4 Z" fill="#f3e5f5" {_O}/><path d="M9 18 H31 Q30 30 20 34 Q10 30 9 18 Z" fill="#ad1457" stroke="none" opacity="0.75"/>'
    f'<path d="M20 36 V62 M10 64 H30" stroke="CC" stroke-width="1.6"/>')
add("sal_flute", "Flûte à champagne", SAL, 30, 80,
    f'<path d="M8 4 H22 L20 44 Q15 48 10 44 Z" fill="#fff8e1" {_O}/><path d="M9 14 H21 L19.5 42 Q15 45 10.5 42 Z" fill="#ffe082" stroke="none"/>'
    f'<path d="M15 47 V72 M7 74 H23" stroke="CC" stroke-width="1.6"/>')
add("sal_tasse", "Tasse et soucoupe", SAL, 70, 50,
    f'<path d="M14 10 H48 V30 Q48 40 38 40 H24 Q14 40 14 30 Z" fill="#ffffff" {_O}/>'
    '<path d="M48 16 Q58 16 58 24 Q58 32 48 32" fill="none" stroke="CC" stroke-width="2"/>'
    f'<path d="M4 42 H66 Q60 48 35 48 Q10 48 4 42 Z" fill="#ffffff" {_O}/><path d="M16 14 H46" stroke="#6d4c41" stroke-width="3"/>')
add("sal_carafe", "Carafe", SAL, 50, 70,
    f'<path d="M18 4 H32 V18 Q46 26 44 50 Q42 66 25 66 Q8 66 6 50 Q4 26 18 18 Z" fill="#e3f2fd" {_O}/>'
    '<path d="M8 40 Q25 36 42 40 Q44 62 25 63 Q8 62 8 40 Z" fill="#90caf9" stroke="none" opacity="0.6"/>')
add("sal_bouteille_vin", "Bouteille de vin", SAL, 30, 90,
    '<path d="M11 4 H19 V28 Q26 34 26 44 V84 Q26 87 23 87 H7 Q4 87 4 84 V44 Q4 34 11 28 Z" fill="#33691e" stroke="CC" stroke-width="1.2"/>'
    '<rect x="11" y="4" width="8" height="10" fill="#880e4f" stroke="none"/><rect x="6" y="52" width="18" height="20" fill="#fff8e1" stroke="none"/>')
add("sal_seau_glace", "Seau à glace", SAL, 60, 60,
    f'<path d="M8 18 H52 L46 56 H14 Z" fill="{_INOX}" {_O}/><path d="M4 18 H56" stroke="CC" stroke-width="2"/>'
    '<path d="M24 4 V18 M24 4 H32 V18" fill="#33691e" stroke="none"/><rect x="24" y="2" width="8" height="18" fill="#33691e" stroke="none"/>'
    '<path d="M14 18 l6 -6 l6 6 M30 18 l6 -7 l6 7" fill="#e1f5fe" stroke="#81d4fa" stroke-width="1"/>')
add("sal_plateau", "Plateau de service", SAL, 90, 30,
    f'<path d="M4 12 H86 L82 20 H8 Z" fill="#8d6e63" {_O}/><rect x="22" y="4" width="14" height="8" fill="#e3f2fd" stroke="CC" stroke-width="0.8"/>'
    '<rect x="44" y="2" width="10" height="10" fill="#e3f2fd" stroke="CC" stroke-width="0.8"/>')
add("sal_limonadier", "Tire-bouchon limonadier", SAL, 90, 40,
    f'<rect x="10" y="16" width="70" height="8" rx="4" fill="#5d4037" stroke="none"/>'
    f'<path d="M14 16 L4 8 L8 6 L18 14" fill="{_INOX2}" stroke="none"/>'
    f'<path d="M44 24 Q40 28 44 30 Q48 32 44 34 Q40 36 44 38" fill="none" stroke="{_INOX2}" stroke-width="2"/>'
    f'<path d="M80 18 L88 14" stroke="{_INOX2}" stroke-width="3"/>')
add("sal_serviette", "Serviette pliée", SAL, 60, 50,
    '<path d="M6 44 L30 6 L54 44 Z" fill="#ffffff" stroke="CC" stroke-width="1.2"/><path d="M30 6 L30 44 M18 25 L42 25" stroke="#e0e0e0" stroke-width="1"/>')
add("sal_carnet", "Bloc de commande et stylo", SAL, 60, 70,
    f'<rect x="8" y="6" width="38" height="58" rx="2" fill="#ffffff" {_O}/><rect x="8" y="6" width="38" height="8" fill="#ffcc80" stroke="none"/>'
    + "".join(f'<path d="M14 {22 + 7 * k} H40" stroke="#90caf9" stroke-width="1"/>' for k in range(6))
    + '<path d="M50 20 L56 58 L53 64 L47 59 Z" fill="#1e88e5" stroke="none"/>')
add("sal_tpe", "Terminal de paiement (carte bancaire)", SAL, 50, 80,
    f'<rect x="6" y="4" width="38" height="72" rx="6" fill="{_NOIR}" {_O}/><rect x="11" y="10" width="28" height="18" rx="1" fill="#b3e5fc" stroke="none"/>'
    + "".join(f'<rect x="{12 + 9 * c}" y="{34 + 8 * r}" width="7" height="5" rx="1" fill="#cfd8dc" stroke="none"/>' for c in range(3) for r in range(4))
    + '<rect x="12" y="68" width="7" height="5" rx="1" fill="#e53935" stroke="none"/><rect x="31" y="68" width="7" height="5" rx="1" fill="#43a047" stroke="none"/>')
add("sal_machine_cafe", "Machine à expresso (percolateur)", SAL, 90, 70,
    f'<rect x="6" y="8" width="78" height="44" rx="4" fill="{_INOX}" {_O}/><rect x="6" y="52" width="78" height="12" fill="{_NOIR}" stroke="none"/>'
    + "".join(f'<path d="M{x} 30 H{x + 14} V36 H{x} Z" fill="{_NOIR}" stroke="none"/><path d="M{x + 14} 33 H{x + 22}" stroke="{_NOIR}" stroke-width="2"/>' for x in (16, 50))
    + "".join(f'<rect x="{x + 2}" y="42" width="9" height="8" rx="1" fill="#ffffff" stroke="CC" stroke-width="0.8"/>' for x in (16, 50))
    + '<path d="M78 14 V40" stroke="#78909c" stroke-width="2"/>')
add("sal_chariot", "Chariot de service (guéridon)", SAL, 90, 70,
    f'<rect x="8" y="14" width="70" height="5" fill="#8d6e63" stroke="none"/><rect x="8" y="42" width="70" height="5" fill="#8d6e63" stroke="none"/>'
    f'<path d="M12 14 V58 M74 14 V58 M74 14 L84 6" stroke="{_INOX2}" stroke-width="2.4"/>'
    '<circle cx="12" cy="62" r="4" fill="#263238" stroke="none"/><circle cx="74" cy="62" r="4" fill="#263238" stroke="none"/>')
add("sal_ardoise", "Ardoise menu du jour", SAL, 60, 80,
    f'<rect x="6" y="6" width="48" height="60" rx="2" fill="#263238" stroke="#8d6e63" stroke-width="3"/>'
    '<path d="M14 66 L10 78 M46 66 L50 78" stroke="#8d6e63" stroke-width="3"/>'
    + t(30, 18, "MENU", 7, "bold").replace('fill="CC"', 'fill="#ffffff"')
    + "".join(f'<path d="M14 {26 + 8 * k} H{46 - 6 * (k % 2)}" stroke="#ffffff" stroke-width="1" stroke-opacity="0.8"/>' for k in range(4)))

# ======================================================================= couture
_FIL = "#e53935"
add("cou_machine", "Machine à coudre", COU, 100, 70,
    '<path d="M10 56 V22 Q10 12 20 12 H76 Q86 12 86 22 V34 H72 V26 H28 V56 Z" fill="#eceff1" stroke="CC" stroke-width="1.2"/>'
    '<rect x="4" y="56" width="92" height="10" rx="2" fill="#b0bec5" stroke="CC" stroke-width="1.2"/>'
    '<path d="M78 34 V48 M76 48 H80" stroke="CC" stroke-width="1.6"/><circle cx="90" cy="22" r="6" fill="#78909c" stroke="none"/>'
    f'<rect x="30" y="4" width="8" height="8" rx="1" fill="{_FIL}" stroke="none"/><rect x="40" y="16" width="20" height="6" rx="1" fill="#90caf9" stroke="none"/>')
add("cou_surjeteuse", "Surjeteuse", COU, 90, 70,
    '<path d="M8 58 V24 Q8 14 18 14 H72 Q82 14 82 24 V58 Z" fill="#eceff1" stroke="CC" stroke-width="1.2"/>'
    + "".join(f'<rect x="{18 + 14 * k}" y="2" width="8" height="12" rx="1" fill="{c}" stroke="none"/>' for k, c in enumerate(("#e53935", "#1e88e5", "#43a047", "#fdd835")))
    + '<rect x="4" y="58" width="82" height="8" rx="2" fill="#b0bec5" stroke="CC" stroke-width="1.2"/><rect x="50" y="34" width="22" height="18" rx="2" fill="#cfd8dc" stroke="none"/>')
add("cou_aiguille", "Aiguille à coudre (avec fil)", COU, 90, 30,
    f'<path d="M6 15 L80 13 Q86 15 80 17 Z" fill="{_INOX}" {_O}/><ellipse cx="74" cy="15" rx="3" ry="1" fill="#ffffff" stroke="CC" stroke-width="0.6"/>'
    f'<path d="M74 15 Q86 4 70 4 Q50 4 40 24" fill="none" stroke="{_FIL}" stroke-width="1.2"/>')
add("cou_epingles", "Épingles et pelote", COU, 70, 60,
    '<path d="M8 44 Q8 24 35 24 Q62 24 62 44 Z" fill="#e53935" stroke="CC" stroke-width="1.2"/><rect x="6" y="44" width="58" height="10" rx="3" fill="#8d6e63" stroke="none"/>'
    + "".join(f'<path d="M{x} 34 L{x + dx} 10" stroke="{_INOX2}" stroke-width="1"/><circle cx="{x + dx}" cy="10" r="2.6" fill="{c}" stroke="none"/>'
              for x, dx, c in ((22, -6, "#fdd835"), (32, 2, "#1e88e5"), (42, 8, "#43a047"), (50, 12, "#ab47bc"))))
add("cou_de", "Dé à coudre", COU, 40, 40,
    f'<path d="M8 36 V18 Q8 4 20 4 Q32 4 32 18 V36 Z" fill="{_INOX}" {_O}/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="1" fill="{_INOX2}" stroke="none"/>' for x in (14, 20, 26) for y in (12, 18, 24, 30)))
add("cou_bobine", "Bobine de fil", COU, 40, 60,
    f'<rect x="4" y="4" width="32" height="6" rx="2" fill="{_BOIS}" {_O}/><rect x="4" y="50" width="32" height="6" rx="2" fill="{_BOIS}" {_O}/>'
    f'<rect x="8" y="10" width="24" height="40" fill="{_FIL}" stroke="none"/>'
    + "".join(f'<path d="M8 {14 + 6 * k} H32" stroke="#b71c1c" stroke-width="0.8"/>' for k in range(6)))
add("cou_ciseaux", "Ciseaux de couturière", COU, 100, 40,
    f'<path d="M34 20 L96 12 Q98 14 96 15 L38 22 Z" fill="{_INOX}" stroke="CC" stroke-width="1"/>'
    f'<path d="M34 20 L92 26 Q94 25 92 23 L38 18 Z" fill="{_INOX2}" stroke="CC" stroke-width="1"/>'
    f'<ellipse cx="14" cy="12" rx="10" ry="6" fill="none" stroke="{_NOIR}" stroke-width="3.6"/><ellipse cx="18" cy="30" rx="12" ry="7" fill="none" stroke="{_NOIR}" stroke-width="3.6"/>'
    f'<path d="M23 14 L34 19 M28 27 L34 21" stroke="{_NOIR}" stroke-width="3.6"/><circle cx="34" cy="20" r="1.6" fill="#cfd8dc" stroke="none"/>')
add("cou_decoud_vite", "Découd-vite", COU, 80, 24,
    f'<rect x="4" y="8" width="34" height="8" rx="4" fill="#ab47bc" stroke="none"/>'
    f'<path d="M38 12 H64 M64 12 Q72 6 76 8 M64 12 L72 12" fill="none" stroke="{_INOX2}" stroke-width="1.8"/><circle cx="72" cy="12" r="1.8" fill="#e53935" stroke="none"/>')
add("cou_metre", "Mètre ruban de couturière", COU, 90, 50,
    '<circle cx="20" cy="25" r="16" fill="#fdd835" stroke="CC" stroke-width="1"/><circle cx="20" cy="25" r="5" fill="#ffffff" stroke="none"/>'
    '<path d="M20 9 H86 V19 H34" fill="#fff59d" stroke="CC" stroke-width="1"/>'
    + "".join(f'<path d="M{40 + 4 * k} 9 V{12 if k % 5 else 15}" stroke="CC" stroke-width="0.6"/>' for k in range(12)))
add("cou_craie", "Craie de tailleur", COU, 50, 40,
    '<path d="M6 30 L24 6 L44 30 Z" fill="#90caf9" stroke="CC" stroke-width="1.2"/><path d="M14 30 L24 16 L36 30" fill="none" stroke="#ffffff" stroke-width="1"/>')
add("cou_roulette", "Roulette à tracer", COU, 80, 40,
    f'<rect x="4" y="16" width="34" height="8" rx="4" fill="#ffca28" stroke="none"/><path d="M38 20 H56" stroke="{_INOX2}" stroke-width="2"/>'
    f'<circle cx="64" cy="20" r="10" fill="{_INOX}" {_O}/>'
    + "".join(f'<path d="M{64 + 10 * dx} {20 + 10 * dy} L{64 + 13 * dx} {20 + 13 * dy}" stroke="CC" stroke-width="1"/>'
              for dx, dy in ((1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7), (-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7))))
add("cou_patron", "Patron (gabarit papier)", COU, 70, 80,
    '<path d="M10 6 H44 L60 22 V74 H10 Z" fill="#fff8e1" stroke="CC" stroke-width="1.2" stroke-dasharray="4 2"/>'
    '<path d="M20 20 V60 M17 24 L20 20 L23 24 M17 56 L20 60 L23 56" fill="none" stroke="CC" stroke-width="1"/>'
    '<path d="M10 40 L14 38 L14 42 Z M60 46 L56 44 L56 48 Z" fill="CC" stroke="none"/>' + t(40, 46, "DEVANT", 5.5, "bold"))
add("cou_mannequin", "Mannequin de couture", COU, 60, 100,
    '<path d="M20 8 Q30 4 40 8 L46 14 Q50 30 44 40 Q40 50 46 60 L42 66 H18 L14 60 Q20 50 16 40 Q10 30 14 14 Z" fill="#d7ccc8" stroke="CC" stroke-width="1.2"/>'
    '<rect x="26" y="2" width="8" height="6" fill="#8d6e63" stroke="none"/><path d="M30 66 V90 M18 94 H42 M30 90 L20 94 M30 90 L40 94" stroke="#5d4037" stroke-width="2.4"/>')
add("cou_fer", "Fer à repasser", COU, 90, 50,
    '<path d="M6 40 Q10 20 40 16 H80 V40 Z" fill="#e3f2fd" stroke="CC" stroke-width="1.2"/>'
    '<path d="M30 16 Q34 4 50 4 H74 Q80 4 80 10 V16" fill="none" stroke="#1e88e5" stroke-width="4"/>'
    f'<rect x="4" y="40" width="78" height="5" rx="2" fill="{_INOX2}" stroke="none"/>')
add("cou_boutons", "Boutons", COU, 70, 40,
    "".join(f'<circle cx="{x}" cy="20" r="{r}" fill="{c}" stroke="CC" stroke-width="1"/>'
            f'<circle cx="{x - 2}" cy="18" r="0.9" fill="#ffffff" stroke="none"/><circle cx="{x + 2}" cy="18" r="0.9" fill="#ffffff" stroke="none"/>'
            f'<circle cx="{x - 2}" cy="22" r="0.9" fill="#ffffff" stroke="none"/><circle cx="{x + 2}" cy="22" r="0.9" fill="#ffffff" stroke="none"/>'
            for x, r, c in ((12, 8, "#1e88e5"), (34, 10, "#8d6e63"), (56, 7, "#e53935"))))
add("cou_fermeture", "Fermeture à glissière", COU, 30, 100,
    '<rect x="6" y="6" width="18" height="88" fill="#1e88e5" stroke="none"/>'
    + "".join(f'<rect x="{12 if k % 2 else 15}" y="{30 + 4 * k}" width="3" height="3" fill="#cfd8dc" stroke="none"/>' for k in range(15))
    + f'<rect x="10" y="20" width="10" height="10" rx="2" fill="{_INOX2}" stroke="CC" stroke-width="0.8"/><rect x="13" y="30" width="4" height="10" rx="2" fill="{_INOX2}" stroke="none"/>')
add("cou_tissu", "Rouleau de tissu", COU, 100, 50,
    '<path d="M20 8 H90 V36 H20" fill="#f48fb1" stroke="CC" stroke-width="1.2"/>'
    '<ellipse cx="20" cy="22" rx="10" ry="14" fill="#f8bbd0" stroke="CC" stroke-width="1.2"/><ellipse cx="20" cy="22" rx="3" ry="4" fill="#8d6e63" stroke="none"/>'
    + "".join(f'<circle cx="{40 + 12 * c}" cy="{16 + 10 * r}" r="2" fill="#ffffff" stroke="none"/>' for c in range(4) for r in range(2)))
add("cou_point_droit", "Point droit (couture)", COU, 100, 20,
    "".join(f'<path d="M{6 + 12 * k} 10 H{14 + 12 * k}" stroke="{_FIL}" stroke-width="2"/>' for k in range(8)))
add("cou_point_zigzag", "Point zigzag (couture)", COU, 100, 20,
    f'<path d="M4 14 ' + " ".join(f"L{8 + 6 * k} {6 if k % 2 == 0 else 14}" for k in range(15)) + f'" fill="none" stroke="{_FIL}" stroke-width="1.6"/>')

# ======================================================================= structure réseau (schéma technologique)
_W = "#ffffff"


def _ports(x0, y0, n, w=5, h=4, gap=2, col="#263238"):
    return "".join(f'<rect x="{x0 + k * (w + gap)}" y="{y0}" width="{w}" height="{h}" fill="{col}" stroke="none"/>' for k in range(n))


add("rst_box", "Box internet professionnelle (fibre)", RST, 80, 60,
    '<path d="M16 14 L40 4 L64 14 L64 46 L40 56 L16 46 Z" fill="#eceff1" stroke="CC" stroke-width="1.2"/>'
    '<path d="M16 14 L40 24 L64 14 M40 24 V56" fill="none" stroke="CC" stroke-width="1"/>'
    '<circle cx="28" cy="28" r="1.6" fill="#43a047" stroke="none"/><circle cx="28" cy="34" r="1.6" fill="#43a047" stroke="none"/>'
    '<path d="M46 34 L58 28 M46 40 L58 34" stroke="#90a4ae" stroke-width="1.2"/>',
    pins=[(40, 0), (40, 60)])
add("rst_parefeu", "Pare-feu UTM (boîtier 1U)", RST, 120, 40,
    f'<rect x="4" y="8" width="112" height="24" rx="2" fill="#1565c0" {_O}/><rect x="8" y="12" width="26" height="16" rx="1" fill="{_W}" stroke="none"/>'
    '<path d="M12 16 H18 M12 20 H22 M12 24 H16" stroke="#e53935" stroke-width="1.6"/>'
    + _ports(42, 14, 8, 6, 5, 2, "#e3f2fd") + _ports(42, 21, 8, 6, 5, 2, "#e3f2fd")
    + '<circle cx="108" cy="16" r="1.5" fill="#43a047" stroke="none"/><circle cx="108" cy="22" r="1.5" fill="#fdd835" stroke="none"/>',
    pins=[(60, 0), (60, 40)])
add("rst_switch", "Switch manageable 24 ports PoE + 4 SFP", RST, 160, 40,
    f'<rect x="4" y="8" width="152" height="24" rx="2" fill="#cfd8dc" {_O}/><rect x="8" y="12" width="12" height="16" rx="1" fill="#90a4ae" stroke="none"/>'
    + _ports(26, 13, 12, 6, 5, 2) + _ports(26, 22, 12, 6, 5, 2)
    + _ports(124, 13, 2, 9, 5, 3, "#546e7a") + _ports(124, 22, 2, 9, 5, 3, "#546e7a")
    + '<circle cx="150" cy="14" r="1.5" fill="#43a047" stroke="none"/>',
    pins=[(80, 0), (40, 40), (80, 40), (120, 40)])
add("rst_serveur", "Serveur rack 1U", RST, 120, 30,
    f'<rect x="4" y="5" width="112" height="20" rx="2" fill="#455a64" {_O}/>'
    + "".join(f'<rect x="{12 + 12 * k}" y="9" width="9" height="12" rx="1" fill="#78909c" stroke="none"/>' for k in range(6))
    + '<path d="M86 9 V21 M90 9 V21 M94 9 V21 M98 9 V21" stroke="#263238" stroke-width="1.4"/>'
    '<circle cx="108" cy="12" r="1.6" fill="#43a047" stroke="none"/><circle cx="108" cy="18" r="1.6" fill="#29b6f6" stroke="none"/>',
    pins=[(60, 0), (60, 30)])
add("rst_serveurs2", "Baie de 2 serveurs (rack)", RST, 120, 60,
    f'<rect x="4" y="4" width="112" height="52" rx="3" fill="#263238" {_O}/>'
    + "".join(f'<rect x="10" y="{10 + 22 * r}" width="100" height="18" rx="2" fill="#546e7a" stroke="none"/>'
              + "".join(f'<rect x="{16 + 11 * k}" y="{13 + 22 * r}" width="8" height="12" rx="1" fill="#90a4ae" stroke="none"/>' for k in range(6))
              + f'<circle cx="102" cy="{19 + 22 * r}" r="1.6" fill="#43a047" stroke="none"/>' for r in range(2)),
    pins=[(60, 0), (60, 60)])
add("rst_ap", "Point d'accès Wi-Fi plafonnier (PoE)", RST, 80, 60,
    '<ellipse cx="40" cy="34" rx="30" ry="14" fill="#fafafa" stroke="CC" stroke-width="1.2"/>'
    '<ellipse cx="40" cy="32" rx="22" ry="9" fill="none" stroke="#e0e0e0" stroke-width="1"/><circle cx="40" cy="33" r="2" fill="#29b6f6" stroke="none"/>'
    + "".join(f'<path d="M{40 - r} {16 - r * 0.2} Q40 {8 - r * 0.8} {40 + r} {16 - r * 0.2}" fill="none" stroke="#29b6f6" stroke-width="1.6"/>' for r in (6, 11)),
    pins=[(40, 0), (80, 30), (0, 30), (40, 60)])
add("rst_pc", "Poste client (unité centrale + écran)", RST, 80, 60,
    f'<rect x="4" y="6" width="46" height="32" rx="2" fill="{_NOIR}" {_O}/><rect x="8" y="10" width="38" height="24" fill="#b3e5fc" stroke="none"/>'
    '<path d="M27 38 V46 M17 48 H37" stroke="CC" stroke-width="2"/>'
    f'<rect x="56" y="4" width="20" height="50" rx="2" fill="#455a64" {_O}/><rect x="60" y="10" width="12" height="3" fill="#90a4ae" stroke="none"/>'
    '<circle cx="66" cy="44" r="2" fill="#43a047" stroke="none"/>',
    pins=[(40, 0), (40, 60)])
add("rst_ssid", "Réseau Wi-Fi (SSID) – cadre à nommer", RST, 180, 40,
    f'<rect x="4" y="6" width="172" height="28" rx="2" fill="{_W}" stroke="CC" stroke-width="1.6"/>',
    pins=[(0, 20), (180, 20)])
add("rst_vlan", "Étiquette VLAN", RST, 180, 20,
    '<rect x="2" y="2" width="176" height="16" rx="8" fill="#e3f2fd" stroke="#1e88e5" stroke-width="1"/>',
    pins=[(90, 0), (90, 20)])
add("rst_legende", "Légende des liaisons (WAN, trunk VLAN, accès)", RST, 120, 70,
    f'<rect x="2" y="2" width="116" height="66" fill="{_W}" stroke="CC" stroke-width="1"/>'
    + t(60, 12, "Légende", 7, "bold")
    + '<path d="M10 26 H34" stroke="#e53935" stroke-width="2"/><path d="M10 40 H34" stroke="#1e88e5" stroke-width="3"/>'
    '<path d="M10 54 H34" stroke="#616161" stroke-width="1.6"/>'
    + t(76, 28, "WAN / DMZ", 6) + t(76, 42, "Trunk VLAN (802.1Q)", 6) + t(76, 56, "Accès (VLAN)", 6))
# le repère s'écrit dans le cadre (nom du SSID, du VLAN)
from .symbols import SYMBOLS as _ALL  # noqa: E402
for _s in _ALL:
    if _s.id in ("rst_ssid", "rst_vlan"):
        _s.label_at = (90, 20) if _s.id == "rst_ssid" else (90, 10)
        _s.label_scale = 1.0
