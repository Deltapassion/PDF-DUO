#!/bin/sh
# Construit pdf-duo_amd64.deb à partir de dist/PDF DUO (PyInstaller)
set -e
VERSION="${1:-1.0.0}"
ROOT=build/deb
rm -rf "$ROOT"
mkdir -p "$ROOT/DEBIAN" "$ROOT/opt/pdf-duo" "$ROOT/usr/bin" "$ROOT/usr/share/applications" "$ROOT/usr/share/pixmaps"
cp -r "dist/PDF DUO/." "$ROOT/opt/pdf-duo/"
cat > "$ROOT/usr/bin/pdf-duo" <<'SH'
#!/bin/sh
exec "/opt/pdf-duo/PDF DUO" "$@"
SH
chmod 755 "$ROOT/usr/bin/pdf-duo"
cp packaging/pdf-duo.desktop "$ROOT/usr/share/applications/"
cp pdfduo/icon.png "$ROOT/usr/share/pixmaps/pdf-duo.png"
cat > "$ROOT/DEBIAN/control" <<CTRL
Package: pdf-duo
Version: $VERSION
Section: graphics
Priority: optional
Architecture: amd64
Maintainer: Jacques Branas <deltapassion@gmx.com>
Suggests: libreoffice
Homepage: https://deltapassion.github.io/PDF-DUO/
Description: PDF, schémas électriques, GRAFCET et plans
 PDF DUO lit, annote, signe et remplit les PDF, dessine des schémas électriques,
 pneumatiques, réseau, des GRAFCET et des plans, et convertit Word / ODF <-> PDF.
CTRL
dpkg-deb --build --root-owner-group "$ROOT" pdf-duo_amd64.deb
