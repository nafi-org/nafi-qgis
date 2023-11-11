from pathlib import Path

from qgis.core import QgsLayerTreeGroup, QgsLayerTreeLayer, QgsProject, QgsVectorLayer

from ntrrp.src.utils import guiError, resolveStylePath

from .item import Item
from .layer import Layer
from .segmentation_metadata import SegmentationMetadata


class SegmentationLayer(QgsVectorLayer, Layer):
    """Layer type for the current NAFI Hires mapping image."""

    def __init__(self, mapping: Item, shapefilePath: Path):
        Layer.__init__(self)

        segmentationMetadata = SegmentationMetadata(shapefilePath)
        QgsVectorLayer.__init__(
            self,
            shapefilePath.as_posix(),
            f"{segmentationMetadata.difference} Threshold {segmentationMetadata.threshold}",
            "ogr",
        )

        self.segmentationMetadata = segmentationMetadata
        self.shapefilePath = shapefilePath
        self.mapping = mapping

    # Item interface
    @property
    def directory(self) -> Path:
        return self.shapefilePath.parent

    @property
    def regionName(self) -> str:
        return self.mapping.regionName

    # Forwarded SegmentationMetadata properties
    @property
    def threshold(self):
        return self.segmentationMetadata.threshold

    @property
    def endDate(self):
        return self.segmentationMetadata.endDate

    @property
    def startDate(self):
        return self.segmentationMetadata.startDate

    @property
    def differenceGroup(self):
        return self.segmentationMetadata.differenceGroup

    @property
    def displayName(self) -> str:
        return f"{self.segmentationMetadata.difference} Threshold {self.segmentationMetadata.threshold}"

    @property
    def itemName(self) -> str:
        return f"{self.segmentationMetadata.difference} Threshold {self.segmentationMetadata.threshold}"

    @property
    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    @property
    def groupName(self) -> str:
        return self.mapping.itemName

    @property
    def group(self) -> QgsLayerTreeGroup:
        return self.mapping.item

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
                    self.loadStyle("lower_threshold")
                else:
                    self.loadStyle("higher_threshold")
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
