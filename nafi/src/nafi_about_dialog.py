from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtWidgets import QLayout

from .nafi_about_dialog_base import Ui_NafiAboutDialogBase


class NafiAboutDialog(QtWidgets.QDialog, Ui_NafiAboutDialogBase):
    def __init__(self, parent=None):
        super(NafiAboutDialog, self).__init__(parent)
        self.setupUi(self)

    def accept(self):
        self.close()
