<p align="center"><img src="docs/icon.png" width="96" alt="PDF DUO"></p>

# PDF DUO

**Site : [deltapassion.github.io/PDF-DUO](https://deltapassion.github.io/PDF-DUO/)** · **Téléchargements : [Releases](https://github.com/Deltapassion/PDF-DUO/releases/latest)**

Logiciel libre pour **lire, annoter, signer et remplir des PDF**, **dessiner des schémas électriques, pneumatiques,
réseau, des GRAFCET et des plans de logement**, et **convertir Word / ODF ↔ PDF**.
Pensé pour l'enseignement dans toutes les sections de lycée professionnel : par exemple les bacs pro MELEC et CIEL, prothésiste dentaire, logistique et magasinier.

*Jacques Branas, en collaboration avec Claude.ai* — licence GNU GPL v3 ou ultérieure.

![PDF DUO](docs/captures/interface-schema.jpg)

## Fonctions (version 1.3.0)

- **PDF** : ouvrir, zoomer, faire défiler, imprimer ; PDF protégés par mot de passe.
- **Annoter / dessiner** : texte, trait, flèche, fil de schéma à angles droits, rectangle, ellipse,
  crayon, surligneur, image.
- **Rotation libre sur 360°** et **miroir** horizontal / vertical de tout élément
  (R = 90°, E = 15°, H / V = miroir, angle précis au dixième de degré dans Propriétés).
- **Grille et aimantation** (pas de 2,5 mm pour les schémas, 1 mm, 5 mm, ou pas réels de 10 / 25 / 50 cm pour les plans).
- **Bibliothèques de symboles** (plus de 700 symboles et 42 formes avec texte) :
  - Électricité – schémas : contacts NO / NF, boutons poussoirs, bobine KM, relais thermique,
    fusible, disjoncteur, lampe, résistance, condensateurs, diodes, LED, transistors, moteur,
    transformateur, appareils de mesure, masse, terre…
  - Fonctions logiques : ET, OU, NON, NON-ET, NON-OU, OU exclusif, en norme CEI et en forme américaine.
  - Plan électrique – logement : prises 2P+T, prises spécialisées, 32 A, RJ45, TV, interrupteurs simple
    allumage, double allumage, va-et-vient, poussoir, variateur, point lumineux DCL, applique, spot,
    tableau, AGCP, compteur, télérupteur, DAAF, VMC, convecteur, chauffe-eau, volets…
  - Architecture – plan (à l'échelle 1/20 à 1/500) : portes (largeur et épaisseur de mur réglables),
    porte double, coulissante, de garage, fenêtres 1 et 2 vantaux, baie coulissante, escalier,
    sanitaires, cuisine, mobilier, flèche Nord.
- **Murs à l'échelle** (épaisseur en cm) et **cotes** affichant la longueur réelle.
- **Repères** (KM1, S1, H2…) sur les symboles, qui restent lisibles quand on tourne le symbole.
- **Capture d'une zone** en image (presse-papiers, collage sur la page, ou PNG).
- **Copier-coller** : les éléments se recollent dans PDF DUO **et** comme image dans Word ou LibreOffice.
- **Signature** dessinée à la souris / au stylet, ou importée ; mémorisable.
- **Formulaires** : remplir les champs d'un PDF, créer des champs texte et des cases à cocher.
- **Pages** : insérer, dupliquer, supprimer, déplacer, pivoter, fusionner des PDF, extraire, diviser.
- **Conversions** : Word / ODT → PDF, PDF → Word (.docx), PDF → ODT, Word ↔ ODT, images → PDF, pages → PNG.
  Word → PDF marche même sans LibreOffice : PDF DUO utilise alors Microsoft Word s'il est installé, sinon sa propre
  conversion (texte, titres, listes, tableaux, images, en-têtes ; mise en page simplifiée). PDF → Word n'a jamais besoin de LibreOffice.
- **Liaisons** : les fils s'accrochent aux bornes des symboles et les suivent quand on déplace un symbole ;
  outil *Liaison* (clic sur une borne, puis l'autre : tracé automatique à angles droits) ;
  points de jonction automatiques.
- **Couleurs de conducteurs** normalisées (phase marron / noir / gris / rouge, neutre bleu, terre vert-jaune rayé,
  retour lampe, navette…) et épaisseur réglable.
- **Numéros de bornes** (A1 / A2, 13-14, 21-22, 1-2, 3-4…) toujours lisibles, repère placé automatiquement à côté.
- **Palette d'écriture** : police, taille, gras, italique, souligné, alignement, couleur, surlignage du texte.
- **Zones interactives** : champ texte, case à cocher, liste déroulante, bouton radio, zone de signature, lien
  (vers une page ou une adresse web).
- **Interface moderne** : thèmes clair, sombre, bleu nuit, sable ; couleur d'accent et fond de travail au choix ;
  palettes affichables / masquables (Affichage › Palettes).
- **Langues** : français, anglais, espagnol, portugais, allemand, italien (Affichage › Langue).
- **Triphasé / puissance** : sectionneur porte-fusibles, contacteur tripolaire, disjoncteur moteur, relais thermique,
  moteur asynchrone 3~, réseau L1 L2 L3 N PE, verrouillage mécanique, contacts de verrouillage électrique 61-62 / 51-52,
  auto-maintien 13-14, contacts F 95-96 / 97-98, arrêt d'urgence, bobines A1/A2, bornier, transformateur de commande.
- **Réseau informatique (CIEL)** : poste, portable, serveur, switch, routeur, Wi-Fi, box, pare-feu, Internet, imprimante,
  téléphone IP, caméra IP, NAS, hub, panneau de brassage, baie, API, CPL, prise RJ45.
- **GRAFCET** : étape initiale, étape, transition + réceptivité, actions (S/R, D), action conditionnelle (condition au-dessus de l'action), divergences ET / OU, macro-étape,
  renvoi, commentaire ; **Ctrl+G** ajoute transition + étape sous l'étape sélectionnée, déjà reliées et numérotées.
- **Algorigramme**, **logigramme** (portes à 2 et 3 entrées, mémoire RS) et **carte mentale** (liaisons courbes).
- **Portes et fenêtres dans les murs** : elles s'alignent sur le mur, prennent son épaisseur et s'ouvrent du côté de la souris.
- **Zones interactives remplissables dans PDF DUO** (double-clic ou panneau Formulaire) ; les valeurs saisies ensuite
  dans Acrobat ou un navigateur sont relues à la réouverture.
- **Commandes d'éclairage (schéma développé)** : va-et-vient, permutateur, double allumage, télérupteur et minuterie
  (bobines A1/A2 et contacts de puissance), contact temporisé au repos.
- **Tableau / protection** (neutre toujours à gauche) : disjoncteurs divisionnaires uni, P+N, bi, tri, tétra
  (repère ×, thermique ⊐, magnétique ⊃) ; interrupteurs et disjoncteurs différentiels ; coupe-circuit et sectionneurs
  porte-fusibles uni, P+N, 2P, tri, tétra avec contacts de pré-coupure et poignée ; symboles de base (interrupteur,
  sectionneur, contacteur, disjoncteur, interrupteur-sectionneur, interrupteur-fusible, sectionneur-fusible, rupteur,
  fusible à percuteur) ; parafoudre ; contacteur complet.
- **Plaque à bornes moteur** (U1 V1 W1 / W2 U2 V2, PE) et **barrettes** pour réaliser les couplages étoile / triangle,
  plus deux plaques corrigées.
- **Sciences** : multimètre (grandeur et valeur affichée réglables), oscilloscope (signaux des 2 voies), GBF (forme et
  fréquence), alimentation stabilisée 0-30 V, piles 9 V et 1,5 V, rhéostat ; verrerie de chimie avec niveau de liquide
  réglable (bécher, erlenmeyer, ballons, éprouvette, fiole jaugée, tube…), agitateur magnétique, burette, potence, bec Bunsen avec flamme bleue ou jaune, trépied… ;
  optique (lentilles, miroirs, prisme, rayons, objet AB…) ; mécanique (masses, ressort, poulie, plan incliné, forces…).
- **Caractères spéciaux** (Ω ω Φ φ Π π Δ μ ° ± ≈ ≤ ≥…) et **racine carrée sur tout le nombre** : écrire √{…}.
- **Agrandissement proportionnel à la souris** : poignée bleue en bas à droite de l'élément sélectionné (Maj = proportionnel aussi pour rectangles et champs).
- **Oscilloscope** : tension sinusoïdale, continue, triangle, créneau, carrée alternative, dent de scie, redressée simple et double alternance ; **symboles continu ⎓ et alternatif ∼** ; **pile 4,5 V**.
- **Boutons toujours visibles dans la barre de menus** : ouvrir, enregistrer, imprimer, annuler, rétablir, zoom −/+, page entière, pleine largeur, caractères spéciaux.
- **Fil volant** (outil à main levée, tracé lissé, fiches banane aux deux bouts) pour les schémas de montage.
- **Cartouche d'un seul bloc** (titre, auteur, établissement, classe, date, échelle, folio), posé en bas à droite de la page.
- **Schémas réseau CIEL (vidéosurveillance, fibre)** : convertisseur de média fibre, châssis, switch PoE, caméras bullet et dôme,
  NVR, poste de supervision, moniteur, opérateur, antenne, routeur 4G, onduleur, tiroir optique ; zones en pointillé avec
  titre, étiquettes de câble ; couleurs de câble fibre / Ethernet / coaxial (exemple-reseau.pdf).
- **Pneumatique (ISO 1219)** : distributeurs 2/2, 3/2, 4/2, 5/2, 5/3 (bouton poussoir, galet, levier, coup de poing,
  électrique, pilotage pneumatique, ressort), vérins simple / double effet, amortis, double tige, rotatif, ventouse,
  source, compresseur, échappement, silencieux, réservoir, FRL, filtre, régulateur, lubrificateur, manomètre, pressostat,
  clapet anti-retour, réducteur de débit, étrangleur, cellules OU / ET, bloqueur, conduites de travail et de pilotage.
- **Recherche dans toute la bibliothèque** : taper un mot (« urgence », « vérin »…) cherche dans toutes les catégories.
- **Aéronautique – câblage** : disjoncteurs à bouton, connecteurs P / J, connecteur multibroches et circulaire, épissure,
  masse structure GD, métallisation, fil blindé, paires torsadées, cosse, bornier, barre bus, relais, générateur, batterie…
- **Énergie solaire photovoltaïque** : symboles normalisés (cellule, module, chaîne PV, onduleur, convertisseurs,
  régulateur MPPT / PWM, batterie 2 / 6 / 12 / 24 / 48 V, shunt, ampèremètre et voltmètre continus, compteur Wh,
  fusible gPV, sectionneur DC, parafoudre, MC4, diode anti-retour, capteur thermique) et **schéma technologique**
  d'une installation en site isolé (panneau, contrôleur de charge, batterie, onduleur, moniteur, protections, charges) ;
  exemple : `exemples/exemple-solaire.pdf` (avec coupe-circuits F1 champ PV, F2 batterie, F3 utilisation).
- **Sources de secours** : éolienne et son régulateur à délestage, groupe électrogène, alternateur de voiture ou de bateau,
  en symbole et en vue réaliste.
- **Organigramme d'entreprise** pour le rapport de stage : *Insertion › Organigramme d'entreprise* pose un modèle relié
  (direction, services, tuteur, stagiaire) à compléter ; exemple : `exemples/exemple-organigramme.pdf`.
- **Prévention électrique** : EPI (casque à écran facial, gants isolants, vêtement, chaussures, lunettes),
  EIS (tapis, outils isolés 1000 V, cadenas de consignation, nappe, tabouret, VAT, macaron « Défense de manœuvrer »),
  ECS (barrière, chaîne, pancarte « Danger de mort », dispositif MALT-CCT, cône) ;
  exemple : `exemples/exemple-consignation.pdf` (les 5 étapes de la consignation et un devis calculé).
- **Travail en hauteur** : échafaudage roulant, plateforme individuelle roulante (PIRL), escabeau, échelle, nacelles
  (ciseaux, articulée, télescopique, mât vertical, camion, remorque), panneaux « harnais obligatoire » et « chute ».
- **Manutention et sécurité** : pictogrammes d'emballage (haut, fragile, humidité, chaleur, centre de gravité, élingage,
  gerbage limité, ne pas retourner…), signalisation (danger, interdiction, obligation) et produits dangereux (SGH01 à SGH09,
  infectieux, radioactif).
- **Logistique** : chariot élévateur, transpalette, diable, table élévatrice, convoyeur, camion, entrepôt, rayonnage,
  palette, colis, scanner et étiquette code-barres, balance, levage de conteneur, bon de livraison.
- **Prothésiste dentaire** : schéma dentaire des deux mâchoires avec la numérotation FDI (11 à 48), prothèse partielle amovible à crochets, dents, couronne, bridge, implant, prothèse amovible, appareil orthodontique, articulateur,
  porte-empreinte, modèle en plâtre, pièce à main, fraise, fauteuil, radiographie, instruments.
- **Outils** de l'électricien, isolés 1000 V (malette, tournevis, pinces coupante, à bec, universelle, à dénuder, à sertir, tournevis testeur, couronne de câble, ruban isolant, ampoules, VAT, mètre, niveau, perceuse, tire-fil), du mécanicien (clés plate, mixte,
  à molette, à cliquet, dynamométrique, marteau, pince-étau, scie, lime, pied à coulisse, étau) et de l'informatique
  (pince à sertir RJ45, connecteur 8P8C, testeur, outil d'insertion, bracelet antistatique).
  Tous ces pictogrammes sont des **dessins originaux** inspirés des normes, libres d'utilisation.
- **Tableaux avec calculs** (menu *Tableau*) : lignes et colonnes, ajout et suppression, fusion de cases, en-tête coloré ;
  formules comme dans un tableur : `=B2*C2`, `=B3 x C3`, `=(A1+A2)/2`, `=√(144)`, `=A1^2`, `=SOMME(D2:D4)`,
  `=MOYENNE(…)`, `=MAX(…)`, `=MIN(…)`, pourcentages ; les résultats se mettent à jour dans la page.
- **Calculatrice scientifique et graphique** (Ctrl+K) : sin, cos, tan et inverses, ln, log, √, puissances, π, degrés ou
  radians, historique ; tracé de trois courbes, zoom à la molette, et insertion du graphique dans la page.
  Les calculs passent par un évaluateur sûr (aucun code n'est exécuté).
- **Gestes qui sauvent** : panneaux (premiers secours, DAE, lavage oculaire, douche), protéger, alerter, PLS, massage cardiaque,
  insufflation, électrodes du défibrillateur, compressions, garrot, brûlure, étouffement (claques, Heimlich), électrisation
  (couper le courant, arrêt d'urgence, ne pas toucher, perche isolante) ; exemple : `exemples/exemple-premiers-secours.pdf`.
- **Biologie de base** : cellules animale et végétale, bactérie, virus, ADN, chromosome, neurone, organes, plante, fleur,
  microscope, lame et lamelle, boîte de Petri.
- **Robotique (technologie au collège)** : cartes Arduino Uno, Raspberry Pi 4/5 et Pico, ESP32, micro:bit, Sense HAT,
  brochage GPIO 40 broches, plaque d'essai, LED (couleur réglable), résistance (anneaux calculés selon la valeur) et tableau
  du code des couleurs, capteurs (ultrasons, PIR, DHT11/DHT22, sol, suiveur de ligne), servomoteur, motoréducteur, relais,
  écrans LCD et OLED, châssis de robot.
- **Sécurité incendie** : détecteurs, déclencheur manuel, sirène, flash, BAAS, BAES, éclairage « SORTIE / EXIT » à flèche
  orientable, extincteurs, RIA, porte coupe-feu, ventouse, CMSI, UGA, désenfumage ; panneaux rouges et verts d'évacuation.
- **Équipements industriels à états réglables** : barrière levante (haut, milieu, bas), tapis roulant, malaxeur, ventilateur,
  monte-charge, ascenseur 3 niveaux, puits, pompe, réservoir et château d'eau avec capteurs H/M/B, système de pompage complet,
  four, vérins simple et double effet avec capteurs, fins de course, capteurs magnétique et inductif, boucle magnétique,
  cellule à miroir, voitures, bras manipulateur, moteur asynchrone et plaque à bornes étoile / triangle ;
  exemples : `exemples/exemple-pompage.pdf`, `exemples/exemple-parking.pdf`.
- **Habitat** : GTL avec goulotte du sol au plafond, radiateur à inertie, radiant, convecteur, plancher chauffant, éclairage
  (spot, tubes, réglette, dalle LED, douille), appareillage étanche, bornes de recharge intérieure et extérieure.
- **Métiers de la sécurité** : sapeurs-pompiers (équipement, points d'eau, triangle du feu, classes de feu), sûreté et
  surveillance (contrôle d'accès, vidéosurveillance, rondes), police et maintien de l'ordre (tenue complète, texte modifiable).
- **Favoris** : clic droit sur un symbole › *Ajouter aux favoris* ; les favoris passent en tête de chaque catégorie et ont leur
  propre catégorie « ★ Favoris », ouverte au démarrage.
- **Annuler / rétablir** illimité (150 étapes).
- **Mode présentation** (F11 ou bouton ⛶) : plein écran avec la page, les outils à gauche et la bibliothèque (2 colonnes) à droite ; les menus réapparaissent
  quand la souris touche le haut de l'écran, Échap pour quitter.

Les dessins sont enregistrés **en vectoriel** dans le PDF (nets à toutes les échelles et à l'impression).
Le fichier garde aussi une copie modifiable : en le rouvrant dans PDF DUO, tous les éléments
se déplacent et se modifient encore. *Fichier › Exporter un PDF final* produit un PDF aplati, sans ces données.

## Télécharger

| Système | Fichier |
|---|---|
| Windows 10 / 11 | [PDF-DUO-Windows-Setup.exe](https://github.com/Deltapassion/PDF-DUO/releases/latest/download/PDF-DUO-Windows-Setup.exe) (installeur) · [PDF-DUO-Windows.zip](https://github.com/Deltapassion/PDF-DUO/releases/latest/download/PDF-DUO-Windows.zip) (portable) |
| Linux Debian / Ubuntu / Mint | [pdf-duo_amd64.deb](https://github.com/Deltapassion/PDF-DUO/releases/latest/download/pdf-duo_amd64.deb) |
| Linux (toutes distributions) | [PDF-DUO-x86_64.AppImage](https://github.com/Deltapassion/PDF-DUO/releases/latest/download/PDF-DUO-x86_64.AppImage) · [PDF-DUO-Linux-x86_64.tar.gz](https://github.com/Deltapassion/PDF-DUO/releases/latest/download/PDF-DUO-Linux-x86_64.tar.gz) |
| macOS Apple Silicon (M1, M2…) | [PDF-DUO-macOS-AppleSilicon.zip](https://github.com/Deltapassion/PDF-DUO/releases/latest/download/PDF-DUO-macOS-AppleSilicon.zip) |
| macOS Intel | [PDF-DUO-macOS-Intel.zip](https://github.com/Deltapassion/PDF-DUO/releases/latest/download/PDF-DUO-macOS-Intel.zip) |

Ces versions sont fabriquées automatiquement par GitHub à chaque étiquette `v…` (fichier `.github/workflows/release.yml`).
Sur macOS, au premier lancement : clic droit sur l'application › Ouvrir. Pour des conversions Word les plus fidèles et pour l'ODT, installer
aussi **LibreOffice** (gratuit).

**Notice d'utilisation illustrée de captures d'écran** en six langues : [français](https://deltapassion.github.io/PDF-DUO/notice/?lang=fr) ·
[English](https://deltapassion.github.io/PDF-DUO/notice/?lang=en) ·
[español](https://deltapassion.github.io/PDF-DUO/notice/?lang=es) ·
[português](https://deltapassion.github.io/PDF-DUO/notice/?lang=pt) ·
[Deutsch](https://deltapassion.github.io/PDF-DUO/notice/?lang=de) ·
[italiano](https://deltapassion.github.io/PDF-DUO/notice/?lang=it) — aussi dans le logiciel : *Aide › Notice d'utilisation* (F1).

**Soutenir le projet** : PDF DUO est gratuit ; un don sur [Ko-fi](https://ko-fi.com/djlatinjazz) aide à le faire évoluer.

## Lancer depuis le code source

Il faut **Python 3.9 ou plus récent**.

```
pip install -r requirements.txt
python3 pdfduo.py
```

```text
Exemples fournis : dossier exemples/ (inversion de sens de marche, GRAFCET, réseau de vidéosurveillance)
```

Linux (Debian, Ubuntu, Mint) : `sudo apt install libreoffice python3-pip` puis les deux commandes ci-dessus
(ajouter `--break-system-packages` à `pip` si le système le demande, ou utiliser un environnement virtuel).

## Remarques

- La conversion PDF → Word reconstruit paragraphes, tableaux et images. Elle est très bonne sur un PDF
  « texte » ; un PDF scanné (image) demandera une reconnaissance de caractères (prévue plus tard).
- Bibliothèques utilisées : Qt / PySide6 (LGPL), PyMuPDF (AGPL), pdf2docx (MIT), LibreOffice (MPL).

## Du même auteur

[**Platine Duo**](https://deltapassion.github.io/Platine-Duo/) — logiciel libre de mix DJ, créé lui aussi avec Claude.ai.
