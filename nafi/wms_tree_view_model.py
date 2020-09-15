# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem, QStandardItemModel 

from owslib.wms import WebMapService
from owslib.map.wms111 import ContentMetadata, WebMapService_1_1_1

from .wms_item import WmsItem

UNWANTED_LAYERS = ["NODATA_RASTER"]

class WmsTreeViewModel(QStandardItemModel):

    def __init__(self, unwantedLayers = UNWANTED_LAYERS):
        """Constructor."""
        super(QStandardItemModel, self).__init__()
        self.unwantedLayers = unwantedLayers
        
    @staticmethod
    def addOwsLayerToTreeViewModel(model, wmsUrl, owsLayer, unwantedLayers = []):
        """Add an OWSLib layer to a QStandardItemModel based structure, potentially with descendant layers and 
        using a list of 'blacklisted' layer names."""
        assert isinstance(model, QStandardItem) or isinstance(model, QStandardItemModel)
        assert isinstance(owsLayer, ContentMetadata)

        if owsLayer.title not in unwantedLayers:
            node = WmsItem(wmsUrl, owsLayer)
            model.appendRow(node)

            # add children to view model
            for childLayer in owsLayer.children:
                WmsTreeViewModel.addOwsLayerToTreeViewModel(node, wmsUrl, childLayer, unwantedLayers)
        else:
            pass

    def setWms(self, wmsUrl):
        """Add an OWSLib WebMapService to this WmsTreeViewModel."""
        wms = WebMapService(wmsUrl)
        assert isinstance(wms, WebMapService_1_1_1)
        # clear all rows
        self.removeRows(0, self.rowCount())
        # the OWSLib structure is not properly organised via its "children" properties, need to fix it up
        owsLayers = [wms.contents[layerName] for layerName in list(wms.contents)]
        # check we've got at least one layer
        assert (len(owsLayers) > 0)
        # calculate our root layer
        rootLayer = WmsTreeViewModel.groupByRootLayers(owsLayers)[0]
        # add layey hierarchy to our tree model
        WmsTreeViewModel.addOwsLayerToTreeViewModel(self, wmsUrl, rootLayer, self.unwantedLayers)

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
            return WmsTreeViewModel.groupByRootLayers(parents.values())    


