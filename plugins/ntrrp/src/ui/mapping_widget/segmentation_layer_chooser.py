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
        self.layerService = LayerService()

        self.segmentationLayerComboBox.setAllowEmptyLayer(False)

        # Handle combo box changes
        self.segmentationLayerComboBox.layerChanged.connect(
            self.segmentationLayerComboBoxChanged
        )

        # Set up active layer handler
        self.layerService.activeMapLayerChanged.connect(self.activeMapLayerChanged)
        self.layerService.layersChanged.connect(self.updateExceptedLayersList)

    @property
    def segmentationLayerIds(self) -> list[str]:
        if self._mapping is None:
            return []
        return [layer.id() for layer in self._mapping.segmentationLayers]

    @property
    def mapping(self) -> Mapping:
        return self._mapping

    @mapping.setter
    def mapping(self, mapping: Mapping) -> None:
        self._mapping = mapping

        if self._mapping is None:
            self.segmentationLayerComboBox.setDisabled(True)
            return

        self.segmentationLayerComboBox.setEnabled(True)
        self.updateExceptedLayersList()

    @property
    def exceptedLayers(self) -> list[QgsMapLayer]:
        return self.layerService.layersBy(
            lambda layer: layer.id() not in self.segmentationLayerIds
        )

    def updateExceptedLayersList(self, _: list[QgsMapLayer] = None) -> None:
        self.segmentationLayerComboBox.setExceptedLayerList(self.exceptedLayers)

    def activeMapLayerChanged(self, layer: Optional[QgsMapLayer]) -> None:
        if layer is None:
            return

        if layer.id() in self.segmentationLayerIds:
            self.segmentationLayerComboBox.setLayer(layer)

    def segmentationLayerComboBoxChanged(
        self, layer: Optional[SegmentationLayer]
    ) -> None:
        if layer is None:
            return

        if layer.id() in self.segmentationLayerIds:
            self.mapping.currentSegmentationLayer = layer
        else:
            self.segmentationLayerComboBox.setLayer(None)
