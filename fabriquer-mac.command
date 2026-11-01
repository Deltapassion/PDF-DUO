#!/bin/bash
# PDF DUO : fabrication de la version macOS (Apple Silicon ou Intel selon le Mac utilisé)
cd "$(dirname "$0")"
echo "==== PDF DUO : fabrication de la version macOS ===="
if ! command -v python3 >/dev/null; then
  echo "Python 3 n'est pas installé : https://www.python.org/downloads/macos/ puis relancer."; read -n1; exit 1
fi
ARCH=$(uname -m); [ "$ARCH" = "arm64" ] && NAME=AppleSilicon || NAME=Intel
python3 -m venv .venv-build && source .venv-build/bin/activate || exit 1
echo "1/3 Installation des outils…"
pip install -q --upgrade pip && pip install -q -r requirements.txt pyinstaller pillow || { echo "Erreur"; read -n1; exit 1; }
echo "2/3 Fabrication du programme…"
pyinstaller --noconfirm --windowed --name "PDF DUO" --icon pdfduo/icon.png \
  --osx-bundle-identifier io.github.deltapassion.pdfduo \
  --add-data "pdfduo/icon.png:pdfduo" --add-data "pdfduo/notices:pdfduo/notices" \
  --collect-submodules pdf2docx --collect-data pymupdf \
  --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.QtWebEngineWidgets \
  --exclude-module PySide6.QtQuick --exclude-module PySide6.QtQml --exclude-module PySide6.Qt3DCore \
  --exclude-module PySide6.QtMultimedia --exclude-module tkinter pdfduo.py || { echo "Erreur"; read -n1; exit 1; }
echo "3/3 Création de l'archive…"
codesign --force --deep --sign - "dist/PDF DUO.app" 2>/dev/null
rm -f "PDF-DUO-macOS-$NAME.zip"
ditto -c -k --sequesterRsrc --keepParent "dist/PDF DUO.app" "PDF-DUO-macOS-$NAME.zip"
echo; echo "Terminé : PDF-DUO-macOS-$NAME.zip (à envoyer sur la Release GitHub)"
open .
read -n1 -p "Appuie sur une touche pour fermer."
