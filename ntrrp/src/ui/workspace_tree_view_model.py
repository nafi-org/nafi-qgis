from qgis.PyQt.QtGui import QStandardItemModel
from owslib.map.wms111 import ContentMetadata

from ntrrp.src.models import Region
from .workspace_layer_item import WorkspaceLayerItem

UNWANTED_LAYERS = ["NODATA_RASTER"]


class WorkspaceTreeViewModel(QStandardItemModel):
    def __init__(self, unwantedLayers=UNWANTED_LAYERS):
        super(QStandardItemModel, self).__init__()
        self.unwantedLayers = unwantedLayers
        self.owsLayers: list[ContentMetadata] = []
        self._region: Region = None

    @property
    def regionName(self) -> str:
        return self._region.regionName

    @property
    def region(self) -> Region:
        return self._region

    @region.setter
    def region(self, region: Region) -> None:
        self._region = region
        self.refresh()

    def refresh(self) -> None:
        # Clear all rows in the model
        self.removeRows(0, self.rowCount())

        # Append an item for each layer in the region
        if self._region is None:
            return

        for owsLayer in self._region.owsLayers:
            self.appendRow(WorkspaceLayerItem(self._region, owsLayer))
