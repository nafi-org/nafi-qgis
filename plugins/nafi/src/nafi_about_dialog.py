from qgis.PyQt import QtWidgets

from .nafi_about_dialog_base import Ui_NafiAboutDialogBase
from .utils import NAFI_SUPPORTERS_URL, getNafiSupportersUrl


class NafiAboutDialog(QtWidgets.QDialog, Ui_NafiAboutDialogBase):
    def __init__(self, parent=None):
        super(NafiAboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.aboutLabel.setText(
            self.aboutLabel.text().replace(NAFI_SUPPORTERS_URL, getNafiSupportersUrl())
        )

    def accept(self):
        self.close()
