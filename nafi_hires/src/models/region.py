from typing import List

from nafi_hires.src.api import MappingResponse
from qgis.core import QgsProject

from .item import Item
from .mapping import Mapping
from .workspace_metadata import WorkspaceMetadata


class Region(Item):
    """Represent a NAFI HiRes Mapping activity for a particular time period."""

    def __init__(
        self,
        data: list[MappingResponse],
        workspaceMetadata: WorkspaceMetadata,
    ):
        Item.__init__(self)
        self.data = data

        self.wmsUrl: str = workspaceMetadata.wmsUrl
        self.owsLayers = workspaceMetadata.owsLayersByRegion(self.regionName)

        self._mappings = [Mapping(self, mapping, workspaceMetadata) for mapping in data]

    @property
    def itemName(self) -> str:
        return self.regionName

    @property
    def regionName(self) -> str:
        return self.data[0].region

    @property
    def item(self):
        """Return the QGIS layer item (in the Layers panel) for this Item."""
        item = self.group.findGroup(self.itemName)
        if item is None:
            self.group.insertGroup(0, self.itemName)
            item = self.group.findGroup(self.itemName)
        return item

    @property
    def groupName(self) -> str:
        """Return the QGIS layer group name for this layer."""
        raise RuntimeError("Region.groupName should not be called")

    @property
    def group(self):
        return QgsProject.instance().layerTreeRoot()

    @property
    def mappingName(self) -> str:
        return self.itemName

    @property
    def mappings(self) -> List[Mapping]:
        """Return a list of all mappings for this region."""
        return list(self._mappings.values())

    @property
    def mappingNames(self) -> List[str]:
        """Return a list of all mapping names for this region."""
        return list(self._mappings.keys())

    def mappingByName(self, mappingName: str) -> Mapping:
        """Return the mapping with the specified name."""
        return self._mappings[mappingName]
