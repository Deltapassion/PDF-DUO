"""Formes avec texte : GRAFCET, algorigramme, carte mentale.

Ces éléments (type « node ») ont un texte modifiable (double-clic), un remplissage,
et des bornes sur leurs côtés pour y accrocher des liaisons.
"""
MM = 72 / 25.4

G = "GRAFCET"
ALG = "Algorigramme"
MAP = "Carte mentale"


class Preset:
    def __init__(self, pid, name, cat, d):
        self.id, self.name, self.cat, self.d = pid, name, cat, d


PRESETS = []


def add(pid, name, cat, **d):
    d.setdefault("type", "node")
    d.setdefault("size", 9)
    d.setdefault("sw", 1.0)
    d.setdefault("color", "#000000")
    PRESETS.append(Preset(pid, name, cat, d))


S10 = 10 * MM
# GRAFCET (NF EN 60848)
add("g_step_init", "Étape initiale", G, shape="step_init", w=S10, h=S10, text="0", size=11)
add("g_step", "Étape", G, shape="step", w=S10, h=S10, text="1", size=11)
add("g_step_cond", "Étape avec condition (trait en haut)", G, shape="step_cond", w=S10, h=S10, text="2", size=11,
    cond="condition")
add("g_transition", "Transition + réceptivité", G, shape="transition", w=S10, h=8 * MM, text="a", size=9, label="")
add("g_action", "Action associée", G, shape="action", w=40 * MM, h=S10, text="Action", size=9, qual="")
add("g_action_s", "Action mémorisée (S / R)", G, shape="action", w=40 * MM, h=S10, text="KM1", size=9, qual="S")
add("g_action_d", "Action retardée (D)", G, shape="action", w=40 * MM, h=S10, text="KM1", size=9, qual="D=3s")
add("g_action_c", "Action conditionnelle (C)", G, shape="action", w=40 * MM, h=S10, text="KM1", size=9, qual="C")
add("g_and_bar", "Divergence / convergence en ET", G, shape="and_bar", w=50 * MM, h=0.9 * MM, text="")
add("g_or_bar", "Divergence / convergence en OU", G, shape="or_bar", w=50 * MM, h=0.5 * MM, text="")
add("g_macro", "Macro-étape", G, shape="macro", w=S10, h=S10, text="M1", size=10)
add("g_renvoi", "Renvoi vers étape", G, shape="renvoi", w=12 * MM, h=6 * MM, text="1", size=9)
add("g_comment", "Commentaire", G, shape="note", w=35 * MM, h=8 * MM, text="Commentaire", size=8,
    fill="#fff8c4")

# Algorigramme (organigramme de programmation)
add("a_debut", "Début / Fin", ALG, shape="terminal", w=30 * MM, h=10 * MM, text="Début", size=10)
add("a_trait", "Traitement", ALG, shape="rect", w=35 * MM, h=12 * MM, text="Traitement", size=10)
add("a_test", "Test (condition)", ALG, shape="diamond", w=35 * MM, h=18 * MM, text="Condition ?", size=10)
add("a_es", "Entrée / sortie", ALG, shape="para", w=35 * MM, h=12 * MM, text="Lire / Afficher", size=10)
add("a_sp", "Sous-programme", ALG, shape="subprog", w=35 * MM, h=12 * MM, text="Sous-programme", size=10)
add("a_conn", "Connecteur", ALG, shape="ellipse", w=8 * MM, h=8 * MM, text="A", size=10)
add("a_boucle", "Boucle (préparation)", ALG, shape="hex", w=35 * MM, h=12 * MM, text="Pour i de 1 à 10", size=9)

# Carte mentale
add("m_centre", "Idée centrale", MAP, shape="ellipse", w=50 * MM, h=24 * MM, text="Sujet", size=14, bold=True,
    fill="#ffcc80", sw=1.5)
add("m_branche", "Branche", MAP, shape="round", w=35 * MM, h=12 * MM, text="Idée", size=11, bold=True,
    fill="#9fd3ff")
add("m_branche2", "Branche (verte)", MAP, shape="round", w=35 * MM, h=12 * MM, text="Idée", size=11, bold=True,
    fill="#a5f3a1")
add("m_branche3", "Branche (rose)", MAP, shape="round", w=35 * MM, h=12 * MM, text="Idée", size=11, bold=True,
    fill="#ffb3d9")
add("m_sous", "Sous-idée", MAP, shape="round", w=30 * MM, h=9 * MM, text="Détail", size=9)
add("m_note", "Note", MAP, shape="note", w=35 * MM, h=14 * MM, text="Note", size=9, fill="#fff8c4")
add("m_cadre", "Cadre / zone", MAP, shape="rect", w=60 * MM, h=40 * MM, text="", size=9, dash="dash")

NETW = "Réseau informatique"
add("n_zone", "Zone (cadre pointillé avec titre)", NETW, shape="zone", w=90 * MM, h=50 * MM, text="Salle de supervision",
    size=9, bold=True, dash="dash", sw=0.8)
add("n_label", "Étiquette de câble / repère", NETW, shape="rect", w=30 * MM, h=7 * MM, text="Fibre multimode 1 km", size=7,
    fill="#ffffff", sw=0.5)
add("n_note", "Légende (texte encadré)", NETW, shape="round", w=40 * MM, h=12 * MM, text="Légende", size=8, fill="#eef6fb", sw=0.6)

BY_ID = {p.id: p for p in PRESETS}
CATEGORIES = [G, ALG, MAP]
