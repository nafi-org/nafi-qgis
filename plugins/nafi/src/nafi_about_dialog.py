from qgis.PyQt import QtWidgets

from .nafi_about_dialog_base import Ui_NafiAboutDialogBase
from .utils import NAFI_SUPPORTERS_URL, getNafiSupportersUrl, getPluginVersion


class NafiAboutDialog(QtWidgets.QDialog, Ui_NafiAboutDialogBase):
    def __init__(self, parent=None):
        super(NafiAboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.versionLabel.setText(f"Version {getPluginVersion()}")
        self.aboutBrowser.setHtml(
            self.aboutBrowser.toHtml().replace(NAFI_SUPPORTERS_URL, getNafiSupportersUrl())
        )

    def accept(self):
        self.close()
