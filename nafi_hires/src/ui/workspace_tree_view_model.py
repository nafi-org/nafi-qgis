from owslib.map.wms111 import ContentMetadata
from qgis.PyQt.QtGui import QStandardItemModel

from nafi_hires.src.models import Region

from .workspace_layer_item import WorkspaceLayerItem

UNWANTED_LAYERS = ["NODATA_RASTER"]


class WorkspaceTreeViewModel(QStandardItemModel):
    def __init__(self, unwantedLayers=UNWANTED_LAYERS):
        super(QStandardItemModel, self).__init__()
        self.unwantedLayers = unwantedLayers
        self.owsLayers: list[ContentMetadata] = []
        self._region: Region = None

    def regionName(self) -> str:
        return self.region().regionName()

    def region(self) -> Region:
        return self._region

    def setRegion(self, region: Region) -> None:
        self._region = region
        self.refresh()

    def refresh(self) -> None:
        # Clear all rows in the model
        self.removeRows(0, self.rowCount())

        # Append an item for each layer in the region
        if self.region() is None:
            return

        for owsLayer in self.region().owsLayers:
            self.appendRow(WorkspaceLayerItem(self.region(), owsLayer))
