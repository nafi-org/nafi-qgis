from typing import Any, Optional
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsMapLayer

from ntrrp.src.models import Mapping, SegmentationLayer
from ntrrp.src.services import LayerService

FORM_CLASS: Any
FORM_CLASS, _ = uic.loadUiType(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "segmentation_layer_chooser.ui")
    )
)


class SegmentationLayerChooser(QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self._mapping: Mapping = None
        self._layerService = LayerService()

        self.segmentationLayerComboBox.setAllowEmptyLayer(False)

        # Handle combo box changes
        self.segmentationLayerComboBox.layerChanged.connect(
            self.segmentationLayerComboBoxChanged
        )

        # Set up active layer handler
        self._layerService.activeMapLayerChanged.connect(self.activeMapLayerChanged)
        self._layerService.layersChanged.connect(self.updateComboBox)

    @property
    def mapping(self) -> Mapping:
        return self._mapping

    @mapping.setter
    def mapping(self, mapping: Mapping) -> None:
        self._mapping = mapping
        self.updateComboBox()

    def _segmentationLayerIds(self) -> list[str]:
        return [l.id() for l in self._mapping.segmentationLayers]

    def updateComboBox(self) -> None:
        if self._mapping is None:
            self.segmentationLayerComboBox.setDisabled(True)
            return

        exceptedLayers: list[QgsMapLayer] = self._layerService.layersBy(
            lambda l: l.id() not in self._segmentationLayerIds()
        )
        self.segmentationLayerComboBox.setExceptedLayerList(exceptedLayers)
        self.segmentationLayerComboBox.setEnabled(True)

    def activeMapLayerChanged(self, activeLayer: Optional[QgsMapLayer]) -> None:
        if activeLayer is None or self._mapping is None:
            return

        if activeLayer.id() in self._segmentationLayerIds():
            self.segmentationLayerComboBox.setLayer(activeLayer)

    def segmentationLayerComboBoxChanged(
        self, layer: Optional[SegmentationLayer]
    ) -> None:
        if layer is None:
            return

        if layer.id() in self._segmentationLayerIds:
            self.mapping.currentSegmentationLayer = layer
        else:
            self.segmentationLayerComboBox.setLayer(None)
