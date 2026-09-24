from qgis.PyQt import QtWidgets, uic

from .utils import NAFI_SUPPORTERS_URL, getNafiSupportersUrl, getPluginVersion, resolvePluginPath

FORM_CLASS, _ = uic.loadUiType(resolvePluginPath("ui/nafi_about_dialog_base.ui"))


class NafiAboutDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(NafiAboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.versionLabel.setText(f"Version {getPluginVersion()}")
        self.aboutBrowser.setHtml(
            self.aboutBrowser.toHtml().replace(NAFI_SUPPORTERS_URL, getNafiSupportersUrl())
        )

    def accept(self):
        self.close()
