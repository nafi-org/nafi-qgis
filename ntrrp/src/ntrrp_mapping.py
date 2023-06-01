# -*- coding: utf-8 -*-
from pathlib import Path
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsProject

import processing

from .layer.current_mapping_layer import CurrentMappingLayer
from .layer.segmentation_layer import SegmentationLayer
from .layer.working_layer import WorkingLayer
from .ntrrp_item import NtrrpItem
from .utils import deriveWorkingDirectory, qgsDebug, NTRRP_REGIONS


class NtrrpMapping(QObject):
    # emit this signal when the data download finishes
    dataDownloadFinished = pyqtSignal()

    # emit this signal when the current mapping download finishes
    currentMappingDownloadFinished = pyqtSignal()

    # emit this signal when the downloaded data layers are changed
    segmentationLayersChanged = pyqtSignal(list)

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
        self.mappingDate = None
        self.segmentationLayers = []
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

    def downloadCurrentMapping(self):
        """Download current mapping for the region and add it to the map."""
        qgsDebug("Downloading current NAFI burnt areas mapping …")

        if deriveWorkingDirectory() is None:
            return None

        params = {
            'Region': NTRRP_REGIONS.index(self.name),
            'WorkingFolder': deriveWorkingDirectory()
        }
        dialog = processing.createAlgorithmDialog(
            'BurntAreas:DownloadCurrentMapping', params)
        dialog.algorithmFinished.connect(lambda _: self.addCurrentMappingLayer(
            dialog.results()['CurrentMappingFolder']))
        for signal in [dialog.algorithmFinished, dialog.accepted, dialog.rejected, dialog.destroyed]:
            signal.connect(lambda: self.currentMappingDownloadFinished.emit())
        dialog.show()
        dialog.runButton().click()

        return True

    def downloadSegmentationData(self):
        """Download segmentation features from NAFI and call back to add them to the map."""
        qgsDebug("Downloading NAFI segmentation features …")

        if deriveWorkingDirectory() is None:
            return None

        params = {
            'Region': NTRRP_REGIONS.index(self.name),
            'WorkingFolder': deriveWorkingDirectory()
        }
        dialog = processing.createAlgorithmDialog(
            'BurntAreas:DownloadSegmentationData', params)
        dialog.algorithmFinished.connect(lambda _: self.addSegmentationLayers(
            dialog.results()['SegmentationDataFolder']))
        for signal in [dialog.algorithmFinished, dialog.accepted, dialog.rejected, dialog.destroyed]:
            signal.connect(lambda: self.dataDownloadFinished.emit())
        dialog.show()
        dialog.runButton().click()

        # self.addSegmentationLayers(Path('C:/Users/tom.lynch/Desktop/Working/Darwin'))

    # add things to the map
    def getSubGroupLayer(self):
        """Get or create the right layer group for an NTRRP data layer."""
        root = QgsProject.instance().layerTreeRoot()
        groupLayer = root.findGroup(self.regionGroup)
        if groupLayer is None:
            root.insertGroup(0, self.regionGroup)
            groupLayer = root.findGroup(self.regionGroup)
        return groupLayer

    def getWorkingLayerByName(self, workingLayerName):
        """Retrieve a current segmentation layer by its display name."""
        matches = [layer for layer in self.workingLayers if layer.getMapLayerName(
        ) == workingLayerName]
        return next(iter(matches), None)

    def createWorkingLayer(self, templateSegmentationLayer):
        """Create a new working layer for this region."""
        workingLayer = WorkingLayer(self.name, templateSegmentationLayer)
        workingLayer.layerRemoved.connect(
            lambda layer: self.removeWorkingLayer(layer))
        self.workingLayers.append(workingLayer)
        workingLayer.addMapLayerIfNotPresent()
        self.workingLayersChanged.emit(self.workingLayers)

    def removeWorkingLayer(self, layer):
        """Remove a working layer and inform subscribers."""
        self.workingLayers.remove(layer)
        self.workingLayersChanged.emit(self.workingLayers)

    def getSegmentationLayerByMapLayer(self, mapLayer):
        """Retrieve a current segmentation layer from its map layer."""

        matches = [segmentationLayer for segmentationLayer in self.segmentationLayers
                   if segmentationLayer.impl.id() == mapLayer.id()]
        return next(iter(matches), None)

    def addCurrentMappingLayer(self, unzipLocation):
        """Add the current mapping layer to the map."""
        if unzipLocation is None:
            return
        rasterFile = next(unzipLocation.rglob("*.tif"))
        self.currentMappingLayer = CurrentMappingLayer(
            self.name, Path(rasterFile))
        self.currentMappingLayer.addMapLayerIfNotPresent()

    def addSegmentationLayers(self, unzipLocation):
        """Add all shapefiles in a directory as data layers to the region group."""
        if unzipLocation is None:
            return

        self.segmentationLayers = [SegmentationLayer(path)
                             for path in unzipLocation.rglob("*.shp")]

        # do not add the layers with no threshold information
        self.segmentationLayers = [
            segmentationLayer for segmentationLayer in self.segmentationLayers if segmentationLayer.threshold is not None]

        for segmentationLayer in self.segmentationLayers:
            segmentationLayer.layerRemoved.connect(
                lambda layer: self.removeSegmentationLayer(layer))
            segmentationLayer.addMapLayerIfNotPresent()

        self.segmentationLayersChanged.emit(self.segmentationLayers)

    def removeSegmentationLayer(self, layer):
        """Remove a segmentation layer and inform subscribers."""
        self.segmentationLayers.remove(layer)
        self.segmentationLayersChanged.emit(self.segmentationLayers)

    def addWmtsLayer(self, item):
        """Add an NTRRP remote layer for this region to the map."""
        assert (isinstance(item, NtrrpItem))

        item.itemLayer.addMapLayerIfNotPresent()

    # upload data
    def processAndUploadBurntAreas(self, activeWorkingLayer):
        """Upload the curated working layer to NAFI."""

        params = {
            'Region': NTRRP_REGIONS.index(self.name),
        }

        if activeWorkingLayer is not None:
            params['ApprovedBurntAreas'] = activeWorkingLayer.impl

        # default current mapping layer if present
        if self.currentMappingLayer is not None:
            params['CurrentMapping'] = self.currentMappingLayer.impl.id()

        paramsWithFsid = processing.execAlgorithmDialog(
            'BurntAreas:ValidateFullBurntAreasProcess', params)

        if paramsWithFsid.get('FsidError', None) is not None:
            fsidError = paramsWithFsid['FsidError']
            fsidError.guiError()
            fsidError.log()
