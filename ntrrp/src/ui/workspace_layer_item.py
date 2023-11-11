from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem

from qgis.core import QgsMapLayer

from ntrrp.src.content_metadata_utils import (
    parseContentMetadataDescription,
    parseContentMetadataRegion,
)
from ntrrp.src.models.workspace_layer import WorkspaceLayer


class WorkspaceLayerItem(QStandardItem):
    def __init__(self, region, owsLayer):
        super(QStandardItem, self).__init__()

        self.setIcon(QIcon(":/plugins/ntrrp/images/globe.png"))

        # assemble some properties
        self.description = parseContentMetadataDescription(owsLayer)
        self.region = parseContentMetadataRegion(owsLayer)

        self.itemLayer = WorkspaceLayer(region, owsLayer)
        self.setText(self.description)

        self.setFlags(Qt.ItemIsEnabled)
        self.setCheckable(False)

        self.restoreLayer()

    def restoreLayer(self):
        """Check if a layer is in the map already and set its icon if it is."""
        layer = self.itemLayer
        if layer is not None and isinstance(layer, QgsMapLayer):
            self.toggleOn(layer)

    def toggleOn(self, layer):
        """Associate this WMS item with an active map layer."""
        if layer is not None and isinstance(layer, QgsMapLayer):
            self.setIcon(QIcon(":/plugins/ntrrp/images/fire.png"))
