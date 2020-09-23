# -*- coding: utf-8 -*-
from qgis.PyQt import QtGui, QtWidgets, uic

from .nafi_about_dialog_base import Ui_NafiAboutDialogBase


class NafiAboutDialog(QtWidgets.QDialog, Ui_NafiAboutDialogBase):

    def __init__(self, parent=None):
        """Constructor."""
        super(NafiAboutDialog, self).__init__(parent)

        self.setupUi(self)

    def accept(self):
        self.close()
