from typing import Any
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

FORM_CLASS: Any
FORM_CLASS, _ = uic.loadUiType(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "about_dialog.ui"))
)


class AboutDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

    def accept(self):
        self.close()
