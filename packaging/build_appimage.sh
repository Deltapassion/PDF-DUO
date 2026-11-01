#!/bin/sh
# Construit PDF-DUO-x86_64.AppImage et PDF-DUO-Linux-x86_64.tar.gz à partir de dist/PDF DUO
set -e
VERSION="${1:-1.0.0}"
# archive portable
tar -C dist -czf PDF-DUO-Linux-x86_64.tar.gz "PDF DUO"
# AppImage
APPDIR=build/AppDir
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps"
cp -r "dist/PDF DUO/." "$APPDIR/usr/bin/"
cat > "$APPDIR/AppRun" <<'SH'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/PDF DUO" "$@"
SH
chmod 755 "$APPDIR/AppRun"
cp packaging/pdf-duo.desktop "$APPDIR/pdf-duo.desktop"
cp packaging/pdf-duo.desktop "$APPDIR/usr/share/applications/"
cp pdfduo/icon.png "$APPDIR/pdf-duo.png"
cp pdfduo/icon.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/pdf-duo.png"
if [ ! -x build/appimagetool ]; then
  wget -q -O build/appimagetool \
    https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage
  chmod +x build/appimagetool
fi
sudo apt-get install -y -qq libfuse2 >/dev/null 2>&1 || true
ARCH=x86_64 VERSION="$VERSION" build/appimagetool --appimage-extract-and-run "$APPDIR" PDF-DUO-x86_64.AppImage
