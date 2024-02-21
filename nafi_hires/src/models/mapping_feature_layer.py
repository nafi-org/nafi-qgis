from qgis.core import (
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsProject,
    QgsVectorTileLayer,
)

from nafi_hires.src.api import MappingResponse
from nafi_hires.src.utils import guiError, qgsDebug, resolveStylePath

from .item import Item
from .layer import Layer


class MappingFeatureLayer(QgsVectorTileLayer, Layer):

    @classmethod
    def xyzLayerUri(cls, data: MappingResponse) -> str:
        return f"{data.url}/{{z}}/{{x}}/{{y}}"

    def __init__(self, mapping: Item):

        self.mapping = mapping

        self.data: MappingResponse = mapping.data
        if not self.data.published:
            qgsDebug("Segmentation dataset is not published")

        Layer.__init__(self)

        self.xyzUri = self.xyzLayerUri(self.data)

        params = {
            "type": "xyz",
            "url": self.xyzUri,
            "zmin": 6,
            "zmax": 22,
        }
        # Init QgsVectorTileLayer
        QgsVectorTileLayer.__init__(
            self,
            "&".join(
                f"{key}={val}" for key, val in params.items()
            ),  # don't URL-encode it
            self.mapping.itemName,
        )

        # Target segmentation layer is not initially set
        self._segmentationLayerId = None

    def approveFeatures(self):
        """Approve the selected features in this layer."""
        pass

    def addMapLayer(self):
        """Add an HiRes data layer to the map."""
        if self.isValid():
            Layer.addMapLayer(self)
            self.loadStyle("approved")
            self.item.setName(self.itemName)
        else:
            error = (
                f"An error occurred adding the layer {self.itemName} to the map.\n"
                f"Check your QGIS logs for details."
            )
            guiError(error)

    @property
    def regionName(self) -> str:
        return self.data.region

    @property
    def itemName(self):
        """Get an appropriate map layer name for this layer."""
        return f"{self.mapping.itemName} - Burnt Areas"

    @property
    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    @property
    def groupName(self) -> str:
        return self.mapping.itemName

    @property
    def group(self) -> QgsLayerTreeGroup:
        return self.mapping.item

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        self.loadNamedStyle(stylePath)
