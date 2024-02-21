import os
from typing import Any

from nafi_hires.src.models import Mapping
from nafi_hires.src.services import MappingService
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QWidget

from .about_dialog import AboutDialog

FORM_CLASS: Any
FORM_CLASS, _ = uic.loadUiType(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "mapping_widget.ui"))
)


class MappingWidget(QWidget, FORM_CLASS):
    dataDownloadFinished = pyqtSignal()
    currentMappingDownloadFinished = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self._mapping: Mapping = None
        self.mappingService = MappingService()

    @property
    def dockWidget(self):
        return self.parent()

    @property
    def mapping(self) -> Mapping:
        return self._mapping

    @mapping.setter
    def mapping(self, mapping: Mapping) -> None:
        self._mapping = mapping
        self.segmentationLayerChooser.mapping = mapping

    def updateToolBar(self):
        "Update toolbar buttons based on mapping state."
        self.mappingToolBar.setApproveButtonEnabled(self.mapping.canApprove)
        self.mappingToolBar.setUploadButtonEnabled(self.mapping.canUpload)

    def aboutButtonClicked(self) -> None:
        """Show an About … dialog."""
        aboutDialog = AboutDialog()
        aboutDialog.exec_()

    def approveButtonClicked(self):
        """Copy any segmentation features that are selected to the working layer, 'approving' them."""
        self.mappingService.approveSelectedFeatures(self.mapping)
        self.updateToolBar()

    def currentMappingButtonClicked(self):
        """Download the current mapping data."""
        self.mappingService.downloadCurrentMapping(self.mapping)
        self.updateToolBar()

    def downloadButtonClicked(self):
        """Download the segmentation data."""
        self.mappingService.downloadSegmentationData(self.mapping)
        self.updateToolBar()

    def refreshButtonClicked(self):
        """Refresh the mapping data."""
        self.parent().refreshRemoteWorkspace()  # type: ignore

    def uploadButtonClicked(self):
        """Convert the currently active working layer to a raster, attribute it and upload to NAFI."""
        self.mappingService.processAndUploadBurntAreas(self.mapping)
        self.updateToolBar()
