"""Bibliothèques de symboles de PDF DUO.

Chaque symbole est un petit dessin SVG.
- Symboles « papier » (schémas, plans électriques) : 10 unités = 1 pas de grille de 2,5 mm,
  les bornes tombent sur la grille (largeur et hauteur multiples de 20).
- Symboles « réels » (architecture) : 1 unité = 1 cm réel, mis à l'échelle du plan (1/50, 1/100...).

Le mot-clé CC est remplacé par la couleur du trait.
"""
import math


TXT = 'fill="CC" stroke="none" font-family="Helvetica, Arial, sans-serif" text-anchor="middle"'


def t(x, y, s, size=8, weight="normal"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" {TXT}>{s}</text>'


class Sym:
    def __init__(self, sid, name, cat, w=0, h=0, body="", kind="paper", params=None, func=None,
                 pins=None, pin_names=""):
        self.id, self.name, self.cat = sid, name, cat
        self.pins = pins or []          # points de connexion [(x, y)] en unités du symbole
        self.pin_names = pin_names      # noms par défaut des bornes, ex. "A1 A2"
        self.w, self.h, self.body = w, h, body
        self.kind = kind          # "paper" ou "real"
        self.params = params or []  # [(clé, libellé, défaut, min, max)]
        self.func = func          # func(params) -> (w, h, body)
        self.texts = []           # textes toujours horizontaux [(x, y, texte, taille, gras)], même en miroir
        self.label_at = None      # (x, y) : le repère (X1…) s'écrit à cet endroit, dans le dessin
        self.label_scale = 1.6    # taille du repère écrit dans le dessin (× taille normale)

    def defaults(self):
        return {spec[0]: spec[2] for spec in self.params}

    def geometry(self, params=None):
        if self.func:
            p = self.defaults()
            p.update(params or {})
            return self.func(p)
        return self.w, self.h, self.body

    def svg(self, color="#000000", sw=1.4, params=None):
        w, h, body = self.geometry(params)
        body = body.replace("CC", color)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
                f'<g fill="none" stroke="{color}" stroke-width="{sw:.3f}" stroke-linecap="round" '
                f'stroke-linejoin="round">{body}</g></svg>')


SYMBOLS = []
CATEGORIES = []


def add(*a, **k):
    s = Sym(*a, **k)
    SYMBOLS.append(s)
    if s.cat not in CATEGORIES:
        CATEGORIES.append(s.cat)
    return s


