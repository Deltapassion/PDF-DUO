# -*- coding: utf-8 -*-
T = {}
T["fr"] = dict(
title="Notice d'utilisation", sub="PDF, schémas électriques, GRAFCET et plans — logiciel libre",
sec=[
("1. Installation", [
 "<b>Windows</b> : lancer l'installeur <code>PDF-DUO-Windows-Setup.exe</code>, ou décompresser <code>PDF-DUO-Windows.zip</code> puis ouvrir <code>PDF DUO.exe</code>.",
 "<b>Linux</b> : double-cliquer sur <code>pdf-duo_amd64.deb</code> (Debian, Ubuntu, Mint), ou utiliser l'AppImage (rendre le fichier exécutable puis l'ouvrir).",
 "<b>macOS</b> : choisir la version Apple Silicon (M1, M2…) ou Intel, décompresser, glisser « PDF DUO » dans Applications. Au premier lancement : clic droit › Ouvrir.",
 "Conversions Word → PDF : PDF DUO utilise <b>LibreOffice</b> s'il est installé (le plus fidèle, gratuit), sinon <b>Microsoft Word</b>, sinon sa propre conversion (mise en page simplifiée). Pour les fichiers ODT, il faut LibreOffice."]),
("2. L'écran", [
 "En haut, à gauche des menus : ouvrir, enregistrer, imprimer, <b>annuler ↶ / rétablir ↷</b>, <b>zoom − / +</b>, page entière, caractères spéciaux <b>Ω √</b>.",
 "À gauche : les outils (sélection, texte, trait, fil, liaison, formes, crayon, surligneur, fil volant, capture).",
 "À droite : la <b>bibliothèque de symboles</b> (choisir une catégorie ou taper un mot dans la recherche) et le panneau <b>Propriétés</b> de l'élément sélectionné.",
 "<i>Affichage › Palettes</i> affiche ou masque chaque panneau ; <i>Affichage › Thème</i> et <i>Langue</i> changent l'apparence et la langue."]),
("3. Ouvrir et enregistrer", [
 "<i>Fichier › Ouvrir</i> accepte les PDF, les documents Word / ODT (convertis automatiquement) et les images.",
 "Les dessins sont enregistrés en vectoriel dans le PDF. En rouvrant le fichier dans PDF DUO, tout reste modifiable.",
 "<i>Fichier › Exporter un PDF final</i> produit un PDF aplati, à distribuer."]),
("4. Dessiner un schéma", [
 "Cliquer un symbole dans la bibliothèque puis cliquer sur la page pour le poser (ou glisser-déposer). <b>Échap</b> pour finir.",
 "<b>R</b> tourne de 90°, <b>E</b> de 15° (Maj = sens inverse), <b>H</b> / <b>V</b> font un miroir. Angle précis dans Propriétés.",
 "La <b>poignée bleue</b> en bas à droite agrandit l'élément en gardant ses proportions.",
 "Le <b>repère</b> (KM1, S1…) et les <b>numéros de bornes</b> se modifient dans Propriétés ; boutons « Repère à gauche / à droite ».",
 "Outil <b>Fil</b> : un clic par angle ; un clic sur une borne (petit cercle) accroche le fil. Outil <b>Liaison</b> : cliquer deux bornes, le tracé se fait seul. Les fils suivent les symboles déplacés.",
 "Liste <b>Conducteur</b> : couleurs normalisées (phase, neutre bleu, terre vert/jaune, fibre, Ethernet…). Les points de jonction se placent automatiquement."]),
("5. Plans de logement", [
 "Régler l'<b>échelle</b> (1/50, 1/100…) et le pas de grille réel dans la barre <i>Plan</i>.",
 "Outil <b>Mur</b> : un clic par angle, double-clic pour finir. Outils <b>Porte</b>, <b>Porte double</b>, <b>Fenêtre</b> : passer sur un mur, l'ouverture s'aligne et prend l'épaisseur du mur.",
 "Outil <b>Cote</b> : glisser d'un point à l'autre, la longueur réelle s'affiche. <i>Insertion › Cartouche</i> ajoute le cartouche."]),
("6. GRAFCET, algorigramme, carte mentale", [
 "Poser une étape initiale, la sélectionner puis <b>Ctrl+G</b> : une transition et l'étape suivante sont ajoutées, reliées et numérotées.",
 "Double-clic sur une forme pour écrire son texte. Choisir <i>Liaison : courbe</i> pour les cartes mentales, cocher <i>Flèche</i> pour les algorigrammes."]),
("7. Formulaires et signature", [
 "Barre <i>Formulaire et signature</i> : champ texte, case à cocher, liste, bouton radio, zone de signature, lien. Double-clic pour remplir ; panneau <i>Formulaire</i> pour tout voir.",
 "Bouton <b>Signature</b> : dessiner ou importer sa signature, puis cliquer où la poser."]),
("8. Texte et caractères spéciaux", [
 "Palette d'écriture : police, taille, gras, italique, souligné, alignement, couleur, surlignage.",
 "Bouton <b>Ω √</b> : Ω, φ, π, Δ, μ, °, ±… Écrire <code>√{12,5}</code> : la barre de la racine couvre tout le nombre."]),
("9. Conversions", [
 "Menu <i>Conversions</i> : Word / ODT → PDF, PDF → Word, PDF → ODT, Word ↔ ODT, images → PDF, pages → PNG."]),
("10. Soutenir le projet", [
 "PDF DUO est gratuit et libre (licence GNU GPL v3). Un don sur <b>ko-fi.com/djlatinjazz</b> aide à le faire évoluer (<i>Aide › Faire un don</i>).",
 "Site : deltapassion.github.io/PDF-DUO — Contact : deltapassion@gmx.com"]),
])
T["en"] = dict(
title="User guide", sub="PDF, electrical diagrams, GRAFCET and floor plans — free software",
sec=[
("1. Installation", [
 "<b>Windows</b>: run the installer <code>PDF-DUO-Windows-Setup.exe</code>, or unzip <code>PDF-DUO-Windows.zip</code> and open <code>PDF DUO.exe</code>.",
 "<b>Linux</b>: double-click <code>pdf-duo_amd64.deb</code> (Debian, Ubuntu, Mint), or use the AppImage (make it executable, then open it).",
 "<b>macOS</b>: pick the Apple Silicon (M1, M2…) or Intel version, unzip, drag “PDF DUO” to Applications. First launch: right-click › Open.",
 "Word → PDF conversions: PDF DUO uses <b>LibreOffice</b> if installed (most faithful, free), otherwise <b>Microsoft Word</b>, otherwise its own converter (simplified layout). ODT files need LibreOffice."]),
("2. The window", [
 "Top, left of the menus: open, save, print, <b>undo ↶ / redo ↷</b>, <b>zoom − / +</b>, whole page, special characters <b>Ω √</b>.",
 "Left: the tools (select, text, line, wire, connection, shapes, pencil, highlighter, flying lead, capture).",
 "Right: the <b>symbol library</b> (choose a category or type a word to search) and the <b>Properties</b> panel of the selected item.",
 "<i>View › Palettes</i> shows or hides each panel; <i>View › Theme</i> and <i>Language</i> change the look and language."]),
("3. Opening and saving", [
 "<i>File › Open</i> accepts PDFs, Word / ODT documents (converted automatically) and images.",
 "Drawings are saved as vectors in the PDF. When the file is reopened in PDF DUO, everything stays editable.",
 "<i>File › Export a final PDF</i> produces a flattened PDF to hand out."]),
("4. Drawing a diagram", [
 "Click a symbol in the library, then click on the page to place it (or drag and drop). <b>Esc</b> to finish.",
 "<b>R</b> rotates 90°, <b>E</b> 15° (Shift = other way), <b>H</b> / <b>V</b> mirror. Exact angle in Properties.",
 "The <b>blue handle</b> at the bottom right enlarges the item proportionally.",
 "The <b>label</b> (KM1, S1…) and <b>terminal numbers</b> are edited in Properties; “Label on the left / right” buttons.",
 "<b>Wire</b> tool: one click per corner; clicking a terminal (small circle) attaches the wire. <b>Connection</b> tool: click two terminals and the route is drawn. Wires follow moved symbols.",
 "<b>Conductor</b> list: standard colours (phase, blue neutral, green/yellow earth, fibre, Ethernet…). Junction dots are placed automatically."]),
("5. Floor plans", [
 "Set the <b>scale</b> (1/50, 1/100…) and the real grid step in the <i>Plan</i> toolbar.",
 "<b>Wall</b> tool: one click per corner, double-click to finish. <b>Door</b>, <b>Double door</b>, <b>Window</b> tools: move over a wall and the opening aligns and takes the wall thickness.",
 "<b>Dimension</b> tool: drag from point to point, the real length is shown. <i>Insert › Title block</i> adds the title block."]),
("6. GRAFCET, flowcharts, mind maps", [
 "Place an initial step, select it, then press <b>Ctrl+G</b>: a transition and the next step are added, connected and numbered.",
 "Double-click a shape to type its text. Choose <i>Connection: curved</i> for mind maps, tick <i>Arrow</i> for flowcharts."]),
("7. Forms and signature", [
 "<i>Form and signature</i> toolbar: text field, check box, list, radio button, signature area, link. Double-click to fill in; the <i>Form</i> panel lists everything.",
 "<b>Signature</b> button: draw or import your signature, then click where to place it."]),
("8. Text and special characters", [
 "Writing palette: font, size, bold, italic, underline, alignment, colour, highlight.",
 "<b>Ω √</b> button: Ω, φ, π, Δ, μ, °, ±… Type <code>√{12.5}</code>: the root bar covers the whole number."]),
("9. Conversions", ["<i>Conversions</i> menu: Word / ODT → PDF, PDF → Word, PDF → ODT, Word ↔ ODT, images → PDF, pages → PNG."]),
("10. Support the project", [
 "PDF DUO is free software (GNU GPL v3). A donation at <b>ko-fi.com/djlatinjazz</b> helps it grow (<i>Help › Donate</i>).",
 "Website: deltapassion.github.io/PDF-DUO — Contact: deltapassion@gmx.com"]),
])
T["es"] = dict(
title="Manual de uso", sub="PDF, esquemas eléctricos, GRAFCET y planos — software libre",
sec=[
("1. Instalación", [
 "<b>Windows</b>: ejecutar el instalador <code>PDF-DUO-Windows-Setup.exe</code>, o descomprimir <code>PDF-DUO-Windows.zip</code> y abrir <code>PDF DUO.exe</code>.",
 "<b>Linux</b>: doble clic en <code>pdf-duo_amd64.deb</code> (Debian, Ubuntu, Mint), o usar la AppImage (hacerla ejecutable y abrirla).",
 "<b>macOS</b>: elegir la versión Apple Silicon (M1, M2…) o Intel, descomprimir y arrastrar «PDF DUO» a Aplicaciones. Primer inicio: clic derecho › Abrir.",
 "Conversiones Word → PDF: PDF DUO usa <b>LibreOffice</b> si está instalado (lo más fiel, gratuito), si no <b>Microsoft Word</b>, y si no su propia conversión (diseño simplificado). Los archivos ODT necesitan LibreOffice."]),
("2. La pantalla", [
 "Arriba, a la izquierda de los menús: abrir, guardar, imprimir, <b>deshacer ↶ / rehacer ↷</b>, <b>zoom − / +</b>, página completa, caracteres especiales <b>Ω √</b>.",
 "A la izquierda: las herramientas (selección, texto, trazo, cable, conexión, formas, lápiz, resaltador, cable volante, captura).",
 "A la derecha: la <b>biblioteca de símbolos</b> (elegir una categoría o buscar una palabra) y el panel <b>Propiedades</b> del elemento seleccionado.",
 "<i>Ver › Paletas</i> muestra u oculta cada panel; <i>Ver › Tema</i> e <i>Idioma</i> cambian el aspecto y el idioma."]),
("3. Abrir y guardar", [
 "<i>Archivo › Abrir</i> acepta PDF, documentos Word / ODT (convertidos automáticamente) e imágenes.",
 "Los dibujos se guardan en vectorial en el PDF. Al reabrirlo en PDF DUO, todo sigue siendo editable.",
 "<i>Archivo › Exportar un PDF final</i> genera un PDF aplanado para distribuir."]),
("4. Dibujar un esquema", [
 "Hacer clic en un símbolo de la biblioteca y luego en la página para colocarlo (o arrastrar y soltar). <b>Esc</b> para terminar.",
 "<b>R</b> gira 90°, <b>E</b> 15° (Mayús = sentido inverso), <b>H</b> / <b>V</b> hacen espejo. Ángulo exacto en Propiedades.",
 "El <b>tirador azul</b> abajo a la derecha amplía el elemento manteniendo sus proporciones.",
 "La <b>referencia</b> (KM1, S1…) y los <b>números de bornes</b> se editan en Propiedades.",
 "Herramienta <b>Cable</b>: un clic por esquina; un clic en un borne (pequeño círculo) conecta el cable. Herramienta <b>Conexión</b>: hacer clic en dos bornes y el trazado se hace solo. Los cables siguen a los símbolos.",
 "Lista <b>Conductor</b>: colores normalizados (fase, neutro azul, tierra verde/amarillo, fibra, Ethernet…). Los puntos de unión se colocan solos."]),
("5. Planos de vivienda", [
 "Ajustar la <b>escala</b> (1/50, 1/100…) y el paso de cuadrícula real en la barra <i>Plano</i>.",
 "Herramienta <b>Muro</b>: un clic por esquina, doble clic para terminar. <b>Puerta</b>, <b>Puerta doble</b>, <b>Ventana</b>: pasar sobre un muro y la abertura se alinea sola.",
 "Herramienta <b>Cota</b>: arrastrar de un punto a otro, se muestra la longitud real. <i>Insertar › Cajetín</i> añade el cajetín."]),
("6. GRAFCET, diagramas de flujo, mapas mentales", [
 "Colocar una etapa inicial, seleccionarla y pulsar <b>Ctrl+G</b>: se añaden una transición y la etapa siguiente, conectadas y numeradas.",
 "Doble clic en una forma para escribir su texto. <i>Conexión: curva</i> para mapas mentales, <i>Flecha</i> para diagramas de flujo."]),
("7. Formularios y firma", [
 "Barra <i>Formulario y firma</i>: campo de texto, casilla, lista, botón de opción, zona de firma, enlace. Doble clic para rellenar.",
 "Botón <b>Firma</b>: dibujar o importar la firma y hacer clic donde colocarla."]),
("8. Texto y caracteres especiales", [
 "Paleta de escritura: fuente, tamaño, negrita, cursiva, subrayado, alineación, color, resaltado.",
 "Botón <b>Ω √</b>: Ω, φ, π, Δ, μ, °, ±… Escribir <code>√{12,5}</code>: la barra de la raíz cubre todo el número."]),
("9. Conversiones", ["Menú <i>Conversiones</i>: Word / ODT → PDF, PDF → Word, PDF → ODT, Word ↔ ODT, imágenes → PDF, páginas → PNG."]),
("10. Apoyar el proyecto", [
 "PDF DUO es gratuito y libre (GNU GPL v3). Una donación en <b>ko-fi.com/djlatinjazz</b> ayuda a mejorarlo (<i>Ayuda › Donar</i>).",
 "Web: deltapassion.github.io/PDF-DUO — Contacto: deltapassion@gmx.com"]),
])
T["pt"] = dict(
title="Manual de utilização", sub="PDF, esquemas elétricos, GRAFCET e plantas — software livre",
sec=[
("1. Instalação", [
 "<b>Windows</b>: executar o instalador <code>PDF-DUO-Windows-Setup.exe</code>, ou descomprimir <code>PDF-DUO-Windows.zip</code> e abrir <code>PDF DUO.exe</code>.",
 "<b>Linux</b>: duplo clique em <code>pdf-duo_amd64.deb</code> (Debian, Ubuntu, Mint), ou usar a AppImage (torná-la executável e abri-la).",
 "<b>macOS</b>: escolher a versão Apple Silicon (M1, M2…) ou Intel, descomprimir e arrastar «PDF DUO» para Aplicações. Primeiro arranque: clique direito › Abrir.",
 "Conversões Word → PDF: o PDF DUO usa o <b>LibreOffice</b> se estiver instalado (o mais fiel, gratuito), senão o <b>Microsoft Word</b>, senão a sua própria conversão (paginação simplificada). Os ficheiros ODT precisam do LibreOffice."]),
("2. O ecrã", [
 "Em cima, à esquerda dos menus: abrir, guardar, imprimir, <b>desfazer ↶ / refazer ↷</b>, <b>zoom − / +</b>, página inteira, caracteres especiais <b>Ω √</b>.",
 "À esquerda: as ferramentas (seleção, texto, traço, fio, ligação, formas, lápis, marcador, fio solto, captura).",
 "À direita: a <b>biblioteca de símbolos</b> (escolher uma categoria ou pesquisar) e o painel <b>Propriedades</b> do elemento selecionado.",
 "<i>Exibir › Paletas</i> mostra ou oculta cada painel; <i>Exibir › Tema</i> e <i>Idioma</i> mudam o aspeto e o idioma."]),
("3. Abrir e guardar", [
 "<i>Arquivo › Abrir</i> aceita PDF, documentos Word / ODT (convertidos automaticamente) e imagens.",
 "Os desenhos ficam guardados em vetorial no PDF. Ao reabrir no PDF DUO, tudo continua editável.",
 "<i>Arquivo › Exportar um PDF final</i> produz um PDF achatado para distribuir."]),
("4. Desenhar um esquema", [
 "Clicar num símbolo da biblioteca e depois na página para o colocar (ou arrastar e largar). <b>Esc</b> para terminar.",
 "<b>R</b> roda 90°, <b>E</b> 15° (Shift = sentido inverso), <b>H</b> / <b>V</b> espelham. Ângulo exato em Propriedades.",
 "A <b>pega azul</b> em baixo à direita amplia o elemento mantendo as proporções.",
 "A <b>referência</b> (KM1, S1…) e os <b>números dos terminais</b> editam-se em Propriedades.",
 "Ferramenta <b>Fio</b>: um clique por canto; um clique num terminal (pequeno círculo) liga o fio. Ferramenta <b>Ligação</b>: clicar em dois terminais e o traçado faz-se sozinho. Os fios seguem os símbolos.",
 "Lista <b>Condutor</b>: cores normalizadas (fase, neutro azul, terra verde/amarelo, fibra, Ethernet…). Os pontos de junção colocam-se sozinhos."]),
("5. Plantas de habitação", [
 "Definir a <b>escala</b> (1/50, 1/100…) e o passo de grelha real na barra <i>Planta</i>.",
 "Ferramenta <b>Parede</b>: um clique por canto, duplo clique para terminar. <b>Porta</b>, <b>Porta dupla</b>, <b>Janela</b>: passar sobre uma parede e a abertura alinha-se.",
 "Ferramenta <b>Cota</b>: arrastar de um ponto a outro, aparece o comprimento real. <i>Inserir › Legenda</i> adiciona a legenda."]),
("6. GRAFCET, fluxogramas, mapas mentais", [
 "Colocar uma etapa inicial, selecioná-la e premir <b>Ctrl+G</b>: são adicionadas uma transição e a etapa seguinte, ligadas e numeradas.",
 "Duplo clique numa forma para escrever o texto. <i>Ligação: curva</i> para mapas mentais, <i>Seta</i> para fluxogramas."]),
("7. Formulários e assinatura", [
 "Barra <i>Formulário e assinatura</i>: campo de texto, caixa, lista, botão de opção, zona de assinatura, ligação web. Duplo clique para preencher.",
 "Botão <b>Assinatura</b>: desenhar ou importar a assinatura e clicar onde a colocar."]),
("8. Texto e caracteres especiais", [
 "Paleta de escrita: tipo de letra, tamanho, negrito, itálico, sublinhado, alinhamento, cor, realce.",
 "Botão <b>Ω √</b>: Ω, φ, π, Δ, μ, °, ±… Escrever <code>√{12,5}</code>: a barra da raiz cobre todo o número."]),
("9. Conversões", ["Menu <i>Conversões</i>: Word / ODT → PDF, PDF → Word, PDF → ODT, Word ↔ ODT, imagens → PDF, páginas → PNG."]),
("10. Apoiar o projeto", [
 "O PDF DUO é gratuito e livre (GNU GPL v3). Um donativo em <b>ko-fi.com/djlatinjazz</b> ajuda a melhorá-lo (<i>Ajuda › Fazer um donativo</i>).",
 "Site: deltapassion.github.io/PDF-DUO — Contacto: deltapassion@gmx.com"]),
])
T["de"] = dict(
title="Bedienungsanleitung", sub="PDF, Schaltpläne, GRAFCET und Grundrisse — freie Software",
sec=[
("1. Installation", [
 "<b>Windows</b>: das Installationsprogramm <code>PDF-DUO-Windows-Setup.exe</code> starten oder <code>PDF-DUO-Windows.zip</code> entpacken und <code>PDF DUO.exe</code> öffnen.",
 "<b>Linux</b>: Doppelklick auf <code>pdf-duo_amd64.deb</code> (Debian, Ubuntu, Mint) oder das AppImage verwenden (ausführbar machen und öffnen).",
 "<b>macOS</b>: Version für Apple Silicon (M1, M2…) oder Intel wählen, entpacken, „PDF DUO“ in Programme ziehen. Erster Start: Rechtsklick › Öffnen.",
 "Konvertierung Word → PDF: PDF DUO nutzt <b>LibreOffice</b>, falls installiert (am genauesten, kostenlos), sonst <b>Microsoft Word</b>, sonst die eigene Konvertierung (vereinfachtes Layout). Für ODT-Dateien wird LibreOffice benötigt."]),
("2. Die Oberfläche", [
 "Oben links neben den Menüs: Öffnen, Speichern, Drucken, <b>Rückgängig ↶ / Wiederholen ↷</b>, <b>Zoom − / +</b>, ganze Seite, Sonderzeichen <b>Ω √</b>.",
 "Links: die Werkzeuge (Auswahl, Text, Linie, Leitung, Verbindung, Formen, Stift, Textmarker, Laborkabel, Aufnahme).",
 "Rechts: die <b>Symbolbibliothek</b> (Kategorie wählen oder ein Wort suchen) und das Feld <b>Eigenschaften</b> des ausgewählten Elements.",
 "<i>Ansicht › Paletten</i> blendet jedes Feld ein oder aus; <i>Ansicht › Design</i> und <i>Sprache</i> ändern Aussehen und Sprache."]),
("3. Öffnen und speichern", [
 "<i>Datei › Öffnen</i> akzeptiert PDF, Word- / ODT-Dokumente (automatisch konvertiert) und Bilder.",
 "Zeichnungen werden als Vektoren im PDF gespeichert. Beim erneuten Öffnen in PDF DUO bleibt alles bearbeitbar.",
 "<i>Datei › Endgültiges PDF exportieren</i> erzeugt ein reduziertes PDF zum Verteilen."]),
("4. Einen Schaltplan zeichnen", [
 "Ein Symbol in der Bibliothek anklicken, dann auf die Seite klicken (oder ziehen und ablegen). <b>Esc</b> zum Beenden.",
 "<b>R</b> dreht um 90°, <b>E</b> um 15° (Umschalt = andere Richtung), <b>H</b> / <b>V</b> spiegeln. Genauer Winkel in Eigenschaften.",
 "Der <b>blaue Griff</b> unten rechts vergrößert das Element proportional.",
 "<b>Kennzeichnung</b> (KM1, S1…) und <b>Klemmennummern</b> werden in Eigenschaften bearbeitet.",
 "Werkzeug <b>Leitung</b>: ein Klick pro Ecke; ein Klick auf eine Klemme (kleiner Kreis) verbindet. Werkzeug <b>Verbindung</b>: zwei Klemmen anklicken, der Verlauf entsteht automatisch. Leitungen folgen verschobenen Symbolen.",
 "Liste <b>Leiter</b>: genormte Farben (Außenleiter, Neutralleiter blau, Schutzleiter grün/gelb, Glasfaser, Ethernet…). Verbindungspunkte werden automatisch gesetzt."]),
("5. Grundrisse", [
 "<b>Maßstab</b> (1/50, 1/100…) und reales Raster in der Leiste <i>Plan</i> einstellen.",
 "Werkzeug <b>Wand</b>: ein Klick pro Ecke, Doppelklick zum Beenden. <b>Tür</b>, <b>Doppeltür</b>, <b>Fenster</b>: über eine Wand fahren, die Öffnung richtet sich aus.",
 "Werkzeug <b>Bemaßung</b>: von Punkt zu Punkt ziehen, die reale Länge wird angezeigt. <i>Einfügen › Schriftfeld</i> fügt das Schriftfeld ein."]),
("6. GRAFCET, Ablaufdiagramme, Mindmaps", [
 "Einen Anfangsschritt setzen, auswählen und <b>Strg+G</b> drücken: Übergang und nächster Schritt werden verbunden und nummeriert hinzugefügt.",
 "Doppelklick auf eine Form, um ihren Text zu schreiben. <i>Verbindung: Kurve</i> für Mindmaps, <i>Pfeil</i> für Ablaufdiagramme."]),
("7. Formulare und Unterschrift", [
 "Leiste <i>Formular und Unterschrift</i>: Textfeld, Kontrollkästchen, Liste, Optionsfeld, Unterschriftsbereich, Link. Doppelklick zum Ausfüllen.",
 "Schaltfläche <b>Unterschrift</b>: Unterschrift zeichnen oder importieren und platzieren."]),
("8. Text und Sonderzeichen", [
 "Schreibpalette: Schrift, Größe, fett, kursiv, unterstrichen, Ausrichtung, Farbe, Hervorhebung.",
 "Schaltfläche <b>Ω √</b>: Ω, φ, π, Δ, μ, °, ±… <code>√{12,5}</code> schreiben: der Wurzelstrich deckt die ganze Zahl ab."]),
("9. Konvertierungen", ["Menü <i>Konvertierung</i>: Word / ODT → PDF, PDF → Word, PDF → ODT, Word ↔ ODT, Bilder → PDF, Seiten → PNG."]),
("10. Das Projekt unterstützen", [
 "PDF DUO ist kostenlos und frei (GNU GPL v3). Eine Spende auf <b>ko-fi.com/djlatinjazz</b> hilft bei der Weiterentwicklung (<i>Hilfe › Spenden</i>).",
 "Website: deltapassion.github.io/PDF-DUO — Kontakt: deltapassion@gmx.com"]),
])
T["it"] = dict(
title="Manuale d'uso", sub="PDF, schemi elettrici, GRAFCET e piante — software libero",
sec=[
("1. Installazione", [
 "<b>Windows</b>: avviare il programma di installazione <code>PDF-DUO-Windows-Setup.exe</code>, oppure estrarre <code>PDF-DUO-Windows.zip</code> e aprire <code>PDF DUO.exe</code>.",
 "<b>Linux</b>: doppio clic su <code>pdf-duo_amd64.deb</code> (Debian, Ubuntu, Mint), oppure usare l'AppImage (renderla eseguibile e aprirla).",
 "<b>macOS</b>: scegliere la versione Apple Silicon (M1, M2…) o Intel, estrarre e trascinare «PDF DUO» in Applicazioni. Primo avvio: clic destro › Apri.",
 "Conversioni Word → PDF: PDF DUO usa <b>LibreOffice</b> se installato (il più fedele, gratuito), altrimenti <b>Microsoft Word</b>, altrimenti la propria conversione (impaginazione semplificata). Per i file ODT serve LibreOffice."]),
("2. La finestra", [
 "In alto, a sinistra dei menu: apri, salva, stampa, <b>annulla ↶ / ripristina ↷</b>, <b>zoom − / +</b>, pagina intera, caratteri speciali <b>Ω √</b>.",
 "A sinistra: gli strumenti (selezione, testo, tratto, filo, collegamento, forme, matita, evidenziatore, filo volante, cattura).",
 "A destra: la <b>libreria di simboli</b> (scegliere una categoria o cercare una parola) e il pannello <b>Proprietà</b> dell'elemento selezionato.",
 "<i>Visualizza › Tavolozze</i> mostra o nasconde ogni pannello; <i>Visualizza › Tema</i> e <i>Lingua</i> cambiano aspetto e lingua."]),
("3. Aprire e salvare", [
 "<i>File › Apri</i> accetta PDF, documenti Word / ODT (convertiti automaticamente) e immagini.",
 "I disegni sono salvati in vettoriale nel PDF. Riaprendo il file in PDF DUO, tutto resta modificabile.",
 "<i>File › Esporta un PDF finale</i> produce un PDF appiattito da distribuire."]),
("4. Disegnare uno schema", [
 "Cliccare un simbolo nella libreria, poi sulla pagina per posizionarlo (o trascinare e rilasciare). <b>Esc</b> per finire.",
 "<b>R</b> ruota di 90°, <b>E</b> di 15° (Maiusc = senso opposto), <b>H</b> / <b>V</b> specchiano. Angolo esatto in Proprietà.",
 "La <b>maniglia blu</b> in basso a destra ingrandisce l'elemento in proporzione.",
 "La <b>sigla</b> (KM1, S1…) e i <b>numeri dei morsetti</b> si modificano in Proprietà.",
 "Strumento <b>Filo</b>: un clic per angolo; un clic su un morsetto (piccolo cerchio) collega il filo. Strumento <b>Collegamento</b>: cliccare due morsetti e il tracciato si fa da solo. I fili seguono i simboli spostati.",
 "Elenco <b>Conduttore</b>: colori normalizzati (fase, neutro blu, terra giallo/verde, fibra, Ethernet…). I punti di giunzione si posizionano da soli."]),
("5. Piante di abitazione", [
 "Impostare la <b>scala</b> (1/50, 1/100…) e il passo reale della griglia nella barra <i>Pianta</i>.",
 "Strumento <b>Muro</b>: un clic per angolo, doppio clic per finire. <b>Porta</b>, <b>Porta doppia</b>, <b>Finestra</b>: passare su un muro e l'apertura si allinea.",
 "Strumento <b>Quota</b>: trascinare da un punto all'altro, compare la lunghezza reale. <i>Inserisci › Cartiglio</i> aggiunge il cartiglio."]),
("6. GRAFCET, diagrammi di flusso, mappe mentali", [
 "Posizionare una tappa iniziale, selezionarla e premere <b>Ctrl+G</b>: vengono aggiunte una transizione e la tappa successiva, collegate e numerate.",
 "Doppio clic su una forma per scriverne il testo. <i>Collegamento: curva</i> per le mappe mentali, <i>Freccia</i> per i diagrammi di flusso."]),
("7. Moduli e firma", [
 "Barra <i>Modulo e firma</i>: campo di testo, casella, elenco, pulsante di opzione, area firma, link. Doppio clic per compilare.",
 "Pulsante <b>Firma</b>: disegnare o importare la firma e cliccare dove posizionarla."]),
("8. Testo e caratteri speciali", [
 "Tavolozza di scrittura: carattere, dimensione, grassetto, corsivo, sottolineato, allineamento, colore, evidenziazione.",
 "Pulsante <b>Ω √</b>: Ω, φ, π, Δ, μ, °, ±… Scrivere <code>√{12,5}</code>: la barra della radice copre tutto il numero."]),
("9. Conversioni", ["Menu <i>Conversioni</i>: Word / ODT → PDF, PDF → Word, PDF → ODT, Word ↔ ODT, immagini → PDF, pagine → PNG."]),
("10. Sostenere il progetto", [
 "PDF DUO è gratuito e libero (GNU GPL v3). Una donazione su <b>ko-fi.com/djlatinjazz</b> aiuta a migliorarlo (<i>Aiuto › Fai una donazione</i>).",
 "Sito: deltapassion.github.io/PDF-DUO — Contatto: deltapassion@gmx.com"]),
])
