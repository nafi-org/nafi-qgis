
from .ntrrp_region import NtrrpRegion
from .ows_utils import parseNtrrpLayerRegion

class NtrrpCapabilities:
    def __init__(self, wmsUrl, owsLayers):
        """Constructor."""
        self.owsLayers = owsLayers
        self.wmsUrl = wmsUrl

        # sort "Darwin", "Katherine" for now
        layersByRegion = {}

        for layer in owsLayers:
            region = parseNtrrpLayerRegion(layer)
            if region is None:
                continue
            if region in layersByRegion:
                layersByRegion[region].append(layer)
            else:
                layersByRegion[region] = [layer]

        self.regions = {region: NtrrpRegion(region, self.wmsUrl, layersByRegion[region]) for region in layersByRegion}


