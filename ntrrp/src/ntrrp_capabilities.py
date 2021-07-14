import re

from owslib.map.wms111 import ContentMetadata

from .utils import qgsDebug

class NtrrpCapabilities:
    def __init__(self, wmsUrl, owsLayers):
        """Constructor."""
        self.wmsUrl = wmsUrl
        self.owsLayers = owsLayers
        # get all the regions from all layers
        regions = [NtrrpCapabilities.parseNtrrpLayerRegion(l) for l in self.owsLayers]
        self.regions = list(set([r for r in regions if r is not None]))
        qgsDebug(str(self.regions))

    @staticmethod
    def parseNtrrpLayerRegion(owsLayer):
        """Parse the NTRRP region from a WMS or WMTS layer title. The expected format is T1T2 Difference Image [Darwin_T20210628_dMIRBI_T20210623]."""
        assert isinstance(owsLayer, ContentMetadata)

        match = re.match("^.*\[(.*)\].*$", owsLayer.title)
        if match is not None:
            ntrrpMeta = match.group(1)
            ntrrpMetaElements = ntrrpMeta.split("_")
            if len(ntrrpMetaElements) > 0: 
                return ntrrpMetaElements[0]
        # nothing was found 
        return None
    
    @staticmethod
    def parseNtrrpLayerDescription(owsLayer):
        """Parse the NTRRP description from a WMS or WMTS layer title. The expected format is T1T2 Difference Image [Darwin_T20210628_dMIRBI_T20210623]."""
        assert isinstance(owsLayer, ContentMetadata)

        match = re.match("^(.*)\[.*\].*$", owsLayer.title)
        if match is not None:
            return match.group(1)
        # nothing was found 
        return None
