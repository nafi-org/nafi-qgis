# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsProject

from .ntrrp_data_client import NtrrpDataClient
from .layer.current_mapping_layer import CurrentMappingLayer
from .layer.source_layer import SourceLayer
from .layer.working_layer import WorkingLayer
from .ntrrp_item import NtrrpItem
from .utils import getNtrrpDataUrl, guiWarning, qgsDebug

class NtrrpRegion(QObject):
    # emit this signal when the downloaded data layers are changed
    sourceLayersChanged = pyqtSignal(list)

    # emit this signal when the remote WMTS layers are changed
    ntrrpItemsChanged = pyqtSignal()

    # emit this signal when working layers are changed
    workingLayersChanged = pyqtSignal(list)

    def __init__(self, region, wmsUrl, owsLayers):
        """Constructor."""
        super(QObject, self).__init__()

        self.name = region
        self.wmsUrl = wmsUrl
        self.owsLayers = owsLayers
        self.sourceLayers = []
        self.workingLayers = []
        self.currentMappingLayer = None
        self.regionGroup = f"{self.name} Burnt Areas"

    # arrange data
    def getNtrrpItems(self):
        """Return a set of NtrrpItem objects corresponding to this region's layers."""
        items = [NtrrpItem(self.wmsUrl, owsLayer)
                 for owsLayer in self.owsLayers]
        for item in items:
            item.itemLayer.layerAdded.connect(
                lambda _: self.ntrrpItemsChanged.emit())
            item.itemLayer.layerRemoved.connect(
                lambda _: self.ntrrpItemsChanged.emit())
        return items

    def getDataUrl(self):
        """Get the distinctive URL used for the data layers for this region."""
        return f"{getNtrrpDataUrl()}/{self.name.lower()}/{self.name.lower()}.zip"

    def getCurrentMappingDataUrl(self):
        """Get the current mapping data URL for the given region."""
        return f"{getNtrrpDataUrl()}/bfnt_{self.name.lower()}_current_sr3577_tif.zip"

    def downloadCurrentMapping(self):
        """Download current mapping for the region."""
        qgsDebug("Downloading current mapping …")
        currentMappingClient = NtrrpDataClient()
        currentMappingClient.dataDownloaded.connect(
            lambda unzipLocation: self.addCurrentMappingLayer(unzipLocation))
        currentMappingClient.downloadData(self.getCurrentMappingDataUrl())

    def downloadData(self):
        """Download burnt areas features from NAFI and call back to add them to the map."""
        qgsDebug("Downloading data …")
        client = NtrrpDataClient()
        client.dataDownloaded.connect(
            lambda unzipLocation: self.addSourceLayers(unzipLocation))
        client.downloadData(self.getDataUrl())

    # add things to the map
    def getSubGroupLayer(self):
        """Get or create the right layer group for an NTRRP data layer."""
        root = QgsProject.instance().layerTreeRoot()
        groupLayer = root.findGroup(self.regionGroup)
        if groupLayer == None:
            root.insertGroup(0, self.regionGroup)
            groupLayer = root.findGroup(self.regionGroup)
        return groupLayer

    def getWorkingLayerByName(self, workingLayerName):
        """Retrieve a current source layer by its display name."""
        matches = [layer for layer in self.workingLayers if layer.getMapLayerName(
        ) == workingLayerName]
        return next(iter(matches), None)

    def createWorkingLayer(self, templateSourceLayer):
        """Create a new working layer for this region."""
        workingLayer = WorkingLayer(templateSourceLayer)
        workingLayer.layerRemoved.connect(
            lambda layer: self.removeWorkingLayer(layer))
        self.workingLayers.append(workingLayer)
        workingLayer.addMapLayer(self.getSubGroupLayer())
        self.workingLayersChanged.emit(self.workingLayers)

    def removeWorkingLayer(self, layer):
        """Remove a working layer and inform subscribers."""
        self.workingLayers.remove(layer)
        self.workingLayersChanged.emit(self.workingLayers)

    def getSourceLayerByDisplayName(self, sourceLayerName):
        """Retrieve a current source layer by its display name."""
        matches = [
            layer for layer in self.sourceLayers if layer.getDisplayName() == sourceLayerName]
        return next(iter(matches), None)

    def addCurrentMappingLayer(self, unzipLocation):
        rasterFile = next(unzipLocation.rglob("*.tif"))
        self.currentMappingLayer = CurrentMappingLayer(rasterFile, self.name)
        self.currentMappingLayer.addMapLayer(self.getSubGroupLayer())

    def addSourceLayers(self, unzipLocation):
        """Add all shapefiles in a directory as data layers to the region group."""
        self.sourceLayers = [SourceLayer(path)
                             for path in unzipLocation.rglob("*.shp")]

        for sourceLayer in self.sourceLayers:
            sourceLayer.layerRemoved.connect(
                lambda layer: self.removeSourceLayer(layer))
            sourceLayer.addMapLayer(self.getSubGroupLayer())

        self.sourceLayersChanged.emit(self.sourceLayers)

    def removeSourceLayer(self, layer):
        """Remove a source layer and inform subscribers."""
        self.sourceLayers.remove(layer)
        self.sourceLayersChanged.emit(self.sourceLayers)

    def addWmtsLayer(self, item):
        """Add an NTRRP remote layer for this region to the map."""
        assert(isinstance(item, NtrrpItem))

        item.itemLayer.addMapLayer(self.getSubGroupLayer())

    # upload data
    def uploadBurntAreas(self):
        """Upload the curated working layer to NAFI."""
        guiWarning("Upload under construction!")
