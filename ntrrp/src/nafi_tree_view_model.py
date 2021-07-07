# -*- coding: utf-8 -*-
from collections import OrderedDict
import re

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem, QStandardItemModel 

from owslib.etree import etree
from owslib.map.wms111 import ContentMetadata 

from .utils import capabilitiesError, qgsDebug
from .wms_item import WmsItem

UNWANTED_LAYERS = ["NODATA_RASTER"]

class NafiTreeViewModel(QStandardItemModel):

    def __init__(self, unwantedLayers = UNWANTED_LAYERS):
        """Constructor."""
        super(QStandardItemModel, self).__init__()
        self.unwantedLayers = unwantedLayers

    def loadWms(self, wmsUrl, wmsXml, additionalItems=[]):
        """Add an OWSLib WebMapService to this NafiTreeViewModel based on the capabilities XML."""

        # etree.fromstring internally for some reason can't handle the XML declaration, 
        # so it gets hacked off here
        wmsXml = re.sub("<\\?xml.*\\?>", "", wmsXml)
        contents = OrderedDict()

        try: 
            parser = etree.XMLParser(dtd_validation=False, load_dtd=False, no_network=True, recover=True, resolve_entities=False)
            capabilities = etree.fromstring(wmsXml, parser)

            capabilityElement = capabilities.find("Capability")

            if capabilityElement is None: 
                raise RuntimeError("Missing 'Capability' Element in parsed XML capabilities")

            # recursively gather content metadata for all layer elements, this is stolen 
            # from OWSLib because it won't let us configure the parser the way we need to
            # to avoid unwanted network activity, entity resolutions etc
            # see https://github.com/geopython/OWSLib/blob/8a94500c2137082dfc4e59acd15389312bcb63fb/owslib/map/wms111.py#L113
            
            # TODO merge this gather with the other tree manipulation functions below
            
            def gatherLayers(parentElement, parentMetadata):
                layers = []
                for index, elem in enumerate(parentElement.findall('Layer')):
                    cm = ContentMetadata(elem, parent=parentMetadata,
                                            index=index + 1,
                                            parse_remote_metadata=False)
                    if cm.id:
                        layers.append(cm)
                        contents[cm.id] = cm
                    cm.children = gatherLayers(elem, cm)
                return layers
            gatherLayers(capabilityElement, None)
        
        except (etree.ParserError, RuntimeError) as pe:
            capabilitiesError(str(pe), wmsXml)
            return

        # clear all rows
        self.removeRows(0, self.rowCount())
        # the OWSLib structure is not properly organised via its "children" properties, need to fix it up
        owsLayers = [contents[layerName] for layerName in list(contents)]
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
        additionalItemsGroup.setIcon(QIcon(":/plugins/ntrrp/images/folder.png"))

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
