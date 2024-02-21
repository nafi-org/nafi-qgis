from qgis.core import (
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsProject,
    QgsVectorTileLayer,
)

from nafi_hires.src.api import MappingResponse
from nafi_hires.src.utils import guiError, resolveStylePath

from .item import Item
from .layer import Layer


class MappingFeatureLayer(QgsVectorTileLayer, Layer):

    def __init__(self, mapping: Item, data: MappingResponse):
        Layer.__init__(self)

        self._mapping = mapping
        self.data: MappingResponse = data
        # Target segmentation layer is not initially set
        self._segmentationLayerId = None

        self.xyzUri = MappingFeatureLayer.xyzLayerUri(data)

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
            self._mapping.itemName(),
        )

    def approveFeatures(self):
        """Approve the selected features in this layer."""
        pass

    # Layer interface
    def regionName(self) -> str:
        return self.data.region

    def itemName(self):
        """Get an appropriate map layer name for this layer."""
        return f"{self._mapping.itemName()} - Burnt Areas"

    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    def groupName(self) -> str:
        return self._mapping.itemName()

    def group(self) -> QgsLayerTreeGroup:
        return self._mapping.item()

    def addMapLayer(self):
        """Add an HiRes data layer to the map."""
        if self.isValid():
            Layer.addMapLayer(self)
            self.loadStyle("approved")
            self.item().setName(self.itemName())
        else:
            error = (
                f"An error occurred adding the layer {self.itemName()} to the map.\n"
                f"Check your QGIS logs for details."
            )
            guiError(error)

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        self.loadNamedStyle(stylePath)

    @staticmethod
    def xyzLayerUri(data: MappingResponse) -> str:
        return f"{data.url}/{{z}}/{{x}}/{{y}}"
