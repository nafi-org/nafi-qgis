from collections import defaultdict
from typing import List

from owslib.map.wms111 import ContentMetadata
from qgis.PyQt.QtCore import QObject

from nafi_hires.src.content_metadata_utils import parseContentMetadataRegion


class WorkspaceMetadata(QObject):
    """Class representing the WMS URL and remote WMS layers for a NAFI HiRes workspace."""

    def __init__(self, wmsUrl: str, owsLayers: List[ContentMetadata]):
        QObject.__init__(self)
        self.wmsUrl: str = wmsUrl
        self.owsLayers: List[ContentMetadata] = owsLayers

        self._owsLayersByRegion = defaultdict(list)
        for layer in self.owsLayers:
            region = parseContentMetadataRegion(layer)
            if region is None:
                continue
            self._owsLayersByRegion[region].append(layer)

        self.regionNames = sorted(self._owsLayersByRegion.keys())

    def owsLayersByRegion(self, regionName: str) -> List[ContentMetadata]:
        """Return the list of layers for the specified region."""
        return self._owsLayersByRegion[regionName]
