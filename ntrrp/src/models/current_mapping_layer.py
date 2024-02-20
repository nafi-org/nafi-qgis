from pathlib import Path

from qgis.core import QgsLayerTreeGroup, QgsLayerTreeLayer, QgsProject, QgsRasterLayer

from ntrrp.src.utils import guiError

from .item import Item
from .layer import Layer


class CurrentMappingLayer(QgsRasterLayer, Layer):
    """Layer type for the current NAFI HiRes mapping image."""

    def __init__(self, mapping: Item, rasterPath: Path):
        self.rasterPath = Path(rasterPath)
        QgsRasterLayer.__init__(
            self,
            self.rasterPath.as_posix(),
            f"{mapping.regionName} Current Mapping",
            "gdal",
        )

        self.mapping = mapping

    # Item interface
    @property
    def directory(self) -> Path:
        return self.mapping.directory

    @property
    def regionName(self) -> str:
        return self.mapping.regionName

    @property
    def itemName(self) -> str:
        return f"{self.mapping.regionName} Current Mapping"

    @property
    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    @property
    def groupName(self) -> str:
        return self.mapping.itemName

    @property
    def group(self) -> QgsLayerTreeGroup:
        return self.mapping.item

    def addMapLayer(self) -> None:
        if self.isValid():
            Layer.addMapLayer(self)
        else:
            error = (
                f"An error occurred adding the layer {self.itemName} to the map.\n"
                f"Check your QGIS logs for details."
            )
            guiError(error)
