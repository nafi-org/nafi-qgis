# -*- coding: utf-8 -*-
from qgis.PyQt import QtWidgets

from .ntrrp_about_dialog_base import Ui_NtrrpAboutDialogBase

class NtrrpAboutDialog(QtWidgets.QDialog, Ui_NtrrpAboutDialogBase):

    def __init__(self, parent=None):
        """Constructor."""
        super(NtrrpAboutDialog, self).__init__(parent)
        self.setupUi(self)

    def accept(self):
        self.close()
