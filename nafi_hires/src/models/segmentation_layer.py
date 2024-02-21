from qgis.core import (
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsProject,
    QgsVectorTileLayer,
)

from nafi_hires.src.api import SegmentationDatasetResponse
from nafi_hires.src.utils import guiError, resolveStylePath

from .item import Item
from .layer import Layer


class SegmentationLayer(QgsVectorTileLayer, Layer):
    """Layer type for the current NAFI HiRes mapping image."""

    def __init__(self, mapping: Item, data: SegmentationDatasetResponse):
        Layer.__init__(self)

        self.xyzUri = SegmentationLayer.xyzLayerUri(data)

        params = {
            "type": "xyz",
            "url": self.xyzUri,
            "zmin": 6,
            "zmax": 22,
        }
        QgsVectorTileLayer.__init__(
            self,
            "&".join(
                f"{key}={val}" for key, val in params.items()
            ),  # don't URL-encode it
            SegmentationLayer.formattedItemName(data),
        )
        self._mapping = mapping
        self.data = data
        # self.setExtent(QgsRectangle(*segmentationDataset.boundary))

    def mapping(self) -> Item:
        return self._mapping

    def displayName(self) -> str:
        # eg 'T1T2 Threshold 200'
        return SegmentationLayer.displayName(self.data)

    # Layer interface
    def regionName(self) -> str:
        return "Darwin"

    def itemName(self) -> str:
        # eg 'T1T2 Differences (Oct 21–Oct 15) Threshold 200'
        return SegmentationLayer.formattedItemName(self.data)

    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    def groupName(self) -> str:
        # eg 'Mapping (Oct 21)'
        return self.mapping().itemName()

    def group(self) -> QgsLayerTreeGroup:
        return self.mapping().item()

    def subGroupName(self) -> str:
        """Difference group name for this segmentation layer."""
        return SegmentationLayer.differenceGroup(self.data)

    def subGroup(self):
        """Difference group for this segmentation layer."""
        subGroup = self.group().findGroup(self.subGroupName())
        if subGroup is None:
            self.group().insertGroup(0, self.subGroupName())
            subGroup = self.group().findGroup(self.subGroupName())
        return subGroup

    def addMapLayer(self) -> None:
        if self.isValid():
            Layer.addMapLayer(self)

            # load one of two styles based on the threshold used to segment these features
            if self.data.threshold < 200:
                self.loadStyle("lower_threshold_vector_tiles")
            else:
                self.loadStyle("higher_threshold_vector_tiles")
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
    def xyzLayerUri(data: SegmentationDatasetResponse) -> str:
        # url = segmentationDataset.url
        return f"http://localhost:3000/sf_{data.name}/{{z}}/{{x}}/{{y}}"

    @staticmethod
    def difference(data: SegmentationDatasetResponse) -> str:
        # eg 'T1T2'
        return f"T{data.code}•T{data.difference_code}"

    @staticmethod
    def differenceGroup(data: SegmentationDatasetResponse) -> str:
        # eg 'T1T2 Differences (Oct 21–Oct 15)'
        return f"{SegmentationLayer.difference(data)} Differences ({data.date.strftime('%b %d')}–{data.difference_date.strftime('%b %d')})"

    @staticmethod
    def displayName(data: SegmentationDatasetResponse) -> str:
        # eg 'T1T2 Threshold 200'
        return f"{SegmentationLayer.difference(data)} Threshold {data.threshold}"

    @staticmethod
    def formattedItemName(data: SegmentationDatasetResponse) -> str:
        # eg 'T1T2 Differences (Oct 21–Oct 15) Threshold 200'
        return f"{SegmentationLayer.difference(data)} Differences Threshold {data.threshold}"
