# -*- coding: utf-8 -*-
# Figures de la notice : {lang: {index_section: [ (images, légende, [repères numérotés]) ]}}
# images : un nom (pleine largeur) ou une liste de noms (côte à côte)
L = ("fr", "en", "es", "pt", "de", "it")
def tr(*v): return dict(zip(L, v))

SCREEN = [
 tr("Barre rapide : ouvrir, enregistrer, imprimer, annuler, rétablir, zoom − / +, caractères Ω √", "Quick bar: open, save, print, undo, redo, zoom − / +, Ω √ characters", "Barra rápida: abrir, guardar, imprimir, deshacer, rehacer, zoom − / +, caracteres Ω √", "Barra rápida: abrir, guardar, imprimir, desfazer, refazer, zoom − / +, caracteres Ω √", "Schnellleiste: öffnen, speichern, drucken, rückgängig, wiederholen, Zoom − / +, Zeichen Ω √", "Barra rapida: apri, salva, stampa, annulla, ripristina, zoom − / +, caratteri Ω √"),
 tr("Menus", "Menus", "Menús", "Menus", "Menüs", "Menu"),
 tr("Outils de dessin", "Drawing tools", "Herramientas de dibujo", "Ferramentas de desenho", "Zeichenwerkzeuge", "Strumenti di disegno"),
 tr("Couleur, épaisseur, conducteur, type de liaison, flèche", "Colour, width, conductor, connection type, arrow", "Color, grosor, conductor, tipo de conexión, flecha", "Cor, espessura, condutor, tipo de ligação, seta", "Farbe, Strichstärke, Leiter, Verbindungsart, Pfeil", "Colore, spessore, conduttore, tipo di collegamento, freccia"),
 tr("Palette d'écriture : police, taille, gras, couleur, surligneur", "Writing palette: font, size, bold, colour, highlighter", "Paleta de escritura: fuente, tamaño, negrita, color, resaltador", "Paleta de escrita: tipo de letra, tamanho, negrito, cor, marcador", "Schreibpalette: Schrift, Größe, fett, Farbe, Textmarker", "Tavolozza di scrittura: carattere, dimensione, grassetto, colore, evidenziatore"),
 tr("Bibliothèque de symboles (catégories et recherche)", "Symbol library (categories and search)", "Biblioteca de símbolos (categorías y búsqueda)", "Biblioteca de símbolos (categorias e pesquisa)", "Symbolbibliothek (Kategorien und Suche)", "Libreria di simboli (categorie e ricerca)"),
 tr("Propriétés de l'élément sélectionné", "Properties of the selected item", "Propiedades del elemento seleccionado", "Propriedades do elemento selecionado", "Eigenschaften des ausgewählten Elements", "Proprietà dell'elemento selezionato"),
 tr("Pages (miniatures) et onglet Formulaire", "Pages (thumbnails) and Form tab", "Páginas (miniaturas) y pestaña Formulario", "Páginas (miniaturas) e separador Formulário", "Seiten (Miniaturen) und Registerkarte Formular", "Pagine (miniature) e scheda Modulo"),
 tr("La page de travail", "The working page", "La página de trabajo", "A página de trabalho", "Die Arbeitsseite", "La pagina di lavoro"),
]
F = {lang: {} for lang in L}
def add(sec, imgs, cap, legend=()):
    for lang in L:
        F[lang].setdefault(sec, []).append((imgs, cap[lang], [x[lang] for x in legend]))

