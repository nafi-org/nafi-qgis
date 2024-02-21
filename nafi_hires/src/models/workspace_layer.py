from qgis.core import QgsLayerTreeLayer, QgsProject, QgsRasterLayer

from nafi_hires.src.content_metadata_utils import parseContentMetadataDescription
from nafi_hires.src.utils import getHiResWmtsUrl, guiError

from .layer import Layer
from .region import Region


class WorkspaceLayer(QgsRasterLayer, Layer):
    """Layer type for a NAFI HiRes WMTS layer hosted on GeoServer."""

    def __init__(self, region: Region, owsLayer):
        if owsLayer.children:
            raise ValueError("WMTS layer must be a child layer")

        # Weirdly true that standard URL-encoding of the layer ID does not work correctly
        encodedLayer = owsLayer.id.replace(" ", "%20")
        wmtsUrl = getHiResWmtsUrl()
        wmtsParams = f"crs=EPSG:3577&format=image/png&layers={encodedLayer}&url={wmtsUrl}&styles&tileMatrixSet=EPSG:3577"

        QgsRasterLayer.__init__(
            self, wmtsParams, parseContentMetadataDescription(owsLayer), "wms"
        )

        self.owsLayer = owsLayer
        self.region = region

    # Layer interface
    def regionName(self) -> str:
        return self.region.regionName()

    def itemName(self) -> str:
        return parseContentMetadataDescription(self.owsLayer)

    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    def groupName(self) -> str:
        return self.region.regionName()

    def addMapLayer(self) -> None:
        if self.isValid():
            Layer.addMapLayer(self)
        else:
            error = (
                f"An error occurred adding the layer {self.itemName()} to the map.\n"
                f"Check your QGIS logs for details."
            )
            guiError(error)
