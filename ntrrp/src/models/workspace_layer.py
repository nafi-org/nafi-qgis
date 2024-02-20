from pathlib import Path

from qgis.core import QgsLayerTreeLayer, QgsProject, QgsRasterLayer

from ntrrp.src.content_metadata_utils import parseContentMetadataDescription
from ntrrp.src.utils import getNtrrpWmtsUrl, guiError

from .layer import Layer
from .region import Region


class WorkspaceLayer(QgsRasterLayer, Layer):
    """Layer type for a NAFI HiRes WMTS layer hosted on GeoServer."""

    def __init__(self, region: Region, owsLayer):
        if owsLayer.children:
            raise ValueError("WMTS layer must be a child layer")

        # weirdly true that URL-encoding of the layer ID does not work correctly
        encodedLayer = owsLayer.id.replace(" ", "%20")
        wmtsUrl = getNtrrpWmtsUrl()
        wmtsParams = f"crs=EPSG:3577&format=image/png&layers={encodedLayer}&url={wmtsUrl}&styles&tileMatrixSet=EPSG:3577"

        QgsRasterLayer.__init__(
            self, wmtsParams, parseContentMetadataDescription(owsLayer), "wms"
        )

        self.owsLayer = owsLayer
        self.region = region

    # Item interface
    @property
    def directory(self) -> Path:
        return self.region.directory

    @property
    def regionName(self) -> str:
        return self.region.regionName

    @property
    def itemName(self) -> str:
        return parseContentMetadataDescription(self.owsLayer)

    @property
    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    @property
    def groupName(self) -> str:
        return self.region.regionName

    def addMapLayer(self) -> None:
        if self.isValid():
            Layer.addMapLayer(self)
        else:
            error = (
                f"An error occurred adding the layer {self.itemName} to the map.\n"
                f"Check your QGIS logs for details."
            )
            guiError(error)