add(1, "01-ecran.jpg", tr("La fenêtre de PDF DUO", "The PDF DUO window", "La ventana de PDF DUO", "A janela do PDF DUO", "Das Fenster von PDF DUO", "La finestra di PDF DUO"), SCREEN)
add(4, "02-symbole.jpg", tr("Un symbole sélectionné et ses propriétés", "A selected symbol and its properties", "Un símbolo seleccionado y sus propiedades", "Um símbolo selecionado e as suas propriedades", "Ein ausgewähltes Symbol und seine Eigenschaften", "Un simbolo selezionato e le sue proprietà"), [
 tr("Symbole sélectionné (cadre pointillé) : poignée bleue en bas à droite pour l'agrandir", "Selected symbol (dotted frame): blue handle at the bottom right to enlarge it", "Símbolo seleccionado (marco punteado): tirador azul abajo a la derecha para ampliarlo", "Símbolo selecionado (moldura tracejada): pega azul em baixo à direita para o ampliar", "Ausgewähltes Symbol (gepunkteter Rahmen): blauer Griff unten rechts zum Vergrößern", "Simbolo selezionato (cornice tratteggiata): maniglia blu in basso a destra per ingrandirlo"),
 tr("Rotation, miroir, couleur, épaisseur, taille, repère KM1 et sa position", "Rotation, mirror, colour, width, size, KM1 label and its position", "Rotación, espejo, color, grosor, tamaño, referencia KM1 y su posición", "Rotação, espelho, cor, espessura, tamanho, referência KM1 e a sua posição", "Drehung, Spiegeln, Farbe, Strichstärke, Größe, Kennzeichnung KM1 und ihre Position", "Rotazione, specchio, colore, spessore, dimensione, sigla KM1 e sua posizione"),
 tr("Choix de la catégorie de symboles", "Choice of the symbol category", "Elección de la categoría de símbolos", "Escolha da categoria de símbolos", "Auswahl der Symbolkategorie", "Scelta della categoria di simboli"),
])
add(4, "03-fils.jpg", tr("Fils, liaisons et couleurs de conducteurs", "Wires, connections and conductor colours", "Cables, conexiones y colores de conductores", "Fios, ligações e cores dos condutores", "Leitungen, Verbindungen und Leiterfarben", "Fili, collegamenti e colori dei conduttori"), [
 tr("Outils Fil et Liaison", "Wire and Connection tools", "Herramientas Cable y Conexión", "Ferramentas Fio e Ligação", "Werkzeuge Leitung und Verbindung", "Strumenti Filo e Collegamento"),
 tr("Couleur normalisée du conducteur", "Standard conductor colour", "Color normalizado del conductor", "Cor normalizada do condutor", "Genormte Leiterfarbe", "Colore normalizzato del conduttore"),
])
add(5, "04-plan.jpg", tr("Plan d'une chambre au 1/50 : murs, porte, fenêtre, prises, cotes", "Plan of a bedroom at 1:50: walls, door, window, sockets, dimensions", "Plano de un dormitorio a 1/50: muros, puerta, ventana, enchufes, cotas", "Planta de um quarto a 1/50: paredes, porta, janela, tomadas, cotas", "Grundriss eines Schlafzimmers 1:50: Wände, Tür, Fenster, Steckdosen, Maße", "Pianta di una camera in scala 1:50: muri, porta, finestra, prese, quote"), [
 tr("Outils Mur, Cote, Porte, Porte double, Fenêtre", "Wall, Dimension, Door, Double door, Window tools", "Herramientas Muro, Cota, Puerta, Puerta doble, Ventana", "Ferramentas Parede, Cota, Porta, Porta dupla, Janela", "Werkzeuge Wand, Bemaßung, Tür, Doppeltür, Fenster", "Strumenti Muro, Quota, Porta, Porta doppia, Finestra"),
])
add(6, "05-grafcet.jpg", tr("Un GRAFCET : étapes, transitions, actions", "A GRAFCET: steps, transitions, actions", "Un GRAFCET: etapas, transiciones, acciones", "Um GRAFCET: etapas, transições, ações", "Ein GRAFCET: Schritte, Übergänge, Aktionen", "Un GRAFCET: tappe, transizioni, azioni"), [
 tr("Catégorie GRAFCET de la bibliothèque", "GRAFCET category of the library", "Categoría GRAFCET de la biblioteca", "Categoria GRAFCET da biblioteca", "Kategorie GRAFCET der Bibliothek", "Categoria GRAFCET della libreria"),
])
add(6, "06-reseau.jpg", tr("Schéma réseau CIEL (vidéosurveillance, fibre) — thème bleu nuit", "CIEL network diagram (CCTV, fibre) — midnight blue theme", "Esquema de red (videovigilancia, fibra) — tema azul noche", "Esquema de rede (videovigilância, fibra) — tema azul-noite", "Netzwerkplan (Videoüberwachung, Glasfaser) — Design Nachtblau", "Schema di rete (videosorveglianza, fibra) — tema blu notte"))
add(7, "07-formulaire.jpg", tr("Champs de formulaire remplissables", "Fillable form fields", "Campos de formulario rellenables", "Campos de formulário preenchíveis", "Ausfüllbare Formularfelder", "Campi modulo compilabili"), [
 tr("Barre Formulaire et signature", "Form and signature toolbar", "Barra Formulario y firma", "Barra Formulário e assinatura", "Leiste Formular und Unterschrift", "Barra Modulo e firma"),
 tr("Panneau Formulaire : tous les champs et leurs valeurs", "Form panel: all fields and their values", "Panel Formulario: todos los campos y sus valores", "Painel Formulário: todos os campos e valores", "Feld Formular: alle Felder und ihre Werte", "Pannello Modulo: tutti i campi e i loro valori"),
])
add(7, "08-signature.jpg", tr("La fenêtre Signature", "The Signature window", "La ventana Firma", "A janela Assinatura", "Das Fenster Unterschrift", "La finestra Firma"))
add(8, "09-texte.jpg", tr("Texte avec caractères spéciaux et racine sur tout le nombre", "Text with special characters and a root over the whole number", "Texto con caracteres especiales y raíz sobre todo el número", "Texto com caracteres especiais e raiz sobre todo o número", "Text mit Sonderzeichen und Wurzel über der ganzen Zahl", "Testo con caratteri speciali e radice su tutto il numero"))
add(10, "10-conversions.jpg", tr("Le menu Conversions", "The Conversions menu", "El menú Conversiones", "O menu Conversões", "Das Menü Konvertierung", "Il menu Conversioni"))
add(11, ["11-aide.jpg", "12-don.jpg"], tr("Menu Aide et fenêtre de don", "Help menu and donation window", "Menú Ayuda y ventana de donación", "Menu Ajuda e janela de donativo", "Menü Hilfe und Spendenfenster", "Menu Aiuto e finestra di donazione"))

