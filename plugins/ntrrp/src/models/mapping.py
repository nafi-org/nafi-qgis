import re

from datetime import datetime
from pathlib import Path

from qgis.core import QgsMapLayer

from .current_mapping_layer import CurrentMappingLayer
from .item import Item
from .segmentation_layer import SegmentationLayer
from .working_layer import WorkingLayer


class Mapping(Item):
    """Represent a NAFI Hires Mapping activity for a particular time period."""

    def __init__(self, region: Item, mappingDirectory: Path):
        Item.__init__(self)

        self._directory: Path = mappingDirectory
        self.region = region

        match = re.match(r"(\d{4})(\d{2})(\d{2})", mappingDirectory.name)
        assert match is not None

        self.mappingDate: datetime = datetime(
            int(match.group(1)), int(match.group(2)), int(match.group(3))
        )
        self.segmentationLayers: list[SegmentationLayer] = []
        self.workingLayer: WorkingLayer = None
        self.currentSegmentationLayer: SegmentationLayer = None
        self.currentMappingLayer: CurrentMappingLayer = None

    @property
    def directory(self) -> Path:
        return self._directory

    @property
    def segmentationDirectory(self) -> Path:
        return Path(self.directory, "Segmentation")

    @property
    def itemName(self) -> str:
        return f"Mapping ({self.mappingDate.strftime('%b %d')})"

    @property
    def item(self):
        item = self.group.findGroup(self.itemName)
        if item is None:
            self.group.insertGroup(0, self.itemName)
            item = self.group.findGroup(self.itemName)
        return item

    @property
    def groupName(self) -> str:
        """Return the QGIS layer group name for this layer."""
        return self.region.regionName

    @property
    def mappingName(self) -> str:
        return self.itemName

    @property
    def regionName(self) -> str:
        return self.region.regionName

    @property
    def canApprove(self) -> bool:
        """Return True if there are any segmentation features selected."""
        return bool(self.currentSegmentationLayer) and bool(self.workingLayer)

    @property
    def canUpload(self) -> bool:
        """Return True if we can upload features."""
        return bool(self.workingLayer) and self.workingLayer.featureCount() > 0

    def segmentationLayerByMapLayer(self, mapLayer: QgsMapLayer):
        """Retrieve a current segmentation layer from its map layer."""
        return next(
            iter(
                segmentationLayer
                for segmentationLayer in self.segmentationLayers
                if segmentationLayer.id() == mapLayer.id()
            ),
            None,
        )
