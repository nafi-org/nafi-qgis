
from .ntrrp_region import NtrrpRegion
from .ows_utils import parseNtrrpLayerRegion

class NtrrpCapabilities:
    def __init__(self, wmsUrl, owsLayers):
        """Constructor."""
        self.owsLayers = owsLayers
        self.wmsUrl = wmsUrl

        layersByRegion = {}

        for layer in owsLayers:
            region = parseNtrrpLayerRegion(layer)
            if region is None:
                continue
            if region in layersByRegion:
                layersByRegion[region].append(layer)
            else:
                layersByRegion[region] = [layer]

        # sort "Darwin", "Katherine" for now
        regions = list(layersByRegion.keys())
        regions.sort()

        # python3 dicts are sorted in insertion order
        self.regions = {region: NtrrpRegion(region, self.wmsUrl, layersByRegion[region]) for region in regions}


