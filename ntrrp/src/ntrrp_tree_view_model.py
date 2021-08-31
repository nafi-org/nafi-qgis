# -*- coding: utf-8 -*-
# from collections import OrderedDict
# import re
from .ntrrp_capabilities import NtrrpCapabilities

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem, QStandardItemModel

from owslib.etree import etree
from owslib.map.wms111 import ContentMetadata

from .ntrrp_capabilities import NtrrpCapabilities
from .utils import capabilitiesError, qgsDebug
from .ntrrp_item import NtrrpItem

UNWANTED_LAYERS = ["NODATA_RASTER"]

class NtrrpTreeViewModel(QStandardItemModel):

    def __init__(self, unwantedLayers = UNWANTED_LAYERS):
        """Constructor."""
        super(QStandardItemModel, self).__init__()
        self.unwantedLayers = unwantedLayers
        self.owsLayers = []
        self.region = ""

    def setRegion(self, region, ntrrpCapabilities):
        """Set the current region for the NTRRP layer model."""
        assert isinstance(ntrrpCapabilities, NtrrpCapabilities)
        assert isinstance(region, str)

        self.region = region

        # clear all rows
        self.removeRows(0, self.rowCount())
        # calculate our root layer
        rootLayer = NtrrpTreeViewModel.groupByRootLayers(ntrrpCapabilities.owsLayers)[0]
        # recursively add layer hierarchy to our tree model
        for childLayer in rootLayer.children:
            NtrrpTreeViewModel.addOwsLayerToTreeViewModel(self, region, ntrrpCapabilities.wmsUrl, childLayer, self.unwantedLayers)

    @staticmethod
    def addOwsLayerToTreeViewModel(model, region, wmsUrl, owsLayer, unwantedLayers = []):
        """Add an OWSLib layer to a QStandardItemModel based structure, potentially with descendant layers and
        using a list of 'blacklisted' layer names."""
        qgsDebug("owsLayer: " + str(owsLayer))
        assert isinstance(model, QStandardItem) or isinstance(model, QStandardItemModel)
        assert isinstance(owsLayer, ContentMetadata)

        if owsLayer.title not in unwantedLayers:
            layerRegion = NtrrpCapabilities.parseNtrrpLayerRegion(owsLayer)
            if layerRegion == region: 
                node = NtrrpItem(wmsUrl, owsLayer)
                model.appendRow(node)
                # add children to view model
                for childLayer in owsLayer.children:
                    NtrrpTreeViewModel.addOwsLayerToTreeViewModel(node, region, wmsUrl, childLayer, unwantedLayers)
        else:
            pass


    @staticmethod
    def groupByRootLayers(layers):
        """Reconstruct the parent-child relationships in an OWSLib ContentMetadata tree."""
        parents = {}
        for layer in layers:
            parent = layer.parent
            # process a child layer
            if layer.parent is not None:
                if not parent.children:
                    parent.children = []
                if layer.parent.title not in parents:
                    parents[parent.title] = parent
                if not any(c.title == layer.title for c in parent.children):
                    layer.parent.children.append(layer)
            # retain any root layers
            else:
                parents[layer.title] = layer

        # if all parents are root layers, return
        if all(map(lambda l: l.parent is None, parents.values())):
            return list(parents.values())
        # otherwise recurse
        else:
            return NtrrpTreeViewModel.groupByRootLayers(parents.values())    
