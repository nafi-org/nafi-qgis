from pathlib import Path

from ntrrp.src.utils import ensureDirectory

from .region import Region
from .workspace_metadata import WorkspaceMetadata


class Project:
    """Class to specify a remote HiRes project potentially containing layers for several HiRes regions."""

    def __init__(self, projectDirectory: Path, workspaceMetadata: WorkspaceMetadata):
        self.directory = projectDirectory
        self.workspaceMetadata = workspaceMetadata

        regionNames = self.workspaceMetadata.regionNames

        for regionName in self.workspaceMetadata.regionNames:
            regionDirectory = Path(self.directory, regionName)
            ensureDirectory(regionDirectory)

        self._regions = {
            regionName: Region(Path(self.directory, regionName), workspaceMetadata)
            for regionName in regionNames
        }

    @property
    def mappings(self):
        """Return a flattened list of all mappings in all regions for this HiRes workspace."""
        return [mapping for region in self.regions for mapping in region.mappings]

    @property
    def regions(self):
        """Return a list of all regions for this HiRes workspace."""
        return list(self._regions.values())

    @property
    def regionNames(self):
        """Return a list of all region names for this HiRes workspace."""
        return list(self._regions.keys())

    def regionByName(self, regionName: str) -> Region:
        """Return the region with the specified name."""
        return self._regions[regionName]