add(2, "13-plein-ecran.jpg", tr("Le mode présentation : la page sur tout l'écran, avec les outils et la bibliothèque", "Presentation mode: the page full screen, with the tools and the library", "Modo presentación: la página a pantalla completa, con las herramientas y la biblioteca", "Modo de apresentação: a página em ecrã inteiro, com as ferramentas e a biblioteca", "Präsentationsmodus: die Seite im Vollbild, mit Werkzeugen und Bibliothek", "Modalità presentazione: la pagina a schermo intero, con strumenti e libreria"), [
 tr("Outils d'écriture et de dessin", "Writing and drawing tools", "Herramientas de escritura y dibujo", "Ferramentas de escrita e desenho", "Schreib- und Zeichenwerkzeuge", "Strumenti di scrittura e disegno"),
 tr("Bibliothèque réduite à deux colonnes", "Library narrowed to two columns", "Biblioteca reducida a dos columnas", "Biblioteca reduzida a duas colunas", "Bibliothek auf zwei Spalten verkleinert", "Libreria ridotta a due colonne"),
])
add(2, "14-plein-ecran-menu.jpg", tr("Souris en haut de l'écran : les menus et le zoom réapparaissent", "Mouse at the top of the screen: menus and zoom reappear", "Ratón en el borde superior: reaparecen los menús y el zoom", "Rato no topo do ecrã: os menus e o zoom reaparecem", "Maus am oberen Rand: Menüs und Zoom erscheinen", "Mouse in cima allo schermo: ricompaiono menu e zoom"), [
 tr("Menus et barre rapide : zoom − / +, page entière, annuler, ⛶ pour quitter", "Menus and quick bar: zoom − / +, whole page, undo, ⛶ to exit", "Menús y barra rápida: zoom − / +, página completa, deshacer, ⛶ para salir", "Menus e barra rápida: zoom − / +, página inteira, desfazer, ⛶ para sair", "Menüs und Schnellleiste: Zoom − / +, ganze Seite, rückgängig, ⛶ zum Beenden", "Menu e barra rapida: zoom − / +, pagina intera, annulla, ⛶ per uscire"),
])

add(4, "15-solaire.jpg", tr("Installation solaire en site isolé : schéma technologique", "Off-grid solar installation: wiring diagram", "Instalación solar aislada: esquema tecnológico", "Instalação solar isolada: esquema tecnológico", "Solare Inselanlage: Anschlussplan", "Impianto solare isolato: schema tecnologico"), [
 tr("Catégories Énergie solaire de la bibliothèque", "Solar energy categories of the library", "Categorías Energía solar de la biblioteca", "Categorias Energia solar da biblioteca", "Kategorien Solarenergie der Bibliothek", "Categorie Energia solare della libreria"),
])
add(4, "16-organigramme.jpg", tr("Organigramme d'entreprise pour le rapport de stage", "Company organisation chart for the internship report", "Organigrama de empresa para el informe de prácticas", "Organograma da empresa para o relatório de estágio", "Firmenorganigramm für den Praktikumsbericht", "Organigramma aziendale per la relazione di stage"))

