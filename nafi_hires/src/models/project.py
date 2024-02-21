from nafi_hires.src.api import HiResApiService, MappingResponse
from nafi_hires.src.utils import HIRES_API_URL

from .mapping import Mapping
from .region import Region
from .workspace_metadata import WorkspaceMetadata


class Project:
    """Class to specify a remote HiRes project potentially containing layers for several HiRes regions."""

    def __init__(self, workspaceMetadata: WorkspaceMetadata):
        self.workspaceMetadata = workspaceMetadata
        self.api = HiResApiService(HIRES_API_URL)

        # TODO Darwin hard-coded here
        self.data: list[MappingResponse] = self.api.getMappings("Darwin")

        regions = [Region(self.data, workspaceMetadata)]
        self._regions: dict[str, Region] = {
            region.regionName(): region for region in regions
        }

    def mappings(self) -> list[Mapping]:
        """Return a flattened list of all mappings in all regions for this HiRes workspace."""
        return [mapping for region in self.regions() for mapping in region.mappings()]

    def regions(self) -> list[Region]:
        """Return a list of all regions for this HiRes workspace."""
        return list(self._regions.values())

    def regionNames(self) -> list[str]:
        """Return a list of all region names for this HiRes workspace."""
        return list(self._regions.keys())

    def regionByName(self, regionName: str) -> Region:
        """Return the region with the specified name."""
        return self._regions[regionName]
