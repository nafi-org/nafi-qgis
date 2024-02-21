from qgis.core import QgsMapLayer, QgsProject

from nafi_hires.src.api import DifferenceResponse, HiResApiService, MappingResponse
from nafi_hires.src.utils import HIRES_API_URL

from .current_mapping_layer import CurrentMappingLayer
from .item import Item
from .mapping_feature_layer import MappingFeatureLayer
from .segmentation_layer import SegmentationLayer
from .workspace_metadata import WorkspaceMetadata


class Mapping(Item):
    """Represent a NAFI HiRes Mapping activity for a particular time period."""

    def __init__(
        self, region: Item, data: MappingResponse, workspaceMetadata: WorkspaceMetadata
    ):
        Item.__init__(self)

        self._region = region
        self.data = data

        self.workspaceMetadata = workspaceMetadata

        self.api = HiResApiService(HIRES_API_URL)

        # Set up empty and populated in MappingService
        self._segmentationLayerIds = []

        self._mappingLayerId: str = None
        self._currentSegmentationLayerId: str = None
        # TODO add this when the current mapping process is implemented as a Celery task
        self._currentMappingLayerId: str = None

    def canApproveFeatures(self) -> bool:
        """Return True if there are any segmentation features selected."""
        return bool(self.currentSegmentationLayer()) and bool(
            self.mappingFeatureLayer()
        )

    def segmentationLayerByMapLayer(self, mapLayer: QgsMapLayer):
        """Retrieve a current segmentation layer from its map layer."""
        return next(
            iter(
                segmentationLayer
                for segmentationLayer in self.segmentationLayers()
                if segmentationLayer.id() == mapLayer.id()
            ),
            None,
        )

    @classmethod
    def _lookup(self, id: str) -> QgsMapLayer:
        """Look up a layer by its ID."""
        return None if id is None else QgsProject.instance().mapLayer(id)

    @classmethod
    def _lookupMany(self, ids: list[str]) -> list[QgsMapLayer]:
        """Look up many layers by their IDs."""
        return [self._lookup(id) for id in ids if self._lookup(id) is not None]

    def segmentationLayers(self) -> list[SegmentationLayer]:
        """Return a list of segmentation layers."""
        return self._lookupMany(self._segmentationLayerIds)

    def setSegmentationLayers(
        self, segmentationLayers: list[SegmentationLayer]
    ) -> None:
        """Set the segmentation layers."""
        self._segmentationLayerIds = [sd.id() for sd in segmentationLayers]

    def mappingFeatureLayer(self) -> MappingFeatureLayer:
        """Return the working layer."""
        return self._lookup(self._mappingLayerId)

    def setMappingFeatureLayer(self, mappingLayer: MappingFeatureLayer) -> None:
        """Set the working layer."""
        self._mappingLayer = mappingLayer.id() if mappingLayer else None

    def currentSegmentationLayer(self) -> SegmentationLayer:
        """Return the current segmentation layer."""
        return self._lookup(self._currentSegmentationLayerId)

    def setCurrentSegmentationLayer(self, currentSegmentationLayer: SegmentationLayer):
        """Set the current segmentation layer."""
        self._currentSegmentationLayerId = (
            currentSegmentationLayer.id() if currentSegmentationLayer else None
        )

    def currentMappingLayer(self) -> CurrentMappingLayer:
        """Return the current mapping layer."""
        return self._lookup(self._currentMappingLayerId)

    def setCurrentMappingLayer(self, currentMappingLayer: CurrentMappingLayer):
        """Set the current mapping layer."""
        self._currentMappingLayerId = (
            currentMappingLayer.id() if currentMappingLayer else None
        )

    # Item interface
    def regionName(self) -> str:
        return self._region.regionName()

    def itemName(self) -> str:
        return f"Mapping ({self.data.date.strftime('%b %d')})"

    def item(self):
        item = self.group().findGroup(self.itemName())
        if item is None:
            self.group().insertGroup(0, self.itemName())
            item = self.group().findGroup(self.itemName())
        return item

    def groupName(self) -> str:
        """Return the QGIS layer group name for this layer."""
        return self._region.itemName()