add(4, "21-prevention.jpg", tr("Prévention électrique, manutention, logistique, dentaire, outils", "Electrical safety, handling, logistics, dental, tools", "Prevención eléctrica, manipulación, logística, dental, herramientas", "Prevenção elétrica, manuseamento, logística, dentário, ferramentas", "Elektrische Sicherheit, Handhabung, Logistik, Zahntechnik, Werkzeuge", "Prevenzione elettrica, movimentazione, logistica, dentale, utensili"), [
 tr("Choisir la catégorie dans la bibliothèque", "Choose the category in the library", "Elegir la categoría en la biblioteca", "Escolher a categoria na biblioteca", "Kategorie in der Bibliothek wählen", "Scegliere la categoria nella libreria"),
])
add(9, "17-tableau.jpg", tr("Un tableau avec calculs : les totaux sont des formules", "A table with calculations: the totals are formulas", "Una tabla con cálculos: los totales son fórmulas", "Uma tabela com cálculos: os totais são fórmulas", "Eine Tabelle mit Berechnungen: die Summen sind Formeln", "Una tabella con calcoli: i totali sono formule"), [
 tr("Menu Tableau", "Table menu", "Menú Tabla", "Menu Tabela", "Menü Tabelle", "Menu Tabella"),
 tr("Taille du tableau et bouton « Modifier le tableau »", "Table size and “Edit table” button", "Tamaño de la tabla y botón «Editar la tabla»", "Tamanho da tabela e botão «Editar a tabela»", "Tabellengröße und Schaltfläche „Tabelle bearbeiten“", "Dimensioni della tabella e pulsante «Modifica la tabella»"),
])
add(9, "18-tableau-edition.jpg", tr("L'édition du tableau (double-clic) : lignes, colonnes, fusion, formules", "Editing the table (double-click): rows, columns, merge, formulas", "Edición de la tabla (doble clic): filas, columnas, combinar, fórmulas", "Edição da tabela (duplo clique): linhas, colunas, unir, fórmulas", "Tabelle bearbeiten (Doppelklick): Zeilen, Spalten, verbinden, Formeln", "Modifica della tabella (doppio clic): righe, colonne, unione, formule"))
add(9, ["19-calculatrice.jpg", "20-graphique.jpg"], tr("La calculatrice scientifique et son onglet Graphique", "The scientific calculator and its Graph tab", "La calculadora científica y su pestaña Gráfico", "A calculadora científica e o separador Gráfico", "Der wissenschaftliche Rechner und die Registerkarte Graph", "La calcolatrice scientifica e la scheda Grafico"))

add(4, "22-favoris.jpg", tr("Les favoris en tête de la bibliothèque", "Favourites at the top of the library", "Los favoritos al principio de la biblioteca", "Os favoritos no topo da biblioteca", "Favoriten oben in der Bibliothek", "I preferiti in cima alla libreria"), [
 tr("Catégorie ★ Favoris", "★ Favourites category", "Categoría ★ Favoritos", "Categoria ★ Favoritos", "Kategorie ★ Favoriten", "Categoria ★ Preferiti"),
 tr("Clic droit sur un symbole : ajouter aux favoris ou les retirer", "Right-click a symbol: add to or remove from favourites", "Clic derecho en un símbolo: añadir o quitar de favoritos", "Clique direito num símbolo: adicionar ou remover dos favoritos", "Rechtsklick auf ein Symbol: zu Favoriten hinzufügen oder entfernen", "Clic destro su un simbolo: aggiungere o togliere dai preferiti"),
])
add(4, "23-etats.jpg", tr("Équipements à états : station de pompage, réglages dans Propriétés", "Equipment with states: pumping station, settings in Properties", "Equipos con estados: estación de bombeo, ajustes en Propiedades", "Equipamentos com estados: estação de bombagem, ajustes em Propriedades", "Geräte mit Zuständen: Pumpstation, Einstellungen in Eigenschaften", "Apparecchiature con stati: stazione di pompaggio, regolazioni in Proprietà"), [
 tr("Niveau du puits, niveau du château d'eau, pompe en marche ou arrêtée", "Well level, water tower level, pump running or stopped", "Nivel del pozo, nivel del depósito, bomba en marcha o parada", "Nível do poço, nível do reservatório, bomba a funcionar ou parada", "Brunnenstand, Wasserturmstand, Pumpe ein oder aus", "Livello del pozzo, livello della torre, pompa in funzione o ferma"),
])
