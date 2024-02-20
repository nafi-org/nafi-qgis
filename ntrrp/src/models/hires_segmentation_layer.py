from pathlib import Path

from qgis.core import (
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsProject,
    QgsRectangle,
    QgsVectorLayer,
    QgsVectorTileLayer,
)

from ntrrp.hires_client.models import SegmentationDatasetResponse
from ntrrp.src.utils import guiError, resolveStylePath

# from .item import Item
from .layer import Layer

# from .segmentation_metadata import SegmentationMetadata


class HiResSegmentationLayer(QgsVectorTileLayer, Layer):
    """Layer type for the current NAFI HiRes mapping image."""

    @classmethod
    def xyzLayerUri(cls, segmentationDataset: SegmentationDatasetResponse) -> str:
        # url = segmentationDataset.get("uri", None)
        return f"http://localhost:3000/sf_{segmentationDataset.name}/{{z}}/{{x}}/{{y}}"

    def __init__(self, segmentationDataset: SegmentationDatasetResponse):
        if not segmentationDataset.published:
            raise ValueError("Segmentation dataset is not published")

        Layer.__init__(self)

        self.xyzUri = self.xyzLayerUri(segmentationDataset)

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
            segmentationDataset.name,
        )

        self.segmentationMetadata = segmentationDataset
        self.setExtent(QgsRectangle(*segmentationDataset.boundary))

    @property
    def directory(self) -> Path:
        return self.shapefilePath.parent

    @property
    def regionName(self) -> str:
        return "Darwin"

    # Forwarded SegmentationMetadata properties
    @property
    def threshold(self):
        return self.segmentationMetadata.threshold

    @property
    def endDate(self):
        return self.segmentationMetadata.difference_date

    @property
    def startDate(self):
        return self.segmentationMetadata.date

    @property
    def differenceGroup(self):
        return f"T{self.segmentationMetadata.code}T{self.segmentationMetadata.difference_code}"

    @property
    def displayName(self) -> str:
        return f"{self.differenceGroup} Threshold {self.segmentationMetadata.threshold}"

    @property
    def itemName(self) -> str:
        return f"{self.differenceGroup} Threshold {self.segmentationMetadata.threshold}"

    @property
    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    @property
    def groupName(self) -> str:
        return "Test"

    @property
    def group(self) -> QgsLayerTreeGroup:
        return QgsProject.instance().layerTreeRoot()

    @property
    def subGroupName(self) -> str:
        """dMIRBI difference group name for this workspace layer."""
        return self.differenceGroup

    @property
    def subGroup(self):
        """dMIRBI difference group for this workspace layer."""
        subGroup = self.group.findGroup(self.subGroupName)
        if subGroup is None:
            self.group.insertGroup(0, self.subGroupName)
            subGroup = self.group.findGroup(self.subGroupName)
        return subGroup

    def addMapLayer(self) -> None:
        if self.isValid():
            Layer.addMapLayer(self)

            # load one of two styles based on the threshold used to segment these features
            if self.segmentationMetadata.threshold is not None:
                if int(self.segmentationMetadata.threshold) < 200:
                    self.loadStyle("lower_threshold_vector_tiles")
                else:
                    self.loadStyle("higher_threshold_vector_tiles")
        else:
            error = (
                f"An error occurred adding the layer {self.itemName} to the map.\n"
                f"Check your QGIS logs for details."
            )
            guiError(error)

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        self.loadNamedStyle(stylePath)
