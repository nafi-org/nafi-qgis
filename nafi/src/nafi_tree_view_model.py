# -*- coding: utf-8 -*-
import re

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem, QStandardItemModel 

from owslib.wms import WebMapService
from owslib.map.wms111 import ContentMetadata, WebMapService_1_1_1

from .wms_item import WmsItem

UNWANTED_LAYERS = ["NODATA_RASTER"]

class NafiTreeViewModel(QStandardItemModel):

    def __init__(self, unwantedLayers = UNWANTED_LAYERS):
        """Constructor."""
        super(QStandardItemModel, self).__init__()
        self.unwantedLayers = unwantedLayers

    def loadWms(self, wmsUrl, wmsXml, additionalItems=[]):
        """Add an OWSLib WebMapService to this NafiTreeViewModel based on the capabilities XML."""
        
        # OWSLib uses etree.readfromstring internally, and for some reason,
        # it can't handle the XML declaration, so it gets hacked off here
        wmsXml = re.sub("<\\?xml.*\\?>", "", wmsXml)
        wms = WebMapService(url=wmsUrl, xml=wmsXml)
        assert isinstance(wms, WebMapService_1_1_1)
        
        # clear all rows
        self.removeRows(0, self.rowCount())
        # the OWSLib structure is not properly organised via its "children" properties, need to fix it up
        owsLayers = [wms.contents[layerName] for layerName in list(wms.contents)]
        # check we've got at least one layer
        assert (len(owsLayers) > 0)
        # calculate our root layer
        rootLayer = NafiTreeViewModel.groupByRootLayers(owsLayers)[0]
        # add layer hierarchy to our tree model
        NafiTreeViewModel.addOwsLayerToTreeViewModel(self, wmsUrl, rootLayer, self.unwantedLayers)
        # add some extras if present
        self.loadAdditionalItems(additionalItems)

    def loadAdditionalItems(self, items):
        """Add some additional layers to this NafiTreeViewModel."""
        additionalItemsGroup = QStandardItem()
        additionalItemsGroup.setFlags(Qt.ItemIsEnabled)
        additionalItemsGroup.setText("Additional layers")
        additionalItemsGroup.setIcon(QIcon(":/plugins/nafi/images/folder.png"))

        for item in items:
            assert isinstance(item, QStandardItem)
            additionalItemsGroup.appendRow(item)

        self.appendRow(additionalItemsGroup)

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
                NafiTreeViewModel.addOwsLayerToTreeViewModel(node, wmsUrl, childLayer, unwantedLayers)
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
            return NafiTreeViewModel.groupByRootLayers(parents.values())    
