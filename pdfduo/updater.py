"""Recherche d'une nouvelle version de PDF DUO sur GitHub et installation.

- Au démarrage (si internet répond, sans bloquer la fenêtre) : si une version plus récente est publiée,
  PDF DUO propose de l'installer.
- Windows : l'installeur est téléchargé puis lancé ; PDF DUO se ferme pour le laisser faire.
- macOS / Linux : la page de téléchargement s'ouvre dans le navigateur.
"""
import os
import re
import sys
import json
import tempfile

from PySide6.QtCore import QObject, QUrl, Qt, QSettings, QTimer
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QPushButton, QApplication
from PySide6.QtGui import QDesktopServices

from .i18n import T

API_URL = "https://api.github.com/repos/Deltapassion/PDF-DUO/releases/latest"
PAGE_URL = "https://github.com/Deltapassion/PDF-DUO/releases/latest"
WIN_ASSET = "PDF-DUO-Windows-Setup.exe"


def version_tuple(s):
    """'Version_1_3_2', 'v1.3.2', '1.3.2' -> (1, 3, 2)."""
    nums = re.findall(r"\d+", s or "")
    return tuple(int(n) for n in nums[:3]) if nums else ()


class Updater(QObject):
    def __init__(self, win, current_version):
        super().__init__(win)
        self.win = win
        self.current = current_version
        from PySide6.QtNetwork import QNetworkProxyFactory
        QNetworkProxyFactory.setUseSystemConfiguration(True)   # proxy du lycée éventuel
        self.net = QNetworkAccessManager(self)
        self.settings = QSettings("Jacques Branas", "PDF DUO")
        self._reply = None
        self._dl = None
        self._progress = None
        self._manual = False

    # ------------------------------------------------------------ réglage
    def auto_enabled(self):
        return str(self.settings.value("maj_auto", "true")).lower() != "false"

    def set_auto(self, on):
        self.settings.setValue("maj_auto", "true" if on else "false")

    # ------------------------------------------------------------ recherche
    def check(self, manual=False):
        """manual=True : menu Aide (on affiche aussi « déjà à jour » ou l'erreur)."""
        if self._reply is not None:
            return
        self._manual = manual
        req = QNetworkRequest(QUrl(API_URL))
        req.setRawHeader(b"Accept", b"application/vnd.github+json")
        req.setRawHeader(b"User-Agent", b"PDF-DUO")
        req.setTransferTimeout(8000)
        self._reply = self.net.get(req)
        self._reply.finished.connect(self._checked)

    def _checked(self):
        r, self._reply = self._reply, None
        r.deleteLater()
        if r.error() != QNetworkReply.NoError:
            if self._manual:            # pas d'internet : silence au démarrage, message seulement à la demande
                QMessageBox.information(self.win, "PDF DUO", T("Impossible de joindre le site des versions. Vérifiez la connexion à internet."))
            return
        try:
            data = json.loads(bytes(r.readAll()).decode("utf-8"))
        except ValueError:
            return
        tag = data.get("tag_name", "")
        latest = version_tuple(tag)
        if not latest or latest <= version_tuple(self.current):
            if self._manual:
                QMessageBox.information(self.win, "PDF DUO", T("PDF DUO est à jour (version {v}).").replace("{v}", self.current))
            return
        if not self._manual and self.settings.value("maj_ignoree", "") == tag:
            return
        shown = ".".join(str(n) for n in latest)
        asset = next((a for a in data.get("assets", []) if a.get("name") == WIN_ASSET), None)
        self._propose(tag, shown, asset)

    def _propose(self, tag, shown, asset):
        box = QMessageBox(self.win)
        box.setWindowTitle("PDF DUO")
        box.setIcon(QMessageBox.Information)
        box.setText(T("Une nouvelle version de PDF DUO est disponible : {new} (vous avez la {cur}).")
                    .replace("{new}", shown).replace("{cur}", self.current))
        windows = sys.platform.startswith("win") and asset is not None
        box.setInformativeText(T("Voulez-vous l'installer maintenant ? PDF DUO se fermera pendant l'installation ; "
                                 "enregistrez d'abord votre travail.") if windows else
                               T("Voulez-vous ouvrir la page de téléchargement ?"))
        b_ok = box.addButton(T("Installer") if windows else T("Ouvrir la page"), QMessageBox.AcceptRole)
        b_later = box.addButton(T("Plus tard"), QMessageBox.RejectRole)
        b_skip = box.addButton(T("Ignorer cette version"), QMessageBox.DestructiveRole)
        box.setDefaultButton(b_ok)
        box.exec()
        c = box.clickedButton()
        if c is b_skip:
            self.settings.setValue("maj_ignoree", tag)
        elif c is b_ok:
            if windows:
                self._download(asset.get("browser_download_url"))
            else:
                QDesktopServices.openUrl(QUrl(PAGE_URL))

    # ------------------------------------------------------------ téléchargement (Windows)
    def _download(self, url):
        if not url:
            QDesktopServices.openUrl(QUrl(PAGE_URL))
            return
        if hasattr(self.win, "maybe_save") and not self.win.maybe_save():
            return
        req = QNetworkRequest(QUrl(url))
        req.setRawHeader(b"User-Agent", b"PDF-DUO")
        req.setAttribute(QNetworkRequest.RedirectPolicyAttribute, QNetworkRequest.NoLessSafeRedirectPolicy)
        self._dl = self.net.get(req)
        self._progress = QProgressDialog(T("Téléchargement de la nouvelle version…"), T("Annuler"), 0, 100, self.win)
        self._progress.setWindowTitle("PDF DUO")
        self._progress.setWindowModality(Qt.WindowModal)
        self._progress.setMinimumDuration(0)
        self._progress.canceled.connect(self._dl.abort)
        self._dl.downloadProgress.connect(self._on_progress)
        self._dl.finished.connect(self._downloaded)

    def _on_progress(self, got, total):
        if self._progress is not None and total > 0:
            self._progress.setValue(int(got * 100 / total))

    def _downloaded(self):
        r, self._dl = self._dl, None
        r.deleteLater()
        if self._progress is not None:
            self._progress.close()
            self._progress = None
        if r.error() != QNetworkReply.NoError:
            if r.error() != QNetworkReply.OperationCanceledError:
                QMessageBox.warning(self.win, "PDF DUO", T("Le téléchargement a échoué. La page de téléchargement va s'ouvrir."))
                QDesktopServices.openUrl(QUrl(PAGE_URL))
            return
        path = os.path.join(tempfile.gettempdir(), WIN_ASSET)
        try:
            with open(path, "wb") as f:
                f.write(bytes(r.readAll()))
            os.startfile(path)          # noqa: lance l'installeur (Windows)
        except OSError:
            QDesktopServices.openUrl(QUrl(PAGE_URL))
            return
        if hasattr(self.win, "_skip_close_check"):
            self.win._skip_close_check = True
        QTimer.singleShot(300, self.win.close)
