from qgis.core import QgsLayerTreeGroup, QgsLayerTreeLayer, QgsProject, QgsRasterLayer

from nafi_hires.src.api import MappingResponse
from nafi_hires.src.utils import guiError

from .item import Item
from .layer import Layer


class CurrentMappingLayer(QgsRasterLayer, Layer):
    """Layer type for the current NAFI HiRes mapping image."""

    def __init__(self, mapping: Item, data: MappingResponse):
        self._mapping = mapping
        self.data: MappingResponse = data

        QgsRasterLayer.__init__(
            self,
            self.data.current_mapping_dataset.url,
            f"{mapping.regionName()} Current Mapping",
            "wms",
        )

    # Layer interface
    def regionName(self) -> str:
        return self._mapping.regionName()

    def itemName(self) -> str:
        return f"{self._mapping.regionName()} Current Mapping"

    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    def groupName(self) -> str:
        return self._mapping.itemName()

    def group(self) -> QgsLayerTreeGroup:
        return self._mapping.item()

    def addMapLayer(self) -> None:
        if self.isValid():
            Layer.addMapLayer(self)
        else:
            error = (
                f"An error occurred adding the layer {self.itemName()} to the map.\n"
                f"Check your QGIS logs for details."
            )
            guiError(error)
