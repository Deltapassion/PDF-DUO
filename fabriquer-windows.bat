@echo off
chcp 65001 >nul
title PDF DUO - fabrication de la version Windows
cd /d "%~dp0"
echo.
echo  ==== PDF DUO : fabrication de la version Windows ====
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo  Python n'est pas installe.
  echo  Installe-le depuis https://www.python.org/downloads/ en cochant "Add Python to PATH",
  echo  puis relance ce fichier.
  pause
  exit /b 1
)
echo  1/3 Installation des outils (quelques minutes la premiere fois)...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt pyinstaller pillow || goto erreur
echo.
echo  2/3 Fabrication du programme...
python -m PyInstaller --noconfirm --windowed --name "PDF DUO" --icon packaging\icon.ico ^
  --add-data "pdfduo/icon.png:pdfduo" --add-data "pdfduo/notices:pdfduo/notices" ^
  --collect-submodules pdf2docx --collect-data pymupdf ^
  --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.QtWebEngineWidgets ^
  --exclude-module PySide6.QtQuick --exclude-module PySide6.QtQml --exclude-module PySide6.Qt3DCore ^
  --exclude-module PySide6.QtMultimedia --exclude-module tkinter pdfduo.py || goto erreur
copy /y README.md "dist\PDF DUO\" >nul
copy /y LICENSE "dist\PDF DUO\" >nul
echo.
echo  3/3 Creation des fichiers a publier...
if exist PDF-DUO-Windows.zip del PDF-DUO-Windows.zip
powershell -NoProfile -Command "Compress-Archive -Path 'dist\PDF DUO' -DestinationPath 'PDF-DUO-Windows.zip'" || goto erreur
set ISCC=
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set ISCC="%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set ISCC="%ProgramFiles%\Inno Setup 6\ISCC.exe"
if defined ISCC (
  %ISCC% /DMyVersion=1.0.0 packaging\pdfduo.iss >nul && move /y packaging\Output\PDF-DUO-Windows-Setup.exe . >nul
  echo  Installeur cree : PDF-DUO-Windows-Setup.exe
) else (
  echo  Pour obtenir aussi l'installeur .exe, installer Inno Setup 6 ^(gratuit : jrsoftware.org^) puis relancer.
)
echo.
echo  Termine. Fichiers a envoyer sur la Release GitHub :
dir /b PDF-DUO-Windows*.*
echo.
pause
exit /b 0
:erreur
echo.
echo  Une erreur s'est produite : envoie une capture de cette fenetre a Claude.
pause
exit /b 1
