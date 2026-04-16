from typing import Any
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS: Any
FORM_CLASS, _ = uic.loadUiType(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "mapping_tool_bar.ui"))
)


class MappingToolBar(QWidget, FORM_CLASS):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self.aboutButton.clicked.connect(self.parent().aboutButtonClicked)
        self.approveButton.clicked.connect(self.parent().approveButtonClicked)
        self.currentMappingButton.clicked.connect(
            self.parent().currentMappingButtonClicked
        )
        self.downloadButton.clicked.connect(self.parent().downloadButtonClicked)
        self.refreshButton.clicked.connect(self.parent().refreshButtonClicked)
        self.uploadButton.clicked.connect(self.parent().uploadButtonClicked)

    def setApproveButtonEnabled(self, enabled: bool) -> None:
        self.approveButton.setEnabled(enabled)

    def setUploadButtonEnabled(self, enabled: bool) -> None:
        self.uploadButton.setEnabled(enabled)
