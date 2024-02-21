import os
from typing import Any, Optional

from qgis.core import QgsMapLayer
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from nafi_hires.src.models import Mapping, SegmentationLayer
from nafi_hires.src.services import LayerService

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

        # TODO might try this out
        # self.segmentationLayerComboBox.setItemDelegate(SegmentationLayerDelegate())

        # Handle combo box changes
        self.segmentationLayerComboBox.layerChanged.connect(
            self.segmentationLayerComboBoxChanged
        )

        # Set up active layer handler
        self._layerService.activeMapLayerChanged.connect(self.activeMapLayerChanged)
        self._layerService.layersChanged.connect(self.updateComboBox)

    def mapping(self) -> Mapping:
        return self._mapping

    def setMapping(self, mapping: Mapping) -> None:
        self._mapping = mapping
        self.updateComboBox()

    def segmentationLayerIds(self) -> list[str]:
        mapping = self.mapping()
        return [l.id() for l in mapping.segmentationLayers()] if mapping else []

    def updateComboBox(self) -> None:
        if self.mapping() is None:
            self.segmentationLayerComboBox.setDisabled(True)
            return

        exceptedLayers: list[QgsMapLayer] = self._layerService.layersBy(
            lambda l: l.id() not in self.segmentationLayerIds()
        )
        self.segmentationLayerComboBox.setExceptedLayerList(exceptedLayers)
        self.segmentationLayerComboBox.setEnabled(True)

    def activeMapLayerChanged(self, activeLayer: Optional[QgsMapLayer]) -> None:
        if activeLayer is None or self.mapping() is None:
            return

        if activeLayer.id() in self.segmentationLayerIds():
            self.segmentationLayerComboBox.setLayer(activeLayer)

    def segmentationLayerComboBoxChanged(
        self, layer: Optional[SegmentationLayer]
    ) -> None:
        if layer is None:
            return

        if layer.id() in self.segmentationLayerIds():
            self.mapping().setCurrentSegmentationLayer(layer)
        else:
            self.segmentationLayerComboBox.setLayer(None)
