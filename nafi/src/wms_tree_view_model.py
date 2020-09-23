# -*- coding: utf-8 -*-
from re import sub

from qgis.PyQt.QtCore import Qt, QUrl
from qgis.PyQt.QtGui import QIcon, QStandardItem, QStandardItemModel 
from qgis.PyQt.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from owslib.wms import WebMapService
from owslib.map.wms111 import ContentMetadata, WebMapService_1_1_1

from .utils import guiError, qgsDebug
from .wms_item import WmsItem

UNWANTED_LAYERS = ["NODATA_RASTER"]

class WmsTreeViewModel(QStandardItemModel):

    def __init__(self, wmsUrl, unwantedLayers = UNWANTED_LAYERS):
        """Constructor."""
        super(QStandardItemModel, self).__init__()
        self.httpClient = None
        self.wmsUrl = wmsUrl
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

    def loadWmsUrl(self, additionalItems=[]):
        """Load the remote WMS URL into this WmsTreeViewModel."""
        # we get the WMS 1.1.1 XML because OWSLib actually works with it
        capabilitiesUrl = f"{self.wmsUrl}?request=GetCapabilities&version=1.1.1"
        request = QNetworkRequest(QUrl(capabilitiesUrl))
        self.httpClient = QNetworkAccessManager()
        self.httpClient.finished.connect(lambda r: self.processCapabilities(r, additionalItems))
        self.httpClient.get(request)

    def processCapabilities(self, response, additionalItems=[]):
        """Handle the response from the WMS capabilities request."""
        if response.error() == QNetworkReply.NoError:
            # OWSLib uses etree.readfromstring internally, and for some reason,
            # it can't handle the XML declaration, so it gets hacked off here
            xml = response.readAll().data().decode("utf-8")
            xml = sub("<\\?xml.*\\?>", "", xml)
            self.loadWmsXml(xml, additionalItems)
        else:
            self.connectionError(response.errorString())

    def connectionError(self, logMessage):
        """Raise a connection error."""
        error = (f"Error connecting to NAFI services!\n"
                    f"Check the QGIS NAFI Fire Maps message log for details.")
        guiError(error)
        qgsDebug(logMessage)

    def loadWmsXml(self, wmsXml, additionalItems=[]):
        """Add an OWSLib WebMapService to this WmsTreeViewModel based on the capabilities XML."""
        wms = WebMapService(url=self.wmsUrl, xml=wmsXml)
        assert isinstance(wms, WebMapService_1_1_1)
        # clear all rows
        self.removeRows(0, self.rowCount())
        # the OWSLib structure is not properly organised via its "children" properties, need to fix it up
        owsLayers = [wms.contents[layerName] for layerName in list(wms.contents)]
        # check we've got at least one layer
        assert (len(owsLayers) > 0)
        # calculate our root layer
        rootLayer = WmsTreeViewModel.groupByRootLayers(owsLayers)[0]
        # add layer hierarchy to our tree model
        WmsTreeViewModel.addOwsLayerToTreeViewModel(self, self.wmsUrl, rootLayer, self.unwantedLayers)
        # add some extras if present
        self.loadAdditionalItems(additionalItems)

    def loadAdditionalItems(self, items):
        """Add some additional layers to this WmsTreeViewModel."""
        additionalItemsGroup = QStandardItem()
        additionalItemsGroup.setFlags(Qt.ItemIsEnabled)
        additionalItemsGroup.setText("Additional layers")
        additionalItemsGroup.setIcon(QIcon(":/plugins/nafi/images/folder.png"))

        for item in items:
            assert isinstance(item, QStandardItem)
            additionalItemsGroup.appendRow(item)

        self.appendRow(additionalItemsGroup)

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
