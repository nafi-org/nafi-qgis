# -*- coding: utf-8 -*-
from .ntrrp_mapping import NtrrpMapping
from .ows_utils import parseNtrrpLayerRegion


class NtrrpCapabilities:
    def __init__(self, wmsUrl, owsLayers):
        """Constructor."""
        self.owsLayers = owsLayers
        self.wmsUrl = wmsUrl

        layersByRegion = {}

        for layer in owsLayers:
            region = parseNtrrpLayerRegion(layer.title)
            if region is None:
                continue
            if region in layersByRegion:
                layersByRegion[region].append(layer)
            else:
                layersByRegion[region] = [layer]

        # sort "Darwin", "Katherine" for now
        regions = sorted(layersByRegion.keys())

        # python3 dicts are sorted in insertion order
        self.mappings = {
            region: NtrrpMapping(region, self.wmsUrl, layersByRegion[region]) for region in regions
        }