# ---------------------------------------------------------------- schéma électrique
E = "Électricité – schémas"
# Convention : fil horizontal ; NO = lame en pente vers le bas et vers la gauche, sous le fil ;
# NF = barre verticale à gauche dessinée vers le haut (miroir du NO).
add("contact_no", "Contact à fermeture (NO)", E, 40, 20,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>', pins=[(0, 10), (40, 10)], pin_names="13 14")
add("contact_nf", "Contact à ouverture (NF)", E, 40, 20,
    '<path d="M0 10 H14 V3 M26 10 H40 M26 10 L12 3.5"/>', pins=[(0, 10), (40, 10)], pin_names="21 22")
add("bp_no", "Bouton poussoir à fermeture", E, 40, 40,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>'
    '<path d="M19 14 V32" stroke-dasharray="2 2"/><path d="M13 28 V32 H25 V28"/>',
    pins=[(0, 10), (40, 10)], pin_names="3 4")
add("bp_nf", "Bouton poussoir à ouverture", E, 40, 40,
    '<path d="M0 10 H14 V3 M26 10 H40 M26 10 L12 3.5"/>'
    '<path d="M19 6.8 V32" stroke-dasharray="2 2"/><path d="M13 28 V32 H25 V28"/>',
    pins=[(0, 10), (40, 10)], pin_names="1 2")
add("inter_manuel", "Interrupteur (commande manuelle)", E, 40, 40,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>'
    '<path d="M19 14 V30" stroke-dasharray="2 2"/><path d="M19 30 H26"/>')
add("contact_tempo", "Contact temporisé travail (NO)", E, 40, 40,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>'
    '<path d="M17 15 V27 M21 14 V27"/><path d="M13 31 A6 6 0 0 1 25 31"/>')
add("bobine", "Bobine relais / contacteur (KM, KA)", E, 40, 20,
    '<path d="M0 10 H15 M25 10 H40"/><rect x="15" y="1" width="10" height="18"/>',
    pins=[(0, 10), (40, 10)], pin_names="A1 A2")
add("relais_therm", "Relais thermique (F)", E, 40, 20,
    '<path d="M0 10 H10 M30 10 H40"/><rect x="10" y="3" width="20" height="14"/>'
    '<path d="M14 10 H17 V6 H23 V10 H26"/>')
add("fusible", "Fusible", E, 40, 20,
    '<path d="M0 10 H40"/><rect x="11" y="5" width="18" height="10"/>')
add("disjoncteur", "Disjoncteur", E, 40, 20,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17 M12 8 L16 12 M16 8 L12 12"/>')
add("sectionneur", "Sectionneur", E, 40, 20,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17 M14 6 V14"/>')
add("lampe", "Lampe / voyant", E, 40, 20,
    '<path d="M0 10 H12 M28 10 H40"/><circle cx="20" cy="10" r="8"/>'
    '<path d="M14.3 4.3 L25.7 15.7 M25.7 4.3 L14.3 15.7"/>')
add("resistance", "Résistance", E, 40, 20,
    '<path d="M0 10 H10 M30 10 H40"/><rect x="10" y="6" width="20" height="8"/>')
add("potentiometre", "Potentiomètre", E, 40, 20,
    '<path d="M0 10 H10 M30 10 H40"/><rect x="10" y="6" width="20" height="8"/>'
    '<path d="M12 18 L28 2"/><path d="M28 2 L23 3 M28 2 L27 7"/>')
add("ldr", "Photorésistance (LDR)", E, 40, 20,
    '<path d="M0 10 H10 M30 10 H40"/><rect x="10" y="7" width="20" height="8"/>'
    '<path d="M8 0 L14 5 M13 1 L14 5 L10 5 M15 0 L21 5 M20 1 L21 5 L17 5"/>')
add("condensateur", "Condensateur", E, 40, 20,
    '<path d="M0 10 H17 M23 10 H40 M17 2 V18 M23 2 V18"/>')
add("condo_pol", "Condensateur polarisé", E, 40, 20,
    '<path d="M0 10 H17 M23 10 H40 M17 2 V18"/><rect x="22" y="2" width="3" height="16" fill="CC"/>'
    '<path d="M11 3 H15 M13 1 V5"/>')
add("inductance", "Bobine / inductance", E, 40, 20,
    '<path d="M0 10 H8 A3 3 0 0 1 14 10 A3 3 0 0 1 20 10 A3 3 0 0 1 26 10 A3 3 0 0 1 32 10 H40"/>')
add("diode", "Diode", E, 40, 20,
    '<path d="M0 10 H14 M25 10 H40 M25 4 V16"/><path d="M14 4 V16 L25 10 Z" fill="CC"/>')
add("led", "DEL (LED)", E, 40, 20,
    '<path d="M0 10 H14 M25 10 H40 M25 4 V16"/><path d="M14 4 V16 L25 10 Z" fill="CC"/>'
    '<path d="M21 4 L26 -1 M23 -1 H26 V2 M25 6 L30 1 M27 1 H30 V4" stroke-width="1"/>')
add("zener", "Diode Zener", E, 40, 20,
    '<path d="M0 10 H14 M25 10 H40 M22 18 L25 16 V4 L28 2"/><path d="M14 4 V16 L25 10 Z" fill="CC"/>')
add("npn", "Transistor NPN", E, 40, 40,
    '<path d="M0 20 H16 M16 10 V30" stroke-width="2.2"/><path d="M16 15 L30 6 V0 M16 25 L30 34 V40"/>'
    '<path d="M30 34 L23 33 L26 29 Z" fill="CC"/><circle cx="22" cy="20" r="13"/>')
add("pnp", "Transistor PNP", E, 40, 40,
    '<path d="M0 20 H16 M16 10 V30" stroke-width="2.2"/><path d="M16 15 L30 6 V0 M16 25 L30 34 V40"/>'
    '<path d="M17 25.6 L24 26.7 L21 30.7 Z" fill="CC"/><circle cx="22" cy="20" r="13"/>')
add("pile", "Pile / batterie", E, 40, 20,
    '<path d="M0 10 H17 M23 10 H40 M17 1 V19"/><path d="M23 5 V15" stroke-width="3"/>'
    '<path d="M10 3 H14 M12 1 V5"/>')
add("source_dc", "Générateur de tension continue", E, 40, 20,
    '<path d="M0 10 H11 M29 10 H40"/><circle cx="20" cy="10" r="9"/><path d="M14 8 H26 M14 12 H17 M19 12 H21 M23 12 H26"/>')
add("source_ac", "Générateur de tension alternative", E, 40, 20,
    '<path d="M0 10 H11 M29 10 H40"/><circle cx="20" cy="10" r="9"/>'
    '<path d="M14 10 Q17 4 20 10 T26 10"/>')
add("moteur", "Moteur", E, 40, 20,
    '<path d="M0 10 H11 M29 10 H40"/><circle cx="20" cy="10" r="9"/>' + t(20, 13.5, "M", 10, "bold"))
add("transfo", "Transformateur", E, 40, 20,
    '<path d="M0 10 H7 M33 10 H40"/><circle cx="15" cy="10" r="8"/><circle cx="25" cy="10" r="8"/>')
add("sonnerie", "Sonnerie", E, 40, 20,
    '<path d="M0 10 H12 M28 10 H40 M12 10 V16 H28 V10"/><path d="M12 16 A8 8 0 0 1 28 16" />')
add("haut_parleur", "Haut-parleur", E, 40, 20,
    '<path d="M0 10 H14 M26 10 H40"/><rect x="14" y="6" width="5" height="8"/><path d="M19 6 L25 1 V19 L19 14"/>')
for sid, nm, lt in (("amperemetre", "Ampèremètre", "A"), ("voltmetre", "Voltmètre", "V"),
                    ("ohmmetre", "Ohmmètre", "Ω"), ("wattmetre", "Wattmètre", "W")):
    add(sid, nm, E, 40, 20, '<path d="M0 10 H11 M29 10 H40"/><circle cx="20" cy="10" r="9"/>'
        + t(20, 13.5, lt, 10, "bold"))
add("jonction", "Point de jonction", E, 20, 20, '<circle cx="10" cy="10" r="1.8" fill="CC"/>')
add("borne", "Borne", E, 20, 20, '<circle cx="10" cy="10" r="2.5"/>')
add("masse", "Masse", E, 20, 20, '<path d="M10 0 V10 M3 10 H17 M3 10 L0 15 M10 10 L7 15 M17 10 L14 15"/>')
add("terre", "Terre", E, 20, 20, '<path d="M10 0 V8 M2 8 H18 M5 12 H15 M8 16 H12"/>')
add("phase_neutre", "Alimentation (+ / L)", E, 20, 20, '<path d="M10 20 V8 M4 8 H16"/>' + t(10, 5, "+", 7))

# ---------------------------------------------------------------- logique
L = "Fonctions logiques / logigramme"
GIN2 = '<path d="M0 10 H10 M0 30 H10"/>'
GOUT = '<path d="M30 20 H40"/>'
GBOX = '<rect x="10" y="2" width="20" height="36"/>'
for sid, nm, lt in (("et_cei", "ET (norme CEI)", "&amp;"), ("ou_cei", "OU (norme CEI)", "≥1"),
                    ("xor_cei", "OU exclusif (norme CEI)", "=1")):
    add(sid, nm, L, 40, 40, GIN2 + GOUT + GBOX + t(20, 13, lt, 8))
for sid, nm, lt in (("nand_cei", "NON-ET (norme CEI)", "&amp;"), ("nor_cei", "NON-OU (norme CEI)", "≥1")):
    add(sid, nm, L, 40, 40, GIN2 + '<path d="M33 20 H40"/><circle cx="31.5" cy="20" r="1.5"/>' + GBOX
        + t(20, 13, lt, 8))
add("non_cei", "NON (norme CEI)", L, 40, 40,
    '<path d="M0 20 H10 M33 20 H40"/><circle cx="31.5" cy="20" r="1.5"/>' + GBOX + t(20, 13, "1", 8))
# Formes américaines (ANSI)
AND = '<path d="M10 4 H20 A16 16 0 0 1 20 36 H10 Z"/>'
OR = '<path d="M8 4 Q15 20 8 36 Q24 36 34 20 Q24 4 8 4 Z"/>'
add("et_us", "ET (forme américaine)", L, 40, 40, '<path d="M0 10 H10 M0 30 H10 M36 20 H40"/>' + AND)
add("nand_us", "NON-ET (forme américaine)", L, 40, 40,
    '<path d="M0 10 H10 M0 30 H10"/>' + '<path d="M10 4 H18 A16 16 0 0 1 18 36 H10 Z"/><circle cx="36.5" cy="20" r="2"/>')
add("ou_us", "OU (forme américaine)", L, 40, 40, '<path d="M0 10 H11 M0 30 H11 M34 20 H40"/>' + OR)
add("nor_us", "NON-OU (forme américaine)", L, 40, 40,
    '<path d="M0 10 H11 M0 30 H11"/><path d="M6 4 Q13 20 6 36 Q21 36 31 20 Q21 4 6 4 Z"/><circle cx="34" cy="20" r="2"/>'.replace("M0 10 H11 M0 30 H11", "M0 10 H9 M0 30 H9"))
add("xor_us", "OU exclusif (forme américaine)", L, 40, 40,
    '<path d="M0 10 H11 M0 30 H11 M34 20 H40"/>' + OR + '<path d="M4 4 Q11 20 4 36"/>')
add("non_us", "NON (forme américaine)", L, 40, 40,
    '<path d="M0 20 H10 M36 20 H40 M10 6 L31 20 L10 34 Z"/><circle cx="33.5" cy="20" r="2.2"/>')
add("entree", "Entrée (variable)", L, 40, 20, '<path d="M2 4 H24 L32 10 L24 16 H2 Z M32 10 H40"/>')
add("sortie", "Sortie (variable)", L, 40, 20, '<path d="M0 10 H8 L16 4 H38 V16 H16 L8 10"/>')

# ---------------------------------------------------------------- plan électrique (installation domestique)
P = "Plan électrique – logement"
TERRE = '<path d="M10 9 V4 M6 4 H14"/>'
PRISE = '<path d="M2 14 H5 A5 5 0 0 1 15 14 H18"/>'          # arc ouvert posé sur le mur
add("prise_2pt", "Prise 16 A avec terre", P, 20, 20, PRISE + TERRE)
add("prise_2p", "Prise 16 A sans terre", P, 20, 20, PRISE)
add("prise_bloc3", "Bloc de 3 prises 16 A", P, 20, 20,
    PRISE + TERRE + '<path d="M6 11 L14 2"/>' + t(17, 4, "3", 5, "bold"))
add("prise_rasoir", "Prise rasoir", P, 20, 20, PRISE + '<path d="M10 9 V7"/><circle cx="10" cy="4.5" r="2.5"/>')
add("prise_20a", "Prise spécialisée 20 A (LL, LV, SL, four)", P, 20, 20,
    '<path d="M2 11 H5 A5 5 0 0 1 15 11 H18 M10 6 V2 M6 2 H14"/>' + t(10, 18, "20A", 5))
add("prise_32a", "Prise spécialisée 32 A (cuisson)", P, 20, 20,
    '<path d="M2 11 H5 A5 5 0 0 1 15 11 H18 M10 6 V2 M6 2 H14"/>' + t(10, 18, "32A", 5))
add("prise_tv", "Prise TV", P, 20, 20,
    '<path d="M1 15 H4 V8 H16 V15 H19 M10 8 V4 M6 4 H14"/>' + t(10, 14, "TV", 4.5))
add("prise_rj45", "Prise réseau Ethernet RJ45", P, 20, 20,
    '<path d="M0 15 H3 V8 H17 V15 H20 M10 8 V4 M6 4 H14"/>' + t(10, 13.8, "RJ45", 3.6))
add("prise_cmd", "Prise commandée", P, 20, 20, PRISE + TERRE + '<path d="M2 14 L-1 11"/>')
TIC = 'M9.8 11.2 L15 6 L17.5 8.5'
add("inter_sa", "Interrupteur simple allumage", P, 20, 20, f'<circle cx="8" cy="13" r="2.5"/><path d="{TIC}"/>')
add("inter_da", "Interrupteur double allumage", P, 20, 20,
    '<circle cx="10" cy="13" r="2.5"/><path d="M11.8 11.2 L16 7 L18.5 9.5 M8.2 11.2 L4 7 L1.5 9.5"/>')
add("inter_voyant", "Interrupteur simple allumage avec voyant", P, 20, 20,
    f'<circle cx="8" cy="13" r="2.5"/><path d="M6.2 11.2 L9.8 14.8 M9.8 11.2 L6.2 14.8 {TIC}"/>')
add("inter_vv", "Interrupteur va-et-vient", P, 20, 20,
    '<circle cx="10" cy="10" r="2.5"/><path d="M11.8 8.2 L16 4 L18.5 6.5 M8.2 11.8 L4 16 L1.5 13.5"/>')
add("inter_dvv", "Interrupteur double va-et-vient", P, 20, 20,
    '<circle cx="10" cy="10" r="2.5"/><path d="M11.8 8.2 L16 4 L18.5 6.5 M8.2 11.8 L4 16 L1.5 13.5'
    ' M8.2 8.2 L4 4 L1.5 6.5 M11.8 11.8 L16 16 L18.5 13.5"/>')
add("inter_bipolaire", "Interrupteur bipolaire", P, 20, 20,
    f'<circle cx="8" cy="13" r="2.5"/><path d="{TIC} M12.5 8.5 L15 11"/>')
add("poussoir", "Bouton poussoir", P, 20, 20, '<circle cx="10" cy="10" r="5"/><circle cx="10" cy="10" r="2.5"/>')
add("poussoir_voyant", "Bouton poussoir avec voyant lumineux", P, 20, 20,
    '<circle cx="10" cy="10" r="6"/><circle cx="10" cy="10" r="3.5"/><path d="M7.5 7.5 L12.5 12.5 M12.5 7.5 L7.5 12.5"/>')
add("variateur", "Variateur", P, 20, 20,
    f'<circle cx="8" cy="13" r="2.5"/><path d="{TIC} M3 19 L15 16 M15 16 L12 14.5 M15 16 L12.5 18.5"/>')
add("detecteur_mvt", "Détecteur de mouvement", P, 20, 20,
    '<path d="M4 16 A6 6 0 0 1 16 16 Z"/><path d="M6 7 A6 6 0 0 1 14 7 M3.5 4 A10 10 0 0 1 16.5 4"/>')
add("point_lum", "Point lumineux (DCL)", P, 20, 20, '<path d="M5 5 L15 15 M15 5 L5 15"/>')
add("applique", "Point lumineux en applique", P, 20, 20, '<path d="M5 3 L14 12 M14 3 L5 12 M3 16 H16"/>')
add("lampe_inc", "Lampe à incandescence", P, 20, 20,
    '<circle cx="10" cy="10" r="6"/><path d="M5.8 5.8 L14.2 14.2 M14.2 5.8 L5.8 14.2"/>')
add("spot", "Spot encastré", P, 20, 20,
    '<circle cx="10" cy="10" r="4"/><path d="M7.2 7.2 L12.8 12.8 M12.8 7.2 L7.2 12.8"/>')
add("reglette", "Réglette / tube fluorescent", P, 40, 20, '<path d="M4 10 H36 M4 6 V14 M36 6 V14"/>')
add("hublot", "Hublot extérieur", P, 20, 20,
    '<circle cx="10" cy="10" r="6"/><path d="M5.8 5.8 L14.2 14.2 M14.2 5.8 L5.8 14.2"/><path d="M4 10 H16" stroke-width="2.5"/>')
add("boite_deriv", "Boîte de dérivation", P, 20, 20, '<circle cx="10" cy="10" r="3.5"/><circle cx="10" cy="10" r="1" fill="CC"/>')
add("sortie_cable", "Sortie de câble", P, 20, 20, '<path d="M10 20 V6 M6 9 L10 4 L14 9"/>')
add("tableau", "Tableau de répartition (GTL)", P, 40, 20,
    '<rect x="2" y="4" width="36" height="12"/><path d="M2 16 L38 4 V16 Z" fill="CC"/>')
add("compteur", "Compteur (Linky)", P, 40, 20, '<rect x="4" y="3" width="32" height="14"/>' + t(20, 13, "kWh", 7, "bold"))
add("disj_branch", "Disjoncteur de branchement (AGCP)", P, 40, 20, '<rect x="4" y="3" width="32" height="14"/>' + t(20, 13, "AGCP", 7, "bold"))
add("telerupteur", "Télérupteur", P, 20, 20, '<rect x="1" y="4" width="18" height="12"/>' + t(10, 12.5, "TL", 7, "bold"))
add("minuterie", "Minuterie", P, 20, 20, '<rect x="1" y="4" width="18" height="12"/>' + t(10, 12.5, "MN", 6.5, "bold"))
add("daaf", "Détecteur de fumée (DAAF)", P, 20, 20, '<circle cx="10" cy="10" r="8"/>' + t(10, 12, "DF", 6, "bold"))
add("sonnette", "Sonnette / carillon", P, 20, 20,
    '<path d="M4 14 A6 6 0 0 1 16 14 Z M10 14 V18"/><path d="M8 18 H12"/>')
add("interphone", "Interphone / visiophone", P, 20, 20, '<rect x="2" y="3" width="16" height="14"/>' + t(10, 12.5, "INT", 5.5, "bold"))
add("vmc", "VMC", P, 20, 20, '<circle cx="10" cy="10" r="8"/>' + t(10, 12, "VMC", 5, "bold"))
add("convecteur", "Convecteur électrique", P, 40, 20,
    '<rect x="2" y="6" width="36" height="8"/><path d="' + " ".join(f"M{x} 6 V14" for x in range(5, 37, 3)) + '" stroke-width="0.6"/>')
add("seche_serv", "Sèche-serviettes", P, 20, 20,
    '<rect x="3" y="2" width="14" height="16"/><path d="M3 6 H17 M3 10 H17 M3 14 H17"/>')
add("chauffe_eau", "Cumulus / chauffe-eau", P, 20, 20,
    '<circle cx="10" cy="10" r="7"/><path d="M4.3 6 H15.7 M3.3 8 H16.7 M3 10 H17 M3.3 12 H16.7 M4.3 14 H15.7" stroke-width="0.7"/>')
add("thermostat", "Thermostat", P, 20, 20, '<rect x="2" y="3" width="16" height="14"/>' + t(10, 13, "θ", 9))
add("volet", "Commande de volet roulant", P, 20, 20,
    '<rect x="2" y="2" width="16" height="16"/><path d="M10 4 L6 8 H14 Z M10 16 L6 12 H14 Z" fill="CC"/>')
add("terre_piquet", "Piquet / prise de terre", P, 20, 20, '<path d="M10 0 V8 M2 8 H18 M5 12 H15 M8 16 H12"/>')
add("barrette_terre", "Barrette de terre", P, 20, 20, '<rect x="3" y="7" width="14" height="6"/><path d="M10 13 V20"/>')
add("lel", "Liaison équipotentielle (LES)", P, 20, 20, '<rect x="2" y="6" width="16" height="8"/>' + t(10, 12.5, "LES", 5, "bold"))

# ---------------------------------------------------------------- architecture (1 unité = 1 cm réel)
A = "Architecture – plan"
AW = ("largeur", "Largeur (cm)", 83, 30, 500)
WALL = ("mur", "Épaisseur du mur (cm)", 20, 5, 60)
MASK = 'fill="#ffffff" stroke="none"'


def porte(p):
    W, T = p["largeur"], p["mur"]
    y = W
    return W, W + T / 2, (f'<rect x="0" y="{y - T/2}" width="{W}" height="{T}" {MASK}/>'
                           f'<path d="M0 {y - T/2} V{y + T/2} M{W} {y - T/2} V{y + T/2}"/>'
                           f'<path d="M0 {y} V0" stroke-width="2.5"/>'
                           f'<path d="M{W} {y} A{W} {W} 0 0 0 0 0" stroke-width="0.8"/>')


def porte_double(p):
    W, T = p["largeur"], p["mur"]
    h, y = W / 2, W / 2
    return W, h + T / 2, (f'<rect x="0" y="{y - T/2}" width="{W}" height="{T}" {MASK}/>'
                           f'<path d="M0 {y - T/2} V{y + T/2} M{W} {y - T/2} V{y + T/2}"/>'
                           f'<path d="M0 {y} V0 M{W} {y} V0" stroke-width="2.5"/>'
                           f'<path d="M{W/2} {y} A{h} {h} 0 0 0 0 0 M{W/2} {y} A{h} {h} 0 0 1 {W} 0" stroke-width="0.8"/>')


def porte_coul(p):
    W, T = p["largeur"], p["mur"]
    return W * 1.6, T + 6, (f'<rect x="0" y="3" width="{W}" height="{T}" {MASK}/>'
                             f'<path d="M0 3 V{T + 3} M{W} 3 V{T + 3}"/>'
                             f'<rect x="{W * 0.15}" y="{T/2 + 3 - 2}" width="{W}" height="4" stroke-width="1.5"/>'
                             f'<path d="M{W*0.5} 1 H{W*1.0} M{W*0.95} -1 L{W} 1 L{W*0.95} 3" stroke-width="0.8"/>')


def porte_garage(p):
    W, T = p["largeur"], p["mur"]
    return W, T, (f'<rect x="0" y="0" width="{W}" height="{T}" {MASK}/>'
                  f'<path d="M0 0 V{T} M{W} 0 V{T}"/>'
                  f'<path d="M0 {T/2} H{W}" stroke-dasharray="10 6" stroke-width="2"/>')


def fenetre(p, n=1):
    W, T = p["largeur"], p["mur"]
    leaf = W / n
    y0 = leaf  # bord intérieur du mur
    arcs = ""
    if n == 1:
        arcs = (f'<path d="M0 {y0} V0" stroke-width="0.6" stroke-dasharray="4 3"/>'
                f'<path d="M{W} {y0} A{W} {W} 0 0 0 0 0" stroke-width="0.6" stroke-dasharray="4 3"/>')
    else:
        arcs = (f'<path d="M0 {y0} A{leaf} {leaf} 0 0 1 {leaf} {y0 - leaf}" stroke-width="0.6" stroke-dasharray="4 3"/>'
                f'<path d="M{W} {y0} A{leaf} {leaf} 0 0 0 {W - leaf} {y0 - leaf}" stroke-width="0.6" stroke-dasharray="4 3"/>')
    return W, leaf + T, (f'<rect x="0" y="{y0}" width="{W}" height="{T}" {MASK}/>'
                          f'<path d="M0 {y0} V{y0 + T} M{W} {y0} V{y0 + T}"/>'
                          f'<path d="M0 {y0 + T/2 - 1.5} H{W} M0 {y0 + T/2 + 1.5} H{W}" stroke-width="0.8"/>'
                          f'<path d="M0 {y0} H{W} M0 {y0 + T} H{W}" stroke-width="0.8"/>' + arcs)


def baie(p):
    W, T = p["largeur"], p["mur"]
    return W, T, (f'<rect x="0" y="0" width="{W}" height="{T}" {MASK}/>'
                  f'<path d="M0 0 V{T} M{W} 0 V{T} M0 0 H{W} M0 {T} H{W}" stroke-width="0.8"/>'
                  f'<path d="M0 {T*0.38} H{W*0.55} M{W*0.45} {T*0.62} H{W}" stroke-width="1.6"/>')


def escalier(p):
    W, Lg, n = p["largeur"], p["longueur"], int(p["marches"])
    step = Lg / n
    lines = "".join(f'M{i * step:.1f} 0 V{W} ' for i in range(1, n))
    return Lg, W, (f'<rect x="0" y="0" width="{Lg}" height="{W}"/><path d="{lines}" stroke-width="0.7"/>'
                   f'<path d="M{step/2} {W/2} H{Lg - step}" stroke-width="0.8"/>'
                   f'<path d="M{Lg - step*1.6} {W/2 - 6} L{Lg - step} {W/2} L{Lg - step*1.6} {W/2 + 6}" stroke-width="0.8"/>'
                   f'<circle cx="{step/2}" cy="{W/2}" r="3" fill="CC"/>')


add("porte", "Porte (1 vantail)", A, kind="real", params=[AW, WALL], func=porte)
add("porte_double", "Porte double", A, kind="real", params=[("largeur", "Largeur (cm)", 140, 60, 500), WALL], func=porte_double)
add("porte_coul", "Porte coulissante", A, kind="real", params=[AW, WALL], func=porte_coul)
add("porte_garage", "Porte de garage", A, kind="real", params=[("largeur", "Largeur (cm)", 240, 100, 600), WALL], func=porte_garage)
add("fenetre1", "Fenêtre 1 vantail", A, kind="real", params=[("largeur", "Largeur (cm)", 60, 30, 300), WALL],
    func=lambda p: fenetre(p, 1))
add("fenetre2", "Fenêtre 2 vantaux", A, kind="real", params=[("largeur", "Largeur (cm)", 120, 60, 400), WALL],
    func=lambda p: fenetre(p, 2))
add("baie", "Baie vitrée coulissante", A, kind="real", params=[("largeur", "Largeur (cm)", 240, 100, 600), WALL], func=baie)
add("escalier", "Escalier droit", A, kind="real",
    params=[("largeur", "Largeur (cm)", 90, 60, 200), ("longueur", "Longueur (cm)", 330, 100, 800),
            ("marches", "Nombre de marches", 15, 3, 30)], func=escalier)


def rect_sym(sid, name, w, h, inner=""):
    add(sid, name, A, kind="real", func=lambda p, w=w, h=h, inner=inner: (w, h, f'<rect x="0" y="0" width="{w}" height="{h}"/>' + inner))


add("wc", "WC", A, kind="real", func=lambda p: (40, 65,
    '<rect x="0" y="0" width="40" height="18" rx="2"/><path d="M5 18 Q5 65 20 65 Q35 65 35 18"/><ellipse cx="20" cy="38" rx="9" ry="14"/>'))
add("lavabo", "Lavabo", A, kind="real", func=lambda p: (60, 45,
    '<rect x="0" y="0" width="60" height="45" rx="6"/><ellipse cx="30" cy="25" rx="21" ry="14"/><circle cx="30" cy="8" r="2"/>'))
add("vasque2", "Meuble double vasque", A, kind="real", func=lambda p: (120, 50,
    '<rect x="0" y="0" width="120" height="50"/><ellipse cx="30" cy="27" rx="20" ry="14"/><ellipse cx="90" cy="27" rx="20" ry="14"/>'))
add("evier", "Évier 2 bacs", A, kind="real", func=lambda p: (120, 60,
    '<rect x="0" y="0" width="120" height="60"/><rect x="6" y="8" width="40" height="44" rx="4"/><rect x="52" y="8" width="40" height="44" rx="4"/>'
    '<path d="M98 12 H114 M98 20 H114 M98 28 H114 M98 36 H114 M98 44 H114" stroke-width="0.6"/>'))
add("baignoire", "Baignoire", A, kind="real", func=lambda p: (170, 70,
    '<rect x="0" y="0" width="170" height="70"/><rect x="8" y="8" width="154" height="54" rx="25"/><circle cx="22" cy="35" r="3"/>'))
add("douche", "Douche", A, kind="real", func=lambda p: (90, 90,
    '<rect x="0" y="0" width="90" height="90"/><path d="M0 0 L90 90 M90 0 L0 90" stroke-width="0.6"/><circle cx="45" cy="45" r="4"/>'))
rect_sym("lave_linge", "Lave-linge", 60, 60, t(30, 36, "LL", 18, "bold"))
rect_sym("seche_linge", "Sèche-linge", 60, 60, t(30, 36, "SL", 18, "bold"))
rect_sym("lave_vaisselle", "Lave-vaisselle", 60, 60, t(30, 36, "LV", 18, "bold"))
rect_sym("frigo", "Réfrigérateur", 60, 65, t(30, 39, "FR", 18, "bold"))
rect_sym("four", "Four", 60, 60, t(30, 36, "FO", 18, "bold"))
add("plaque", "Plaque de cuisson", A, kind="real", func=lambda p: (60, 60,
    '<rect x="0" y="0" width="60" height="60"/><circle cx="17" cy="17" r="10"/><circle cx="43" cy="17" r="8"/>'
    '<circle cx="17" cy="43" r="8"/><circle cx="43" cy="43" r="10"/>'))
add("lit2", "Lit 2 places (140 × 190)", A, kind="real", func=lambda p: (140, 200,
    '<rect x="0" y="0" width="140" height="200"/><rect x="10" y="12" width="52" height="30" rx="6"/>'
    '<rect x="78" y="12" width="52" height="30" rx="6"/><path d="M0 60 H140"/>'))
add("lit1", "Lit 1 place (90 × 190)", A, kind="real", func=lambda p: (90, 200,
    '<rect x="0" y="0" width="90" height="200"/><rect x="12" y="12" width="66" height="30" rx="6"/><path d="M0 60 H90"/>'))
add("table4", "Table + 4 chaises", A, kind="real", func=lambda p: (160, 160,
    '<rect x="30" y="40" width="100" height="80"/>'
    '<rect x="45" y="8" width="25" height="25" rx="3"/><rect x="90" y="8" width="25" height="25" rx="3"/>'
    '<rect x="45" y="127" width="25" height="25" rx="3"/><rect x="90" y="127" width="25" height="25" rx="3"/>'))
add("canape", "Canapé 3 places", A, kind="real", func=lambda p: (200, 90,
    '<rect x="0" y="0" width="200" height="90" rx="8"/><path d="M0 22 H200 M20 22 V90 M180 22 V90 M73 22 V90 M127 22 V90"/>'))
add("armoire", "Armoire / placard", A, kind="real", func=lambda p: (120, 60,
    '<rect x="0" y="0" width="120" height="60"/><path d="M0 0 L120 60 M60 0 V60"/>'))
add("nord", "Flèche Nord", A, 40, 60,
    '<circle cx="20" cy="36" r="16"/><path d="M20 8 L28 44 L20 38 L12 44 Z" fill="CC"/>' + t(20, 7, "N", 10, "bold"))


# ancrage des ouvertures sur l'axe du mur : (x, y) en cm dans le dessin du symbole
BY_ID0 = {x.id: x for x in SYMBOLS}
BY_ID0["porte"].wall_anchor = lambda p: (p["largeur"] / 2, p["largeur"])
BY_ID0["porte_double"].wall_anchor = lambda p: (p["largeur"] / 2, p["largeur"] / 2)
BY_ID0["porte_coul"].wall_anchor = lambda p: (p["largeur"] / 2, 3 + p["mur"] / 2)
BY_ID0["porte_garage"].wall_anchor = lambda p: (p["largeur"] / 2, p["mur"] / 2)
BY_ID0["fenetre1"].wall_anchor = lambda p: (p["largeur"] / 2, p["largeur"] + p["mur"] / 2)
BY_ID0["fenetre2"].wall_anchor = lambda p: (p["largeur"] / 2, p["largeur"] / 2 + p["mur"] / 2)
BY_ID0["baie"].wall_anchor = lambda p: (p["largeur"] / 2, p["mur"] / 2)

# ---------------------------------------------------------------- triphasé / puissance (schémas verticaux)
TRI = "Électricité – triphasé / puissance"
X3 = (10, 30, 50)


def poles(fn):
    return "".join(fn(x) for x in X3)


def link(y, x0=3, x1=50):
    return f'<path d="M{x0} {y} H{x1}" stroke-dasharray="2 2"/>'


PINS6 = [(10, 0), (30, 0), (50, 0), (10, 40), (30, 40), (50, 40)]
# contact vertical : borne fixe en haut, lame partant de la borne du bas vers le haut-gauche
add("km_puissance", "Contacteur tripolaire (contacts de puissance)", TRI, 60, 40,
    poles(lambda x: f'<path d="M{x} 0 V14 M{x} 26 V40 M{x} 26 L{x - 7} 12.5"/>'
                    f'<path d="M{x - 2.5} 14 A2.5 2.5 0 0 0 {x + 2.5} 14"/>') + link(19.5, 6.5, 46.5),
    pins=PINS6, pin_names="1 3 5 2 4 6")
add("sect_fus", "Sectionneur porte-fusibles tripolaire", TRI, 60, 60,
    poles(lambda x: f'<path d="M{x} 0 V18 M{x - 3} 18 H{x + 3} M{x} 32 V60 M{x} 32 L{x - 8} 16.5"/>'
                    f'<rect x="{x - 3}" y="38" width="6" height="16"/>') + link(24, 6, 46)
    + '<path d="M0 24 H4" /><path d="M0 20 V28"/>',
    pins=[(10, 0), (30, 0), (50, 0), (10, 60), (30, 60), (50, 60)], pin_names="1 3 5 2 4 6")
add("disj_moteur", "Disjoncteur moteur tripolaire", TRI, 60, 40,
    poles(lambda x: f'<path d="M{x} 0 V14 M{x} 26 V40 M{x} 26 L{x - 7} 12.5 M{x - 2} 12 L{x + 2} 16 M{x + 2} 12 L{x - 2} 16"/>')
    + link(19.5, 6.5, 46.5) + '<rect x="0" y="16" width="5" height="8"/>',
    pins=PINS6, pin_names="1 3 5 2 4 6")
add("rt_puissance", "Relais thermique tripolaire (puissance)", TRI, 60, 40,
    '<rect x="2" y="12" width="56" height="16" stroke-dasharray="3 2"/>'
    + poles(lambda x: f'<path d="M{x} 0 V15 H{x + 4} V25 H{x} V40"/>'),
    pins=PINS6, pin_names="1 3 5 2 4 6")
add("moteur3", "Moteur asynchrone triphasé", TRI, 60, 60,
    '<path d="M10 0 V14 L19 24 M30 0 V18 M50 0 V14 L41 24"/><circle cx="30" cy="34" r="16"/>'
    + t(30, 34, "M", 11, "bold") + t(30, 45, "3~", 8),
    pins=[(10, 0), (30, 0), (50, 0)], pin_names="U V W")
add("reseau3", "Réseau triphasé L1 L2 L3", TRI, 60, 40,
    '<path d="M10 40 V14 M30 40 V14 M50 40 V14"/>' + t(10, 10, "L1", 7, "bold") + t(30, 10, "L2", 7, "bold")
    + t(50, 10, "L3", 7, "bold"), pins=[(10, 40), (30, 40), (50, 40)])
add("reseau3n", "Réseau L1 L2 L3 N PE", TRI, 100, 40,
    "".join(f'<path d="M{x} 40 V14"/>' + t(x, 10, n, 7, "bold")
            for x, n in ((10, "L1"), (30, "L2"), (50, "L3"), (70, "N"), (90, "PE"))),
    pins=[(10, 40), (30, 40), (50, 40), (70, 40), (90, 40)])
add("verrou_meca", "Verrouillage mécanique (▽)", TRI, 40, 20,
    '<path d="M0 10 H14 M26 10 H40" stroke-dasharray="2 2"/><path d="M14 5 H26 L20 15 Z"/>')
add("contact_nf_6162", "Contact NF de verrouillage électrique (61-62)", TRI, 40, 20,
    '<path d="M0 10 H14 V3 M26 10 H40 M26 10 L12 3.5"/>', pins=[(0, 10), (40, 10)], pin_names="61 62")
add("contact_nf_5152", "Contact NF de verrouillage (51-52)", TRI, 40, 20,
    '<path d="M0 10 H14 V3 M26 10 H40 M26 10 L12 3.5"/>', pins=[(0, 10), (40, 10)], pin_names="51 52")
add("contact_am_1314", "Contact d'auto-maintien (NO 13-14)", TRI, 40, 20,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>', pins=[(0, 10), (40, 10)], pin_names="13 14")
add("contact_no_2324", "Contact NO (23-24)", TRI, 40, 20,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>', pins=[(0, 10), (40, 10)], pin_names="23 24")
add("contact_f_9596", "Contact du relais thermique (NF 95-96)", TRI, 40, 40,
    '<path d="M0 10 H14 V3 M26 10 H40 M26 10 L12 3.5"/>'
    '<path d="M19 6.8 V26" stroke-dasharray="2 2"/><path d="M13 26 H17 V32 H21 V26 H25"/>',
    pins=[(0, 10), (40, 10)], pin_names="95 96")
add("contact_f_9798", "Contact du relais thermique (NO 97-98)", TRI, 40, 40,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>'
    '<path d="M19 13.5 V26" stroke-dasharray="2 2"/><path d="M13 26 H17 V32 H21 V26 H25"/>',
    pins=[(0, 10), (40, 10)], pin_names="97 98")
add("au", "Arrêt d'urgence (coup de poing, NF)", TRI, 40, 40,
    '<path d="M0 10 H14 V3 M26 10 H40 M26 10 L12 3.5"/>'
    '<path d="M19 6.8 V30" stroke-dasharray="2 2"/><path d="M12 30 H26 A7 7 0 0 1 12 30 Z"/>',
    pins=[(0, 10), (40, 10)], pin_names="1 2")
add("bobine_km", "Bobine de contacteur KM (A1 / A2)", TRI, 40, 20,
    '<path d="M0 10 H15 M25 10 H40"/><rect x="15" y="1" width="10" height="18"/>',
    pins=[(0, 10), (40, 10)], pin_names="A1 A2")
add("voyant_marche", "Voyant (H)", TRI, 40, 20,
    '<path d="M0 10 H12 M28 10 H40"/><circle cx="20" cy="10" r="8"/>'
    '<path d="M14.3 4.3 L25.7 15.7 M25.7 4.3 L14.3 15.7"/>', pins=[(0, 10), (40, 10)], pin_names="X1 X2")
add("bornier", "Bornier (X)", TRI, 60, 20,
    poles(lambda x: f'<rect x="{x - 4}" y="5" width="8" height="10"/><circle cx="{x}" cy="10" r="1.6"/>'),
    pins=[(10, 0), (30, 0), (50, 0), (10, 20), (30, 20), (50, 20)])
add("transfo_cmd", "Transformateur de commande (T)", TRI, 40, 40,
    '<path d="M0 10 H8 A3 3 0 0 1 14 10 A3 3 0 0 1 20 10 A3 3 0 0 1 26 10 A3 3 0 0 1 32 10 H40 '
    'M0 30 H8 A3 3 0 0 0 14 30 A3 3 0 0 0 20 30 A3 3 0 0 0 26 30 A3 3 0 0 0 32 30 H40 M6 20 H34"/>',
    pins=[(0, 10), (40, 10), (0, 30), (40, 30)])

# ---------------------------------------------------------------- réseau informatique (CIEL)
NET = "Réseau informatique"
add("pc", "Ordinateur (poste client)", NET, 40, 40,
    '<rect x="6" y="4" width="28" height="20" rx="2"/><rect x="9" y="7" width="22" height="14" stroke-width="0.6"/>'
    '<path d="M20 24 V29 M13 30 H27 M5 36 H35 L33 32 H7 Z"/>')
add("portable", "Ordinateur portable", NET, 40, 40,
    '<rect x="8" y="8" width="24" height="17" rx="1.5"/><path d="M3 30 H37 L33 25 H7 Z"/>')
add("serveur", "Serveur", NET, 40, 40,
    '<rect x="11" y="2" width="18" height="36" rx="2"/><path d="M14 8 H26 M14 12 H26 M14 16 H26"/>'
    '<circle cx="20" cy="30" r="2"/>')
add("switch", "Commutateur (switch)", NET, 40, 40,
    '<rect x="2" y="12" width="36" height="16" rx="2"/>'
    '<path d="M8 17 H18 M15 15 L18 17 L15 19 M32 23 H22 M25 21 L22 23 L25 25 M22 17 H32 M29 15 L32 17 L29 19 M18 23 H8 M11 21 L8 23 L11 25"/>')
add("routeur", "Routeur", NET, 40, 40,
    '<ellipse cx="20" cy="15" rx="16" ry="6"/><path d="M4 15 V25 A16 6 0 0 0 36 25 V15"/>'
    '<path d="M14 13 L10 17 M10 13 V17 H14 M26 17 L30 13 M30 17 V13 H26"/>')
add("wifi", "Point d'accès Wi-Fi", NET, 40, 40,
    '<rect x="6" y="24" width="28" height="10" rx="2"/><circle cx="20" cy="18" r="1.6" fill="CC"/>'
    '<path d="M14 13 A8 8 0 0 1 26 13 M10 9 A13 13 0 0 1 30 9 M6 5 A18 18 0 0 1 34 5"/>')
add("box", "Box internet / modem", NET, 40, 40,
    '<rect x="4" y="18" width="32" height="14" rx="3"/><path d="M28 18 L32 4"/>'
    '<circle cx="10" cy="25" r="1.3" fill="CC"/><circle cx="15" cy="25" r="1.3" fill="CC"/><circle cx="20" cy="25" r="1.3" fill="CC"/>')
add("parefeu", "Pare-feu", NET, 40, 40,
    '<rect x="4" y="8" width="32" height="24"/><path d="M4 14 H36 M4 20 H36 M4 26 H36 M12 8 V14 M24 8 V14 M18 14 V20 '
    'M30 14 V20 M12 20 V26 M24 20 V26 M18 26 V32 M30 26 V32"/>')
add("internet", "Internet (nuage)", NET, 40, 40,
    '<path d="M11 30 A7 7 0 0 1 10 16 A8 8 0 0 1 24 11 A7 7 0 0 1 33 18 A6 6 0 0 1 31 30 Z"/>')
add("imprimante", "Imprimante réseau", NET, 40, 40,
    '<rect x="5" y="14" width="30" height="14" rx="2"/><path d="M11 14 V5 H29 V14 M11 24 V35 H29 V24 M14 29 H26 M14 32 H24"/>')
add("telephone_ip", "Téléphone IP", NET, 40, 40,
    '<rect x="12" y="8" width="22" height="26" rx="2"/><rect x="16" y="11" width="14" height="7"/>'
    '<path d="M6 8 V34 M6 8 H10 M6 34 H10"/>'
    '<circle cx="18" cy="23" r="1" fill="CC"/><circle cx="23" cy="23" r="1" fill="CC"/><circle cx="28" cy="23" r="1" fill="CC"/>'
    '<circle cx="18" cy="28" r="1" fill="CC"/><circle cx="23" cy="28" r="1" fill="CC"/><circle cx="28" cy="28" r="1" fill="CC"/>')
add("smartphone", "Smartphone", NET, 40, 40, '<rect x="13" y="3" width="14" height="34" rx="3"/><path d="M18 33 H22"/>')
add("tablette", "Tablette", NET, 40, 40, '<rect x="7" y="5" width="26" height="32" rx="3"/><circle cx="20" cy="33" r="1.2"/>')
add("camera_ip", "Caméra IP", NET, 40, 40,
    '<rect x="6" y="12" width="22" height="12" rx="2"/><path d="M28 15 L35 11 V25 L28 21 M14 24 L12 32 H22"/>')
add("nas", "NAS / stockage réseau", NET, 40, 40,
    '<rect x="8" y="4" width="24" height="32" rx="2"/><path d="M12 10 H28 M12 16 H28 M12 22 H28"/><circle cx="26" cy="30" r="1.5"/>')
add("hub", "Concentrateur (hub)", NET, 40, 40,
    '<rect x="2" y="13" width="36" height="14" rx="2"/>'
    + "".join(f'<rect x="{x}" y="18" width="4" height="4"/>' for x in (7, 13, 19, 25, 31)))
add("brassage", "Panneau de brassage", NET, 60, 20,
    '<rect x="1" y="3" width="58" height="14" rx="1"/>'
    + "".join(f'<rect x="{x}" y="7" width="4" height="5"/>' for x in range(6, 56, 6)))
add("baie_info", "Baie informatique", NET, 40, 40,
    '<rect x="8" y="2" width="24" height="36"/><path d="M8 9 H32 M8 15 H32 M8 21 H32 M8 27 H32" stroke-width="0.8"/>')
add("automate", "Automate programmable (API)", NET, 40, 40,
    '<rect x="4" y="8" width="32" height="24" rx="2"/>' + t(20, 23, "API", 9, "bold")
    + "".join(f'<path d="M{x} 8 V4 M{x} 32 V36"/>' for x in (10, 16, 22, 28)))
add("cpl", "Adaptateur CPL", NET, 40, 40,
    '<rect x="10" y="6" width="20" height="28" rx="3"/><path d="M15 2 V6 M25 2 V6"/>' + t(20, 24, "CPL", 6, "bold"))
add("rj45_mural", "Prise RJ45 murale", NET, 40, 40,
    '<rect x="8" y="8" width="24" height="24" rx="2"/><path d="M14 16 H26 V26 H14 Z M17 16 V13 H23 V16"/>')

# ---------------------------------------------------------------- logigramme : portes à 3 entrées
add("et3_cei", "ET à 3 entrées (norme CEI)", L, 40, 40,
    '<path d="M0 10 H10 M0 20 H10 M0 30 H10 M30 20 H40"/><rect x="10" y="2" width="20" height="36"/>' + t(20, 13, "&amp;", 8),
    pins=[(0, 10), (0, 20), (0, 30), (40, 20)])
add("ou3_cei", "OU à 3 entrées (norme CEI)", L, 40, 40,
    '<path d="M0 10 H10 M0 20 H10 M0 30 H10 M30 20 H40"/><rect x="10" y="2" width="20" height="36"/>' + t(20, 13, "≥1", 8),
    pins=[(0, 10), (0, 20), (0, 30), (40, 20)])
add("memoire_rs", "Mémoire RS (bascule)", L, 40, 40,
    '<path d="M0 10 H10 M0 30 H10 M30 10 H40"/><rect x="10" y="2" width="20" height="36"/>'
    + t(14, 13, "S", 7) + t(14, 33, "R", 7) + t(26, 13, "Q", 7), pins=[(0, 10), (0, 30), (40, 10)])

# ---------------------------------------------------------------- commandes d'éclairage (schéma développé)
add("va_et_vient", "Va-et-vient (commutateur)", E, 40, 40,
    '<path d="M0 20 H12 M26 10 H40 M26 30 H40 M12 20 L27 11.5"/>'
    '<path d="M19.5 15.8 V36" stroke-dasharray="2 2"/><path d="M19.5 36 H26"/>',
    pins=[(0, 20), (40, 10), (40, 30)], pin_names="C 1 2")
add("permutateur", "Permutateur (inverseur)", E, 40, 40,
    '<path d="M0 10 H12 M0 30 H12 M28 10 H40 M28 30 H40 M12 10 L27 6 M12 30 L27 26"/>'
    '<path d="M12 10 L28 30 M12 30 L28 10" stroke-dasharray="2 2" stroke-width="0.8"/>',
    pins=[(0, 10), (0, 30), (40, 10), (40, 30)], pin_names="1 2 3 4")
add("double_allumage", "Interrupteur double allumage (schéma)", E, 40, 40,
    '<path d="M0 20 H8 V10 H14 M8 20 V30 H14 M26 10 H40 M26 30 H40 M26 10 L12 17 M26 30 L12 37"/>',
    pins=[(0, 20), (40, 10), (40, 30)], pin_names="L 1 2")
PULSE = '<path d="M17 13 H19 V7 H21 V13 H23" stroke-width="0.9"/>'
add("bobine_tl", "Bobine de télérupteur (A1 / A2)", E, 40, 20,
    '<path d="M0 10 H13 M27 10 H40"/><rect x="13" y="1" width="14" height="18"/>' + PULSE,
    pins=[(0, 10), (40, 10)], pin_names="A1 A2")
add("contact_tl", "Contact de puissance de télérupteur (1-2)", E, 40, 20,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>',
    pins=[(0, 10), (40, 10)], pin_names="1 2")
add("contact_tl2", "Contacts de télérupteur bipolaire (1-2 / 3-4)", E, 40, 40,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17 M0 30 H14 M26 30 H40 M26 30 L12 37"/>'
    '<path d="M19 13.5 V33.5" stroke-dasharray="2 2"/>',
    pins=[(0, 10), (40, 10), (0, 30), (40, 30)], pin_names="1 2 3 4")
CLOCK = '<circle cx="20" cy="10" r="5" stroke-width="0.9"/><path d="M20 6.5 V10 H22.5" stroke-width="0.8"/>'
add("bobine_mn", "Bobine de minuterie (A1 / A2)", E, 40, 20,
    '<path d="M0 10 H13 M27 10 H40"/><rect x="13" y="1" width="14" height="18"/>' + CLOCK,
    pins=[(0, 10), (40, 10)], pin_names="A1 A2")
add("contact_mn", "Contact de puissance de minuterie (temporisé, 1-2)", E, 40, 40,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>'
    '<path d="M17 15 V27 M21 14 V27"/><path d="M13 27 A6 6 0 0 0 25 27"/>',
    pins=[(0, 10), (40, 10)], pin_names="1 2")
add("contact_tempo_repos", "Contact temporisé au repos (NO)", E, 40, 40,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>'
    '<path d="M17 15 V27 M21 14 V27"/><path d="M13 31 A6 6 0 0 1 25 31"/>',
    pins=[(0, 10), (40, 10)], pin_names="1 2")

# ---------------------------------------------------------------- contacteur complet (comme sur les fiches)
KMX = (30, 50, 70)
add("km_complet", "Contacteur complet (bobine + 3 pôles + 13-14)", TRI, 100, 60,
    '<path d="M10 0 V22 M10 38 V60"/><rect x="2" y="22" width="16" height="16"/>'
    + "".join(f'<path d="M{x} 0 V22 M{x} 38 V60 M{x} 38 L{x - 8} 21"/>'
              f'<path d="M{x} 22 V24 M{x} 19 A2.5 2.5 0 0 0 {x} 24" />' for x in KMX)
    + '<path d="M90 0 V22 M90 38 V60 M90 38 L82 21"/>'
    + '<path d="M18 30 H87" stroke-dasharray="3 2"/>',
    pins=[(10, 0), (10, 60), (30, 0), (50, 0), (70, 0), (90, 0), (30, 60), (50, 60), (70, 60), (90, 60)],
    pin_names="A1 A2 1 3 5 13 2 4 6 14")


# ---------------------------------------------------------------- distribution / tableau (multifilaire, vertical)
D = "Électricité – tableau / protection"
import math as _m


def _pole(x, mark="", fuse=False, prot="", top=0, bot=60):
    """Un pôle vertical : borne fixe en haut (y=12), lame de (x,30) vers (x-9,11), puis protection."""
    wire_end = {"semi": 14.5, "circle": 8.2}.get(mark, 12)
    o = f'<path d="M{x} {top} V{wire_end}"/>'
    if mark in ("bar", "cross", "bar_circle"):
        o += f'<path d="M{x - 3} 12 H{x + 3}"/>'
    if mark == "cross":
        o += f'<path d="M{x - 2.2} 5.8 L{x + 2.2} 10.2 M{x + 2.2} 5.8 L{x - 2.2} 10.2"/>'
    if mark in ("circle", "bar_circle"):
        o += f'<circle cx="{x}" cy="{8.5 if mark == "bar_circle" else 10}" r="1.8"/>'
    if mark == "semi":
        o += f'<path d="M{x} 9.5 A2.5 2.5 0 0 0 {x} 14.5"/>'      # demi-rond à gauche
    if mark == "flag":
        o += f'<path d="M{x - 9} 11 L{x - 4} 9 L{x - 3} 13 L{x - 8} 15 Z" fill="CC"/>'
    o += f'<path d="M{x} 30 L{x - 9} 11"/>'
    if fuse:
        ang = _m.degrees(_m.atan2(-19, -9))
        cx, cy = x - 4.5, 20.5
        o += (f'<rect x="{cx - 2.6}" y="{cy - 6.5}" width="5.2" height="13" '
              f'transform="rotate({ang + 90:.2f} {cx} {cy})"/>')
    if prot == "mt":        # thermique ⊐ + magnétique ⊃
        o += f'<path d="M{x} 30 V33 H{x + 5} V39 H{x} V42 A4 4 0 0 1 {x} 50 V{bot}"/>'
    elif prot == "t":
        o += f'<path d="M{x} 30 V36 H{x + 5} V43 H{x} V{bot}"/>'
    else:
        o += f'<path d="M{x} 30 V{bot}"/>'
    return o


def appareil(poles, link=True, torus=False, handle=False, extra=None, h=60):
    """poles : liste de (nom_haut, nom_bas, mark, fuse, prot)."""
    n = len(poles)
    xs = [20 + 20 * i for i in range(n)]
    body = "".join(_pole(x, m, f, pr, bot=h) for x, (_, _, m, f, pr) in zip(xs, poles))
    pins, names_t, names_b = [], [], []
    last = xs[-1]
    if extra:          # contacts de pré-coupure à droite
        xe = [last + 30 + 20 * i for i in range(len(extra))]
        for x, (nt, nb) in zip(xe, extra):
            body += f'<path d="M{x} 0 V12 M{x} 30 V{h} M{x} 30 L{x - 9} 11"/>'
        last = xe[-1]
        xs_all = xs + xe
        all_names = [(p[0], p[1]) for p in poles] + list(extra)
    else:
        xs_all = xs
        all_names = [(p[0], p[1]) for p in poles]
    if link and len(xs_all) > 1:
        body += f'<path d="M{xs[0] - 4.5} 20.5 H{last - 4.5}" stroke-dasharray="2.5 2"/>'
    if handle:
        body += (f'<path d="M{xs[0] - 4.5} 20.5 H4 M4 14 V27" stroke-dasharray="0"/>'
                 f'<circle cx="4" cy="30" r="1.3" fill="CC"/>')
    if torus:
        cx = (xs[0] + xs[-1]) / 2
        rx = (xs[-1] - xs[0]) / 2 + 8
        body += (f'<path d="M{xs[0] - 8} 52 H{cx + rx - 4} A4 4 0 0 1 {cx + rx - 4} 60 H{xs[0] - 8} A4 4 0 0 1 {xs[0] - 8} 52 Z"/>'
                 f'<path d="M{xs[0] - 12} 56 H6 V20.5 H{xs[0] - 4.5}" stroke-dasharray="2.5 2"/>')
        h = max(h, 64)
    w = 20 * ((last + 20 + 19) // 20)
    pins = [(x, 0) for x in xs_all] + [(x, h if not torus else 64) for x in xs_all]
    nm = " ".join([t for t, _ in all_names] + [b for _, b in all_names])
    return w, h, body, pins, nm


def _add_app(sid, name, cat=D, **kw):
    w, h, body, pins, nm = appareil(**kw)
    if kw.get("torus"):
        body = body.replace(f'V{60}"/>', 'V64"/>')
    add(sid, name, cat, w, h, body, pins=pins, pin_names=nm)


N_ = ("N", "N", "", False, "")
Nb = ("N", "N", "bar", False, "")
PH = lambda a, b: (a, b, "cross", False, "mt")
# disjoncteurs divisionnaires (neutre à gauche)
_add_app("pia_1", "Disjoncteur divisionnaire unipolaire", poles=[PH("1", "2")], link=False)
_add_app("pia_fn", "Disjoncteur divisionnaire phase + neutre", poles=[("N", "N", "cross", False, ""), PH("1", "2")])
_add_app("pia_2", "Disjoncteur divisionnaire bipolaire", poles=[PH("1", "2"), PH("3", "4")])
_add_app("pia_3", "Disjoncteur divisionnaire tripolaire", poles=[PH("1", "2"), PH("3", "4"), PH("5", "6")])
_add_app("pia_4", "Disjoncteur divisionnaire tétrapolaire (3P + N)",
         poles=[("N", "N", "cross", False, ""), PH("1", "2"), PH("3", "4"), PH("5", "6")])
# différentiels
IDP = lambda a, b: (a, b, "", False, "")
_add_app("id_2", "Interrupteur différentiel bipolaire", poles=[IDP("N", "N"), IDP("1", "2")], torus=True)
_add_app("id_4", "Interrupteur différentiel tétrapolaire", poles=[IDP("N", "N"), IDP("1", "2"), IDP("3", "4"), IDP("5", "6")], torus=True)
_add_app("dd_2", "Disjoncteur différentiel phase + neutre", poles=[("N", "N", "cross", False, ""), PH("1", "2")], torus=True)
_add_app("dd_4", "Disjoncteur différentiel tétrapolaire",
         poles=[("N", "N", "cross", False, ""), PH("1", "2"), PH("3", "4"), PH("5", "6")], torus=True)
# coupe-circuit / sectionneurs porte-fusibles (fusible sur la lame)
FU = lambda a, b: (a, b, "bar", True, "")
_add_app("ccpf_1", "Coupe-circuit / sectionneur porte-fusibles unipolaire", poles=[FU("1", "2")], link=False)
_add_app("ccpf_pn", "Sectionneur porte-fusibles bipolaire P + N", poles=[Nb, FU("1", "2")])
_add_app("ccpf_2", "Sectionneur porte-fusibles bipolaire 2P", poles=[FU("1", "2"), FU("3", "4")])
_add_app("ccpf_3", "Sectionneur porte-fusibles tripolaire", poles=[FU("1", "2"), FU("3", "4"), FU("5", "6")])
_add_app("ccpf_4pc", "Sectionneur porte-fusibles tétrapolaire + 2 contacts de pré-coupure",
         poles=[FU("1", "2"), FU("3", "4"), FU("5", "6"), ("7", "8", "bar", False, "")],
         extra=[("13", "14"), ("23", "24")], handle=True)
_add_app("inter_sect_2", "Interrupteur-sectionneur bipolaire", poles=[("N", "N", "bar_circle", False, ""),
                                                                    ("1", "2", "bar_circle", False, "")])
# symboles de base (un pôle, comme sur les fiches)
for sid, nm, mk, fu in (("b_inter", "Interrupteur (pouvoir de coupure)", "circle", False),
                        ("b_sect", "Sectionneur", "bar", False),
                        ("b_contacteur", "Contacteur (pôle)", "semi", False),
                        ("b_disj", "Disjoncteur (pôle)", "cross", False),
                        ("b_disj2", "Disjoncteur (variante à drapeau)", "flag", False),
                        ("b_inter_sect", "Interrupteur-sectionneur", "bar_circle", False),
                        ("b_inter_fus", "Interrupteur-fusible", "circle", True),
                        ("b_sect_fus", "Sectionneur-fusible", "bar", True)):
    add(sid, nm, D, 40, 60, _pole(20, mk, fu), pins=[(20, 0), (20, 60)])
add("b_rupteur", "Rupteur", D, 40, 60, _pole(20, "") + '<path d="M17 12 H23 M17 12 V9 M23 12 L19 7"/>',
    pins=[(20, 0), (20, 60)])
add("b_disj_diff", "Disjoncteur différentiel (unifilaire)", D, 40, 64,
    _pole(20, "cross", prot="mt", bot=64)
    + '<path d="M12 52 H28 A4 4 0 0 1 28 60 H12 A4 4 0 0 1 12 52 Z"/><path d="M8 56 H5 V20.5 H15.5" stroke-dasharray="2.5 2"/>',
    pins=[(20, 0), (20, 64)])
add("fusible_uni", "Fusible", D, 40, 60, '<path d="M20 0 V60"/><rect x="16" y="20" width="8" height="20"/>',
    pins=[(20, 0), (20, 60)])
add("fusible_perc", "Fusible à percuteur", D, 40, 60,
    '<path d="M20 0 V60"/><rect x="16" y="20" width="8" height="20"/><path d="M24 30 H38" stroke-dasharray="2.5 2"/>',
    pins=[(20, 0), (20, 60)])
add("parafoudre", "Parafoudre", D, 40, 60,
    '<path d="M20 0 V18 M20 42 V60"/><rect x="14" y="18" width="12" height="24"/><path d="M20 22 L17 30 H23 L20 38"/>',
    pins=[(20, 0), (20, 60)])
add("disj_uni", "Disjoncteur divisionnaire (unifilaire, n pôles)", D, 40, 60,
    _pole(20, "cross", prot="mt") + '<path d="M14 56 L26 52"/>', pins=[(20, 0), (20, 60)])

# le sectionneur porte-fusibles tripolaire de la catégorie puissance prend le même dessin (fusible sur la lame)
SYMBOLS[:] = [x for x in SYMBOLS if x.id != "sect_fus"]
_add_app("sect_fus", "Sectionneur porte-fusibles tripolaire", cat=TRI,
         poles=[FU("1", "2"), FU("3", "4"), FU("5", "6")], handle=True)

# ---------------------------------------------------------------- contacteur tripolaire (dessin des fiches)
SYMBOLS[:] = [x for x in SYMBOLS if x.id != "km_puissance"]
add("km_puissance", "Contacteur tripolaire (contacts de puissance)", TRI, 60, 60,
    poles(lambda x: f'<path d="M{x} 0 V22 M{x} 16 A3 3 0 0 0 {x} 22 M{x} 40 V60 M{x} 40 L{x - 10} 15"/>')
    + '<path d="M5 27.5 H45" stroke-dasharray="3 2"/>',
    pins=[(10, 0), (30, 0), (50, 0), (10, 60), (30, 60), (50, 60)], pin_names="1 3 5 2 4 6")

add("km_uni", "Contacteur unipolaire (pôle de puissance)", TRI, 40, 60,
    '<path d="M20 0 V22 M20 16 A3 3 0 0 0 20 22 M20 40 V60 M20 40 L10 15"/>',
    pins=[(20, 0), (20, 60)], pin_names="1 2")
add("inter_uni", "Interrupteur unipolaire", TRI, 40, 60,
    '<path d="M20 0 V16.5"/><circle cx="20" cy="19" r="2.5"/><path d="M20 40 V60 M20 40 L10 15"/>',
    pins=[(20, 0), (20, 60)])

# ---------------------------------------------------------------- borniers (repère et numéros toujours horizontaux)
def _bornier(n=10, terre=True):
    """Bornier vertical : tête avec le repère (X1), n bornes numérotées, borne de terre en bas.
    Raccordement à gauche et à droite de chaque borne."""
    top = 40
    cells = n + (1 if terre else 0)
    h = top + 20 * cells
    o = '<rect x="2" y="2" width="56" height="28" rx="6"/><path d="M20 30 V40 M40 30 V40"/>'
    o += f'<rect x="10" y="{top}" width="40" height="{20 * cells}" rx="3"/>'
    o += "".join(f'<path d="M10 {top + 20 * k} H50"/>' for k in range(1, cells))
    pins = []
    for k in range(cells):
        y = top + 10 + 20 * k
        pins += [(10, y), (50, y)]
    if terre:
        y = top + 10 + 20 * n
        o += (f'<path d="M30 {y - 6} V{y} M20 {y} H40 M23 {y + 3} H37 M26.5 {y + 6} H33.5"/>')
    sym = add(f"bornier_{n}", f"Bornier X ({n} bornes" + (" + terre)" if terre else ")"), TRI, 60, h, o,
              pins=pins)
    sym.texts = [(30, top + 10 + 20 * k, str(k + 1), 8, False) for k in range(n)]
    sym.label_at = (30, 16)
    return sym


_bornier(10, True)
add("borne_seule", "Borne seule (X1.1)", TRI, 20, 20,
    '<path d="M10 0 V6 M10 14 V20"/><circle cx="10" cy="10" r="4"/><path d="M6.5 13.5 L13.5 6.5"/>',
    pins=[(10, 0), (10, 20)])

# ---------------------------------------------------------------- plaque à bornes moteur + barrettes (couplages)
PLATE = ('<rect x="2" y="2" width="76" height="56" rx="4" fill="#dce6ef"/>'
         '<circle cx="9" cy="9" r="3.2" fill="#3fa34d"/><path d="M6 9 H12" stroke="#f2d21b" stroke-width="1.6"/>'
         + t(18, 11, "PE", 5, "bold"))


def _plate(extra=""):
    o = PLATE
    for (x, y, nm) in ((20, 20, "U1"), (40, 20, "V1"), (60, 20, "W1"), (20, 40, "W2"), (40, 40, "U2"), (60, 40, "V2")):
        o += (f'<circle cx="{x}" cy="{y}" r="5" fill="#ffffff"/>'
              f'<path d="M{x - 2.2} {y - 1.2} L{x} {y - 2.5} L{x + 2.2} {y - 1.2} V{y + 1.2} L{x} {y + 2.5} L{x - 2.2} {y + 1.2} Z" stroke-width="0.6" fill="#b0bec5"/>'
              + t(x, y + 10.5, nm, 4.5, "bold"))
    return o + extra


BAR = 'fill="#c8803a" stroke-width="0.8"'
PLATE_PINS = [(20, 20), (40, 20), (60, 20), (20, 40), (40, 40), (60, 40), (9, 9)]
add("plaque_bornes", "Plaque à bornes moteur (à câbler)", TRI, 80, 60, _plate(), pins=PLATE_PINS,
    pin_names="")
add("plaque_etoile", "Plaque à bornes – couplage étoile (corrigé)", TRI, 80, 60,
    _plate(f'<rect x="17" y="37.5" width="46" height="5" rx="2.5" {BAR}/>'), pins=PLATE_PINS)
add("plaque_triangle", "Plaque à bornes – couplage triangle (corrigé)", TRI, 80, 60,
    _plate("".join(f'<rect x="{x - 2.5}" y="17" width="5" height="26" rx="2.5" {BAR}/>' for x in (20, 40, 60))),
    pins=PLATE_PINS)
add("barrette", "Barrette de couplage", TRI, 40, 20,
    f'<rect x="6" y="7.5" width="28" height="5" rx="2.5" {BAR}/><circle cx="10" cy="10" r="1.3" fill="#ffffff"/>'
    '<circle cx="30" cy="10" r="1.3" fill="#ffffff"/>', pins=[(10, 10), (30, 10)])
add("barrette_etoile", "Barrette d'étoile (3 bornes)", TRI, 60, 20,
    f'<rect x="6" y="7.5" width="48" height="5" rx="2.5" {BAR}/>'
    + "".join(f'<circle cx="{x}" cy="10" r="1.3" fill="#ffffff"/>' for x in (10, 30, 50)),
    pins=[(10, 10), (30, 10), (50, 10)])

# ---------------------------------------------------------------- domestique (schéma développé)
DOM = "Électricité – domestique (schéma développé)"
for _x in SYMBOLS:
    if _x.id in ("va_et_vient", "permutateur", "double_allumage", "bobine_tl", "contact_tl", "contact_tl2",
                 "bobine_mn", "contact_mn", "contact_tempo_repos"):
        _x.cat = DOM
add("vv_dom", "Va-et-vient (L, L1, L2)", DOM, 40, 40,
    '<path d="M0 20 H10.5 M13 19 L28 9.5 M26 10 H40 M26 30 H40"/><circle cx="12" cy="20" r="1.8"/>'
    '<path d="M13.5 21 L27 29.5" stroke-dasharray="2 1.6"/>',
    pins=[(0, 20), (40, 10), (40, 30)], pin_names="L L1 L2")
add("inter_dom", "Interrupteur simple allumage (schéma)", DOM, 40, 20,
    '<path d="M0 10 H11.2"/><circle cx="13" cy="10" r="1.8"/><path d="M26 10 H40 M26 10 L11 17.5"/>',
    pins=[(0, 10), (40, 10)], pin_names="L 1")
add("bp_dom", "Bouton poussoir (schéma)", DOM, 40, 40,
    '<path d="M0 10 H14 M26 10 H40 M26 10 L12 17"/>'
    '<path d="M19 14 V32" stroke-dasharray="2 2"/><path d="M13 28 V32 H25 V28"/>',
    pins=[(0, 10), (40, 10)], pin_names="3 4")
add("lampe_dom", "Lampe (schéma)", DOM, 40, 20,
    '<path d="M0 10 H12 M28 10 H40"/><circle cx="20" cy="10" r="8"/>'
    '<path d="M14.3 4.3 L25.7 15.7 M25.7 4.3 L14.3 15.7"/>', pins=[(0, 10), (40, 10)], pin_names="X1 X2")
add("prise_dom", "Prise de courant (schéma)", DOM, 40, 40,
    '<path d="M10 0 V14 M30 0 V14 M20 0 V8 M4 14 H36 V30 H4 Z"/><path d="M15 22 H17 M23 22 H25"/>'
    + t(20, 38, "2P+T", 5), pins=[(10, 0), (30, 0), (20, 0)], pin_names="L N PE")

# ---------------------------------------------------------------- sciences physiques : appareils de mesure et sources
SP = "Sciences – appareils de mesure"
MODES = ["V=", "V~", "A=", "A~", "Ω", "))"]  # « = » est dessiné en symbole continu ⎓


def multimetre(p):
    mode = p.get("mode", "V=")
    disp = p.get("affichage", "12.00")
    o = ('<rect x="2" y="2" width="56" height="96" rx="6" fill="#ffca28"/>'
         '<rect x="8" y="8" width="44" height="18" rx="2" fill="#cfe3c8"/>'
         f'<text x="49" y="22" font-size="11" font-family="DejaVu Sans Mono, monospace" text-anchor="end" fill="#1b1b1b" stroke="none">{disp}</text>'
         '<circle cx="30" cy="56" r="13" fill="#37474f"/><circle cx="30" cy="56" r="5" fill="#90a4ae"/>')
    angs = [-75, -45, -15, 15, 45, 75]
    for m, a in zip(MODES, angs):
        r = _m.radians(a)
        lx, ly = 30 + 20 * _m.sin(r), 56 - 20 * _m.cos(r) + 2
        w = "bold" if m == mode else "normal"
        col = "#c62828" if m == mode else "#1b1b1b"
        letter = m[0] if m[-1] in "=~" else m
        o += f'<text x="{lx - (2 if m[-1] in "=~" else 0):.1f}" y="{ly:.1f}" font-size="{5.5 if m == mode else 5}" font-weight="{w}" fill="{col}" stroke="none" font-family="Helvetica" text-anchor="middle">{letter}</text>'
        gx, gy = lx + 1.2, ly - 2.2
        if m.endswith("="):   # continu : trait plein au-dessus d'un trait pointillé
            o += (f'<path d="M{gx:.1f} {gy - 1:.1f} h4" stroke="{col}" stroke-width="0.7"/>'
                  f'<path d="M{gx:.1f} {gy + 0.8:.1f} h4" stroke="{col}" stroke-width="0.7" stroke-dasharray="1 0.6"/>')
        elif m.endswith("~"):
            o += f'<path d="M{gx:.1f} {gy:.1f} q1 -1.6 2 0 t2 0" stroke="{col}" stroke-width="0.7"/>'
    a = _m.radians(angs[MODES.index(mode)] if mode in MODES else 0)
    o += f'<path d="M30 56 L{30 + 12 * _m.sin(a):.1f} {56 - 12 * _m.cos(a):.1f}" stroke="#ffffff" stroke-width="2.2"/>'
    for x, nm, col in ((9, "10A", "#c62828"), (23, "A", "#c62828"), (37, "COM", "#1b1b1b"), (51, "VΩ", "#c62828")):
        o += (f'<circle cx="{x}" cy="88" r="3.5" fill="{col}"/>'
              f'<text x="{x}" y="81" font-size="4" fill="#1b1b1b" stroke="none" font-family="Helvetica" text-anchor="middle">{nm}</text>')
    return 60, 100, o


add("multimetre", "Multimètre (grandeur réglable)", SP,
    params=[("mode", "Grandeur mesurée", "V=", MODES), ("affichage", "Valeur affichée", "12.00", None)],
    func=multimetre, pins=[(9, 88), (23, 88), (37, 88), (51, 88)], pin_names="")


OSC_SIGNALS = ["sinusoïdale (alternative)", "continue", "triangle", "créneau (0 / +U)", "carrée (alternative ±U)",
               "dent de scie", "redressée simple alternance", "redressée double alternance", "continue négative",
               "aucun"]


def _wave(kind, x0, x1, yc, amp, periods=2):
    kind = {"sinus": "sinusoïdale (alternative)", "carré": "carrée (alternative ±U)", "continu": "continue",
            "créneau": "créneau (0 / +U)"}.get(kind, kind)
    pts = []
    n = 120
    for i in range(n + 1):
        u = i / n
        ph = u * periods
        f = ph % 1
        if kind.startswith("sinus"):
            y = _m.sin(ph * 2 * _m.pi)
        elif kind.startswith("carrée"):
            y = 1 if f < 0.5 else -1
        elif kind.startswith("créneau"):
            y = 1 if f < 0.5 else 0
        elif kind == "triangle":
            y = 4 * f - 1 if f < 0.5 else 3 - 4 * f
        elif kind == "dent de scie":
            y = 2 * f - 1
        elif kind == "redressée simple alternance":
            y = max(0.0, _m.sin(ph * 2 * _m.pi))
        elif kind == "redressée double alternance":
            y = abs(_m.sin(ph * 2 * _m.pi))
        elif kind == "continue":
            y = 0.6
        elif kind == "continue négative":
            y = -0.6
        else:
            return ""
        pts.append((x0 + (x1 - x0) * u, yc - amp * y))
    if kind.startswith("carrée") or kind.startswith("créneau"):
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        prev = pts[0][1]
        for x, y in pts[1:]:
            if y != prev:
                d += f" H{x:.1f} V{y:.1f}"
                prev = y
        d += f" H{x1:.1f}"
        return d
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def oscillo(p):
    sig = p.get("signal", "sinus")
    sig2 = p.get("voie2", "aucun")
    o = ('<rect x="2" y="2" width="116" height="76" rx="4" fill="#cfd8dc"/>'
         '<rect x="8" y="8" width="70" height="56" fill="#0f2a1d"/>')
    for i in range(1, 10):
        o += f'<path d="M{8 + i * 7} 8 V64" stroke="#2f6b4c" stroke-width="0.4"/>'
    for i in range(1, 8):
        o += f'<path d="M8 {8 + i * 7} H78" stroke="#2f6b4c" stroke-width="0.4"/>'
    o += '<path d="M8 36 H78" stroke="#4f8f6c" stroke-width="0.6"/><path d="M8 33 L11 36 L8 39 Z" fill="#ffeb3b" stroke="none"/>'
    if sig != "aucun":
        o += f'<path d="{_wave(sig, 8, 78, 36, 16)}" stroke="#ffeb3b" stroke-width="1.2"/>'
    if sig2 != "aucun":
        o += f'<path d="{_wave(sig2, 8, 78, 36, 9, 3)}" stroke="#4fc3f7" stroke-width="1.2"/>'
    for (x, y) in ((88, 14), (104, 14), (88, 32), (104, 32)):
        o += f'<circle cx="{x}" cy="{y}" r="5" fill="#455a64"/>'
    o += ('<circle cx="90" cy="64" r="4" fill="#ffeb3b"/><circle cx="106" cy="64" r="4" fill="#4fc3f7"/>'
          + t(90, 56, "CH1", 4.5) + t(106, 56, "CH2", 4.5) + t(43, 73, "Oscilloscope", 5))
    return 120, 80, o


add("oscilloscope", "Oscilloscope", SP,
    params=[("signal", "Voie 1", "sinusoïdale (alternative)", OSC_SIGNALS),
            ("voie2", "Voie 2", "aucun", ["aucun"] + OSC_SIGNALS[:-1])],
    func=oscillo, pins=[(90, 64), (106, 64)], pin_names="")


def gbf(p):
    forme = p.get("forme", "sinus")
    f = p.get("frequence", "1.000 kHz")
    o = ('<rect x="2" y="2" width="96" height="56" rx="4" fill="#b3e5fc"/>'
         '<rect x="8" y="8" width="50" height="14" rx="2" fill="#263238"/>'
         f'<text x="55" y="19" font-size="8" fill="#80ff80" stroke="none" font-family="DejaVu Sans Mono, monospace" text-anchor="end">{f}</text>')
    for i, k in enumerate(("sinus", "carré", "triangle")):
        x = 8 + i * 17
        fill = "#ff7043" if k == forme else "#ffffff"
        o += f'<rect x="{x}" y="28" width="14" height="10" rx="1.5" fill="{fill}"/>'
        o += f'<path d="{_wave(k, x + 2, x + 12, 33, 3, 1)}" stroke-width="0.8"/>'
    o += ('<circle cx="74" cy="20" r="9" fill="#455a64"/><circle cx="74" cy="20" r="3" fill="#90a4ae"/>'
          '<circle cx="80" cy="46" r="4" fill="#212121"/><circle cx="92" cy="46" r="2.5" fill="#212121"/>'
          + t(80, 56, "OUT", 4) + t(30, 52, "GBF", 7, "bold"))
    return 100, 60, o


add("gbf", "Générateur basse fréquence (GBF)", SP,
    params=[("forme", "Forme du signal", "sinus", ["sinus", "carré", "triangle"]),
            ("frequence", "Fréquence affichée", "1.000 kHz", None)],
    func=gbf, pins=[(80, 46), (92, 46)], pin_names="")


def alim(p):
    u, i = p.get("tension", "12.0 V"), p.get("courant", "0.50 A")
    o = ('<rect x="2" y="2" width="96" height="56" rx="4" fill="#eceff1"/>'
         '<rect x="8" y="8" width="38" height="14" rx="2" fill="#263238"/>'
         '<rect x="52" y="8" width="38" height="14" rx="2" fill="#263238"/>'
         f'<text x="43" y="19" font-size="7.5" fill="#ff8a65" stroke="none" font-family="DejaVu Sans Mono, monospace" text-anchor="end">{u}</text>'
         f'<text x="87" y="19" font-size="7.5" fill="#80ff80" stroke="none" font-family="DejaVu Sans Mono, monospace" text-anchor="end">{i}</text>'
         '<circle cx="20" cy="36" r="7" fill="#455a64"/><circle cx="44" cy="36" r="7" fill="#455a64"/>'
         + t(20, 47, "V", 5) + t(44, 47, "A", 5)
         + '<circle cx="66" cy="44" r="4" fill="#d32f2f"/><circle cx="78" cy="44" r="4" fill="#212121"/>'
           '<circle cx="90" cy="44" r="3" fill="#3fa34d"/>'
         + t(66, 37, "+", 6, "bold") + t(78, 37, "−", 6, "bold") + t(50, 55, "Alimentation 0 – 30 V", 4.5))
    return 100, 60, o


add("alim_stab", "Alimentation stabilisée 0 – 30 V", SP,
    params=[("tension", "Tension affichée", "12.0 V", None), ("courant", "Courant affiché", "0.50 A", None)],
    func=alim, pins=[(66, 44), (78, 44), (90, 44)], pin_names="")
add("pile9v", "Pile 9 V", SP, 40, 60,
    '<rect x="6" y="12" width="28" height="46" rx="3" fill="#455a64"/><rect x="6" y="12" width="28" height="12" fill="#ffb300"/>'
    '<circle cx="13" cy="7" r="3.5" fill="#cfd8dc"/><path d="M24 4 H30 L32 7 L30 10 H24 L22 7 Z" fill="#cfd8dc"/>'
    + t(20, 44, "9 V", 9, "bold").replace('fill="CC"', 'fill="#ffffff"') + t(13, 22, "+", 7, "bold") + t(27, 22, "−", 7, "bold"),
    pins=[(13, 0), (27, 0)], pin_names="")
add("pile15", "Pile 1,5 V (LR6)", SP, 60, 20,
    '<rect x="4" y="3" width="48" height="14" rx="2" fill="#26a69a"/><rect x="52" y="7" width="4" height="6" fill="#cfd8dc"/>'
    + t(28, 13, "1,5 V", 7, "bold").replace('fill="CC"', 'fill="#ffffff"') + t(47, 13, "+", 6, "bold"),
    pins=[(0, 10), (60, 10)], pin_names="")
add("pile45", "Pile 4,5 V (plate)", SP, 60, 60,
    '<rect x="6" y="18" width="48" height="38" rx="2" fill="#1e88e5"/><rect x="6" y="18" width="48" height="10" fill="#fdd835"/>'
    '<path d="M18 18 V4 H24 V10" stroke="#9e9e9e" stroke-width="2.4" fill="none"/>'
    '<path d="M38 18 V2 H44 V12" stroke="#9e9e9e" stroke-width="2.4" fill="none"/>'
    + t(30, 46, "4,5 V", 9, "bold").replace('fill="CC"', 'fill="#ffffff"') + t(21, 26, "+", 7, "bold") + t(41, 26, "−", 7, "bold"),
    pins=[(24, 10), (44, 12)], pin_names="")
add("sym_continu", "Symbole continu ⎓", SP, 40, 20,
    '<path d="M6 7 H34" stroke-width="1.6"/><path d="M6 13 H34" stroke-width="1.6" stroke-dasharray="5 3"/>')
add("sym_alternatif", "Symbole alternatif ∼", SP, 40, 20, '<path d="M6 10 Q13 1 20 10 T34 10" stroke-width="1.6"/>')
add("sym_alt_cont", "Symbole alternatif et continu", SP, 40, 20,
    '<path d="M6 6 Q13 0 20 6 T34 6" stroke-width="1.4"/><path d="M6 12 H34" stroke-width="1.4"/>'
    '<path d="M6 17 H34" stroke-width="1.4" stroke-dasharray="5 3"/>')
add("rheostat", "Rhéostat", SP, 40, 20,
    '<path d="M0 10 H10 M30 10 H40"/><rect x="10" y="6" width="20" height="8"/><path d="M20 0 V6 M17 3 L20 6 L23 3"/>',
    pins=[(0, 10), (40, 10), (20, 0)])
add("ampoule_support", "Lampe sur support", SP, 40, 40,
    '<path d="M14 26 A10 10 0 1 1 26 26 V30 H14 Z" fill="#fff59d"/><rect x="12" y="30" width="16" height="6" fill="#90a4ae"/>'
    '<path d="M17 24 L20 14 L23 24"/>', pins=[(12, 33), (28, 33)])
add("interrupteur_labo", "Interrupteur de laboratoire", SP, 40, 20,
    '<rect x="4" y="12" width="32" height="6" rx="1" fill="#90a4ae"/><path d="M10 12 L30 4" stroke-width="1.6"/>'
    '<circle cx="10" cy="12" r="1.6" fill="CC"/>', pins=[(4, 15), (36, 15)])
add("fil_labo", "Fil de connexion (banane)", SP, 60, 20,
    '<path d="M6 10 C20 0, 40 20, 54 10" stroke="#d32f2f" stroke-width="1.6"/>'
    '<rect x="0" y="8" width="7" height="4" fill="#d32f2f"/><rect x="53" y="8" width="7" height="4" fill="#d32f2f"/>',
    pins=[(0, 10), (60, 10)])

# ---------------------------------------------------------------- chimie (verrerie, niveau de liquide réglable)
CH = "Sciences – chimie (verrerie)"
LIQ = 'fill="#90caf9" stroke="none" opacity="0.8"'
NIV = ("niveau", "Niveau du liquide (%)", 40, 0, 100)


def _clip_rect(x, y0, y1, w):
    return f'<rect x="{x}" y="{y0}" width="{w}" height="{max(0, y1 - y0)}" {LIQ}/>'


def tube(p):
    n = p["niveau"] / 100
    top = 72 - 66 * n
    liq = f'<path d="M7 {top:.1f} V68 A5 5 0 0 0 17 68 V{top:.1f} Z" {LIQ}/>' if n > 0 else ""
    return 24, 80, liq + '<path d="M7 4 V68 A5 5 0 0 0 17 68 V4"/>'


def becher(p):
    n = p["niveau"] / 100
    top = 56 - 46 * n
    return 60, 60, (_clip_rect(9, top, 56, 42) if n > 0 else "") + '<path d="M4 6 Q8 6 8 10 V56 H52 V8"/>'


def _liq_poly(top, bottom, half, cx=30):
    """Polygone de liquide entre top et bottom ; half(y) = demi-largeur intérieure."""
    if bottom - top < 0.3:
        return ""
    ys = [top + (bottom - top) * i / 24 for i in range(25)]
    left = [(cx - half(y), y) for y in ys]
    right = [(cx + half(y), y) for y in reversed(ys)]
    return '<path d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in left + right) + f' Z" {LIQ}/>'


def erlen(p):
    n = p["niveau"] / 100
    top = 65 - 41 * n
    half = lambda y: 6 + (min(y, 65) - 24) * (18 / 40) if y > 24 else 5.5
    return 60, 70, (_liq_poly(top, 65, half) if n > 0 else "") + \
        '<path d="M24 4 V24 L6 64 Q5 66 8 66 H52 Q55 66 54 64 L36 24 V4"/>'


def ballon(p, plat=False):
    n = p["niveau"] / 100
    if not plat:
        cy, r, bottom = 45.4, 19.5, 64.8
        shape = 'M25 4 V26 A20 20 0 1 0 35 26 V4'
    else:
        cy, r, bottom = 45, 18.5, 63.5
        shape = 'M25 4 V28 A18 18 0 0 0 14 64 H46 A18 18 0 0 0 35 28 V4'
    top = bottom - (bottom - (cy - r + 2)) * n
    half = lambda y: max(0.0, (r * r - (y - cy) ** 2)) ** 0.5 if abs(y - cy) < r else 4.5
    return 60, 74, (_liq_poly(top, bottom, lambda y: max(half(y), 4.5)) if n > 0 else "") + f'<path d="{shape}"/>'


def eprouvette(p):
    n = p["niveau"] / 100
    top = 80 - 70 * n
    grads = "".join(f'<path d="M22 {y} H{26 if (y // 7) % 2 else 28}" stroke-width="0.5"/>' for y in range(14, 80, 7))
    return 40, 92, ((_clip_rect(13, top, 80, 14) if n > 0 else "") +
                    '<path d="M12 4 V80 M28 4 V80 M12 80 H28 M4 88 H36 M20 80 V88"/>' + grads)


def fiole(p):
    n = p["niveau"] / 100
    top = 76 - 34 * n
    half = lambda y: 3 + (y - 40) * (9 / 34) if y > 40 else 2.6
    return 48, 80, (_liq_poly(top, 76, half, cx=24) if n > 0 else "") + \
        '<path d="M21 4 V40 L12 74 Q11 77 14 77 H34 Q37 77 36 74 L27 40 V4 M19 22 H29" />'


add("tube_essai", "Tube à essais", CH, params=[NIV], func=tube)
add("becher", "Bécher", CH, params=[NIV], func=becher)
add("erlenmeyer", "Erlenmeyer", CH, params=[NIV], func=erlen)
add("ballon_rond", "Ballon à fond rond", CH, params=[NIV], func=ballon)
add("ballon_plat", "Ballon à fond plat", CH, params=[NIV], func=lambda p: ballon(p, True))
add("eprouvette", "Éprouvette graduée", CH, params=[NIV], func=eprouvette)
add("fiole_jaugee", "Fiole jaugée", CH, params=[NIV], func=fiole)
add("verre_pied", "Verre à pied", CH, 60, 70, '<path d="M6 6 L27 50 M54 6 L33 50 M27 50 H33 M30 50 V64 M18 64 H42"/>')
add("entonnoir", "Entonnoir", CH, 60, 70, '<path d="M4 6 L26 40 V66 M56 6 L34 40 V66"/>')
add("flacon", "Flacon", CH, 50, 70, '<path d="M18 4 V14 Q6 16 6 28 V64 H44 V28 Q44 16 32 14 V4 Z"/>')
add("ampoule_decanter", "Ampoule à décanter", CH, 50, 90,
    '<path d="M22 4 V12 A14 14 0 0 0 22 40 L24 60 V86 M28 4 V12 A14 14 0 0 1 28 40 L26 60 V86"/>'
    '<path d="M18 60 H32" stroke-width="2"/><circle cx="25" cy="60" r="2.5"/>')
add("pissette", "Pissette", CH, 50, 80,
    '<rect x="10" y="28" width="30" height="48" rx="6"/><rect x="16" y="20" width="18" height="8"/>'
    '<path d="M25 20 V10 L40 4"/><path d="M14 40 H36" stroke-width="0.6"/>')
add("agitateur_magn", "Agitateur magnétique chauffant (touilleur)", CH, 80, 40,
    '<rect x="4" y="16" width="72" height="20" rx="3" fill="#eceff1"/><rect x="10" y="10" width="60" height="6" rx="1" fill="#b0bec5"/>'
    '<circle cx="62" cy="26" r="4" fill="#455a64"/><circle cx="48" cy="26" r="4" fill="#455a64"/>'
    '<rect x="12" y="23" width="20" height="6" rx="1" fill="#263238"/>')
add("barreau_aimante", "Barreau aimanté", CH, 40, 20, '<rect x="8" y="7" width="24" height="6" rx="3" fill="#ffffff"/>')
add("baguette", "Agitateur en verre (baguette)", CH, 20, 80, '<rect x="8" y="4" width="4" height="72" rx="2"/>')
add("thermometre", "Thermomètre", CH, 20, 90,
    '<path d="M7 6 A3 3 0 0 1 13 6 V70 A6 6 0 1 1 7 70 Z"/><circle cx="10" cy="77" r="4" fill="#e53935" stroke="none"/>'
    '<rect x="9" y="40" width="2" height="34" fill="#e53935" stroke="none"/>')
add("pipette", "Pipette jaugée", CH, 20, 100,
    '<path d="M9 4 V36 Q4 40 4 48 Q4 58 9 60 V94 L10 98 L11 94 V60 Q16 58 16 48 Q16 40 11 36 V4"/><path d="M7 20 H13"/>')
add("burette", "Burette graduée", CH, 30, 100,
    '<path d="M10 4 V78 L14 84 V96 M20 4 V78 L16 84 V96"/><path d="M8 84 H22" stroke-width="2"/>'
    + "".join(f'<path d="M15 {y} H{20 if (y // 6) % 2 else 18}" stroke-width="0.5"/>' for y in range(10, 76, 6)))
add("potence", "Support (potence) avec pince", CH, 60, 100,
    '<rect x="4" y="90" width="52" height="6" fill="#90a4ae"/><path d="M12 90 V6" stroke-width="2.2"/>'
    '<path d="M12 30 H44" stroke-width="1.6"/><path d="M44 26 Q50 30 44 34" />')
def _bunsen(p):
    """Bec Bunsen : flamme bleue (virole ouverte), jaune (virole fermée) ou éteint."""
    fl = p.get("flamme", "bleue (virole ouverte)")
    flame = ""
    if fl.startswith("bleue"):
        flame = ('<path d="M20 34 C10 26 12 12 20 1 C28 12 30 26 20 34 Z" fill="#9fd0ff" fill-opacity="0.85" stroke="#5aa9f0" stroke-width="0.6"/>'
                 '<path d="M20 34 C15.5 29 16.5 21 20 14 C23.5 21 24.5 29 20 34 Z" fill="#1e5fd6" stroke="none"/>')
    elif fl.startswith("jaune"):
        flame = ('<path d="M20 34 C8 27 11 15 17 8 C16 13 19 14 20 1 C24 10 31 16 29 25 C28 30 24 33 20 34 Z" '
                 'fill="#ffb300" stroke="#f57c00" stroke-width="0.6"/>'
                 '<path d="M20 34 C14 30 15 22 19 15 C20 21 23 22 22 17 C26 23 26 30 20 34 Z" fill="#ffe082" stroke="none"/>')
    return (40, 90,
            flame +
            '<rect x="16.5" y="34" width="7" height="44" fill="#cfd8dc"/>'                      # cheminée
            '<rect x="15" y="58" width="10" height="8" rx="1" fill="#90a4ae"/>'                  # virole (bague d'air)
            '<circle cx="20" cy="62" r="1.8" fill="#37474f" stroke="none"/>'
            '<path d="M6 86 H34 L30 78 H10 Z" fill="#78909c"/>'                                 # socle
            '<path d="M30 82 H39" stroke-width="2.4"/>')                                       # arrivée de gaz


add("bec_bunsen", "Bec Bunsen (avec flamme)", CH,
    params=[("flamme", "Flamme", "bleue (virole ouverte)", ["bleue (virole ouverte)", "jaune (virole fermée)", "éteint"])],
    func=_bunsen)
add("trepied", "Trépied avec toile métallique", CH, 70, 50,
    '<path d="M6 8 H64" stroke-width="2.6"/>'
    '<path d="M8 6 H62" stroke-width="0.6" stroke-dasharray="1.5 1.2"/>'
    '<path d="M14 9 L6 48 M35 9 V48 M56 9 L64 48" stroke-width="1.8"/>')
add("cristallisoir", "Cristallisoir", CH, 80, 30, '<path d="M4 4 V26 H76 V4"/>')
add("verre_montre", "Verre de montre", CH, 60, 20, '<path d="M4 6 Q30 22 56 6"/>')
add("spatule", "Spatule", CH, 80, 20, '<path d="M4 10 H54"/><path d="M54 6 H74 Q78 10 74 14 H54 Z"/>')
add("balance", "Balance électronique", CH,
    params=[("affichage", "Masse affichée", "125.0 g", None)],
    func=lambda p: (80, 40, '<rect x="4" y="14" width="72" height="22" rx="3" fill="#eceff1"/>'
                            '<rect x="14" y="8" width="52" height="6" rx="1" fill="#b0bec5"/>'
                            '<rect x="10" y="20" width="34" height="11" rx="1.5" fill="#263238"/>'
                            f'<text x="42" y="29" font-size="7" fill="#80ff80" stroke="none" font-family="DejaVu Sans Mono, monospace" text-anchor="end">{p["affichage"]}</text>'))
add("mortier", "Mortier et pilon", CH, 60, 50,
    '<path d="M6 20 Q30 50 54 20 Z" fill="#eceff1"/><path d="M36 22 L50 4" stroke-width="3"/>')

# ---------------------------------------------------------------- optique
OP = "Sciences – optique"
add("lentille_conv", "Lentille convergente (symbole)", OP, 20, 80,
    '<path d="M10 4 V76 M5 10 L10 4 L15 10 M5 70 L10 76 L15 70"/>', pins=[(10, 40)])
add("lentille_div", "Lentille divergente (symbole)", OP, 20, 80,
    '<path d="M10 4 V76 M5 4 L10 10 L15 4 M5 76 L10 70 L15 76"/>', pins=[(10, 40)])
add("lentille_convexe", "Lentille convexe", OP, 20, 80, '<path d="M10 4 Q22 40 10 76 Q-2 40 10 4 Z" fill="#e1f5fe"/>')
add("lentille_concave", "Lentille concave", OP, 20, 80, '<path d="M2 4 H18 Q10 40 18 76 H2 Q10 40 2 4 Z" fill="#e1f5fe"/>')
add("miroir_plan", "Miroir plan", OP, 80, 20,
    '<path d="M4 6 H76" stroke-width="2"/>' + "".join(f'<path d="M{x} 6 L{x - 5} 14" stroke-width="0.7"/>' for x in range(10, 78, 7)))
add("miroir_concave", "Miroir concave", OP, 30, 80, '<path d="M8 4 Q24 40 8 76" stroke-width="2"/>')
add("miroir_convexe", "Miroir convexe", OP, 30, 80, '<path d="M22 4 Q6 40 22 76" stroke-width="2"/>')
add("prisme", "Prisme", OP, 60, 60, '<path d="M30 6 L56 54 H4 Z" fill="#e1f5fe"/>')
add("demi_cylindre", "Demi-cylindre (verre)", OP, 60, 40, '<path d="M4 34 A26 26 0 0 1 56 34 Z" fill="#e1f5fe"/>')
add("rayon", "Rayon lumineux", OP, 80, 20, '<path d="M2 10 H78" stroke="#e53935"/><path d="M36 6 L44 10 L36 14 Z" fill="#e53935" stroke="none"/>',
    pins=[(2, 10), (78, 10)])
add("faisceau", "Faisceau de lumière", OP, 80, 40,
    "".join(f'<path d="M2 {y} H78" stroke="#e53935"/><path d="M36 {y - 3} L44 {y} L36 {y + 3} Z" fill="#e53935" stroke="none"/>' for y in (8, 20, 32)))
add("axe_optique", "Axe optique", OP, 120, 20, '<path d="M2 10 H118" stroke-dasharray="10 3 2 3" stroke-width="0.8"/>')
add("objet_ab", "Objet AB (flèche)", OP, 20, 60, '<path d="M10 56 V6 M5 14 L10 6 L15 14"/>' + t(16, 58, "A", 7) + t(16, 8, "B", 7),
    pins=[(10, 56)])
add("foyer", "Foyer (F / F')", OP, 20, 20, '<path d="M10 6 V14"/>' + t(10, 4, "F", 6), pins=[(10, 10)])
add("source_lum", "Source de lumière", OP, 40, 40,
    '<circle cx="20" cy="20" r="7" fill="#ff5252" stroke="none"/>'
    + "".join(f'<path d="M{20 + 10 * _m.cos(a):.1f} {20 + 10 * _m.sin(a):.1f} L{20 + 16 * _m.cos(a):.1f} {20 + 16 * _m.sin(a):.1f}" stroke="#ff5252"/>'
              for a in [i * _m.pi / 4 for i in range(8)]))
add("laser", "Laser", OP, 60, 20, '<rect x="2" y="4" width="40" height="12" rx="2" fill="#455a64"/><path d="M42 10 H58" stroke="#e53935" stroke-width="1.6"/>',
    pins=[(58, 10)])
add("ecran", "Écran", OP, 20, 80, '<rect x="6" y="4" width="8" height="72" fill="#eceff1"/>')
add("oeil", "Œil", OP, 60, 40, '<path d="M4 20 Q30 0 56 20 Q30 40 4 20 Z"/><circle cx="30" cy="20" r="8" fill="#64b5f6"/><circle cx="30" cy="20" r="3.5" fill="#000000"/>')
add("diaphragme", "Diaphragme / fente", OP, 20, 80, '<path d="M10 4 V32 M10 48 V76" stroke-width="3"/>')

# ---------------------------------------------------------------- mécanique
ME = "Sciences – mécanique"
add("sol", "Sol / support (hachures)", ME, 80, 20,
    '<path d="M4 6 H76"/>' + "".join(f'<path d="M{x} 6 L{x - 5} 14" stroke-width="0.7"/>' for x in range(10, 78, 7)))
add("mur_support", "Mur / plafond (hachures)", ME, 20, 80,
    '<path d="M6 4 V76"/>' + "".join(f'<path d="M6 {y} L14 {y - 5}" stroke-width="0.7"/>' for y in range(10, 78, 7)))
add("masse", "Masse marquée", ME, 40, 50,
    '<path d="M20 4 V10"/><path d="M14 10 Q20 4 26 10" /><rect x="8" y="14" width="24" height="32" rx="3" fill="#90a4ae"/>' + t(20, 34, "m", 9, "bold"),
    pins=[(20, 4)])
add("ressort", "Ressort", ME, 20, 80,
    '<path d="M10 2 V10 L4 14 L16 20 L4 26 L16 32 L4 38 L16 44 L4 50 L16 56 L4 62 L10 66 V78"/>', pins=[(10, 2), (10, 78)])
add("poulie", "Poulie", ME, 40, 40, '<circle cx="20" cy="20" r="14" fill="#cfd8dc"/><circle cx="20" cy="20" r="3" fill="CC"/>', pins=[(20, 20)])
add("plan_incline", "Plan incliné", ME, 100, 50,
    '<path d="M4 46 H96 V6 Z" fill="#eceff1"/><path d="M80 46 A16 16 0 0 0 78 38"/>' + t(72, 42, "α", 7))
add("dynamometre", "Dynamomètre", ME, 20, 90,
    '<rect x="5" y="6" width="10" height="56" rx="2" fill="#fff9c4"/>'
    + "".join(f'<path d="M5 {y} H9" stroke-width="0.5"/>' for y in range(12, 60, 6))
    + '<path d="M10 2 V6 M10 62 V80 M6 84 Q10 90 14 84"/>', pins=[(10, 2), (10, 86)])
add("balance_roberval", "Balance à fléau", ME, 100, 60,
    '<path d="M50 54 V14 M10 14 H90" stroke-width="1.6"/><path d="M30 54 H70"/>'
    '<path d="M10 14 L4 30 H16 Z M90 14 L84 30 H96 Z"/><path d="M46 14 L50 6 L54 14"/>')
add("chariot", "Chariot / mobile", ME, 80, 40,
    '<rect x="6" y="6" width="68" height="20" rx="2" fill="#bbdefb"/><circle cx="20" cy="32" r="6" fill="#455a64"/>'
    '<circle cx="60" cy="32" r="6" fill="#455a64"/>')
add("pendule", "Pendule simple", ME, 60, 90,
    '<path d="M6 4 H54" stroke-width="2"/><path d="M30 4 L44 70" /><circle cx="46" cy="76" r="7" fill="#90a4ae"/>'
    '<path d="M30 4 V60" stroke-dasharray="3 2" stroke-width="0.6"/>')
add("vecteur_force", "Vecteur force F", ME, 80, 20,
    '<path d="M4 10 H70" stroke-width="1.6"/><path d="M66 5 L76 10 L66 15 Z" fill="CC"/>'
    '<path d="M36 2 H44 M42 0 L44 2 L42 4" stroke-width="0.6"/>' + t(40, 8, "F", 7, "bold"), pins=[(4, 10)])
add("repere_xy", "Repère (x, y)", ME, 60, 60,
    '<path d="M8 52 H56 M8 52 V4 M52 49 L56 52 L52 55 M5 8 L8 4 L11 8"/>' + t(54, 60, "x", 7) + t(4, 6, "y", 7) + t(5, 60, "O", 6))
add("solide", "Solide (bloc)", ME, 40, 40, '<rect x="6" y="6" width="28" height="28" fill="#ffe0b2"/>', pins=[(20, 20)])
add("aimant_droit", "Aimant droit", ME, 80, 20,
    '<rect x="4" y="4" width="36" height="12" fill="#e53935"/><rect x="40" y="4" width="36" height="12" fill="#1e88e5"/>'
    + t(22, 13, "N", 7, "bold").replace('fill="CC"', 'fill="#ffffff"') + t(58, 13, "S", 7, "bold").replace('fill="CC"', 'fill="#ffffff"'))
add("aimant_u", "Aimant en U", ME, 60, 60,
    '<path d="M8 6 V34 A22 22 0 0 0 52 34 V6 H40 V34 A10 10 0 0 1 20 34 V6 Z" fill="#b0bec5"/>'
    '<rect x="8" y="6" width="12" height="10" fill="#e53935"/><rect x="40" y="6" width="12" height="10" fill="#1e88e5"/>')
add("boussole", "Boussole", ME, 40, 40,
    '<circle cx="20" cy="20" r="16" fill="#ffffff"/><path d="M20 6 L24 20 L16 20 Z" fill="#e53935" stroke="none"/>'
    '<path d="M20 34 L24 20 L16 20 Z" fill="#1e88e5" stroke="none"/>')
add("levier", "Levier", ME, 100, 40, '<path d="M6 16 H94" stroke-width="2.2"/><path d="M50 16 L42 34 H58 Z" fill="#cfd8dc"/>')

# ---------------------------------------------------------------- réseau : vidéosurveillance / fibre (CIEL)
add("conv_fibre", "Convertisseur de média fibre", NET, 60, 40,
    '<rect x="4" y="8" width="52" height="26" rx="3" fill="#455a64"/><rect x="4" y="8" width="52" height="5" fill="#263238"/>'
    '<rect x="10" y="20" width="9" height="7" fill="#90caf9"/><rect x="24" y="20" width="9" height="7" fill="#90caf9"/>'
    '<rect x="40" y="19" width="10" height="9" fill="#cfd8dc"/><circle cx="12" cy="16" r="1" fill="#76ff03" stroke="none"/>',
    pins=[(4, 24), (56, 24)])
add("chassis_conv", "Châssis de convertisseurs (rack)", NET, 100, 40,
    '<rect x="2" y="8" width="96" height="26" rx="2" fill="#b0bec5"/>'
    + "".join(f'<rect x="{x}" y="11" width="6" height="20" fill="#eceff1" stroke-width="0.6"/>'
              f'<rect x="{x + 1}" y="22" width="4" height="4" fill="#4fa3d9" stroke="none"/>' for x in range(6, 94, 8)),
    pins=[(2, 21), (98, 21)])
add("switch_poe", "Switch PoE", NET, 60, 40,
    '<rect x="2" y="12" width="56" height="18" rx="2" fill="#78909c"/>'
    + "".join(f'<rect x="{x}" y="17" width="5" height="5" fill="#263238"/>' for x in range(6, 40, 7))
    + '<rect x="42" y="16" width="12" height="8" fill="#43a047" stroke="none"/>' + t(48, 22.5, "PoE", 4.5, "bold").replace('fill="CC"', 'fill="#ffffff"'),
    pins=[(2, 21), (58, 21)])
add("camera_bullet", "Caméra bullet sur potence", NET, 50, 50,
    '<path d="M6 46 V30 H22" stroke-width="2"/><rect x="18" y="14" width="26" height="12" rx="4" fill="#eceff1"/>'
    '<rect x="42" y="16" width="5" height="8" fill="#263238"/><path d="M18 14 L22 10 H44 L46 14" fill="#cfd8dc"/>',
    pins=[(6, 46)])
add("camera_dome", "Caméra dôme", NET, 40, 30,
    '<rect x="6" y="4" width="28" height="5" rx="1" fill="#cfd8dc"/><path d="M8 9 A12 12 0 0 0 32 9 Z" fill="#37474f"/>'
    '<circle cx="20" cy="14" r="3" fill="#90caf9" stroke="none"/>', pins=[(20, 4)])
add("nvr", "Enregistreur vidéo (NVR)", NET, 60, 40,
    '<rect x="2" y="12" width="56" height="18" rx="2" fill="#37474f"/>' + t(16, 24, "NVR", 6, "bold").replace('fill="CC"', 'fill="#ffffff"')
    + '<circle cx="46" cy="21" r="2" fill="#76ff03" stroke="none"/>', pins=[(2, 21), (58, 21)])
add("moniteur", "Moniteur / écran", NET, 40, 40,
    '<rect x="4" y="5" width="32" height="22" rx="2" fill="#263238"/><rect x="6" y="7" width="28" height="18" fill="#4fc3f7"/>'
    '<path d="M20 27 V33 M12 35 H28"/>', pins=[(20, 35)])
add("poste_supervision", "Poste de supervision (2 écrans + opérateur)", NET, 100, 70,
    '<rect x="10" y="40" width="80" height="5" fill="#8d6e63"/><path d="M16 45 V66 M84 45 V66"/>'
    '<rect x="18" y="12" width="28" height="20" rx="2" fill="#263238"/><rect x="20" y="14" width="24" height="16" fill="#4fc3f7"/>'
    '<rect x="54" y="12" width="28" height="20" rx="2" fill="#263238"/><rect x="56" y="14" width="24" height="16" fill="#4fc3f7"/>'
    '<path d="M32 32 V40 M68 32 V40"/>'
    '<circle cx="50" cy="44" r="6" fill="#ffcc80"/><path d="M40 66 Q40 52 50 51 Q60 52 60 66 Z" fill="#5c6bc0"/>'
    '<path d="M40 60 H60" stroke-width="0.6"/>', pins=[(10, 42), (90, 42)])
add("operateur", "Opérateur (personne)", NET, 30, 50,
    '<circle cx="15" cy="10" r="7" fill="#ffcc80"/><path d="M3 48 Q3 22 15 20 Q27 22 27 48 Z" fill="#5c6bc0"/>')
add("antenne", "Antenne / liaison radio", NET, 40, 50,
    '<path d="M20 48 V14 M12 48 H28 M14 6 L20 14 L26 6"/><path d="M8 8 A14 14 0 0 1 8 22 M32 8 A14 14 0 0 0 32 22" stroke-width="0.8"/>',
    pins=[(20, 48)])
add("routeur_4g", "Routeur 4G / 5G", NET, 50, 40,
    '<rect x="4" y="16" width="42" height="18" rx="3" fill="#eceff1"/><path d="M12 16 V4 M38 16 V4"/>'
    + t(25, 28, "4G", 7, "bold"), pins=[(4, 25), (46, 25)])
add("onduleur", "Onduleur", NET, 40, 50,
    '<rect x="6" y="4" width="28" height="42" rx="3" fill="#455a64"/>' + t(20, 30, "UPS", 6, "bold").replace('fill="CC"', 'fill="#ffffff"'),
    pins=[(20, 46)])
add("tiroir_optique", "Tiroir optique / boîtier de raccordement", NET, 60, 30,
    '<rect x="2" y="6" width="56" height="18" rx="2" fill="#cfd8dc"/>'
    + "".join(f'<circle cx="{x}" cy="15" r="2.5" fill="#4fa3d9"/>' for x in range(10, 54, 8)), pins=[(2, 15), (58, 15)])

# ---------------------------------------------------------------- pneumatique (ISO 1219)
PN = "Pneumatique"


def _arrow(x1, y1, x2, y2):
    a = _m.atan2(y2 - y1, x2 - x1)
    L = 3.2
    p1 = (x2 - L * _m.cos(a - 0.4), y2 - L * _m.sin(a - 0.4))
    p2 = (x2 - L * _m.cos(a + 0.4), y2 - L * _m.sin(a + 0.4))
    return (f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke-width="0.9"/>'
            f'<path d="M{x2:.1f} {y2:.1f} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" fill="CC" stroke="none"/>')


def _block(x, y, down=False):
    """Orifice obturé : petit T."""
    d = 1 if down else -1
    return f'<path d="M{x} {y} V{y + 4 * d} M{x - 2.5} {y + 4 * d} H{x + 2.5}" stroke-width="0.9"/>'


def _actuator(kind, x, side):
    """Commande dessinée contre le carré (x = bord du carré), côté 'g' ou 'd'."""
    s = -1 if side == "g" else 1
    y0, y1, ym = 9, 21, 15
    if kind == "ressort":
        pts = " ".join(f"L{x + s * (2 + 2 * i):.1f} {ym + (4 if i % 2 else -4)}" for i in range(5))
        return f'<path d="M{x} {ym} {pts} L{x + s * 12} {ym}" stroke-width="0.9"/>'
    if kind == "bp":
        return f'<path d="M{x} {ym} H{x + s * 7} M{x + s * 7} {ym - 4} V{ym + 4}" stroke-width="0.9"/>' \
               f'<path d="M{x + s * 7} {ym - 4} H{x + s * 10} M{x + s * 7} {ym + 4} H{x + s * 10}" stroke-width="0.9"/>'
    if kind == "manuel":
        return f'<path d="M{x} {ym} H{x + s * 5} M{x + s * 5} {ym - 4} V{ym + 4} M{x + s * 5} {ym - 4} H{x + s * 10}" stroke-width="0.9"/>'
    if kind == "levier":
        return f'<path d="M{x} {ym} H{x + s * 5} M{x + s * 5} {ym} L{x + s * 10} {ym - 6}" stroke-width="0.9"/><circle cx="{x + s * 10}" cy="{ym - 6}" r="1" fill="CC"/>'
    if kind == "solenoide":
        xa, xb = sorted((x, x + s * 9))
        return f'<rect x="{xa}" y="{y0 + 1}" width="9" height="10" stroke-width="0.9"/><path d="M{xa} {y1 - 1} L{xb} {y0 + 1}" stroke-width="0.9"/>'
    if kind == "pilote":
        xt = x + s * 3
        return (f'<path d="M{x + s * 12} {ym} H{xt}" stroke-dasharray="1.5 1" stroke-width="0.8"/>'
                f'<path d="M{x} {ym} L{xt} {ym - 3} L{xt} {ym + 3} Z" fill="CC" stroke="none"/>')
    if kind == "galet":
        return f'<path d="M{x} {ym} H{x + s * 6}"/><circle cx="{x + s * 9}" cy="{ym}" r="3" stroke-width="0.9"/>'
    if kind == "poing":
        return f'<path d="M{x} {ym} H{x + s * 6}"/><path d="M{x + s * 6} {ym - 6} A6 6 0 0 {1 if s > 0 else 0} {x + s * 6} {ym + 6} Z" stroke-width="0.9"/>'
    return ""


def distributeur(n_pos, ports_top, ports_bot, cells, left, right, rest):
    """cells[i] : contenu du carré i (coordonnées locales 0..20) ; rest = indice de la position repos (orifices)."""
    x0 = 14
    body = ""
    for i in range(n_pos):
        xs = x0 + 20 * i
        body += f'<rect x="{xs}" y="5" width="20" height="20"/>'
        body += cells[i](xs)
    xr = x0 + 20 * rest
    for fx, nm in ports_top:
        body += f'<path d="M{xr + fx * 20:.1f} 5 V0" stroke-width="0.9"/>'
    for fx, nm in ports_bot:
        body += f'<path d="M{xr + fx * 20:.1f} 25 V30" stroke-width="0.9"/>'
    for kinds, side in ((left, "g"), (right, "d")):
        xe = x0 if side == "g" else x0 + 20 * n_pos
        for j, k in enumerate(kinds):
            body += _actuator(k, xe - (11 * j if side == "g" else -11 * j), side)
    w = x0 * 2 + 20 * n_pos + (11 * (max(len(left), len(right)) - 1) * 2 if max(len(left), len(right)) > 1 else 0)
    w = 20 * ((w + 19) // 20)
    pins = [(xr + fx * 20, 0) for fx, _ in ports_top] + [(xr + fx * 20, 30) for fx, _ in ports_bot]
    names = " ".join([nm for _, nm in ports_top] + [nm for _, nm in ports_bot])
    return w, 30, body, pins, names


def C32_rest(xs):   # 3/2 NF repos : 2 -> 3, 1 obturé
    return _arrow(xs + 10, 6, xs + 15, 24) + _block(xs + 5, 25, False)


def C32_work(xs):
    return _arrow(xs + 5, 24, xs + 10, 6) + _block(xs + 15, 25, False)


def C52_rest(xs):   # 5/2 repos : 1 -> 2, 4 -> 5
    return _arrow(xs + 10, 24, xs + 14, 6) + _arrow(xs + 6, 6, xs + 4, 24) + _block(xs + 16, 25, False)


def C52_work(xs):   # travail : 1 -> 4, 2 -> 3
    return _arrow(xs + 10, 24, xs + 6, 6) + _arrow(xs + 14, 6, xs + 16, 24) + _block(xs + 4, 25, False)


def C53_mid(xs):    # centre fermé
    return _block(xs + 6, 5, True) + _block(xs + 14, 5, True) + _block(xs + 4, 25) + _block(xs + 10, 25) + _block(xs + 16, 25)


def C42_rest(xs):
    return _arrow(xs + 6, 24, xs + 14, 6) + _arrow(xs + 6, 6, xs + 14, 24)


def C42_work(xs):
    return _arrow(xs + 6, 24, xs + 6, 6) + _arrow(xs + 14, 6, xs + 14, 24)


def C22_rest(xs):
    return _block(xs + 10, 5, True) + _block(xs + 10, 25)


def C22_work(xs):
    return _arrow(xs + 10, 24, xs + 10, 6)


P32 = ([(0.5, "2")], [(0.25, "1"), (0.75, "3")])
P52 = ([(0.3, "4"), (0.7, "2")], [(0.2, "5"), (0.5, "1"), (0.8, "3")])
P42 = ([(0.3, "4"), (0.7, "2")], [(0.3, "1"), (0.7, "3")])
P22 = ([(0.5, "2")], [(0.5, "1")])
for sid, nm, npos, ports, cells, L_, R_, rest in (
        ("d32_bp", "Distributeur 3/2 NF, bouton poussoir / ressort", 2, P32, [C32_work, C32_rest], ["bp"], ["ressort"], 1),
        ("d32_galet", "Distributeur 3/2 NF à galet (capteur fin de course)", 2, P32, [C32_work, C32_rest], ["galet"], ["ressort"], 1),
        ("d32_ev", "Électrovanne 3/2 NF (électrique / ressort)", 2, P32, [C32_work, C32_rest], ["solenoide"], ["ressort"], 1),
        ("d32_pilote", "Distributeur 3/2 à pilotage pneumatique / ressort", 2, P32, [C32_work, C32_rest], ["pilote"], ["ressort"], 1),
        ("d32_au", "Distributeur 3/2 d'arrêt d'urgence (coup de poing)", 2, P32, [C32_work, C32_rest], ["poing"], ["ressort"], 1),
        ("d32_manuel", "Distributeur 3/2 à commande manuelle (levier)", 2, P32, [C32_work, C32_rest], ["levier"], ["ressort"], 1),
        ("d22_ev", "Électrovanne 2/2 NF", 2, P22, [C22_work, C22_rest], ["solenoide"], ["ressort"], 1),
        ("d42_manuel", "Distributeur 4/2 manuel / ressort", 2, P42, [C42_work, C42_rest], ["manuel"], ["ressort"], 1),
        ("d52_mono_ev", "Électrodistributeur 5/2 monostable (électrique / ressort)", 2, P52, [C52_work, C52_rest], ["solenoide"], ["ressort"], 1),
        ("d52_bi_ev", "Électrodistributeur 5/2 bistable (2 bobines)", 2, P52, [C52_work, C52_rest], ["solenoide"], ["solenoide"], 1),
        ("d52_bi_pil", "Distributeur 5/2 bistable à pilotage pneumatique", 2, P52, [C52_work, C52_rest], ["pilote"], ["pilote"], 1),
        ("d52_mono_pil", "Distributeur 5/2 monostable pilotage pneumatique / ressort", 2, P52, [C52_work, C52_rest], ["pilote"], ["ressort"], 1),
        ("d53_cf", "Électrodistributeur 5/3 centre fermé", 3, P52, [C52_work, C53_mid, C52_rest], ["solenoide", "ressort"], ["ressort", "solenoide"], 1)):
    w_, h_, b_, p_, n_ = distributeur(npos, ports[0], ports[1], cells, L_, R_, rest)
    add(sid, nm, PN, w_, h_, b_, pins=p_, pin_names=n_)

# vérins
add("verin_se", "Vérin simple effet (rappel par ressort)", PN, 80, 30,
    '<rect x="4" y="5" width="50" height="16"/><path d="M24 5 V21" stroke-width="2"/><path d="M24 13 H76" stroke-width="2"/>'
    '<path d="M26 13 L30 7 L34 19 L38 7 L42 19 L46 7 L50 19 L53 13" stroke-width="0.8"/><path d="M10 21 V30"/>',
    pins=[(10, 30)], pin_names="")
add("verin_de", "Vérin double effet", PN, 80, 30,
    '<rect x="4" y="5" width="50" height="16"/><path d="M24 5 V21" stroke-width="2"/><path d="M24 13 H76" stroke-width="2"/>'
    '<path d="M10 21 V30 M48 21 V30"/>', pins=[(10, 30), (48, 30)], pin_names="")
add("verin_de_amorti", "Vérin double effet à amortissement réglable", PN, 80, 30,
    '<rect x="4" y="5" width="50" height="16"/><path d="M24 5 V21" stroke-width="2"/><path d="M24 13 H76" stroke-width="2"/>'
    '<rect x="6" y="9" width="5" height="8" stroke-width="0.7"/><rect x="47" y="9" width="5" height="8" stroke-width="0.7"/>'
    '<path d="M4 23 L13 3 M45 23 L54 3" stroke-width="0.6"/><path d="M10 21 V30 M48 21 V30"/>',
    pins=[(10, 30), (48, 30)], pin_names="")
add("verin_de_dt", "Vérin double effet double tige", PN, 100, 30,
    '<rect x="24" y="5" width="50" height="16"/><path d="M48 5 V21" stroke-width="2"/><path d="M4 13 H96" stroke-width="2"/>'
    '<path d="M30 21 V30 M68 21 V30"/>', pins=[(30, 30), (68, 30)], pin_names="")
add("verin_rotatif", "Vérin rotatif / moteur pneumatique", PN, 40, 40,
    '<circle cx="20" cy="18" r="12"/><path d="M14 22 L20 10 L26 22 Z" fill="CC"/><path d="M10 30 V40 M30 30 V40"/>',
    pins=[(10, 40), (30, 40)])
add("ventouse", "Ventouse (venturi)", PN, 40, 30,
    '<path d="M20 2 V12 M10 12 H30 L26 22 H14 Z"/>', pins=[(20, 2)])

# énergie et traitement de l'air
add("source_p", "Source de pression (air comprimé)", PN, 20, 20,
    '<circle cx="10" cy="10" r="6"/><circle cx="10" cy="10" r="1.6" fill="CC"/>', pins=[(10, 16)])
add("compresseur", "Compresseur", PN, 40, 40,
    '<circle cx="20" cy="20" r="12"/><path d="M20 8 L15 17 H25 Z" fill="CC"/><path d="M20 32 V40"/>', pins=[(20, 40)])
add("echappement", "Échappement", PN, 20, 20, '<path d="M10 0 V8 M4 8 H16 L10 18 Z"/>', pins=[(10, 0)])
add("silencieux", "Silencieux d'échappement", PN, 20, 20,
    '<path d="M10 0 V6"/><path d="M5 6 H15 L10 18 Z"/><path d="M7 9 H13 M8 12 H12" stroke-width="0.6"/>', pins=[(10, 0)])
add("reservoir", "Réservoir", PN, 60, 30, '<rect x="6" y="6" width="48" height="18" rx="9"/><path d="M30 0 V6"/>', pins=[(30, 0)])
add("filtre", "Filtre (purge manuelle)", PN, 40, 40,
    '<path d="M20 6 L32 20 L20 34 L8 20 Z M20 6 V34" stroke-width="0.9"/><path d="M8 20 H0 M32 20 H40" stroke-width="0.9"/>'
    '<path d="M20 6 V34" stroke-dasharray="2 1.5" stroke-width="0.7"/>', pins=[(0, 20), (40, 20)])
add("regulateur", "Régulateur de pression (détendeur)", PN, 40, 40,
    '<rect x="10" y="8" width="20" height="24"/><path d="M16 28 L24 12" stroke-width="0.9"/>'
    '<path d="M24 12 L20 13 M24 12 L23 16" stroke-width="0.9"/><path d="M0 20 H10 M30 20 H40"/>'
    '<path d="M20 32 V36 L16 38 L24 40" stroke-width="0.7"/>', pins=[(0, 20), (40, 20)])
add("lubrificateur", "Lubrificateur", PN, 40, 40,
    '<path d="M20 6 L32 20 L20 34 L8 20 Z" stroke-width="0.9"/><path d="M14 26 H26 M20 26 V14" stroke-width="0.9"/>'
    '<path d="M0 20 H8 M32 20 H40"/>', pins=[(0, 20), (40, 20)])
add("frl", "Unité FRL (filtre-régulateur-lubrificateur)", PN, 60, 40,
    '<rect x="8" y="6" width="44" height="28" stroke-dasharray="3 2" stroke-width="0.8"/>'
    '<path d="M18 12 L24 20 L18 28 L12 20 Z M30 14 V26 M30 14 L34 18" stroke-width="0.8"/>'
    '<path d="M42 12 L48 20 L42 28 L36 20 Z M39 24 H45" stroke-width="0.8"/><path d="M0 20 H8 M52 20 H60"/>',
    pins=[(0, 20), (60, 20)])
add("manometre", "Manomètre", PN, 30, 40, '<circle cx="15" cy="14" r="10"/><path d="M9 20 L21 8 M21 8 L17 9 M21 8 L20 12" stroke-width="0.9"/><path d="M15 24 V40"/>',
    pins=[(15, 40)])
add("pressostat", "Pressostat / capteur de pression", PN, 40, 40,
    '<rect x="6" y="8" width="18" height="20"/><path d="M24 18 H32 M30 14 L36 18 L30 22" stroke-width="0.9"/>'
    '<path d="M15 28 V40" stroke-dasharray="2 1.5"/>', pins=[(15, 40)])

# clapets et fonctions logiques pneumatiques
add("clapet_ar", "Clapet anti-retour", PN, 40, 20,
    '<path d="M0 10 H12 M28 10 H40"/><circle cx="18" cy="10" r="5"/><path d="M24 4 L18 10 L24 16" />', pins=[(0, 10), (40, 10)])
add("limiteur_debit", "Réducteur de débit unidirectionnel", PN, 60, 40,
    '<path d="M0 20 H60"/><path d="M22 14 Q30 20 22 26 M38 14 Q30 20 38 26" stroke-width="0.9"/>'
    '<path d="M22 30 L38 10 M38 10 L34 11 M38 10 L37 14" stroke-width="0.8"/>'
    '<path d="M10 20 V34 H50 V20"/><circle cx="28" cy="34" r="3.5"/><path d="M33 30 L28 34 L33 38"/>', pins=[(0, 20), (60, 20)])
add("etrangleur", "Étrangleur réglable (bidirectionnel)", PN, 40, 20,
    '<path d="M0 10 H40"/><path d="M12 4 Q20 10 12 16 M28 4 Q20 10 28 16" stroke-width="0.9"/>'
    '<path d="M12 18 L28 2 M28 2 L24 3 M28 2 L27 6" stroke-width="0.8"/>', pins=[(0, 10), (40, 10)])
add("selecteur_ou", "Sélecteur de circuit (fonction OU)", PN, 40, 30,
    '<rect x="6" y="8" width="28" height="14"/><circle cx="20" cy="15" r="4" fill="CC"/><path d="M0 15 H6 M34 15 H40 M20 8 V0"/>',
    pins=[(0, 15), (40, 15), (20, 0)], pin_names="")
add("fonction_et", "Cellule ET (deux pressions)", PN, 40, 30,
    '<rect x="6" y="8" width="28" height="14"/><rect x="16" y="11" width="8" height="8" fill="CC"/><path d="M0 15 H6 M34 15 H40 M20 8 V0"/>',
    pins=[(0, 15), (40, 15), (20, 0)])
add("bloqueur", "Bloqueur / clapet piloté", PN, 40, 30,
    '<path d="M0 15 H12 M28 15 H40"/><circle cx="18" cy="15" r="5"/><path d="M24 9 L18 15 L24 21"/>'
    '<path d="M20 0 V8" stroke-dasharray="2 1.5"/>', pins=[(0, 15), (40, 15), (20, 0)])
add("conduite", "Conduite de travail (trait plein)", PN, 60, 20, '<path d="M2 10 H58"/>', pins=[(2, 10), (58, 10)])
add("conduite_pilote", "Conduite de pilotage (pointillé)", PN, 60, 20, '<path d="M2 10 H58" stroke-dasharray="4 2"/>',
    pins=[(2, 10), (58, 10)])

# ---------------------------------------------------------------- aéronautique : schémas de câblage
AE = "Aéronautique – câblage"
add("ae_cb", "Disjoncteur aéronautique (thermique, à bouton)", AE, 40, 20,
    '<path d="M0 14 H12 M28 14 H40"/><path d="M12 14 A8 8 0 0 1 28 14"/><path d="M20 6 V2 M16 2 H24" stroke-width="1.6"/>',
    pins=[(0, 14), (40, 14)], pin_names="")
add("ae_cb3", "Disjoncteur aéronautique tripolaire", AE, 40, 60,
    "".join(f'<path d="M0 {y} H12 M28 {y} H40"/><path d="M12 {y} A8 8 0 0 1 28 {y}"/>' for y in (14, 34, 54))
    + '<path d="M20 6 V50" stroke-dasharray="2 1.6"/><path d="M20 6 V2 M16 2 H24" stroke-width="1.6"/>',
    pins=[(0, 14), (40, 14), (0, 34), (40, 34), (0, 54), (40, 54)])
add("ae_plug", "Connecteur – fiche mâle (P, broche)", AE, 40, 20,
    '<path d="M0 10 H24 M18 5 L26 10 L18 15"/>', pins=[(0, 10), (26, 10)], pin_names="")
add("ae_recept", "Connecteur – embase femelle (J, douille)", AE, 40, 20,
    '<path d="M40 10 H22 M18 4 A6 6 0 0 0 18 16"/>', pins=[(40, 10), (16, 10)], pin_names="")
add("ae_conn_pair", "Connecteur P/J accouplé", AE, 40, 20,
    '<path d="M0 10 H17 M12 5 L19 10 L12 15 M40 10 H24 M22 4 A6 6 0 0 0 22 16"/>', pins=[(0, 10), (40, 10)])
add("ae_conn_box", "Connecteur multibroches (bloc P1 / J1)", AE, 40, 80,
    '<rect x="12" y="4" width="16" height="72" rx="2"/>'
    + "".join(f'<path d="M0 {y} H12 M28 {y} H40"/>' + t(20, y + 2, str(i + 1), 5) for i, y in enumerate(range(12, 76, 12))),
    pins=[(0, y) for y in range(12, 76, 12)] + [(40, y) for y in range(12, 76, 12)])
add("ae_circ", "Connecteur circulaire (vue de face)", AE, 40, 40,
    '<circle cx="20" cy="20" r="16"/><circle cx="20" cy="20" r="12" stroke-width="0.6"/>'
    + "".join(f'<circle cx="{20 + 7 * _m.cos(a):.1f}" cy="{20 + 7 * _m.sin(a):.1f}" r="1.6" fill="CC"/>'
              for a in [i * _m.pi / 3 for i in range(6)]) + '<circle cx="20" cy="20" r="1.6" fill="CC"/><path d="M20 2 V5" stroke-width="2"/>')
add("ae_splice", "Épissure (splice SP)", AE, 40, 20,
    '<path d="M0 10 H40"/><circle cx="20" cy="10" r="3" fill="CC"/>' + t(20, 4, "SP", 5), pins=[(0, 10), (40, 10)])
add("ae_ground", "Masse structure (GD)", AE, 20, 30,
    '<path d="M10 0 V12 M2 12 H18 M5 16 H15 M8 20 H12"/>' + t(10, 29, "GD", 5), pins=[(10, 0)])
add("ae_bond", "Métallisation / tresse de masse", AE, 40, 20,
    '<path d="M0 10 H8 M32 10 H40"/><path d="M8 10 Q12 4 16 10 T24 10 T32 10" stroke-width="0.9"/>'
    '<path d="M8 13 Q12 7 16 13 T24 13 T32 13" stroke-width="0.9"/>', pins=[(0, 10), (40, 10)])
add("ae_shield", "Fil blindé (blindage à la masse)", AE, 60, 30,
    '<path d="M0 12 H60"/><ellipse cx="30" cy="12" rx="8" ry="6" stroke-dasharray="2 1.4"/>'
    '<path d="M30 18 V24 H40" stroke-dasharray="2 1.4"/><path d="M40 24 V28 M36 28 H44"/>', pins=[(0, 12), (60, 12)])
add("ae_twisted", "Paire torsadée", AE, 60, 20,
    '<path d="M0 6 H10 C16 6 18 14 24 14 S32 6 38 6 S46 14 50 14 H60"/>'
    '<path d="M0 14 H10 C16 14 18 6 24 6 S32 14 38 14 S46 6 50 6 H60"/>',
    pins=[(0, 6), (0, 14), (60, 14), (60, 6)])
add("ae_twisted_sh", "Paire torsadée blindée", AE, 60, 30,
    '<path d="M0 6 H10 C16 6 18 14 24 14 S32 6 38 6 S46 14 50 14 H60"/>'
    '<path d="M0 14 H10 C16 14 18 6 24 6 S32 14 38 14 S46 6 50 6 H60"/>'
    '<ellipse cx="30" cy="10" rx="10" ry="8" stroke-dasharray="2 1.4"/><path d="M30 18 V26" stroke-dasharray="2 1.4"/>',
    pins=[(0, 6), (0, 14), (60, 14), (60, 6)])
add("ae_lug", "Cosse à œillet (terminal)", AE, 40, 20,
    '<path d="M0 10 H24"/><circle cx="29" cy="10" r="5"/><circle cx="29" cy="10" r="1.6"/>', pins=[(0, 10)])
add("ae_tb", "Bornier (TB)", AE, 40, 60,
    '<rect x="12" y="4" width="16" height="52"/>'
    + "".join(f'<path d="M0 {y} H40"/><circle cx="20" cy="{y}" r="2"/>' for y in (14, 30, 46)) + t(20, 2.5, "TB", 4.5),
    pins=[(0, 14), (0, 30), (0, 46), (40, 14), (40, 30), (40, 46)])
add("ae_bus", "Barre bus (BUS)", AE, 100, 20, '<path d="M4 10 H96" stroke-width="3.2"/>' + t(50, 6, "BUS", 5, "bold"),
    pins=[(20, 10), (40, 10), (60, 10), (80, 10)])
add("ae_toggle", "Interrupteur à bascule (inverseur)", AE, 40, 40,
    '<path d="M0 20 H10 M30 10 H40 M30 30 H40 M12 20 L29 11"/><circle cx="11" cy="20" r="1.6"/>'
    '<path d="M20 15 L16 4" stroke-width="1.6"/><circle cx="16" cy="4" r="1.6" fill="CC"/>',
    pins=[(0, 20), (40, 10), (40, 30)], pin_names="C 1 2")
add("ae_relay", "Relais / contacteur de puissance (K)", AE, 60, 40,
    '<rect x="4" y="12" width="14" height="16"/><path d="M0 20 H4 M11 0 V12 M11 28 V40"/>'
    '<path d="M18 20 H32" stroke-dasharray="2 1.6"/><path d="M34 6 H46 M54 6 H60 M54 6 L40 14 M34 34 H46 M54 34 H60 M54 34 L40 26"/>',
    pins=[(11, 0), (11, 40), (34, 6), (60, 6), (34, 34), (60, 34)], pin_names="X1 X2")
add("ae_gen", "Générateur / alternateur (GEN)", AE, 40, 40, '<circle cx="20" cy="20" r="14"/>' + t(20, 23.5, "GEN", 7, "bold"),
    pins=[(20, 6), (20, 34)])
add("ae_batt", "Batterie de bord (BAT)", AE, 40, 40,
    '<path d="M20 0 V12 M20 28 V40 M10 12 H30 M14 17 H26 M10 22 H30 M14 27 H26"/>' + t(36, 22, "BAT", 4.5, "bold"),
    pins=[(20, 0), (20, 40)])
add("ae_annunc", "Voyant d'alarme (annunciator)", AE, 40, 30,
    '<rect x="4" y="5" width="32" height="20" rx="2" fill="#ffecb3"/>' + t(20, 17.5, "WARN", 5.5, "bold"), pins=[(4, 15), (36, 15)])
add("ae_feed", "Traversée étanche (cloison)", AE, 40, 40,
    '<path d="M18 0 V40 M22 0 V40" stroke-width="1.4"/><path d="M0 20 H40"/><circle cx="20" cy="20" r="4"/>',
    pins=[(0, 20), (40, 20)])
add("ae_wire_id", "Repère de fil (ex. W1001-22)", AE, 60, 20,
    '<path d="M0 12 H60"/><rect x="14" y="3" width="32" height="7" fill="#ffffff" stroke-width="0.6"/>' + t(30, 8.6, "W1001-22", 4.5),
    pins=[(0, 12), (60, 12)])

# ---------------------------------------------------------------- énergie solaire photovoltaïque
SOL = "Énergie solaire – symboles"
SOLT = "Énergie solaire – schéma technologique"
_W = lambda s: s.replace('fill="CC"', 'fill="#ffffff"')

add("pv_cellule", "Cellule photovoltaïque", SOL, 20, 40,
    '<path d="M10 0 V6 M10 34 V40"/><rect x="3" y="6" width="14" height="28"/><path d="M3 6 L10 13 L17 6"/>',
    pins=[(10, 0), (10, 40)])
add("pv_module", "Module / panneau photovoltaïque (symbole)", SOL, 40, 60,
    '<path d="M20 0 V8 M20 52 V60"/><rect x="8" y="8" width="24" height="44"/><path d="M8 8 L20 20 L32 8"/>'
    + t(28, 6, "+", 7, "bold") + t(28, 60, "−", 7, "bold"),
    pins=[(20, 0), (20, 60)], pin_names="+ −")
add("pv_chaine", "Chaîne de modules PV (string)", SOL, 100, 60,
    "".join(f'<rect x="{x}" y="10" width="16" height="40"/><path d="M{x} 10 L{x + 8} 18 L{x + 16} 10"/>' for x in (6, 30, 78))
    + '<path d="M0 30 H6 M22 30 H30 M46 30 H52 M72 30 H78 M94 30 H100"/><path d="M54 30 H70" stroke-dasharray="2 3"/>'
    + t(4, 24, "+", 7, "bold") + t(96, 24, "−", 7, "bold"),
    pins=[(0, 30), (100, 30)], pin_names="+ −")


def _conv(a, b, name):
    def f(p):
        return (40, 40, '<path d="M0 20 H6 M34 20 H40"/><rect x="6" y="6" width="28" height="28"/><path d="M6 34 L34 6"/>' + a + b)
    return f


_DC_TL = '<path d="M10 12 H20" stroke-width="1.2"/><path d="M10 16 H20" stroke-width="1.2" stroke-dasharray="3 2"/>'
_DC_BR = '<path d="M20 26 H30" stroke-width="1.2"/><path d="M20 30 H30" stroke-width="1.2" stroke-dasharray="3 2"/>'
_AC_TL = '<path d="M10 15 Q12.5 10 15 15 T20 15" stroke-width="1.2"/>'
_AC_BR = '<path d="M20 28 Q22.5 23 25 28 T30 28" stroke-width="1.2"/>'
add("pv_onduleur", "Onduleur (continu → alternatif)", SOL, 40, 40, func=_conv(_DC_TL, _AC_BR, ""), pins=[(0, 20), (40, 20)])
add("pv_dcdc", "Convertisseur continu / continu", SOL, 40, 40, func=_conv(_DC_TL, _DC_BR, ""), pins=[(0, 20), (40, 20)])
add("pv_chargeur", "Chargeur / redresseur (alternatif → continu)", SOL, 40, 40, func=_conv(_AC_TL, _DC_BR, ""), pins=[(0, 20), (40, 20)])


def _regul(p):
    ty = p.get("type", "MPPT")
    return (80, 60,
            '<rect x="10" y="10" width="60" height="40"/><path d="M10 50 L70 10" stroke-width="0.8"/>'
            '<path d="M16 17 H28" stroke-width="1.2"/><path d="M16 21 H28" stroke-width="1.2" stroke-dasharray="3 2"/>'
            '<path d="M52 39 H64" stroke-width="1.2"/><path d="M52 43 H64" stroke-width="1.2" stroke-dasharray="3 2"/>'
            + t(40, 33, ty, 7, "bold")
            + '<path d="M0 20 H10 M0 40 H10 M70 20 H80 M70 40 H80 M30 50 V60 M50 50 V60"/>'
            + t(4, 17, "+", 6) + t(4, 37, "−", 6) + t(76, 17, "+", 6) + t(76, 37, "−", 6)
            + t(18, 8, "PV", 5) + t(62, 8, "BAT", 5) + t(40, 59, "U", 5))


add("pv_regulateur", "Régulateur de charge (MPPT / PWM)", SOL,
    params=[("type", "Type", "MPPT", ["MPPT", "PWM"])], func=_regul,
    pins=[(0, 20), (0, 40), (80, 20), (80, 40), (30, 60), (50, 60)], pin_names="")


def _bat_sym(p):
    v = p.get("tension", "12 V")
    n = {"2 V": 1, "6 V": 3, "12 V": 6, "24 V": 12, "48 V": 24}.get(v, 6)
    if n == 1:
        body = '<path d="M0 20 H36 M44 20 H80 M36 8 V32"/><path d="M44 13 V27" stroke-width="3"/>'
    else:
        body = ('<path d="M0 20 H12 M68 20 H80"/>'
                '<path d="M12 8 V32"/><path d="M18 13 V27" stroke-width="3"/><path d="M18 20 H24"/>'
                '<path d="M24 8 V32"/><path d="M30 13 V27" stroke-width="3"/>'
                '<path d="M32 20 H48" stroke-dasharray="2 2.5"/>'
                '<path d="M50 8 V32"/><path d="M56 13 V27" stroke-width="3"/><path d="M56 20 H62"/>'
                '<path d="M62 8 V32"/><path d="M68 13 V27" stroke-width="3"/>')
    x1, x2 = (34, 48) if n == 1 else (8, 74)
    return (80, 40, body + t(x1, 6, "+", 7, "bold") + t(x2, 6, "−", 7, "bold")
            + t(40, 39, v + (f" ({n} × 2 V)" if n > 1 else ""), 6))


add("pv_batterie", "Batterie d'accumulateurs (2 / 12 / 24 / 48 V)", SOL,
    params=[("tension", "Tension", "12 V", ["2 V", "6 V", "12 V", "24 V", "48 V"])], func=_bat_sym,
    pins=[(0, 20), (80, 20)], pin_names="+ −")
add("pv_shunt", "Shunt de mesure de courant", SOL, 40, 20,
    '<path d="M0 12 H8 M32 12 H40"/><rect x="8" y="8" width="24" height="8"/><path d="M14 8 V2 M26 8 V2"/>' + t(20, 20, "shunt", 4.5),
    pins=[(0, 10), (40, 10)])
add("pv_capteur_i", "Capteur de courant (pince / effet Hall)", SOL, 40, 40,
    '<path d="M0 20 H40"/><ellipse cx="20" cy="20" rx="7" ry="13"/><path d="M20 7 V0"/>' + t(31, 9, "I", 7, "bold"),
    pins=[(0, 20), (40, 20)])
add("pv_ampere_dc", "Ampèremètre continu (A ⎓)", SOL, 40, 20,
    '<path d="M0 10 H11 M29 10 H40"/><circle cx="20" cy="10" r="9"/>' + t(20, 11.5, "A", 7, "bold")
    + '<path d="M16 15.5 H24" stroke-width="0.7"/><path d="M16 17 H24" stroke-width="0.7" stroke-dasharray="1.5 1"/>',
    pins=[(0, 10), (40, 10)])
add("pv_volt_dc", "Voltmètre continu (V ⎓)", SOL, 40, 20,
    '<path d="M0 10 H11 M29 10 H40"/><circle cx="20" cy="10" r="9"/>' + t(20, 11.5, "V", 7, "bold")
    + '<path d="M16 15.5 H24" stroke-width="0.7"/><path d="M16 17 H24" stroke-width="0.7" stroke-dasharray="1.5 1"/>',
    pins=[(0, 10), (40, 10)])
add("pv_compteur", "Compteur d'énergie (Wh)", SOL, 40, 40,
    '<path d="M20 0 V6 M20 34 V40"/><rect x="8" y="6" width="24" height="28" rx="4"/><path d="M8 13 H32"/>' + t(20, 27, "Wh", 7, "bold"),
    pins=[(20, 0), (20, 40)])
add("pv_fusible", "Fusible PV (gPV)", SOL, 20, 40,
    '<path d="M10 0 V40"/><rect x="5" y="10" width="10" height="20"/>' + t(19, 8, "gPV", 4.5),
    pins=[(10, 0), (10, 40)])
add("pv_sect_dc", "Interrupteur-sectionneur continu (DC)", SOL, 40, 40,
    '<path d="M20 0 V12 M20 28 V40 M20 28 L11 13 M17 12 H23"/>'
    '<path d="M26 18 H34" stroke-width="1"/><path d="M26 21 H34" stroke-width="1" stroke-dasharray="2 1.5"/>',
    pins=[(20, 0), (20, 40)])
add("pv_parafoudre", "Parafoudre (protection surtension)", SOL, 20, 60,
    '<path d="M10 0 V6 M10 54 V60"/><rect x="3" y="6" width="14" height="22"/><rect x="3" y="32" width="14" height="22"/>'
    '<path d="M3 11 H17 M3 49 H17"/><path d="M10 14 V25 M7 21 L10 25 L13 21"/><path d="M10 47 V36 M7 40 L10 36 L13 40"/>',
    pins=[(10, 0), (10, 60)])
add("pv_mc4", "Connecteur photovoltaïque (MC4)", SOL, 40, 20,
    '<path d="M0 10 H12 M28 10 H40"/><path d="M12 3 L19 10 L12 17"/><path d="M20 3 L27 10 L20 17"/><path d="M27 10 H28"/>',
    pins=[(0, 10), (40, 10)])
add("pv_diode", "Diode anti-retour (by-pass)", SOL, 40, 20,
    '<path d="M0 10 H8 M32 10 H40"/><rect x="8" y="4" width="24" height="12"/><path d="M13 10 H27"/>'
    '<path d="M16 6.5 L22 10 L16 13.5 Z" fill="CC"/><path d="M22 6 V14"/>',
    pins=[(0, 10), (40, 10)])
add("pv_thermique", "Capteur solaire thermique", SOL, 80, 80,
    '<path d="M12 74 L66 20 L76 30 L22 84 Z" transform="translate(-4 -6)"/>'
    '<circle cx="64" cy="22" r="4"/><path d="M61 19 L67 25 M67 19 L61 25"/>'
    '<circle cx="21" cy="65" r="4"/><path d="M18 62 L24 68 M24 62 L18 68"/>'
    + "".join(f'<path d="M{x} {y} L{x + 9} {y + 9} M{x + 9} {y + 5} V{y + 9} H{x + 5}"/>' for x, y in ((4, 30), (16, 18), (28, 6), (40, -4))),
    pins=[])
add("pv_soleil", "Soleil (rayonnement)", SOL, 40, 40,
    '<circle cx="20" cy="20" r="8" fill="#ffca28"/>'
    + "".join(f'<path d="M{20 + 11 * c:.1f} {20 + 11 * s:.1f} L{20 + 17 * c:.1f} {20 + 17 * s:.1f}"/>'
              for c, s in ((1, 0), (0.707, 0.707), (0, 1), (-0.707, 0.707), (-1, 0), (-0.707, -0.707), (0, -1), (0.707, -0.707))),
    pins=[])


# ---- schéma technologique (site isolé)
def _panneau(p):
    pw = p.get("puissance", "300 Wc")
    cells = "".join(f'<rect x="{8 + c * 14}" y="{8 + r * 14}" width="13" height="13" fill="#1f4e9a" stroke="#9fb8e0" stroke-width="0.5"/>'
                    for r in range(9) for c in range(6))
    return (100, 160,
            '<rect x="3" y="3" width="94" height="136" rx="1.5" fill="#d7dde5" stroke="#5f6b7a" stroke-width="1.6"/>' + cells
            + t(50, 137.5, pw, 5, "bold")
            + '<rect x="40" y="139" width="20" height="7" fill="#263238" stroke="none"/>'
            + '<path d="M44 146 V160" stroke="#111111" stroke-width="2"/><path d="M56 146 V160" stroke="#d32f2f" stroke-width="2"/>'
            + t(38, 157, "−", 7, "bold") + t(62, 157, "+", 7, "bold"))


add("pvt_panneau", "Panneau solaire (vue)", SOLT,
    params=[("puissance", "Puissance", "300 Wc", None)], func=_panneau, pins=[(40, 160), (60, 160)], pin_names="")


def _regul_vue(p):
    ty = p.get("type", "MPPT")
    pv = '<rect x="15" y="62" width="14" height="10" fill="#1f4e9a" stroke="#ffffff" stroke-width="0.6"/><path d="M15 67 H29 M22 62 V72" stroke="#9fb8e0" stroke-width="0.5"/>'
    bat = '<rect x="64" y="63" width="14" height="9" rx="1" fill="#ffffff" stroke="none"/><rect x="66" y="61" width="3" height="2" fill="#ffffff" stroke="none"/><rect x="73" y="61" width="3" height="2" fill="#ffffff" stroke="none"/>'
    bulb = '<circle cx="118" cy="66" r="4.5" fill="#ffeb3b" stroke="none"/><rect x="116" y="70" width="4" height="3" fill="#ffffff" stroke="none"/>'
    term = "".join(f'<rect x="{x - 4}" y="80" width="8" height="8" fill="#9e9e9e" stroke="#424242" stroke-width="0.6"/>'
                   f'<circle cx="{x}" cy="84" r="1.8" fill="#424242" stroke="none"/>' for x in (12, 32, 62, 82, 112, 132))
    return (144, 100,
            '<rect x="2" y="2" width="140" height="88" rx="6" fill="#2b3442" stroke="#111a24" stroke-width="1.4"/>'
            '<rect x="44" y="12" width="56" height="28" rx="2" fill="#b9f6ca" stroke="#0f2a16" stroke-width="1"/>'
            + '<text x="72" y="31" font-size="11" fill="#0f3d1f" stroke="none" font-family="DejaVu Sans Mono, monospace" text-anchor="middle">13.6 V</text>'
            + _W(t(72, 52, ty + " · contrôleur de charge", 6, "bold")) + _W(t(20, 12, "SOLAR", 5)) + pv + bat + bulb + term
            + t(12, 98, "+", 7, "bold") + t(32, 98, "−", 7, "bold") + t(62, 98, "+", 7, "bold") + t(82, 98, "−", 7, "bold")
            + t(112, 98, "+", 7, "bold") + t(132, 98, "−", 7, "bold"))


add("pvt_regulateur", "Contrôleur de charge (vue)", SOLT,
    params=[("type", "Type", "MPPT", ["MPPT", "PWM"])], func=_regul_vue,
    pins=[(12, 90), (32, 90), (62, 90), (82, 90), (112, 90), (132, 90)], pin_names="")


def _bat_vue(p):
    v = p.get("tension", "12 V")
    ah = p.get("capacite", "100 Ah")
    return (120, 80,
            '<rect x="2" y="12" width="116" height="66" rx="4" fill="#37474f" stroke="#1c262b" stroke-width="1.4"/>'
            '<rect x="2" y="12" width="116" height="12" rx="4" fill="#263238" stroke="none"/>'
            '<rect x="16" y="4" width="14" height="10" rx="1.5" fill="#d32f2f" stroke="none"/>'
            '<rect x="90" y="4" width="14" height="10" rx="1.5" fill="#212121" stroke="none"/>'
            '<circle cx="60" cy="48" r="14" fill="#29b6f6" stroke="#ffffff" stroke-width="1.4"/>'
            '<path d="M62 37 L54 50 H60 L57 60 L66 46 H60 Z" fill="#ffffff" stroke="none"/>'
            + _W(t(23, 22, "+", 9, "bold")) + _W(t(97, 22, "−", 9, "bold"))
            + _W(t(24, 52, v, 9, "bold")) + _W(t(96, 52, ah, 7, "bold")) + _W(t(60, 74, "Batterie solaire", 5)))


add("pvt_batterie", "Batterie solaire (vue)", SOLT,
    params=[("tension", "Tension", "12 V", ["2 V", "6 V", "12 V", "24 V", "48 V"]), ("capacite", "Capacité", "100 Ah", None)],
    func=_bat_vue, pins=[(20, 0), (100, 0)], pin_names="")


def _ond_vue(p):
    pw = p.get("puissance", "1000 VA")
    return (90, 140,
            '<rect x="3" y="3" width="84" height="124" rx="5" fill="#eceff1" stroke="#455a64" stroke-width="1.4"/>'
            '<rect x="3" y="3" width="84" height="18" rx="5" fill="#455a64" stroke="none"/>'
            '<rect x="20" y="30" width="50" height="22" rx="2" fill="#263238" stroke="none"/>'
            '<text x="45" y="45" font-size="9" fill="#80deea" stroke="none" font-family="DejaVu Sans Mono, monospace" text-anchor="middle">230 V~</text>'
            '<rect x="25" y="62" width="40" height="40" fill="#ffffff" stroke="#455a64" stroke-width="1"/><path d="M25 102 L65 62" stroke="#455a64"/>'
            '<path d="M30 70 H42" stroke="#455a64" stroke-width="1.4"/><path d="M30 74 H42" stroke="#455a64" stroke-width="1.4" stroke-dasharray="3 2"/>'
            '<path d="M48 93 Q51 87 54 93 T60 93" stroke="#455a64" stroke-width="1.4"/>'
            + _W(t(45, 15, "Onduleur cc / ca", 6, "bold")) + t(45, 115, pw, 6, "bold")
            + '<path d="M15 127 V140" stroke="#d32f2f" stroke-width="2"/><path d="M28 127 V140" stroke="#111111" stroke-width="2"/>'
            + '<path d="M62 127 V140" stroke="#8b4513" stroke-width="2"/><path d="M75 127 V140" stroke="#1e63c8" stroke-width="2"/>'
            + t(10, 136, "+", 6, "bold") + t(34, 136, "−", 6, "bold") + t(56, 136, "L", 5, "bold") + t(81, 136, "N", 5, "bold"))


add("pvt_onduleur", "Onduleur / convertisseur CC-CA (vue)", SOLT,
    params=[("puissance", "Puissance", "1000 VA", None)], func=_ond_vue,
    pins=[(15, 140), (28, 140), (62, 140), (75, 140)], pin_names="")


def _moniteur(p):
    return (80, 50,
            '<rect x="2" y="2" width="76" height="40" rx="4" fill="#263238" stroke="#111111" stroke-width="1.2"/>'
            '<rect x="8" y="8" width="64" height="26" rx="2" fill="#0d47a1" stroke="none"/>'
            f'<text x="40" y="19" font-size="8" fill="#e3f2fd" stroke="none" font-family="DejaVu Sans Mono, monospace" text-anchor="middle">{p.get("tension", "12.8 V")}</text>'
            f'<text x="40" y="30" font-size="8" fill="#ffeb3b" stroke="none" font-family="DejaVu Sans Mono, monospace" text-anchor="middle">{p.get("courant", "5.2 A")}</text>'
            '<path d="M30 42 V50 M50 42 V50" stroke="#555555" stroke-width="1.6"/>')


add("pvt_moniteur", "Moniteur de batterie (tension / courant)", SOLT,
    params=[("tension", "Tension affichée", "12.8 V", None), ("courant", "Courant affiché", "5.2 A", None)],
    func=_moniteur, pins=[(30, 50), (50, 50)], pin_names="")
add("pvt_shunt", "Shunt de mesure (vue)", SOLT, 80, 30,
    '<rect x="4" y="10" width="72" height="14" rx="2" fill="#b0bec5" stroke="#455a64" stroke-width="1"/>'
    '<rect x="26" y="6" width="28" height="22" rx="2" fill="#ffd54f" stroke="#8d6e00" stroke-width="1"/>'
    '<circle cx="10" cy="17" r="3" fill="#455a64" stroke="none"/><circle cx="70" cy="17" r="3" fill="#455a64" stroke="none"/>'
    + t(40, 19.5, "500 A / 50 mV", 4),
    pins=[(10, 30), (70, 30)], pin_names="")
add("pvt_disj_dc", "Disjoncteur continu / sectionneur (vue)", SOLT, 40, 70,
    '<rect x="4" y="4" width="32" height="62" rx="3" fill="#f5f5f5" stroke="#424242" stroke-width="1.2"/>'
    '<rect x="13" y="24" width="14" height="20" rx="2" fill="#1565c0" stroke="none"/><rect x="15" y="26" width="10" height="7" fill="#ffffff" stroke="none"/>'
    + t(20, 14, "DC", 6, "bold") + t(20, 58, "C16", 5)
    + '<path d="M20 0 V4 M20 66 V70" stroke-width="1.6"/>',
    pins=[(20, 0), (20, 70)], pin_names="")
add("pvt_fusible", "Porte-fusible PV (vue)", SOLT, 30, 70,
    '<rect x="4" y="4" width="22" height="62" rx="3" fill="#eceff1" stroke="#424242" stroke-width="1.2"/>'
    '<rect x="9" y="18" width="12" height="34" rx="5" fill="#fff8e1" stroke="#8d6e63" stroke-width="1"/>' + t(15, 38, "15A", 4.5, "bold")
    + '<path d="M15 0 V4 M15 66 V70" stroke-width="1.6"/>',
    pins=[(15, 0), (15, 70)], pin_names="")
add("pvt_ampoule", "Ampoule (charge)", SOLT, 30, 50,
    '<path d="M15 4 C5 4 3 14 7 20 C10 24 10 27 10 30 H20 C20 27 20 24 23 20 C27 14 25 4 15 4 Z" fill="#fff59d" stroke="#8d6e00" stroke-width="1"/>'
    '<rect x="10" y="30" width="10" height="8" fill="#9e9e9e" stroke="none"/><path d="M11 38 V50 M19 38 V50" stroke-width="1.4"/>',
    pins=[(10, 50), (20, 50)], pin_names="")
add("pvt_prise", "Prise de courant 230 V (vue)", SOLT, 40, 40,
    '<rect x="3" y="3" width="34" height="34" rx="6" fill="#fafafa" stroke="#616161" stroke-width="1.2"/>'
    '<circle cx="20" cy="20" r="11" fill="#eeeeee" stroke="#9e9e9e" stroke-width="0.8"/>'
    '<circle cx="15" cy="20" r="2" fill="#424242" stroke="none"/><circle cx="25" cy="20" r="2" fill="#424242" stroke="none"/>'
    '<rect x="18.5" y="9" width="3" height="4" fill="#9e9e9e" stroke="none"/>',
    pins=[(14, 40), (26, 40)], pin_names="")

def _ccpf_vue(p):
    cal = p.get("calibre", "10 A")
    pol = p.get("poles", "+ / −")
    a, b = pol.split(" / ")
    o = ""
    for i, (x, lab) in enumerate(((2, a), (22, b))):
        o += (f'<rect x="{x}" y="6" width="18" height="58" rx="2" fill="#f5f5f5" stroke="#424242" stroke-width="1.1"/>'
              f'<rect x="{x + 3}" y="16" width="12" height="30" rx="3" fill="#cfd8dc" stroke="#607d8b" stroke-width="0.8"/>'
              f'<rect x="{x + 5}" y="20" width="8" height="22" rx="3" fill="#fff8e1" stroke="#8d6e63" stroke-width="0.6"/>'
              f'<circle cx="{x + 9}" cy="11" r="2" fill="#9e9e9e" stroke="none"/><circle cx="{x + 9}" cy="59" r="2" fill="#9e9e9e" stroke="none"/>'
              + t(x + 9, 53, lab, 6, "bold") + t(x + 9, 33, cal, 3.6, "bold"))
    return (42, 70, o
            + '<path d="M11 0 V6 M31 0 V6 M11 64 V70 M31 64 V70" stroke-width="1.4"/>')


add("pvt_ccpf2", "Coupe-circuit porte-fusibles 2 pôles (vue)", SOLT,
    params=[("calibre", "Calibre", "10 A", None), ("poles", "Pôles", "+ / −", ["+ / −", "− / +", "Ph / N"])],
    func=_ccpf_vue, pins=[(11, 0), (31, 0), (11, 70), (31, 70)], pin_names="")

# ---- sources d'énergie de secours / complémentaires
add("src_eolienne", "Éolienne (aérogénérateur, symbole)", SOL, 40, 60,
    '<circle cx="20" cy="40" r="11"/>' + t(20, 43.5, "G", 9, "bold")
    + '<path d="M20 29 V18"/><circle cx="20" cy="15" r="2.5" fill="CC"/>'
    '<path d="M20 15 L20 2 M20 15 L8.7 21.5 M20 15 L31.3 21.5" stroke-width="2.2"/>'
    '<path d="M20 51 V60"/>' + t(34, 55, "∼", 7),
    pins=[(20, 60)])
add("src_ge", "Groupe électrogène (moteur + génératrice, symbole)", SOL, 80, 40,
    '<rect x="3" y="8" width="26" height="24"/>' + t(16, 24, "M", 9, "bold")
    + '<path d="M29 20 H41" stroke-width="2.4"/><circle cx="53" cy="20" r="12"/>' + t(53, 23, "G", 9, "bold")
    + t(53, 31, "∼", 6) + '<path d="M65 20 H80"/>' + t(16, 39, "thermique", 4.5),
    pins=[(80, 20)])
add("src_alternateur", "Alternateur (voiture / bateau) avec redresseur", SOL, 80, 40,
    '<circle cx="18" cy="20" r="12"/>' + t(18, 23, "G", 9, "bold") + t(18, 30.5, "3∼", 5)
    + '<path d="M30 20 H40"/><rect x="40" y="9" width="22" height="22"/><path d="M40 31 L62 9" stroke-width="0.8"/>'
    + '<path d="M44 15 Q46 12 48 15 T52 15" stroke-width="0.9"/><path d="M50 25 H58" stroke-width="0.9"/><path d="M50 27.5 H58" stroke-width="0.9" stroke-dasharray="2 1.2"/>'
    + '<path d="M62 14 H80 M62 26 H80"/>' + t(76, 12, "+", 6, "bold") + t(76, 34, "−", 6, "bold"),
    pins=[(80, 14), (80, 26)], pin_names="B+ B−")
add("src_regul_eol", "Régulateur éolien (avec résistance de délestage)", SOL, 80, 60,
    '<rect x="10" y="10" width="44" height="40"/><path d="M10 50 L54 10" stroke-width="0.8"/>'
    '<path d="M15 18 Q17 14 19 18 T23 18" stroke-width="1.1"/><path d="M40 40 H50" stroke-width="1.1"/><path d="M40 43 H50" stroke-width="1.1" stroke-dasharray="2.5 1.5"/>'
    '<path d="M0 30 H10 M54 22 H80 M54 38 H80"/><path d="M32 50 V56 H58 M74 56 H78"/><rect x="58" y="52" width="16" height="8"/>'
    + t(5, 27, "∼", 6) + t(76, 20, "+", 6, "bold") + t(76, 36, "−", 6, "bold") + t(66, 49, "délestage", 4),
    pins=[(0, 30), (80, 22), (80, 38)], pin_names="")


def _eol_vue(p):
    blades = "".join(f'<path d="M40 30 L{40 + 34 * c:.1f} {30 + 34 * s:.1f}" stroke="#eceff1" stroke-width="5" stroke-linecap="round"/>'
                     f'<path d="M40 30 L{40 + 34 * c:.1f} {30 + 34 * s:.1f}" stroke="#90a4ae" stroke-width="1"/>'
                     for c, s in ((0, -1), (-0.866, 0.5), (0.866, 0.5)))
    return (80, 170,
            '<path d="M37 34 L35 160 H45 L43 34 Z" fill="#cfd8dc" stroke="#78909c" stroke-width="1"/>'
            + blades + '<ellipse cx="40" cy="30" rx="8" ry="6" fill="#ffffff" stroke="#607d8b" stroke-width="1"/>'
            '<circle cx="40" cy="30" r="2.5" fill="#607d8b" stroke="none"/>'
            '<rect x="26" y="156" width="28" height="6" fill="#9e9e9e" stroke="none"/>'
            + t(40, 154, p.get("puissance", "400 W"), 5, "bold")
            + '<path d="M34 162 V170" stroke="#8b4513" stroke-width="2"/><path d="M40 162 V170" stroke="#111111" stroke-width="2"/>'
            '<path d="M46 162 V170" stroke="#7f7f7f" stroke-width="2"/>')


add("pvt_eolienne", "Éolienne (vue)", SOLT, params=[("puissance", "Puissance", "400 W", None)], func=_eol_vue,
    pins=[(34, 170), (40, 170), (46, 170)], pin_names="")


def _ge_vue(p):
    return (130, 90,
            '<rect x="6" y="14" width="118" height="60" rx="6" fill="#f9a825" stroke="#6d4c00" stroke-width="1.4"/>'
            '<path d="M10 14 V6 H120 V14 M10 74 V82 H120 V74" stroke="#424242" stroke-width="2.4" fill="none"/>'
            '<rect x="16" y="22" width="52" height="40" rx="4" fill="#424242" stroke="none"/>'
            + "".join(f'<path d="M22 {y} H62" stroke="#757575" stroke-width="1.6"/>' for y in range(28, 60, 6))
            + '<rect x="78" y="24" width="38" height="36" rx="3" fill="#eceff1" stroke="#455a64" stroke-width="1"/>'
            '<circle cx="88" cy="36" r="5" fill="#ffffff" stroke="#455a64" stroke-width="1"/><circle cx="86.5" cy="36" r="0.9" fill="#424242" stroke="none"/><circle cx="89.5" cy="36" r="0.9" fill="#424242" stroke="none"/>'
            '<rect x="100" y="31" width="10" height="10" rx="1" fill="#e53935" stroke="none"/>'
            + t(97, 54, p.get("puissance", "3 kVA"), 6, "bold") + _W(t(42, 70, "Groupe électrogène", 5, "bold"))
            + '<path d="M100 82 V90" stroke="#8b4513" stroke-width="2"/><path d="M110 82 V90" stroke="#1e63c8" stroke-width="2"/>'
            + t(95, 89, "L", 5, "bold") + t(116, 89, "N", 5, "bold"))


add("pvt_ge", "Groupe électrogène (vue)", SOLT, params=[("puissance", "Puissance", "3 kVA", None)], func=_ge_vue,
    pins=[(100, 90), (110, 90)], pin_names="")


def _alt_vue(p):
    return (100, 70,
            '<circle cx="46" cy="34" r="26" fill="#b0bec5" stroke="#455a64" stroke-width="1.4"/>'
            + "".join(f'<path d="M{46 + 9 * c:.1f} {34 + 9 * s:.1f} L{46 + 23 * c:.1f} {34 + 23 * s:.1f}" stroke="#78909c" stroke-width="2.2"/>'
                      for c, s in ((1, 0), (0.5, 0.866), (-0.5, 0.866), (-1, 0), (-0.5, -0.866), (0.5, -0.866)))
            + '<circle cx="46" cy="34" r="8" fill="#90a4ae" stroke="#455a64" stroke-width="1"/>'
            '<rect x="2" y="27" width="16" height="14" rx="2" fill="#424242" stroke="none"/>'
            + "".join(f'<path d="M{x} 27 V41" stroke="#757575" stroke-width="0.8"/>' for x in range(5, 18, 3))
            + '<rect x="70" y="18" width="18" height="10" rx="2" fill="#d32f2f" stroke="none"/>' + _W(t(79, 25.5, "B+", 5, "bold"))
            + '<rect x="80" y="50" width="14" height="9" rx="2" fill="#212121" stroke="none"/>' + _W(t(87, 57, "−", 6, "bold"))
            + '<path d="M87 59 V70" stroke="#111111" stroke-width="1.6"/>' + t(46, 68, p.get("modele", "14 V – 90 A"), 5, "bold")
            + '<path d="M88 23 H100" stroke="#d32f2f" stroke-width="2"/>')


add("pvt_alternateur", "Alternateur voiture / bateau (vue)", SOLT, params=[("modele", "Modèle", "14 V – 90 A", None)],
    func=_alt_vue, pins=[(100, 23), (87, 70)], pin_names="")

# ================================================================ v1.2.0 : prévention, manutention, logistique,
# dentaire, outils. Dessins originaux (inspirés des pictogrammes normalisés, sans copie d'images).
PREV = "Prévention électrique – EPI, EIS, ECS"
EMB = "Manutention – pictogrammes d'emballage"
SIGN = "Sécurité – signalisation et produits dangereux"
LOG = "Logistique – équipements"
DENT = "Prothésiste dentaire"
OEL = "Outils – électricien"
OMEC = "Outils – mécanicien"
OINF = "Outils – informatique et réseau"
_K = "#212121"


def _frame(body, w=60, h=60):
    return f'<rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="#ffffff" stroke="CC" stroke-width="1.6"/>' + body


def _cross(x1=12, y1=12, x2=48, y2=48):
    return (f'<path d="M{x1} {y1} L{x2} {y2} M{x2} {y1} L{x1} {y2}" stroke="CC" stroke-width="3.2"/>')


def _forklift(x=0, y=0, s=1.0, col="CC"):
    g = (f'<g transform="translate({x} {y}) scale({s})" fill="{col}" stroke="none">'
         '<path d="M6 30 H30 V16 H22 L18 8 H8 V30 Z"/><rect x="10" y="10" width="7" height="8" fill="#ffffff"/>'
         '<rect x="32" y="2" width="3" height="30"/><rect x="35" y="27" width="12" height="3"/>'
         '<circle cx="11" cy="32" r="4.5"/><circle cx="26" cy="32" r="4.5"/>'
         '<circle cx="11" cy="32" r="1.6" fill="#ffffff"/><circle cx="26" cy="32" r="1.6" fill="#ffffff"/></g>')
    return g


def _box(x, y, w, h, col="#c69c6d"):
    return (f'<path d="M{x} {y + h * .25} L{x + w * .5} {y} L{x + w} {y + h * .25} V{y + h * .8} L{x + w * .5} {y + h} L{x} {y + h * .8} Z" '
            f'fill="{col}" stroke="#6d4c2d" stroke-width="1"/>'
            f'<path d="M{x} {y + h * .25} L{x + w * .5} {y + h * .5} L{x + w} {y + h * .25} M{x + w * .5} {y + h * .5} V{y + h}" stroke="#6d4c2d" stroke-width="1" fill="none"/>')


# ---------------------------------------------------------------- prévention électrique (EPI / EIS / ECS)
add("epi_gants", "Gants isolants (EPI)", PREV, 60, 60,
    '<path d="M18 56 V36 L12 24 Q11 20 14 19 L20 30 V12 Q20 8 23 8 Q26 8 26 12 V28 V8 Q26 5 29 5 Q32 5 32 8 V28 V10 Q32 7 35 7 Q38 7 38 10 V30 V16 Q38 13 41 13 Q44 13 44 16 V40 Q44 48 40 56 Z" '
    'fill="#fbc02d" stroke="#8d6e00" stroke-width="1.2"/><path d="M16 48 H44" stroke="#e53935" stroke-width="3"/>' + t(30, 56, "00", 5, "bold"))
add("epi_vetement", "Vêtement de travail électricien (EPI)", PREV, 60, 60,
    '<path d="M20 6 L40 6 L52 16 L46 26 L42 22 V56 H32 L30 36 L28 56 H18 V22 L14 26 L8 16 Z" fill="#283593" stroke="CC" stroke-width="1.2"/>'
    '<path d="M30 6 V34" stroke="#c5cae9" stroke-width="1"/><path d="M18 30 H42" stroke="#ffeb3b" stroke-width="2.5"/>')
add("epi_chaussures", "Chaussures de sécurité (EPI)", PREV, 60, 40,
    '<path d="M6 30 V14 Q6 8 12 8 H26 L30 18 Q44 20 52 24 Q56 26 56 30 V34 H6 Z" fill="#3e2723" stroke="CC" stroke-width="1.2"/>'
    '<path d="M6 34 H56" stroke="#ff8f00" stroke-width="3"/><path d="M42 21 Q52 24 54 30" stroke="#9e9e9e" stroke-width="2.4" fill="none"/>')
add("epi_lunettes", "Lunettes de protection (EPI)", PREV, 60, 30,
    '<path d="M4 10 Q4 6 10 6 H50 Q56 6 56 10 V18 Q56 24 48 24 H38 Q34 24 32 18 Q30 15 28 18 Q26 24 22 24 H12 Q4 24 4 18 Z" fill="#b3e5fc" fill-opacity="0.7" stroke="CC" stroke-width="1.4"/>')
add("eis_tapis", "Tapis isolant (EIS)", PREV, 60, 40,
    '<path d="M4 30 L16 10 H56 L44 30 Z" fill="#455a64" stroke="CC" stroke-width="1.2"/>'
    + "".join(f'<path d="M{8 + i * 5} {28} L{19 + i * 5} {12}" stroke="#78909c" stroke-width="0.8"/>' for i in range(8)))
add("eis_outils", "Outils isolés 1000 V (EIS)", PREV, 60, 60,
    '<rect x="6" y="40" width="22" height="7" rx="3" fill="#e53935"/><rect x="18" y="40" width="10" height="7" rx="2" fill="#fdd835"/>'
    '<path d="M28 43.5 H54" stroke="#9e9e9e" stroke-width="3"/>'
    '<path d="M14 8 L22 30 M22 8 L14 30" stroke="#9e9e9e" stroke-width="3"/>'
    '<path d="M10 24 L4 38 M26 24 L32 38" stroke="#e53935" stroke-width="5" stroke-linecap="round"/>'
    + t(46, 30, "1000 V", 6, "bold") + '<path d="M40 14 L44 20 L48 14 Z" fill="#fdd835" stroke="CC" stroke-width="0.8"/>')
add("eis_cadenas", "Cadenas de consignation (EIS)", PREV, 60, 60,
    '<path d="M20 26 V16 Q20 6 30 6 Q40 6 40 16 V26" stroke="#9e9e9e" stroke-width="4" fill="none"/>'
    '<rect x="14" y="24" width="32" height="26" rx="4" fill="#e53935" stroke="CC" stroke-width="1"/>'
    '<circle cx="30" cy="35" r="3" fill="CC" stroke="none"/><path d="M30 37 V43" stroke="CC" stroke-width="2"/>'
    '<path d="M44 46 L54 54 L48 58 L40 50 Z" fill="#ffffff" stroke="CC" stroke-width="0.8"/>')
add("eis_nappe", "Nappe isolante (EIS)", PREV, 60, 50,
    '<path d="M8 8 Q20 4 34 8 T56 8 V40 Q44 44 32 40 T8 40 Z" fill="#e0f2f1" fill-opacity="0.85" stroke="#00796b" stroke-width="1.4"/>'
    '<circle cx="14" cy="14" r="2" fill="#00796b" stroke="none"/><circle cx="50" cy="14" r="2" fill="#00796b" stroke="none"/>')
add("eis_tabouret", "Tabouret isolant (EIS)", PREV, 60, 50,
    '<path d="M8 12 H52 L48 20 H12 Z" fill="#cfd8dc" stroke="CC" stroke-width="1.2"/>'
    '<path d="M14 20 L10 46 M46 20 L50 46 M22 20 L20 46 M38 20 L40 46" stroke="#90a4ae" stroke-width="3"/>'
    '<path d="M8 46 H52" stroke="CC" stroke-width="1.4"/>')
add("eis_vat", "Vérificateur d'absence de tension (VAT)", PREV, 40, 70,
    '<rect x="8" y="6" width="24" height="40" rx="5" fill="#fdd835" stroke="CC" stroke-width="1.2"/>'
    '<rect x="12" y="12" width="16" height="12" rx="1.5" fill="#263238"/><circle cx="16" cy="30" r="2.5" fill="#e53935" stroke="none"/><circle cx="24" cy="30" r="2.5" fill="#43a047" stroke="none"/>'
    '<path d="M20 46 V64" stroke="#e53935" stroke-width="3"/><path d="M20 64 V68" stroke="#9e9e9e" stroke-width="1.6"/>'
    + _W(t(20, 21, "0 V", 6, "bold")))
add("eis_macaron", "Macaron « Défense de manœuvrer » (EIS)", PREV, 60, 60,
    '<circle cx="30" cy="30" r="27" fill="#e53935" stroke="CC" stroke-width="1"/><circle cx="30" cy="30" r="14" fill="#ffffff" stroke="none"/>'
    '<path d="M32 19 L25 31 H31 L27 41 L36 28 H30 Z" fill="#e53935" stroke="none"/>'
    + _W(t(30, 11, "DÉFENSE DE", 4.4, "bold")) + _W(t(30, 53, "MANŒUVRER", 4.4, "bold")))
add("ecs_barriere", "Barrière de balisage (ECS)", PREV, 70, 50,
    '<path d="M10 8 V48 M60 8 V48" stroke="CC" stroke-width="2.4"/>'
    + "".join(f'<rect x="{10 + i * 10}" y="12" width="10" height="9" fill="{"#e53935" if i % 2 == 0 else "#ffffff"}" stroke="none"/>' for i in range(5))
    + '<rect x="10" y="12" width="50" height="9" fill="none" stroke="CC" stroke-width="0.8"/>'
    '<path d="M4 48 H16 M54 48 H66" stroke="CC" stroke-width="3"/>')
add("ecs_chaine", "Chaîne et piquets de balisage (ECS)", PREV, 80, 50,
    '<path d="M10 10 V46 M70 10 V46" stroke="#e53935" stroke-width="3.4"/><path d="M10 14 V20 M10 28 V34 M70 14 V20 M70 28 V34" stroke="#ffffff" stroke-width="3.4"/>'
    '<path d="M10 14 Q40 32 70 14" stroke="#e53935" stroke-width="2.2" fill="none" stroke-dasharray="4 3"/>'
    '<path d="M4 46 H16 M64 46 H76" stroke="CC" stroke-width="3"/>')
add("ecs_pancarte", "Pancarte « Danger de mort » (ECS)", PREV, 70, 40,
    '<rect x="3" y="3" width="64" height="34" fill="#ffffff" stroke="CC" stroke-width="1.4"/>'
    '<path d="M16 8 L26 26 H6 Z" fill="#fdd835" stroke="CC" stroke-width="1.2"/><path d="M17 12 L13 20 H17 L15 25 L20 18 H16 Z" fill="CC" stroke="none"/>'
    + t(48, 17, "DANGER", 7, "bold").replace('fill="CC"', 'fill="#e53935"') + t(48, 27, "DE MORT", 7, "bold").replace('fill="CC"', 'fill="#e53935"'))
add("ecs_malt", "Dispositif de mise à la terre et en court-circuit (MALT-CCT)", PREV, 80, 60,
    '<path d="M6 54 L40 10" stroke="#fdd835" stroke-width="3.4"/><path d="M6 54 L18 38" stroke="#e53935" stroke-width="3.4"/>'
    '<path d="M40 10 L44 6 M44 6 L48 10" stroke="#9e9e9e" stroke-width="2"/>'
    '<path d="M44 8 Q60 20 52 38 M44 8 Q70 14 68 34 M44 8 Q50 30 40 44" stroke="#bf8040" stroke-width="2" fill="none"/>'
    '<path d="M48 36 L56 40 M64 32 L72 36 M36 42 L44 46" stroke="#616161" stroke-width="3"/>'
    '<path d="M40 44 L40 54 M34 54 H46 M36 57 H44" stroke="#2e9b3a" stroke-width="1.6"/>')
add("ecs_cone", "Cône de signalisation (ECS)", PREV, 40, 50,
    '<path d="M16 6 H24 L34 44 H6 Z" fill="#ff6f00" stroke="CC" stroke-width="1"/><path d="M12 22 H28 L30 30 H10 Z" fill="#ffffff" stroke="none"/>'
    '<rect x="2" y="44" width="36" height="4" fill="CC" stroke="none"/>')

# ---------------------------------------------------------------- manutention : pictogrammes d'emballage (style ISO 780)
add("emb_haut", "Haut (sens de stockage)", EMB, 60, 60, _frame(
    '<path d="M20 44 V18 M40 44 V18" stroke="CC" stroke-width="4"/><path d="M13 22 L20 11 L27 22 Z M33 22 L40 11 L47 22 Z" fill="CC" stroke="none"/>'
    '<path d="M12 48 H48" stroke="CC" stroke-width="3.4"/>'))
add("emb_fragile", "Fragile – manipuler avec précaution", EMB, 60, 60, _frame(
    '<path d="M18 10 H42 Q42 30 30 32 Q18 30 18 10 Z" fill="CC" stroke="none"/><path d="M30 32 V48 M22 49 H38" stroke="CC" stroke-width="3"/>'
    '<path d="M31 11 L27 19 L32 21 L28 28" stroke="#ffffff" stroke-width="1.6" fill="none"/>'))
add("emb_humidite", "Craint l'humidité", EMB, 60, 60, _frame(
    '<path d="M12 30 Q30 10 48 30 Z" fill="CC" stroke="none"/><path d="M30 30 V46 Q30 50 26 50 Q23 50 23 47" stroke="CC" stroke-width="2.6" fill="none"/>'
    + "".join(f'<path d="M{x} {y} l-1.5 4" stroke="CC" stroke-width="1.6"/>' for x, y in ((18, 10), (26, 7), (36, 8), (44, 12)))))
add("emb_chaleur", "Craint la chaleur – protéger du soleil", EMB, 60, 60, _frame(
    '<circle cx="34" cy="14" r="4" fill="CC" stroke="none"/>'
    + "".join(f'<path d="M{34 + 6 * c:.1f} {14 + 6 * s:.1f} L{34 + 10 * c:.1f} {14 + 10 * s:.1f}" stroke="CC" stroke-width="1.4"/>'
              for c, s in ((1, 0), (0.7, 0.7), (-0.7, 0.7), (-1, 0), (-0.7, -0.7), (0.7, -0.7), (0, -1)))
    + '<path d="M10 34 L30 24 L50 34" stroke="CC" stroke-width="3" fill="none"/><rect x="22" y="36" width="16" height="12" fill="CC" stroke="none"/>'))
add("emb_froid", "Protéger du froid", EMB, 60, 60, _frame(
    "".join(f'<path d="M{30 - 18 * c:.1f} {30 - 18 * s:.1f} L{30 + 18 * c:.1f} {30 + 18 * s:.1f}" stroke="CC" stroke-width="2.6"/>' for c, s in ((1, 0), (0.5, 0.866), (-0.5, 0.866)))
    + "".join(f'<path d="M{30 + 12 * c:.1f} {30 + 12 * s:.1f} l{4 * c - 4 * s:.1f} {4 * s + 4 * c:.1f} M{30 + 12 * c:.1f} {30 + 12 * s:.1f} l{4 * c + 4 * s:.1f} {4 * s - 4 * c:.1f}" stroke="CC" stroke-width="1.6"/>'
              for c, s in ((1, 0), (0.5, 0.866), (-0.5, 0.866), (-1, 0), (-0.5, -0.866), (0.5, -0.866)))))
add("emb_cg", "Centre de gravité", EMB, 60, 60, _frame(
    '<path d="M30 8 V52 M8 30 H52" stroke="CC" stroke-width="2.6"/><circle cx="30" cy="30" r="10" fill="none" stroke="CC" stroke-width="3"/>'
    '<path d="M30 20 A10 10 0 0 1 40 30 L30 30 Z M30 40 A10 10 0 0 1 20 30 L30 30 Z" fill="CC" stroke="none"/>'))
add("emb_elingage", "Élinguer ici", EMB, 60, 60, _frame(
    "".join(f'<rect x="25" y="{y}" width="10" height="16" rx="5" fill="none" stroke="CC" stroke-width="3"/>' for y in (6, 22, 38))))
add("emb_pinces", "Pinces ici (prise par serrage)", EMB, 60, 60, _frame(
    '<rect x="20" y="18" width="20" height="24" fill="CC" stroke="none"/><path d="M17 16 V44 M43 16 V44" stroke="CC" stroke-width="2"/>'
    '<path d="M6 30 H13 M47 30 H54" stroke="CC" stroke-width="3"/><path d="M11 25 L16 30 L11 35 Z M49 25 L44 30 L49 35 Z" fill="CC" stroke="none"/>'))
add("emb_pas_pinces", "Ne pas saisir avec des pinces", EMB, 60, 60, _frame(
    '<rect x="20" y="18" width="20" height="24" fill="CC" stroke="none"/><path d="M6 30 H13 M47 30 H54" stroke="CC" stroke-width="3"/>'
    '<path d="M11 25 L16 30 L11 35 Z M49 25 L44 30 L49 35 Z" fill="CC" stroke="none"/>' + _cross(10, 10, 50, 50)))


def _gerbage(p):
    n = p.get("niveaux", "3")
    return (60, 60, _frame('<path d="M30 6 V14" stroke="CC" stroke-width="3"/><path d="M24 12 L30 18 L36 12 Z" fill="CC" stroke="none"/>'
                           '<rect x="18" y="20" width="24" height="5" fill="CC" stroke="none"/><rect x="18" y="28" width="24" height="22" fill="CC" stroke="none"/>'
                           + _W(t(30, 44, n, 12, "bold"))))


add("emb_gerbage", "Gerbage limité (nombre de niveaux)", EMB, params=[("niveaux", "Niveaux", "3", None)], func=_gerbage)
add("emb_pas_gerber", "Ne pas gerber", EMB, 60, 60, _frame(
    '<rect x="20" y="8" width="20" height="18" fill="none" stroke="CC" stroke-width="2.4"/><path d="M20 8 L40 26 M40 8 L20 26" stroke="CC" stroke-width="2.4"/>'
    '<rect x="18" y="30" width="24" height="22" fill="CC" stroke="none"/>'))
add("emb_temperature", "Limites de température", EMB, 60, 60, _frame(
    '<path d="M27 10 Q27 6 30 6 Q33 6 33 10 V38 A7 7 0 1 1 27 38 Z" fill="none" stroke="CC" stroke-width="2"/>'
    '<circle cx="30" cy="44" r="4" fill="CC" stroke="none"/><path d="M30 44 V22" stroke="CC" stroke-width="2.6"/>'
    '<path d="M12 40 H20 L40 16 H48" stroke="CC" stroke-width="1.8" fill="none"/>'))
add("emb_pas_fourches", "Ne pas prendre avec des fourches", EMB, 60, 60, _frame(
    '<path d="M14 22 V38 H46 M14 30 H46" stroke="CC" stroke-width="2.6" fill="none"/><path d="M10 14 V42" stroke="CC" stroke-width="3"/>' + _cross()))
add("emb_pas_retourner", "Ne pas retourner", EMB, 60, 60, _frame(
    '<rect x="20" y="30" width="20" height="20" fill="CC" stroke="none"/><path d="M14 30 Q14 10 30 10 Q46 10 46 26" stroke="CC" stroke-width="2.6" fill="none" stroke-dasharray="5 3"/>'
    '<path d="M41 24 L46 30 L51 24 Z" fill="CC" stroke="none"/>' + _cross(14, 8, 46, 40)))
add("emb_pas_crochet", "Ne pas utiliser de crochet", EMB, 60, 60, _frame(
    '<path d="M30 8 V30 Q30 44 20 44 Q12 44 12 36" stroke="CC" stroke-width="3.4" fill="none"/><path d="M24 8 H36" stroke="CC" stroke-width="3.4"/>' + _cross()))
add("emb_soin", "Manipuler avec soin", EMB, 60, 60, _frame(
    _box(20, 8, 20, 20, "CC").replace('fill="CC" stroke="#6d4c2d"', 'fill="CC" stroke="#ffffff"').replace('stroke="#6d4c2d" stroke-width="1" fill="none"', 'stroke="#ffffff" stroke-width="1" fill="none"')
    + '<path d="M8 36 Q14 34 18 40 L26 48 M52 36 Q46 34 42 40 L34 48" stroke="CC" stroke-width="3.4" fill="none"/>'))
add("emb_poids", "Poids (masse brute)", EMB, params=[("masse", "Masse", "25 kg", None)],
    func=lambda p: (60, 60, _frame('<path d="M24 16 Q24 10 30 10 Q36 10 36 16" stroke="CC" stroke-width="2.6" fill="none"/>'
                                   '<path d="M16 18 H44 L50 50 H10 Z" fill="CC" stroke="none"/>' + _W(t(30, 40, p["masse"], 8, "bold")))))
add("emb_recyclable", "Recyclable", EMB, 60, 60, _frame(
    "".join(f'<g transform="rotate({a} 30 32)"><path d="M18 40 L26 26 L30 30 L30 20 L21 22 L24 25 L15 39 Z" fill="CC" stroke="none"/></g>' for a in (0, 120, 240))))
add("emb_poubelle", "Jeter dans une poubelle", EMB, 60, 60, _frame(
    '<path d="M14 26 H30 L28 50 H16 Z" fill="none" stroke="CC" stroke-width="2"/><path d="M18 30 V46 M22 30 V46 M26 30 V46" stroke="CC" stroke-width="1"/>'
    '<circle cx="42" cy="12" r="4" fill="CC" stroke="none"/><path d="M42 16 V36 L36 50 M42 36 L48 50 M42 22 L28 22" stroke="CC" stroke-width="3.4" fill="none"/>'))

# ---------------------------------------------------------------- sécurité : signalisation (style ISO 7010) et produits dangereux (SGH)
add("sig_interdit_engins", "Circulation d'engins interdite", SIGN, 60, 60,
    '<circle cx="30" cy="30" r="26" fill="#ffffff" stroke="#d32f2f" stroke-width="5"/>' + _forklift(10, 12, 0.85)
    + '<path d="M12 12 L48 48" stroke="#d32f2f" stroke-width="5"/>')
add("sig_danger_engins", "Danger : circulation d'engins", SIGN, 64, 56,
    '<path d="M32 4 L61 52 H3 Z" fill="#fdd835" stroke="CC" stroke-width="3.4" stroke-linejoin="round"/>' + _forklift(14, 22, 0.75))
add("sig_danger_elec", "Danger électrique", SIGN, 64, 56,
    '<path d="M32 4 L61 52 H3 Z" fill="#fdd835" stroke="CC" stroke-width="3.4" stroke-linejoin="round"/>'
    '<path d="M35 16 L24 36 H32 L27 48 L42 30 H33 Z" fill="CC" stroke="none"/>')
add("sig_danger_general", "Danger général", SIGN, 64, 56,
    '<path d="M32 4 L61 52 H3 Z" fill="#fdd835" stroke="CC" stroke-width="3.4" stroke-linejoin="round"/>'
    '<path d="M32 18 V38" stroke="CC" stroke-width="5"/><circle cx="32" cy="45" r="3" fill="CC" stroke="none"/>')


def _oblig(body):
    return '<circle cx="30" cy="30" r="27" fill="#1565c0" stroke="none"/>' + body


add("sig_chaussures", "Port de chaussures de sécurité obligatoire", SIGN, 60, 60, _oblig(
    '<path d="M16 42 V20 Q16 16 20 16 H28 L30 30 Q40 32 44 36 Q46 38 46 42 Z" fill="#ffffff" stroke="none"/><path d="M16 45 H46" stroke="#ffffff" stroke-width="3"/>'))
add("sig_gants", "Port de gants obligatoire", SIGN, 60, 60, _oblig(
    '<path d="M22 48 V34 L17 26 Q16 23 19 22 L24 30 V16 Q24 13 26.5 13 Q29 13 29 16 V28 V13 Q29 11 31.5 11 Q34 11 34 13 V28 V15 Q34 13 36.5 13 Q39 13 39 15 V30 V20 Q39 18 41 18 Q43 18 43 20 V38 Q43 44 40 48 Z" fill="#ffffff" stroke="none"/>'))
add("sig_casque", "Port du casque obligatoire", SIGN, 60, 60, _oblig(
    '<path d="M14 36 Q14 16 30 16 Q46 16 46 36 Z" fill="#ffffff" stroke="none"/><path d="M10 38 H50" stroke="#ffffff" stroke-width="3.4"/>'))
add("sig_lunettes", "Port de lunettes obligatoire", SIGN, 60, 60, _oblig(
    '<path d="M10 24 H50 V32 Q50 38 44 38 H37 Q33 38 32 33 Q30 30 28 33 Q27 38 23 38 H16 Q10 38 10 32 Z" fill="#ffffff" stroke="none"/>'))


def _ghs(body):
    return ('<path d="M30 3 L57 30 L30 57 L3 30 Z" fill="#ffffff" stroke="#d32f2f" stroke-width="4" stroke-linejoin="miter"/>' + body)


add("ghs_explosif", "Matière explosive (SGH01)", SIGN, 60, 60, _ghs(
    '<circle cx="27" cy="34" r="7" fill="CC" stroke="none"/>'
    + "".join(f'<path d="M{27 + 9 * c:.1f} {34 + 9 * s:.1f} L{27 + 14 * c:.1f} {34 + 14 * s:.1f}" stroke="CC" stroke-width="2"/>' for c, s in ((0, -1), (0.7, -0.7), (1, 0), (-0.7, -0.7), (-1, 0), (0.7, 0.7)))
    + '<rect x="36" y="22" width="4" height="4" fill="CC" stroke="none"/><rect x="18" y="20" width="3" height="3" fill="CC" stroke="none"/>'))
add("ghs_inflammable", "Matière inflammable (SGH02)", SIGN, 60, 60, _ghs(
    '<path d="M30 14 Q38 24 36 32 Q40 30 40 26 Q46 34 42 40 Q38 46 30 46 Q22 46 19 40 Q16 32 24 26 Q24 32 27 33 Q24 22 30 14 Z" fill="CC" stroke="none"/>'
    '<path d="M18 46 H42" stroke="CC" stroke-width="2.4"/>'))
add("ghs_comburant", "Matière comburante (SGH03)", SIGN, 60, 60, _ghs(
    '<circle cx="30" cy="36" r="8" fill="none" stroke="CC" stroke-width="3"/>'
    '<path d="M30 12 Q37 20 35 27 Q38 24 38 22 Q42 28 38 31 M30 12 Q24 20 25 27 Q22 24 22 22 Q18 28 22 31" stroke="CC" stroke-width="2.4" fill="none"/>'
    '<path d="M18 46 H42" stroke="CC" stroke-width="2.4"/>'))
add("ghs_gaz", "Gaz sous pression (SGH04)", SIGN, 60, 60, _ghs(
    '<rect x="17" y="24" width="26" height="12" rx="6" fill="CC" stroke="none" transform="rotate(-20 30 30)"/><rect x="40" y="18" width="5" height="5" fill="CC" stroke="none" transform="rotate(-20 30 30)"/>'))
add("ghs_corrosif", "Matière corrosive (SGH05)", SIGN, 60, 60, _ghs(
    '<path d="M16 18 L24 14 L26 18 L18 22 Z M34 14 L42 18 L40 22 L32 18 Z" fill="CC" stroke="none"/>'
    '<path d="M22 24 V28 M38 24 V29" stroke="CC" stroke-width="1.6"/>'
    '<path d="M14 36 H28 L26 32 H16 Z" fill="CC" stroke="none"/><path d="M33 36 H45 V40 H33 Z" fill="CC" stroke="none"/>'
    '<path d="M18 44 H42" stroke="CC" stroke-width="2.4"/>'))
add("ghs_toxique", "Toxicité aiguë – provoque la mort (SGH06)", SIGN, 60, 60, _ghs(
    '<circle cx="30" cy="25" r="8" fill="CC" stroke="none"/><circle cx="27" cy="24" r="2" fill="#ffffff" stroke="none"/><circle cx="33" cy="24" r="2" fill="#ffffff" stroke="none"/>'
    '<rect x="26" y="31" width="8" height="4" fill="CC" stroke="none"/><path d="M18 34 L42 44 M42 34 L18 44" stroke="CC" stroke-width="3.4"/>'))
add("ghs_nocif", "Nocif / irritant (SGH07)", SIGN, 60, 60, _ghs(
    '<path d="M30 16 V34" stroke="CC" stroke-width="5"/><circle cx="30" cy="41" r="3" fill="CC" stroke="none"/>'))
add("ghs_sante", "Danger pour la santé (SGH08)", SIGN, 60, 60, _ghs(
    '<circle cx="30" cy="20" r="5" fill="CC" stroke="none"/><path d="M22 46 V30 Q22 26 30 26 Q38 26 38 30 V46 Z" fill="CC" stroke="none"/>'
    '<path d="M26 32 L30 36 L34 32 L30 42 Z" fill="#ffffff" stroke="none"/>'))
add("ghs_environnement", "Danger pour l'environnement (SGH09)", SIGN, 60, 60, _ghs(
    '<path d="M18 22 L22 14 L26 22 Z M17 30 L22 20 L27 30 Z" fill="CC" stroke="none"/><path d="M22 30 V36" stroke="CC" stroke-width="2"/>'
    '<path d="M28 42 Q34 36 40 42 Q34 46 28 42 Z M40 42 L44 39 V45 Z" fill="CC" stroke="none"/><path d="M14 36 H32" stroke="CC" stroke-width="1.6"/>'))
add("ghs_infectieux", "Matière infectieuse (risque biologique)", SIGN, 60, 60,
    '<path d="M30 3 L57 30 L30 57 L3 30 Z" fill="#ffffff" stroke="CC" stroke-width="2.4"/>'
    + "".join(f'<g transform="rotate({a} 30 26)"><circle cx="30" cy="19" r="6" fill="none" stroke="CC" stroke-width="2.4"/></g>' for a in (0, 120, 240))
    + '<circle cx="30" cy="26" r="3" fill="none" stroke="CC" stroke-width="1.6"/>' + t(30, 50, "6", 6, "bold"))
add("ghs_radioactif", "Matière radioactive", SIGN, 60, 60,
    '<path d="M30 3 L57 30 L30 57 L3 30 Z" fill="#fdd835" stroke="CC" stroke-width="2.4"/>'
    + "".join(f'<g transform="rotate({a} 30 28)"><path d="M30 28 L24 17 A13 13 0 0 1 36 17 Z" fill="CC" stroke="none"/></g>' for a in (0, 120, 240))
    + '<circle cx="30" cy="28" r="2.6" fill="CC" stroke="none"/><circle cx="30" cy="28" r="4.6" fill="none" stroke="#fdd835" stroke-width="1.6"/>' + t(30, 52, "7", 6, "bold"))

# ---------------------------------------------------------------- logistique : équipements
add("log_chariot", "Chariot élévateur", LOG, 60, 50, _forklift(4, 4, 1.15, "#f9a825").replace('fill="#f9a825" stroke="none">', 'fill="#f9a825" stroke="#5d4300" stroke-width="0.6">'))
add("log_transpalette", "Transpalette manuel", LOG, 70, 50,
    '<path d="M16 4 L18 34" stroke="CC" stroke-width="3"/><path d="M12 4 H22" stroke="CC" stroke-width="3"/>'
    '<rect x="10" y="32" width="14" height="8" rx="2" fill="#e53935" stroke="none"/><path d="M24 40 H66" stroke="CC" stroke-width="4"/>'
    '<circle cx="16" cy="44" r="4" fill="CC" stroke="none"/><circle cx="60" cy="45" r="2.5" fill="CC" stroke="none"/>')
add("log_diable", "Diable (chariot à deux roues)", LOG, 50, 60,
    '<path d="M10 4 L20 46 H36" stroke="CC" stroke-width="3" fill="none"/><path d="M6 6 H14" stroke="CC" stroke-width="3"/>'
    '<circle cx="22" cy="50" r="6" fill="CC" stroke="none"/><circle cx="22" cy="50" r="2" fill="#ffffff" stroke="none"/>' + _box(18, 22, 20, 24))
add("log_table_elev", "Table élévatrice à ciseaux", LOG, 60, 50,
    '<rect x="10" y="8" width="44" height="5" fill="CC" stroke="none"/><path d="M14 13 L48 40 M48 13 L14 40" stroke="CC" stroke-width="2.6"/>'
    '<rect x="8" y="40" width="48" height="4" fill="CC" stroke="none"/><circle cx="12" cy="47" r="3" fill="CC" stroke="none"/><circle cx="52" cy="47" r="3" fill="CC" stroke="none"/>'
    '<path d="M6 30 V18" stroke="CC" stroke-width="2"/>')
add("log_convoyeur", "Convoyeur à rouleaux", LOG, 80, 40,
    _box(12, 2, 16, 18) + _box(40, 4, 20, 16) + '<rect x="4" y="22" width="72" height="5" fill="#90a4ae" stroke="CC" stroke-width="1"/>'
    + "".join(f'<circle cx="{8 + i * 8}" cy="31" r="3" fill="CC" stroke="none"/>' for i in range(9)) + '<path d="M8 34 V39 M72 34 V39" stroke="CC" stroke-width="2"/>')
add("log_camion", "Camion semi-remorque", LOG, 100, 50,
    '<rect x="4" y="8" width="64" height="28" fill="#eceff1" stroke="CC" stroke-width="1.4"/>'
    '<path d="M70 18 H86 L94 28 V36 H70 Z" fill="#1976d2" stroke="CC" stroke-width="1.2"/><path d="M74 20 H84 L89 27 H74 Z" fill="#bbdefb" stroke="none"/>'
    + "".join(f'<circle cx="{x}" cy="40" r="5" fill="CC" stroke="none"/><circle cx="{x}" cy="40" r="1.8" fill="#ffffff" stroke="none"/>' for x in (14, 26, 52, 78, 88)))
add("log_entrepot", "Entrepôt", LOG, 70, 50,
    '<path d="M4 18 L35 4 L66 18 V46 H4 Z" fill="#eceff1" stroke="CC" stroke-width="1.4"/>'
    '<rect x="18" y="24" width="34" height="22" fill="#90a4ae" stroke="CC" stroke-width="1"/>'
    + "".join(f'<path d="M18 {27 + i * 3} H52" stroke="#eceff1" stroke-width="0.8"/>' for i in range(6)))
add("log_rayonnage", "Rayonnage à palettes", LOG, 70, 60,
    '<path d="M4 4 V56 M66 4 V56 M4 28 H66 M4 54 H66" stroke="#1565c0" stroke-width="2.6"/>' + _box(10, 8, 18, 18) + _box(40, 8, 18, 18) + _box(24, 34, 18, 18))
add("log_palette", "Palette chargée", LOG, 60, 50,
    _box(10, 2, 20, 18) + _box(30, 2, 20, 18) + _box(20, 14, 20, 18)
    + '<rect x="6" y="36" width="48" height="4" fill="#bf8040" stroke="#6d4c2d" stroke-width="0.8"/><rect x="6" y="44" width="48" height="3" fill="#bf8040" stroke="#6d4c2d" stroke-width="0.8"/>'
    '<rect x="8" y="40" width="6" height="4" fill="#8d6e63" stroke="none"/><rect x="27" y="40" width="6" height="4" fill="#8d6e63" stroke="none"/><rect x="46" y="40" width="6" height="4" fill="#8d6e63" stroke="none"/>')
add("log_colis", "Colis (carton)", LOG, 50, 50, _box(5, 5, 40, 40))
add("log_scanner", "Scanner de codes-barres", LOG, 60, 50,
    '<path d="M6 10 H34 L40 18 H26 L22 46 H12 L16 18 H6 Z" fill="#424242" stroke="CC" stroke-width="1"/><path d="M40 14 L58 6 M40 16 L58 26" stroke="#e53935" stroke-width="1.2"/>'
    + "".join(f'<path d="M{46 + i * 2} 30 V44" stroke="CC" stroke-width="{1.4 if i % 3 else 0.6}"/>' for i in range(6)))
add("log_balance", "Balance de pesée (plateforme)", LOG, 60, 60,
    '<circle cx="44" cy="14" r="10" fill="#ffffff" stroke="CC" stroke-width="1.6"/><path d="M44 14 L50 9" stroke="#e53935" stroke-width="1.4"/>'
    '<path d="M44 24 V48" stroke="CC" stroke-width="3"/><rect x="4" y="46" width="48" height="6" fill="#90a4ae" stroke="CC" stroke-width="1"/>' + _box(10, 26, 20, 20))
add("log_grue", "Levage par crochet (conteneur)", LOG, 60, 60,
    '<rect x="26" y="2" width="8" height="10" fill="#fdd835" stroke="CC" stroke-width="1"/><path d="M30 12 V18 Q30 24 25 22" stroke="CC" stroke-width="2.4" fill="none"/>'
    '<path d="M30 20 L10 34 M30 20 L50 34" stroke="CC" stroke-width="1.4"/><rect x="8" y="34" width="44" height="22" fill="#e65100" stroke="CC" stroke-width="1"/>'
    + "".join(f'<path d="M{12 + i * 5} 37 V53" stroke="#bf360c" stroke-width="1.2"/>' for i in range(8)))
add("log_bon", "Bon de livraison / liste de contrôle", LOG, 50, 60,
    '<rect x="6" y="6" width="38" height="50" rx="2" fill="#ffffff" stroke="CC" stroke-width="1.6"/><rect x="18" y="2" width="14" height="7" rx="2" fill="#9e9e9e" stroke="none"/>'
    + "".join(f'<path d="M12 {18 + i * 8} l2 2 l4 -4" stroke="#43a047" stroke-width="1.4" fill="none"/><path d="M22 {17 + i * 8} H38" stroke="CC" stroke-width="1"/>' for i in range(4)))
add("log_code_barres", "Étiquette code-barres", LOG, 60, 40,
    '<rect x="3" y="3" width="54" height="34" rx="2" fill="#ffffff" stroke="CC" stroke-width="1.2"/>'
    + "".join(f'<rect x="{8 + i * 2.2:.1f}" y="8" width="{1.4 if i % 4 else 0.7}" height="20" fill="CC" stroke="none"/>' for i in range(20))
    + t(30, 34, "3 760 123 456 789", 4.5))

# ---------------------------------------------------------------- prothésiste dentaire
_DT = 'fill="#ffffff" stroke="CC" stroke-width="1.6"'
add("dent_incisive", "Dent incisive", DENT, 40, 60,
    f'<path d="M10 6 H30 Q32 18 28 26 L24 54 Q20 58 16 54 L12 26 Q8 18 10 6 Z" {_DT}/><path d="M12 26 H28" stroke="#ef9a9a" stroke-width="1.2"/>')
add("dent_molaire", "Dent molaire (racines)", DENT, 50, 60,
    f'<path d="M6 12 Q6 4 14 6 Q20 2 25 6 Q30 2 36 6 Q44 4 44 12 Q46 24 40 28 L38 52 Q34 56 32 50 L28 34 Q25 32 22 34 L18 50 Q16 56 12 52 L10 28 Q4 24 6 12 Z" {_DT}/>'
    '<path d="M10 28 H40" stroke="#ef9a9a" stroke-width="1.2"/>')
add("dent_couronne", "Couronne prothétique", DENT, 50, 40,
    '<path d="M6 30 Q4 10 14 8 Q20 4 25 8 Q30 4 36 8 Q46 10 44 30 Z" fill="#fff8e1" stroke="CC" stroke-width="1.6"/>'
    '<path d="M12 30 Q12 22 25 22 Q38 22 38 30" stroke="#bdbdbd" stroke-width="1.2" fill="none"/><path d="M6 30 H44" stroke="#ffb300" stroke-width="2"/>')
add("dent_bridge", "Bridge 3 éléments", DENT, 90, 50,
    "".join(f'<path d="M{x} 30 Q{x - 2} 10 {x + 8} 8 Q{x + 14} 4 {x + 19} 8 Q{x + 24} 4 {x + 30} 8 Q{x + 40} 10 {x + 38} 30 Z" fill="#fff8e1" stroke="CC" stroke-width="1.4"/>' for x in (4, 30, 56))
    + '<path d="M8 40 L12 32 M78 40 L82 32" stroke="CC" stroke-width="1"/><path d="M6 32 Q8 46 16 46 Q22 46 24 32 M66 32 Q68 46 76 46 Q82 46 84 32" fill="#ffffff" stroke="CC" stroke-width="1.4"/>'
    + t(45, 44, "pontique", 5))
add("dent_implant", "Implant dentaire (vis, pilier, couronne)", DENT, 40, 70,
    '<path d="M6 20 Q4 4 14 4 Q20 2 26 4 Q36 4 34 20 Z" fill="#fff8e1" stroke="CC" stroke-width="1.4"/>'
    '<rect x="14" y="20" width="12" height="8" fill="#b0bec5" stroke="CC" stroke-width="1"/>'
    '<path d="M13 28 H27 L24 64 H16 Z" fill="#90a4ae" stroke="CC" stroke-width="1"/>'
    + "".join(f'<path d="M14 {32 + i * 6} L26 {35 + i * 6}" stroke="#455a64" stroke-width="1.2"/>' for i in range(5)))
add("dent_ortho", "Appareil orthodontique (bagues et arc)", DENT, 80, 40,
    "".join(f'<rect x="{6 + i * 12}" y="8" width="10" height="24" rx="4" fill="#ffffff" stroke="CC" stroke-width="1.2"/><rect x="{8 + i * 12}" y="16" width="6" height="6" fill="#90a4ae" stroke="none"/>' for i in range(6))
    + '<path d="M4 19 H78" stroke="#607d8b" stroke-width="1.4"/>')
add("dent_articulateur", "Articulateur dentaire", DENT, 60, 60,
    '<rect x="8" y="50" width="44" height="6" fill="#90a4ae" stroke="CC" stroke-width="1"/><path d="M44 50 V12 H14" stroke="#607d8b" stroke-width="3" fill="none"/>'
    '<path d="M44 30 H18" stroke="#607d8b" stroke-width="2.4"/><circle cx="44" cy="30" r="3" fill="#455a64" stroke="none"/>'
    '<path d="M14 14 H30 V22 H14 Z M18 32 H34 V40 H18 Z" fill="#f48fb1" stroke="CC" stroke-width="0.8"/><path d="M20 40 V50" stroke="#607d8b" stroke-width="2"/>')
add("dent_porte_empreinte", "Porte-empreinte", DENT, 70, 40,
    '<path d="M6 20 Q6 4 30 4 Q54 4 54 20 Q54 34 30 34 Q6 34 6 20 Z" fill="#cfd8dc" stroke="CC" stroke-width="1.4"/>'
    '<path d="M14 20 Q14 12 30 12 Q46 12 46 20 Q46 26 30 26 Q14 26 14 20 Z" fill="#fff59d" stroke="CC" stroke-width="0.8"/><path d="M54 20 H68" stroke="CC" stroke-width="4"/>')
add("dent_modele", "Modèle en plâtre", DENT, 60, 50,
    '<path d="M6 30 Q6 8 30 8 Q54 8 54 30 V44 H6 Z" fill="#eeeeee" stroke="CC" stroke-width="1.2"/>'
    + "".join(f'<rect x="{11 + i * 5}" y="{16 - (3 if 2 < i < 6 else 0)}" width="4.4" height="8" rx="2" fill="#ffffff" stroke="CC" stroke-width="0.6"/>' for i in range(8)))
add("dent_piece_main", "Pièce à main / micromoteur", DENT, 80, 30,
    '<path d="M4 15 L10 13 V17 Z" fill="#9e9e9e" stroke="none"/><rect x="10" y="10" width="12" height="10" rx="2" fill="#b0bec5" stroke="CC" stroke-width="1"/>'
    '<rect x="22" y="9" width="36" height="12" rx="5" fill="#cfd8dc" stroke="CC" stroke-width="1"/><path d="M58 15 Q68 15 78 22" stroke="#616161" stroke-width="3" fill="none"/>')
add("dent_fraise", "Fraise dentaire", DENT, 20, 60,
    '<rect x="8" y="4" width="4" height="34" fill="#bdbdbd" stroke="CC" stroke-width="0.8"/><path d="M6 38 H14 L12 54 Q10 58 8 54 Z" fill="#ffd54f" stroke="CC" stroke-width="1"/>'
    + "".join(f'<path d="M7 {41 + i * 4} L13 {43 + i * 4}" stroke="#8d6e00" stroke-width="0.8"/>' for i in range(3)))
add("dent_miroir", "Miroir dentaire", DENT, 20, 70,
    '<circle cx="10" cy="10" r="7" fill="#e3f2fd" stroke="CC" stroke-width="1.4"/><path d="M10 17 V66" stroke="#9e9e9e" stroke-width="2.4"/>')
add("dent_sonde", "Sonde dentaire", DENT, 20, 70,
    '<path d="M10 66 V20 Q10 8 4 6" stroke="#9e9e9e" stroke-width="2" fill="none"/><path d="M8 40 V62" stroke="#757575" stroke-width="4.4"/>')
add("dent_brosse", "Brosse à dents", DENT, 80, 30,
    '<path d="M4 18 H52" stroke="#42a5f5" stroke-width="5" stroke-linecap="round"/><rect x="52" y="14" width="22" height="7" rx="2" fill="#42a5f5" stroke="none"/>'
    + "".join(f'<path d="M{55 + i * 3} 14 V4" stroke="#90caf9" stroke-width="1.6"/>' for i in range(7)))
add("dent_fauteuil", "Fauteuil dentaire (unit)", DENT, 80, 60,
    '<path d="M10 10 Q8 4 14 4 L22 6 Q26 8 24 14 L22 30 H52 Q58 30 60 36 L62 40 H20 Q14 40 14 34 Z" fill="#26a69a" stroke="CC" stroke-width="1.2"/>'
    '<path d="M36 40 V52 M24 54 H48" stroke="#607d8b" stroke-width="4"/><path d="M66 6 V30 M56 8 H76" stroke="#607d8b" stroke-width="2"/>'
    '<circle cx="56" cy="12" r="5" fill="#fff59d" stroke="CC" stroke-width="1"/><rect x="62" y="30" width="12" height="4" fill="#90a4ae" stroke="none"/>')
add("dent_dentifrice", "Tube de dentifrice", DENT, 80, 30,
    '<path d="M4 6 H50 L60 11 V19 L50 24 H4 Q2 15 4 6 Z" fill="#e3f2fd" stroke="CC" stroke-width="1.2"/><rect x="60" y="10" width="8" height="10" fill="#1565c0" stroke="none"/>'
    '<path d="M4 10 H48 M4 20 H48" stroke="#e53935" stroke-width="1.6"/><path d="M68 15 Q74 10 78 15" stroke="#ffffff" stroke-width="4" fill="none"/><path d="M68 15 Q74 10 78 15" stroke="#4fc3f7" stroke-width="1.4" fill="none"/>')
add("dent_technicien", "Prothésiste au travail (poste de laboratoire)", DENT, 80, 60,
    '<circle cx="24" cy="14" r="7" fill="CC" stroke="none"/><path d="M14 46 V30 Q14 24 24 24 Q32 24 36 30 L46 36" stroke="CC" stroke-width="6" fill="none" stroke-linecap="round"/>'
    '<rect x="4" y="44" width="72" height="5" fill="#8d6e63" stroke="CC" stroke-width="0.8"/><path d="M10 49 V58 M70 49 V58" stroke="CC" stroke-width="2"/>'
    '<path d="M52 44 Q52 36 60 36 Q68 36 68 44 Z" fill="#ffffff" stroke="CC" stroke-width="1"/><path d="M46 36 L54 30" stroke="#9e9e9e" stroke-width="2"/>'
    '<path d="M60 10 V24 M54 24 H66" stroke="#607d8b" stroke-width="2"/><path d="M52 24 L60 32 L68 24 Z" fill="#fff59d" stroke="none" opacity="0.6"/>')
add("dent_radio", "Radiographie dentaire", DENT, 60, 50,
    '<rect x="4" y="4" width="52" height="42" rx="3" fill="#263238" stroke="CC" stroke-width="1"/>'
    '<path d="M18 12 Q18 8 24 9 Q30 6 36 9 Q42 8 42 12 Q44 20 40 22 L38 40 Q35 42 34 38 L32 28 Q30 26 28 28 L26 38 Q25 42 22 40 L20 22 Q16 20 18 12 Z" fill="#cfd8dc" stroke="none"/>')

# ---------------------------------------------------------------- outils
def _pince(jaws, col="#e53935"):
    return ('<path d="M30 30 L8 56" stroke="' + col + '" stroke-width="6" stroke-linecap="round"/><path d="M30 30 L52 56" stroke="' + col + '" stroke-width="6" stroke-linecap="round"/>'
            '<circle cx="30" cy="30" r="4" fill="#757575" stroke="CC" stroke-width="0.8"/>' + jaws)


add("oel_metre", "Mètre ruban", OEL, 70, 50,
    '<rect x="4" y="6" width="38" height="38" rx="8" fill="#fdd835" stroke="CC" stroke-width="1.4"/><circle cx="23" cy="25" r="9" fill="#424242" stroke="none"/>'
    '<rect x="42" y="36" width="24" height="6" fill="#fff59d" stroke="CC" stroke-width="0.8"/>' + "".join(f'<path d="M{45 + i * 4} 36 V{39 if i % 2 else 40}" stroke="CC" stroke-width="0.6"/>' for i in range(6))
    + '<path d="M66 34 V44" stroke="CC" stroke-width="1.6"/>')
add("oel_niveau", "Niveau à bulle", OEL, 90, 20,
    '<rect x="4" y="4" width="82" height="12" rx="1.5" fill="#fdd835" stroke="CC" stroke-width="1.2"/><rect x="38" y="6" width="14" height="8" rx="3" fill="#c5e1a5" stroke="CC" stroke-width="0.8"/>'
    '<circle cx="45" cy="10" r="2.4" fill="#ffffff" stroke="none"/><path d="M41 6 V14 M49 6 V14" stroke="CC" stroke-width="0.6"/>')
add("oel_perceuse", "Perceuse-visseuse sans fil", OEL, 70, 60,
    '<path d="M10 8 H48 Q54 8 54 14 V20 Q54 24 48 24 H34 L30 46 H18 L22 24 H10 Q6 24 6 18 V14 Q6 8 10 8 Z" fill="#43a047" stroke="CC" stroke-width="1.2"/>'
    '<rect x="14" y="46" width="22" height="10" rx="2" fill="#263238" stroke="none"/><rect x="54" y="12" width="8" height="8" fill="#424242" stroke="none"/>'
    '<path d="M62 16 H70" stroke="#9e9e9e" stroke-width="2"/>')
add("oel_tire_fil", "Tire-fil (aiguille)", OEL, 80, 50,
    '<circle cx="22" cy="25" r="18" fill="#263238" stroke="CC" stroke-width="1"/><circle cx="22" cy="25" r="10" fill="#ffffff" stroke="none"/>'
    '<path d="M38 18 Q60 6 76 14" stroke="#455a64" stroke-width="2.4" fill="none"/><circle cx="76" cy="14" r="2" fill="#9e9e9e" stroke="none"/>')
add("omec_cle_plate", "Clé plate", OMEC, 90, 30,
    '<path d="M18 15 H72" stroke="#9e9e9e" stroke-width="7" stroke-linecap="round"/>'
    '<path d="M4 9 L10 4 H20 L24 10 L18 12 V18 L24 20 L20 26 H10 L4 21 Z" fill="#9e9e9e" stroke="CC" stroke-width="1"/>'
    '<path d="M86 9 L80 4 H70 L66 10 L72 12 V18 L66 20 L70 26 H80 L86 21 Z" fill="#9e9e9e" stroke="CC" stroke-width="1"/>' + t(45, 18, "13", 5, "bold"))
add("omec_cle_mixte", "Clé mixte (plate et polygonale)", OMEC, 90, 30,
    '<path d="M18 15 H72" stroke="#9e9e9e" stroke-width="7" stroke-linecap="round"/>'
    '<path d="M4 9 L10 4 H20 L24 10 L18 12 V18 L24 20 L20 26 H10 L4 21 Z" fill="#9e9e9e" stroke="CC" stroke-width="1"/>'
    '<circle cx="76" cy="15" r="10" fill="#9e9e9e" stroke="CC" stroke-width="1"/><circle cx="76" cy="15" r="5" fill="#ffffff" stroke="CC" stroke-width="0.8"/>')
add("omec_cle_molette", "Clé à molette", OMEC, 90, 40,
    '<path d="M26 22 H84" stroke="#9e9e9e" stroke-width="8" stroke-linecap="round"/>'
    '<path d="M4 8 Q4 4 10 4 H22 Q28 4 28 12 V30 Q28 36 22 36 H14 V28 H20 V14 H8 Z" fill="#9e9e9e" stroke="CC" stroke-width="1"/>'
    '<circle cx="30" cy="22" r="4" fill="#757575" stroke="CC" stroke-width="0.8"/><circle cx="80" cy="22" r="2" fill="#ffffff" stroke="none"/>')
add("omec_cliquet", "Clé à cliquet et douille", OMEC, 90, 40,
    '<path d="M24 20 H84" stroke="#757575" stroke-width="7" stroke-linecap="round"/><circle cx="18" cy="20" r="10" fill="#9e9e9e" stroke="CC" stroke-width="1"/>'
    '<rect x="10" y="26" width="16" height="12" rx="2" fill="#bdbdbd" stroke="CC" stroke-width="1"/><path d="M14 30 L18 34 L22 30" stroke="CC" stroke-width="0.8" fill="none"/>')
add("omec_allen", "Clé Allen (six pans mâle)", OMEC, 50, 60,
    '<path d="M12 6 V44 Q12 52 20 52 H44" stroke="#424242" stroke-width="5" fill="none" stroke-linejoin="round"/>')
add("omec_marteau", "Marteau", OMEC, 70, 60,
    '<rect x="8" y="6" width="40" height="14" rx="2" fill="#757575" stroke="CC" stroke-width="1"/><path d="M8 6 L2 9 V17 L8 20" fill="#9e9e9e" stroke="CC" stroke-width="1"/>'
    '<rect x="30" y="20" width="8" height="38" rx="3" fill="#bf8040" stroke="CC" stroke-width="1"/>')
add("omec_maillet", "Maillet", OMEC, 70, 60,
    '<rect x="10" y="4" width="40" height="18" rx="6" fill="#e53935" stroke="CC" stroke-width="1"/><rect x="26" y="22" width="8" height="36" rx="3" fill="#bf8040" stroke="CC" stroke-width="1"/>')
add("omec_pince_etau", "Pince-étau", OMEC, 90, 40,
    '<path d="M4 16 L18 10 L26 18 L10 22 Z M4 24 L18 30 L26 22 L10 18 Z" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>'
    '<path d="M26 18 H80" stroke="#757575" stroke-width="6" stroke-linecap="round"/><path d="M26 22 Q50 34 76 28" stroke="#9e9e9e" stroke-width="4" fill="none"/>'
    '<circle cx="84" cy="18" r="4" fill="#424242" stroke="none"/>')
add("omec_scie", "Scie à métaux", OMEC, 90, 40,
    '<path d="M18 30 V8 H80 V30" stroke="#1565c0" stroke-width="3" fill="none"/><path d="M18 28 H80" stroke="#9e9e9e" stroke-width="2"/>'
    + "".join(f'<path d="M{20 + i * 4} 29 l2 2" stroke="#757575" stroke-width="0.6"/>' for i in range(15))
    + '<path d="M18 22 L6 36" stroke="#212121" stroke-width="6" stroke-linecap="round"/>')
add("omec_lime", "Lime", OMEC, 90, 20,
    '<rect x="4" y="5" width="24" height="10" rx="4" fill="#bf8040" stroke="CC" stroke-width="1"/><path d="M28 6 H80 L86 10 L80 14 H28 Z" fill="#9e9e9e" stroke="CC" stroke-width="1"/>'
    + "".join(f'<path d="M{32 + i * 4} 6 l3 8" stroke="#616161" stroke-width="0.5"/>' for i in range(12)))
add("omec_pied_coulisse", "Pied à coulisse", OMEC, 100, 50,
    '<rect x="4" y="14" width="92" height="8" fill="#cfd8dc" stroke="CC" stroke-width="1"/>' + "".join(f'<path d="M{16 + i * 4} 14 V{17 if i % 5 else 19}" stroke="CC" stroke-width="0.6"/>' for i in range(20))
    + '<path d="M4 4 V46 L10 40 V22" fill="#b0bec5" stroke="CC" stroke-width="1"/><path d="M30 10 H44 V22 H40 V46 L34 40 V22 H30 Z" fill="#b0bec5" stroke="CC" stroke-width="1"/>')
add("omec_dynamometrique", "Clé dynamométrique", OMEC, 100, 30,
    '<circle cx="12" cy="15" r="9" fill="#9e9e9e" stroke="CC" stroke-width="1"/><path d="M20 15 H92" stroke="#757575" stroke-width="7" stroke-linecap="round"/>'
    '<rect x="56" y="10" width="26" height="10" rx="2" fill="#1565c0" stroke="none"/>' + _W(t(69, 17.5, "50 N·m", 4.6, "bold")))
add("omec_etau", "Étau d'établi", OMEC, 80, 50,
    '<rect x="6" y="38" width="60" height="6" fill="#90a4ae" stroke="CC" stroke-width="1"/><rect x="10" y="14" width="18" height="24" fill="#1565c0" stroke="CC" stroke-width="1"/>'
    '<rect x="40" y="14" width="18" height="24" fill="#1565c0" stroke="CC" stroke-width="1"/><path d="M28 26 H40" stroke="#757575" stroke-width="3"/>'
    '<path d="M58 26 H74 M74 18 V34" stroke="#424242" stroke-width="3"/><path d="M10 14 H28 M40 14 H58" stroke="#9e9e9e" stroke-width="3"/>')
add("oinf_pince_rj45", "Pince à sertir RJ45", OINF, 80, 60,
    '<path d="M10 10 L50 6 Q58 6 58 14 L56 24 L12 26 Q6 26 6 20 V14 Q6 10 10 10 Z" fill="#424242" stroke="CC" stroke-width="1"/>'
    '<rect x="40" y="10" width="12" height="9" rx="1" fill="#90a4ae" stroke="none"/><rect x="26" y="11" width="10" height="7" rx="1" fill="#90a4ae" stroke="none"/>'
    '<path d="M54 22 L76 44 M14 26 L60 52" stroke="#e53935" stroke-width="6" stroke-linecap="round"/><circle cx="54" cy="22" r="3" fill="#9e9e9e" stroke="none"/>')
add("oinf_rj45", "Connecteur RJ45 (embout 8P8C)", OINF, 60, 40,
    '<path d="M4 10 H40 V30 H4 Z" fill="#e3f2fd" fill-opacity="0.8" stroke="CC" stroke-width="1.4"/>'
    + "".join(f'<rect x="{8 + i * 4}" y="12" width="2" height="7" fill="#ffb300" stroke="none"/>' for i in range(8))
    + '<path d="M14 30 L18 36 H30" stroke="CC" stroke-width="1.4" fill="none"/>'
    + '<path d="M40 20 H58" stroke="#1565c0" stroke-width="7"/>'
    + "".join(f'<path d="M24 {21 + i * 1.1:.1f} H40" stroke="{c}" stroke-width="0.9"/>' for i, c in enumerate(("#ff9800", "#ffffff", "#43a047", "#1e88e5", "#ffffff", "#795548", "#ffffff", "#ff9800"))))
add("oinf_testeur", "Testeur de câble réseau", OINF, 80, 50,
    '<rect x="4" y="6" width="34" height="40" rx="4" fill="#1565c0" stroke="CC" stroke-width="1"/>'
    + "".join(f'<circle cx="{11 + i * 3.3:.1f}" cy="14" r="1.2" fill="#76ff03" stroke="none"/>' for i in range(8))
    + '<rect x="12" y="34" width="18" height="10" fill="#e3f2fd" stroke="CC" stroke-width="0.8"/>'
    '<rect x="50" y="18" width="24" height="26" rx="3" fill="#1565c0" stroke="CC" stroke-width="1"/><rect x="54" y="34" width="16" height="8" fill="#e3f2fd" stroke="CC" stroke-width="0.6"/>'
    + _W(t(21, 28, "LAN", 6, "bold")))
add("oinf_insertion", "Outil d'insertion (punch-down)", OINF, 90, 20,
    '<rect x="4" y="4" width="44" height="12" rx="5" fill="#fdd835" stroke="CC" stroke-width="1"/><rect x="48" y="6" width="12" height="8" fill="#424242" stroke="none"/>'
    '<path d="M60 10 H80" stroke="#9e9e9e" stroke-width="3"/><path d="M80 7 V13 H86 Z" fill="#757575" stroke="none"/>')
add("oinf_denudeur", "Dénude-câble rotatif", OINF, 50, 40,
    '<path d="M6 20 Q6 6 24 6 H40 Q46 6 46 14 V26 Q46 34 40 34 H24 Q6 34 6 20 Z" fill="#7cb342" stroke="CC" stroke-width="1.2"/>'
    '<circle cx="24" cy="20" r="6" fill="#ffffff" stroke="CC" stroke-width="1"/><path d="M0 20 H48" stroke="#1565c0" stroke-width="2.4"/>')
add("oinf_precision", "Tournevis de précision", OINF, 80, 20,
    '<rect x="4" y="5" width="34" height="10" rx="3" fill="#546e7a" stroke="CC" stroke-width="1"/>' + "".join(f'<path d="M{8 + i * 4} 5 V15" stroke="#37474f" stroke-width="0.8"/>' for i in range(6))
    + '<circle cx="6" cy="10" r="3" fill="#90a4ae" stroke="none"/><path d="M38 10 H72" stroke="#9e9e9e" stroke-width="1.6"/><path d="M72 9 H76 V11 H72 Z" fill="#757575" stroke="none"/>')
add("oinf_bracelet", "Bracelet antistatique", OINF, 70, 50,
    '<ellipse cx="20" cy="24" rx="14" ry="18" fill="none" stroke="#1565c0" stroke-width="5"/><rect x="30" y="18" width="10" height="12" rx="2" fill="#9e9e9e" stroke="CC" stroke-width="0.8"/>'
    '<path d="M40 24 Q50 24 52 30 Q54 36 60 36 Q66 36 66 42" stroke="#212121" stroke-width="1.6" fill="none"/><path d="M62 44 L70 48 L66 40 Z" fill="#2e9b3a" stroke="none"/>')
add("oinf_cable", "Câble réseau RJ45", OINF, 90, 30,
    '<rect x="2" y="9" width="14" height="12" rx="1" fill="#e3f2fd" stroke="CC" stroke-width="1"/><rect x="74" y="9" width="14" height="12" rx="1" fill="#e3f2fd" stroke="CC" stroke-width="1"/>'
    '<path d="M16 15 Q30 4 45 15 T74 15" stroke="#1565c0" stroke-width="4" fill="none"/>' + t(45, 28, "Cat. 6", 5))
add("oinf_cle_usb", "Clé USB", OINF, 60, 24,
    '<rect x="4" y="5" width="36" height="14" rx="3" fill="#424242" stroke="CC" stroke-width="1"/><rect x="40" y="7" width="14" height="10" fill="#cfd8dc" stroke="CC" stroke-width="0.8"/>'
    '<rect x="44" y="9" width="3" height="2" fill="CC" stroke="none"/><rect x="49" y="9" width="3" height="2" fill="CC" stroke="none"/>')

# ================================================================ v1.2.1 : travail en hauteur, outils isolés, prothèses, schéma dentaire
HAUT = "Travail en hauteur – échafaudage, nacelles"
_RED, _YEL, _ALU = "#d32f2f", "#fdd835", "#b0bec5"


def _arch_pts(theta_max, n, cx, y0, w, h, up=False):
    """Points d'une arcade dentaire (demi-ellipse) : (x, y, angle de la tangente, normale extérieure)."""
    out = []
    for i in range(n):
        th = math.radians(-theta_max + 2 * theta_max * i / (n - 1))
        x = cx + w * math.sin(th)
        y = y0 + h * (1 - math.cos(th)) if not up else y0 - h * (1 - math.cos(th))
        tx, ty = w * math.cos(th), (h * math.sin(th)) * (1 if not up else -1)
        nx, ny = h * math.sin(th), (-w * math.cos(th)) * (1 if not up else -1)
        L = math.hypot(nx, ny) or 1
        out.append((x, y, math.degrees(math.atan2(ty, tx)), nx / L, ny / L))
    return out


def _at(th_deg, cx, y0, w, h, up=False):
    th = math.radians(th_deg)
    x = cx + w * math.sin(th)
    y = y0 + h * (1 - math.cos(th)) if not up else y0 - h * (1 - math.cos(th))
    tx, ty = w * math.cos(th), (h * math.sin(th)) * (1 if not up else -1)
    nx, ny = h * math.sin(th), (-w * math.cos(th)) * (1 if not up else -1)
    L = math.hypot(nx, ny) or 1
    return x, y, math.degrees(math.atan2(ty, tx)), nx / L, ny / L


def _tooth(x, y, ang, size, molar, fill="#fbf3dc"):
    rx, ry = size / 2, size * (0.46 if molar else 0.36)
    s = (f'<g transform="translate({x:.2f} {y:.2f}) rotate({ang:.1f})">'
         f'<rect x="{-rx:.2f}" y="{-ry:.2f}" width="{2 * rx:.2f}" height="{2 * ry:.2f}" rx="{ry * 0.8:.2f}" fill="{fill}" stroke="CC" stroke-width="0.9"/>')
    if molar:
        s += f'<path d="M{-rx * 0.55:.2f} 0 H{rx * 0.55:.2f} M0 {-ry * 0.55:.2f} V{ry * 0.55:.2f}" stroke="#a1887f" stroke-width="0.6"/>'
    return s + '</g>'


_SIZES = [7.0, 6.4, 7.0, 7.6, 7.6, 11.0, 10.4, 9.6]      # 1 incisive centrale … 8 dent de sagesse


def _fdi(up):
    cx, w, h = 50, 33, 52
    y0 = 14 if not up else 84
    dth = 92 / 8
    body = ""
    q_left, q_right = (1, 2) if not up else (4, 3)
    for side, quad in ((-1, q_left), (1, q_right)):
        for k in range(1, 9):
            x, y, a, nx, ny = _at(side * (k - 0.5) * dth, cx, y0, w, h, up)
            body += _tooth(x, y, a, _SIZES[k - 1], k >= 6)
            body += t(x + nx * 11.5, y + ny * 11.5 + 2.4, f"{quad}{k}", 6.2, "bold")
    lab = "Maxillaire" if not up else "Mandibule"
    body += t(50, 52 if not up else 50, lab, 6.5)
    return body


add("dent_fdi_sup", "Schéma dentaire – mâchoire supérieure (numérotation FDI 11 à 28)", "Prothésiste dentaire", 100, 90, _fdi(False))
add("dent_fdi_inf", "Schéma dentaire – mâchoire inférieure (numérotation FDI 31 à 48)", "Prothésiste dentaire", 100, 90, _fdi(True))


def _band(pts, width, col="#f48fb1"):
    d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y, *_ in pts)
    return (f'<path d="{d}" stroke="CC" stroke-width="{width + 2.2}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path d="{d}" stroke="{col}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def _prothese_complete():
    cx, y0, w, h = 50, 14, 33, 50
    arch = _arch_pts(95, 60, cx, y0, w, h)
    o, f = _band(arch, 15)
    pal = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y, *_ in _arch_pts(95, 40, cx, y0 + 6, w - 7, h - 6)) + " Z"
    body = o + f + f'<path d="{pal}" fill="#f8bbd0" stroke="#ec407a" stroke-width="0.6"/>'
    body += '<path d="M40 40 Q50 36 60 40 M38 48 Q50 44 62 48 M39 56 Q50 52 61 56" stroke="#ec407a" stroke-width="0.6" fill="none"/>'
    dth = 90 / 7
    for side in (-1, 1):
        for k in range(1, 8):
            x, y, a, nx, ny = _at(side * (k - 0.5) * dth, cx, y0, w, h)
            body += _tooth(x + nx * 1.5, y + ny * 1.5, a, _SIZES[k - 1] * 0.95, k >= 6)
    return body


def _prothese_partielle():
    cx, y0, w, h = 50, 80, 32, 54
    full = _arch_pts(96, 60, cx, y0, w, h, up=True)
    arms_l = [p for p in full if p[0] < cx - 20]
    arms_r = [p for p in full if p[0] > cx + 20]
    o1, f1 = _band(full, 8)
    o2, f2 = _band(arms_l, 17)
    o3, f3 = _band(arms_r, 17)
    body = o1 + o2 + o3 + f1 + f2 + f3
    # festons du bord intérieur (barre linguale)
    for th in range(-36, 40, 9):
        x, y, a, nx, ny = _at(th, cx, y0, w, h, up=True)
        body += f'<circle cx="{x - nx * 4.2:.2f}" cy="{y - ny * 4.2:.2f}" r="2.2" fill="#f48fb1" stroke="CC" stroke-width="0.7"/>'
    body = o1 + o2 + o3 + body[len(o1 + o2 + o3):]
    dth = 92 / 8
    for side in (-1, 1):
        for k in (4, 5, 6, 7):
            x, y, a, nx, ny = _at(side * (k - 0.5) * dth, cx, y0, w, h, up=True)
            body += _tooth(x, y, a, _SIZES[k - 1] * 1.2, k >= 6, "#f3e3b8")
        # crochet métallique (stellite) autour de la dent naturelle voisine
        x, y, a, nx, ny = _at(side * 2.7 * dth, cx, y0, w, h, up=True)
        body += (f'<path d="M{x - nx * 3:.2f} {y - ny * 3:.2f} C{x + nx * 9 - ny * 7:.2f} {y + ny * 9 + nx * 7:.2f} '
                 f'{x + nx * 9 + ny * 7:.2f} {y + ny * 9 - nx * 7:.2f} {x + nx * 2 + ny * 5:.2f} {y + ny * 2 - nx * 5:.2f}" '
                 'stroke="#546e7a" stroke-width="2" fill="none" stroke-linecap="round"/>')
    return body


add("dent_prothese", "Prothèse complète amovible (maxillaire, vue de dessus)", "Prothésiste dentaire", 100, 80, _prothese_complete())
add("dent_partielle", "Prothèse partielle amovible avec crochets", "Prothésiste dentaire", 100, 90, _prothese_partielle())
add("dent_brosse_elec", "Brosse à dents électrique", "Prothésiste dentaire", 30, 90,
    '<rect x="8" y="34" width="14" height="52" rx="6" fill="#eceff1" stroke="CC" stroke-width="1.2"/><circle cx="15" cy="52" r="3" fill="#42a5f5" stroke="none"/>'
    '<path d="M12 34 L13 12 H17 L18 34 Z" fill="#eceff1" stroke="CC" stroke-width="1"/><ellipse cx="15" cy="9" rx="5" ry="6" fill="#ffffff" stroke="CC" stroke-width="1"/>'
    + "".join(f'<path d="M{11 + i * 2} 6 V12" stroke="#64b5f6" stroke-width="1"/>' for i in range(5)))
add("dent_fil", "Fil dentaire", "Prothésiste dentaire", 60, 50,
    '<rect x="6" y="14" width="30" height="30" rx="5" fill="#80deea" stroke="CC" stroke-width="1.2"/><rect x="6" y="8" width="30" height="9" rx="3" fill="#ffffff" stroke="CC" stroke-width="1"/>'
    '<path d="M34 12 Q46 6 56 16" stroke="#9e9e9e" stroke-width="1" fill="none"/>')

# ---------------------------------------------------------------- casque d'électricien (vue de trois quarts)
_casque = (
    # visière (écran facial) relevée sur les pivots, devant et sous la visière du casque
    '<path d="M8 33 L9 49 Q10 55 18 55.5 L44 55 Q51 54.5 52 48 L53 35 C38 39 22 38 8 33 Z" fill="#81d4fa" fill-opacity="0.45" stroke="#0277bd" stroke-width="1.3"/>'
    '<path d="M15 39 L16 51 M21 40 L22 52" stroke="#ffffff" stroke-width="1.8" stroke-opacity="0.85"/>'
    '<path d="M9 49 Q10 55 18 55.5 L44 55 Q51 54.5 52 48" stroke="#01579b" stroke-width="2" fill="none"/>'
    # coque
    '<path d="M13 31 C12 15 25 5 40 5 C55 5 65 15 64 29 C56 34 26 35 13 31 Z" fill="#fafafa" stroke="CC" stroke-width="1.5"/>'
    '<path d="M20 12 C30 4 50 4 61 17" stroke="#cfd8dc" stroke-width="3" fill="none" stroke-linecap="round"/>'
    '<path d="M27 8 C34 14 37 24 36 33" stroke="#cfd8dc" stroke-width="1.2" fill="none"/>'
    # rebord / petite visière avant
    '<path d="M4 31 C10 36 30 39 50 37 C58 36 64 33 66 29 C62 31 56 33 48 33.5 C30 35 14 33 8 29 Z" fill="#eceff1" stroke="CC" stroke-width="1.3"/>'
    # support d'écran et pivot latéral
    '<path d="M9 32 C22 37 40 38 53 34" stroke="#37474f" stroke-width="2.4" fill="none"/>'
    '<circle cx="54" cy="34" r="3.6" fill="#37474f" stroke="CC" stroke-width="0.8"/><circle cx="54" cy="34" r="1.3" fill="#b0bec5" stroke="none"/>'
    # pastille isolant électrique (double triangle)
    '<path d="M44 14 L50 24 H38 Z" fill="#fdd835" stroke="CC" stroke-width="0.8"/><path d="M45 16 L41.5 21 H44.5 L43 24 L47.5 18.5 H44.5 Z" fill="CC" stroke="none"/>')
add("epi_casque", "Casque d'électricien avec écran facial (EPI)", "Prévention électrique – EPI, EIS, ECS", 70, 60, _casque)

# ---------------------------------------------------------------- outils isolés 1000 V
def _tv_iso(tip):
    return ('<path d="M4 6 Q2 10 4 14 H30 L34 15.5 H40 V4.5 H34 L30 6 Z" fill="' + _RED + '" stroke="CC" stroke-width="1"/>'
            '<path d="M8 6.5 V13.5 M13 6.5 V13.5 M18 6.5 V13.5 M23 6.5 V13.5" stroke="#b71c1c" stroke-width="1"/>'
            '<path d="M34 4 H43 Q45 10 43 16 H34 Z" fill="' + _YEL + '" stroke="CC" stroke-width="1"/>'
            '<rect x="43" y="8" width="42" height="4" rx="1.5" fill="' + _RED + '" stroke="CC" stroke-width="0.6"/>'
            + tip + '<path d="M24 1 L27 5 H21 Z M28 1 L31 5 H25 Z" fill="' + _YEL + '" stroke="CC" stroke-width="0.4"/>')


_TIPS = {"plat": '<path d="M85 8.6 H93 L96 9 V11 L93 11.4 H85 Z" fill="#9e9e9e" stroke="CC" stroke-width="0.6"/>',
         "cruci": '<path d="M85 8.6 H92 L97 10 L92 11.4 H85 Z" fill="#9e9e9e" stroke="CC" stroke-width="0.6"/><path d="M90 10 H97" stroke="#616161" stroke-width="0.6"/>'}
add("oel_tournevis_plat", "Tournevis plat isolé 1000 V", "Outils – électricien", 100, 20, _tv_iso(_TIPS["plat"]))
add("oel_tournevis_cruci", "Tournevis cruciforme isolé 1000 V", "Outils – électricien", 100, 20, _tv_iso(_TIPS["cruci"]))


def _pince_iso(jaws, extra=""):
    h = ""
    for d in ("M22 40 Q17 62 11 86", "M28 40 Q33 62 39 86"):
        h += f'<path d="{d}" stroke="CC" stroke-width="10.4" fill="none" stroke-linecap="round"/>'
    for d in ("M22 40 Q17 62 11 86", "M28 40 Q33 62 39 86"):
        h += f'<path d="{d}" stroke="{_RED}" stroke-width="8" fill="none" stroke-linecap="round"/>'
    for d in ("M22.5 40 L20.6 49", "M27.5 40 L29.4 49"):
        h += f'<path d="{d}" stroke="CC" stroke-width="12.4" fill="none" stroke-linecap="round"/><path d="{d}" stroke="{_YEL}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    return (extra + h + jaws + '<circle cx="25" cy="37" r="4.4" fill="#78909c" stroke="CC" stroke-width="0.9"/>'
            '<circle cx="25" cy="37" r="1.5" fill="#cfd8dc" stroke="none"/>'
            '<path d="M5 74 L8 79 H2 Z" fill="' + _YEL + '" stroke="CC" stroke-width="0.4"/>')


_JG = 'fill="#9e9e9e" stroke="CC" stroke-width="0.9"'
add("oel_pince_coupante", "Pince coupante diagonale isolée", "Outils – électricien", 50, 90, _pince_iso(
    f'<path d="M25 40 C15 34 14 18 21 7 L25.6 10 C23 20 24 30 25 40 Z" {_JG}/>'
    f'<path d="M25 40 C35 34 36 18 29 7 L24.4 10 C27 20 26 30 25 40 Z" {_JG}/>'
    '<path d="M25 11 V33" stroke="#eeeeee" stroke-width="0.8"/>'))
add("oel_pince_bec", "Pince à bec demi-rond isolée", "Outils – électricien", 50, 90, _pince_iso(
    f'<path d="M25 40 L18 31 L22.6 3 Q24 1 25 1 V40 Z" {_JG}/><path d="M25 40 L32 31 L27.4 3 Q26 1 25 1 V40 Z" {_JG}/>'
    '<path d="M23.5 8 H26.5 M23.3 13 H26.7 M23 18 H27" stroke="#616161" stroke-width="0.6"/>'))
add("oel_pince_univ", "Pince universelle isolée", "Outils – électricien", 50, 90, _pince_iso(
    f'<path d="M25 40 L16 30 L17 9 Q18 6 25 6 V40 Z" {_JG}/><path d="M25 40 L34 30 L33 9 Q32 6 25 6 V40 Z" {_JG}/>'
    '<path d="M20 11 H30 M20 15 H30 M20 19 H30" stroke="#616161" stroke-width="0.7"/><path d="M22 25 Q25 28 28 25" stroke="#eeeeee" stroke-width="1" fill="none"/>'))
add("oel_pince_denuder", "Pince à dénuder isolée (à vis de réglage)", "Outils – électricien", 50, 90, _pince_iso(
    f'<path d="M25 40 L17 30 L19 8 H24 L25 13 Z" {_JG}/><path d="M25 40 L33 30 L31 8 H26 L25 13 Z" {_JG}/>'
    '<circle cx="25" cy="12" r="1.4" fill="#ffffff" stroke="none"/>',
    '<path d="M16 58 H34" stroke="#616161" stroke-width="1.6"/><rect x="31" y="55" width="6" height="6" rx="1" fill="#424242" stroke="none"/>'))
add("oel_pince_sertir", "Pince à sertir les cosses isolée", "Outils – électricien", 50, 90, _pince_iso(
    f'<path d="M25 40 L17 31 L18 6 H25 Z" {_JG}/><path d="M25 40 L33 31 L32 6 H25 Z" {_JG}/>'
    '<circle cx="25" cy="12" r="2" fill="#e53935" stroke="CC" stroke-width="0.4"/><circle cx="25" cy="19" r="2" fill="#1e88e5" stroke="CC" stroke-width="0.4"/>'
    '<circle cx="25" cy="26" r="2" fill="#fdd835" stroke="CC" stroke-width="0.4"/>'))
add("oel_couteau", "Couteau d'électricien", "Outils – électricien", 90, 20,
    '<path d="M4 7 Q4 4 8 4 H40 Q44 4 44 8 V12 Q44 16 40 16 H8 Q4 16 4 13 Z" fill="#8d6e63" stroke="CC" stroke-width="1"/>'
    '<path d="M8 8 Q20 6 40 9 M8 12 Q22 14 40 11" stroke="#6d4c41" stroke-width="0.6" fill="none"/>'
    '<rect x="40" y="6" width="5" height="8" fill="#bdbdbd" stroke="CC" stroke-width="0.6"/>'
    '<path d="M45 7 H74 Q84 8 87 12 L45 13 Z" fill="#e0e0e0" stroke="CC" stroke-width="1"/><path d="M48 9 H72" stroke="#ffffff" stroke-width="0.8"/>')
add("oel_testeur", "Tournevis testeur de phase", "Outils – électricien", 90, 20,
    '<path d="M4 6 H40 L44 8 V12 L40 14 H4 Q2 10 4 6 Z" fill="#fff59d" fill-opacity="0.85" stroke="CC" stroke-width="1"/>'
    '<rect x="14" y="8" width="12" height="4" rx="2" fill="#ff7043" stroke="none"/><path d="M6 4 H30" stroke="#616161" stroke-width="1.4"/>'
    '<path d="M44 10 H82" stroke="#9e9e9e" stroke-width="2"/><path d="M82 9 H87 V11 H82 Z" fill="#757575" stroke="none"/>')
add("oel_couronne", "Couronne de câble", "Outils – électricien", 70, 50,
    "".join(f'<ellipse cx="35" cy="26" rx="{30 - i * 2.2:.1f}" ry="{15 - i * 1.1:.1f}" fill="none" stroke="CC" stroke-width="2"/>' for i in range(5))
    + '<ellipse cx="35" cy="26" rx="18" ry="9" fill="#ffffff" stroke="CC" stroke-width="1.2"/>'
    '<path d="M60 22 Q66 14 68 8 M8 32 Q2 38 3 44" stroke="CC" stroke-width="2" fill="none"/>')
add("oel_ruban", "Ruban adhésif isolant", "Outils – électricien", 60, 50,
    '<path d="M8 18 V32 A20 10 0 0 0 48 32 V18" fill="#1565c0" stroke="CC" stroke-width="1.2"/>'
    '<ellipse cx="28" cy="18" rx="20" ry="10" fill="#1e88e5" stroke="CC" stroke-width="1.2"/><ellipse cx="28" cy="18" rx="9" ry="4.5" fill="#ffffff" stroke="CC" stroke-width="1"/>'
    '<path d="M48 28 L58 38 L56 46 L45 34 Z" fill="#1e88e5" stroke="CC" stroke-width="1"/>')
add("oel_ampoule", "Ampoule LED (culot E27)", "Outils – électricien", 40, 60,
    '<path d="M20 4 C8 4 3 13 5 22 C7 30 12 32 13 38 H27 C28 32 33 30 35 22 C37 13 32 4 20 4 Z" fill="#fff9c4" stroke="CC" stroke-width="1.3"/>'
    '<path d="M15 28 V22 Q20 16 25 22 V28" stroke="#ffb300" stroke-width="1.2" fill="none"/>'
    '<path d="M13 38 H27 V50 Q20 55 13 50 Z" fill="#bdbdbd" stroke="CC" stroke-width="1"/><path d="M13 42 H27 M13 46 H27" stroke="#757575" stroke-width="1"/>'
    '<path d="M18 54 H22 V57 H18 Z" fill="#424242" stroke="none"/>')
add("oel_fluo", "Lampe fluocompacte", "Outils – électricien", 40, 70,
    '<path d="M12 40 V8 Q12 3 16 3 Q20 3 20 8 V40 M20 40 V8 Q20 3 24 3 Q28 3 28 8 V40" stroke="CC" stroke-width="6.4" fill="none"/>'
    '<path d="M12 40 V8 Q12 3 16 3 Q20 3 20 8 V40 M20 40 V8 Q20 3 24 3 Q28 3 28 8 V40" stroke="#ffffff" stroke-width="4" fill="none"/>'
    '<path d="M8 40 H32 L30 52 H10 Z" fill="#eceff1" stroke="CC" stroke-width="1.2"/>'
    '<path d="M12 52 H28 V62 Q20 67 12 62 Z" fill="#bdbdbd" stroke="CC" stroke-width="1"/><path d="M12 56 H28" stroke="#757575" stroke-width="1"/>')
add("oel_malette", "Malette d'outils isolés 1000 V", "Outils – électricien", 80, 60,
    '<path d="M28 12 V6 H52 V12" stroke="CC" stroke-width="3" fill="none"/><rect x="4" y="12" width="72" height="44" rx="4" fill="#e53935" stroke="CC" stroke-width="1.4"/>'
    '<rect x="4" y="22" width="72" height="4" fill="#b71c1c" stroke="none"/><rect x="34" y="20" width="12" height="8" rx="1.5" fill="#fdd835" stroke="CC" stroke-width="0.8"/>'
    '<path d="M40 34 L50 50 H30 Z" fill="#fdd835" stroke="CC" stroke-width="1"/><path d="M41 37 L37 44 H40.5 L38.5 49 L44 41.5 H40.5 Z" fill="CC" stroke="none"/>'
    + _W(t(18, 48, "1000 V", 6, "bold")))

# ---------------------------------------------------------------- travail en hauteur
_SC = "#90a4ae"
add("haut_echafaudage", "Échafaudage roulant (2 niveaux)", HAUT, 80, 110,
    # montants arrière (profondeur)
    '<path d="M20 4 V94 M76 4 V94" stroke="#cfd8dc" stroke-width="2.4"/>'
    '<path d="M12 10 L20 4 M68 10 L76 4 M12 50 L20 44 M68 50 L76 44 M12 92 L20 86 M68 92 L76 86" stroke="#cfd8dc" stroke-width="1.6"/>'
    # montants avant, lisses, diagonales
    f'<path d="M12 10 V100 M68 10 V100" stroke="{_SC}" stroke-width="3.4"/>'
    f'<path d="M12 10 H68 M12 24 H68 M12 66 H68 M12 92 H68" stroke="{_SC}" stroke-width="2"/>'
    f'<path d="M12 92 L68 52 M12 50 L68 26" stroke="{_SC}" stroke-width="1.6"/>'
    # planchers et plinthes
    '<rect x="10" y="48" width="60" height="5" fill="#a1887f" stroke="CC" stroke-width="0.8"/><rect x="10" y="88" width="60" height="5" fill="#a1887f" stroke="CC" stroke-width="0.8"/>'
    '<rect x="12" y="42" width="56" height="6" fill="#ffca28" stroke="CC" stroke-width="0.6"/>'
    # roues
    '<circle cx="12" cy="104" r="4.5" fill="#37474f" stroke="none"/><circle cx="68" cy="104" r="4.5" fill="#37474f" stroke="none"/>'
    '<path d="M12 100 V104 M68 100 V104" stroke="#37474f" stroke-width="2"/>')
add("haut_pirl", "Plateforme individuelle roulante (PIRL)", HAUT, 70, 90,
    f'<path d="M14 8 V44 M56 8 V44 M14 8 H56 M14 24 H56 M34 8 V44" stroke="{_ALU}" stroke-width="2.6" fill="none"/>'
    '<rect x="10" y="44" width="50" height="5" fill="#cfd8dc" stroke="CC" stroke-width="1"/>'
    '<path d="M12 49 L6 86 M58 49 L62 82 M24 49 L20 86" stroke="#1565c0" stroke-width="3.2"/>'
    '<path d="M9 66 H22 M7.5 76 H21" stroke="#9e9e9e" stroke-width="3"/>'
    '<rect x="3" y="85" width="8" height="3" fill="#ff5722" stroke="none"/><rect x="17" y="85" width="8" height="3" fill="#ff5722" stroke="none"/>'
    '<circle cx="62" cy="84" r="4.5" fill="#37474f" stroke="none"/><circle cx="62" cy="84" r="1.6" fill="#cfd8dc" stroke="none"/>')
add("haut_escabeau", "Escabeau", HAUT, 50, 90,
    '<path d="M16 4 L4 86 M22 4 L40 86 M16 4 H24" stroke="#90a4ae" stroke-width="3.4" fill="none"/>'
    + "".join(f'<path d="M{16 - i * 1.95:.1f} {16 + i * 14} H{22 + i * 2.85:.1f}" stroke="#78909c" stroke-width="2.6"/>' for i in range(5))
    + '<rect x="12" y="2" width="14" height="5" fill="#ff7043" stroke="CC" stroke-width="0.6"/>'
    '<path d="M2 86 H8 M37 86 H43" stroke="#212121" stroke-width="3"/>')
add("haut_echelle", "Échelle", HAUT, 30, 90,
    '<path d="M6 2 V88 M24 2 V88" stroke="#90a4ae" stroke-width="3"/>'
    + "".join(f'<path d="M6 {8 + i * 10} H24" stroke="#78909c" stroke-width="2.2"/>' for i in range(8)))


def _wheels(*xs, y=0, r=5):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#263238" stroke="none"/><circle cx="{x}" cy="{y}" r="{r * 0.4:.1f}" fill="#b0bec5" stroke="none"/>' for x in xs)


def _panier(x, y):
    return (f'<rect x="{x}" y="{y}" width="14" height="10" fill="#ffffff" stroke="CC" stroke-width="1.2"/>'
            f'<path d="M{x} {y + 4} H{x + 14} M{x + 7} {y} V{y + 10}" stroke="CC" stroke-width="0.6"/>')


_JN = "#f9a825"
add("haut_nacelle_ciseaux", "Nacelle à ciseaux", HAUT, 70, 90,
    '<rect x="8" y="6" width="54" height="12" fill="none" stroke="CC" stroke-width="1.6"/><path d="M8 12 H62 M22 6 V18 M35 6 V18 M48 6 V18" stroke="CC" stroke-width="0.8"/>'
    '<rect x="6" y="18" width="58" height="4" fill="#546e7a" stroke="CC" stroke-width="0.8"/>'
    + "".join(f'<path d="M12 {22 + i * 14} L58 {36 + i * 14} M58 {22 + i * 14} L12 {36 + i * 14}" stroke="{_JN}" stroke-width="3" stroke-linecap="round"/>' for i in range(3))
    + '<rect x="6" y="64" width="58" height="12" rx="2" fill="' + _JN + '" stroke="CC" stroke-width="1"/>' + _wheels(16, 54, y=80))
add("haut_nacelle_articulee", "Nacelle articulée automotrice", HAUT, 110, 70,
    '<rect x="8" y="48" width="56" height="10" rx="3" fill="' + _JN + '" stroke="CC" stroke-width="1"/>'
    '<path d="M24 48 V38 H46 V48 Z" fill="#455a64" stroke="CC" stroke-width="0.8"/>' + _wheels(18, 54, y=60, r=6)
    + f'<path d="M40 40 L58 20 L82 30" stroke="{_JN}" stroke-width="5" fill="none" stroke-linejoin="round"/><path d="M82 30 L94 14" stroke="{_JN}" stroke-width="3.4"/>'
    + _panier(88, 4))
add("haut_nacelle_telescopique", "Nacelle télescopique automotrice", HAUT, 110, 70,
    '<rect x="8" y="48" width="56" height="10" rx="3" fill="' + _JN + '" stroke="CC" stroke-width="1"/>'
    '<path d="M22 48 V38 H44 V48 Z" fill="#455a64" stroke="CC" stroke-width="0.8"/>' + _wheels(18, 54, y=60, r=6)
    + f'<path d="M34 40 L92 12" stroke="{_JN}" stroke-width="6" stroke-linecap="round"/><path d="M60 27 L92 12" stroke="#fbc02d" stroke-width="3.6"/>'
    + _panier(90, 2))
add("haut_nacelle_mat", "Nacelle à mât vertical", HAUT, 60, 90,
    '<rect x="6" y="66" width="38" height="12" rx="3" fill="' + _JN + '" stroke="CC" stroke-width="1"/>' + _wheels(14, 38, y=80)
    + f'<rect x="20" y="22" width="8" height="44" fill="#eceff1" stroke="CC" stroke-width="1"/><path d="M24 22 L40 14" stroke="{_JN}" stroke-width="3.4"/>'
    + _panier(38, 6).replace('width="14"', 'width="16"'))
add("haut_nacelle_camion", "Camion nacelle", HAUT, 120, 70,
    '<rect x="6" y="40" width="74" height="10" fill="#eceff1" stroke="CC" stroke-width="1"/>'
    '<path d="M80 50 V30 H98 L108 40 V50 Z" fill="#eceff1" stroke="CC" stroke-width="1"/><path d="M84 33 H96 L102 40 H84 Z" fill="#b3e5fc" stroke="none"/>'
    + _wheels(20, 34, 96, y=54, r=6)
    + '<path d="M10 50 L4 62 M70 50 L76 62 M1 62 H8 M73 62 H80" stroke="#455a64" stroke-width="2.4"/>'
    + f'<rect x="12" y="34" width="12" height="6" fill="#455a64" stroke="none"/><path d="M18 34 L52 14 L36 6" stroke="{_JN}" stroke-width="4" fill="none" stroke-linejoin="round"/>'
    + _panier(22, 0))
add("haut_nacelle_remorque", "Nacelle sur remorque", HAUT, 120, 60,
    '<rect x="20" y="38" width="60" height="6" fill="' + _JN + '" stroke="CC" stroke-width="1"/><path d="M20 41 H4 L2 44" stroke="CC" stroke-width="2" fill="none"/>'
    + _wheels(50, y=48, r=6)
    + '<path d="M24 44 L14 56 M76 44 L86 56 M10 56 H18 M82 56 H90" stroke="#455a64" stroke-width="2.4"/>'
    + f'<rect x="58" y="30" width="10" height="8" fill="#455a64" stroke="none"/><path d="M63 30 L86 20 L104 14" stroke="{_JN}" stroke-width="3.6" fill="none"/>'
    + _panier(100, 2))
add("sig_harnais", "Port du harnais antichute obligatoire", "Sécurité – signalisation et produits dangereux", 60, 60,
    '<circle cx="30" cy="30" r="27" fill="#1565c0" stroke="none"/><circle cx="30" cy="13" r="4.5" fill="#ffffff" stroke="none"/>'
    '<path d="M24 20 H36 V36 H33 V48 H27 V36 H24 Z" fill="#ffffff" stroke="none"/>'
    '<path d="M25 20 L35 34 M35 20 L25 34 M24 36 H36 M27 36 L30 42 L33 36" stroke="#1565c0" stroke-width="1.6" fill="none"/>'
    '<path d="M30 27 Q36 18 42 12" stroke="#ffffff" stroke-width="1.6" fill="none" stroke-dasharray="2 1.4"/><circle cx="43.5" cy="10.5" r="2.6" fill="none" stroke="#ffffff" stroke-width="1.6"/>')
add("sig_chute", "Danger : chute avec dénivellation", "Sécurité – signalisation et produits dangereux", 64, 56,
    '<path d="M32 4 L61 52 H3 Z" fill="#fdd835" stroke="CC" stroke-width="3.4" stroke-linejoin="round"/>'
    '<path d="M14 44 H30 V36 H48" stroke="CC" stroke-width="2.4" fill="none"/><circle cx="38" cy="22" r="2.6" fill="CC" stroke="none"/>'
    '<path d="M36 25 L32 31 L26 30 M32 31 L36 35 M34 27 L40 28" stroke="CC" stroke-width="2.2" fill="none" stroke-linecap="round"/>')


def _reorder(cat, ids):
    pos = [i for i, s in enumerate(SYMBOLS) if s.cat == cat]
    items = [SYMBOLS[i] for i in pos]
    rank = {k: n for n, k in enumerate(ids)}
    items.sort(key=lambda s: (rank.get(s.id, len(ids)), pos[items.index(s)] if False else 0))
    first = [s for s in items if s.id in rank]
    rest = [SYMBOLS[i] for i in pos if SYMBOLS[i].id not in rank]
    for i, s in zip(pos, first + rest):
        SYMBOLS[i] = s


_reorder("Outils – électricien", ["oel_malette", "oel_tournevis_plat", "oel_tournevis_cruci", "oel_testeur", "oel_pince_coupante",
                                  "oel_pince_bec", "oel_pince_univ", "oel_pince_denuder", "oel_pince_sertir", "oel_couteau"])
_reorder("Prévention électrique – EPI, EIS, ECS", ["epi_casque"])
_reorder("Prothésiste dentaire", ["dent_fdi_sup", "dent_fdi_inf", "dent_incisive", "dent_molaire", "dent_couronne", "dent_bridge",
                                  "dent_implant", "dent_prothese", "dent_partielle"])

# ---------------------------------------------------------------- bibliothèques 1.3.0 (module séparé)
from . import symbols_v130  # noqa: E402,F401
from . import symbols_soins  # noqa: E402,F401
from . import symbols_v132  # noqa: E402,F401

# ---------------------------------------------------------------- repères et tailles par défaut
DEFAULT_LABELS = {
    "km_puissance": "KM1", "km_complet": "KM1", "sect_fus": "Q1", "disj_moteur": "Q1", "rt_puissance": "F1",
    "moteur3": "M1", "bobine_km": "KM1", "bobine": "KA1", "contact_am_1314": "KM1", "contact_no_2324": "KM1",
    "contact_nf_6162": "KM2", "contact_nf_5152": "KM2", "contact_f_9596": "F1", "contact_f_9798": "F1",
    "au": "S0", "bp_no": "S1", "bp_nf": "S0", "voyant_marche": "H1", "transfo_cmd": "T1", "bornier": "X1", "bornier_10": "X1", "rst_ssid": "SSID_Eleves (VLAN 10)", "rst_vlan": "VLAN 10 : postes élèves", "borne_seule": "X1.1", "km_uni": "KM1",
    "pia_1": "Q1", "pia_fn": "Q1", "pia_2": "Q1", "pia_3": "Q1", "pia_4": "Q1", "id_2": "Q1", "id_4": "Q1",
    "dd_2": "Q1", "dd_4": "Q1", "ccpf_1": "F1", "ccpf_pn": "F1", "ccpf_2": "F1", "ccpf_3": "F1", "ccpf_4pc": "Q1",
    "bobine_tl": "KA1", "contact_tl": "KA1", "contact_tl2": "KA1", "bobine_mn": "KA2", "contact_mn": "KA2",
    "vv_dom": "S1", "va_et_vient": "S1", "verin_se": "1A", "verin_de": "1A", "verin_de_amorti": "1A",
    "verin_de_dt": "1A", "d52_mono_ev": "1V1", "d52_bi_ev": "1V1", "d53_cf": "1V1", "d32_ev": "1V1",
    "d32_bp": "1S1", "d32_galet": "1S2", "d32_au": "0S1", "frl": "0Z1", "limiteur_debit": "1V2", "inter_dom": "S1", "bp_dom": "S1", "lampe_dom": "E1", "lampe": "H1",
    "pv_module": "PV1", "pv_chaine": "PV1", "pv_onduleur": "U1", "pv_regulateur": "U1", "pv_batterie": "G1",
    "pv_fusible": "F1", "pv_sect_dc": "Q1", "pv_parafoudre": "F2", "pv_shunt": "R1", "pv_compteur": "P1", "pvt_ccpf2": "F1", "src_ge": "G2", "src_eolienne": "G3", "src_alternateur": "G4",
}
DEFAULT_SCALES = {"conv_fibre": 1.5, "chassis_conv": 1.5, "switch_poe": 1.5, "camera_bullet": 1.5,
                  "nvr": 1.5, "poste_supervision": 2.0, "moniteur": 1.5, "camera_dome": 1.5, "plaque_bornes": 2.0, "plaque_etoile": 2.0, "plaque_triangle": 2.0, "barrette": 2.0,
                  "barrette_etoile": 2.0, "multimetre": 1.6, "oscilloscope": 1.6, "gbf": 1.6, "alim_stab": 1.6,
                  "pile9v": 1.4, "pile15": 1.4, "pile45": 1.4,
                  "pvt_panneau": 1.0, "pvt_regulateur": 1.0, "pvt_batterie": 1.0, "pvt_onduleur": 1.0}
for _x in SYMBOLS:
    _x.default_label = DEFAULT_LABELS.get(_x.id, "")
    _x.default_scale = DEFAULT_SCALES.get(_x.id, 1.0)

# ---------------------------------------------------------------- bornes de connexion par défaut
AUTO_PINS = {
    "npn": [(0, 20), (30, 0), (30, 40)], "pnp": [(0, 20), (30, 0), (30, 40)],
    "jonction": [(10, 10)], "borne": [(10, 10)], "masse": [(10, 0)], "terre": [(10, 0)],
    "phase_neutre": [(10, 20)], "entree": [(40, 10)], "sortie": [(0, 10)],
    "inter_manuel": [(0, 10), (40, 10)], "contact_tempo": [(0, 10), (40, 10)],
}
for _s in SYMBOLS:
    if _s.pins:
        continue
    if _s.id in AUTO_PINS:
        _s.pins = AUTO_PINS[_s.id]
    elif _s.cat == L:
        _s.pins = [(0, 20), (40, 20)] if _s.id.startswith("non") else \
            ([(0, 10), (0, 30), (40, 20)] if _s.h == 40 else [])
    elif _s.cat == E and _s.h == 20 and _s.w == 40:
        _s.pins = [(0, 10), (40, 10)]
    elif _s.cat in (P,) or _s.kind == "real":
        _s.pins = []      # plans : on accroche les liaisons au centre (voir items.py)
_s = None

BY_ID = {s.id: s for s in SYMBOLS}
