from nafi_hires.src.api import HiResApiService, MappingResponse
from nafi_hires.src.utils import HIRES_API_URL
from qgis.core import QgsMapLayer, QgsProject

from .current_mapping_layer import CurrentMappingLayer
from .item import Item
from .mapping_feature_layer import MappingFeatureLayer
from .segmentation_layer import SegmentationLayer


class Mapping(Item):
    """Represent a NAFI HiRes Mapping activity for a particular time period."""

    def __init__(self, region: Item, data: MappingResponse):
        Item.__init__(self)

        self.data = data
        self.api = HiResApiService(HIRES_API_URL)

        self.mappingDate = data.date

        self._segmentationLayerIds: list[str] = [
            sd.uuid for sd in self.api.getIngestedSegmentationDatasets(self.data)
        ]
        self._mappingLayerId: str = self.data.uuid
        self._currentSegmentationLayerId: str = None
        # TODO add this when the current mapping process is implemented as a Celery task
        self._currentMappingLayerId: str = None

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
        return self.data.region

    @property
    def mappingName(self) -> str:
        return self.itemName

    @property
    def regionName(self) -> str:
        return self.data.region

    @property
    def canApprove(self) -> bool:
        """Return True if there are any segmentation features selected."""
        return bool(self.currentSegmentationLayer) and bool(self.mappingLayer)

    # @property
    # def canUpload(self) -> bool:
    #     """Return True if we can upload features."""
    #     return bool(self.workingLayer) and self.workingLayer.featureCount() > 0

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

    @classmethod
    def _lookup(self, id: str) -> QgsMapLayer:
        """Look up a layer by its ID."""
        return None if id is None else QgsProject.instance().mapLayer(id)

    @classmethod
    def _lookupMany(self, ids: list[str]) -> list[QgsMapLayer]:
        """Look up many layers by their IDs."""
        return [self._lookup(id) for id in ids if self._lookup(id) is not None]

    @property
    def segmentationLayers(self) -> list[SegmentationLayer]:
        """Return a list of segmentation layers."""
        return self._lookupMany(self._segmentationLayerIds)

    @segmentationLayers.setter
    def segmentationLayers(self, segmentationLayers: list[SegmentationLayer]) -> None:
        """Set the segmentation layers."""
        self._segmentationLayerIds = [
            sd.uuid for sd in self.api.getIngestedSegmentationDatasets(self.data)
        ]

    @property
    def mappingLayer(self) -> MappingFeatureLayer:
        """Return the working layer."""
        return self._lookup(self._mappingLayerId)

    @mappingLayer.setter
    def mappingLayer(self, mappingLayer: MappingFeatureLayer) -> None:
        """Set the working layer."""
        self._mappingLayer = mappingLayer.id() if mappingLayer else None

    @property
    def currentSegmentationLayer(self) -> SegmentationLayer:
        """Return the current segmentation layer."""
        return self._lookup(self._currentSegmentationLayerId)

    @currentSegmentationLayer.setter
    def currentSegmentationLayer(self, currentSegmentationLayer: SegmentationLayer):
        """Set the current segmentation layer."""
        self._currentSegmentationLayer = (
            currentSegmentationLayer.id() if currentSegmentationLayer else None
        )

    @property
    def currentMappingLayer(self) -> CurrentMappingLayer:
        """Return the current mapping layer."""
        return self._lookup(self._currentMappingLayerId)

    @currentMappingLayer.setter
    def currentMappingLayer(self, currentMappingLayer: CurrentMappingLayer):
        """Set the current mapping layer."""
        self._currentMappingLayerId = (
            currentMappingLayer.id() if currentMappingLayer else None
        )
