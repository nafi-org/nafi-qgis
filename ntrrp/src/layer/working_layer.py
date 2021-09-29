# -*- coding: utf-8 -*-
from pathlib import Path

from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer
from qgis.utils import iface as QgsInterface

from .abstract_layer import AbstractLayer
from .source_layer import SourceLayer
from ..utils import ensureDirectory, getWorkingShapefilePath, qgsDebug

class WorkingLayer(AbstractLayer):

    def __init__(self):
        """Constructor."""
        self.index = 1
        self.layerName = f"Burnt Areas - Approved #{self.index}" # TODO
        self.workingLayer = QgsVectorLayer("Polygon?crs=epsg:3577", self.getMapLayerName(), "memory")
        self.shapefilePath = getWorkingShapefilePath()

        # source layer is not initially set
        self.sourceLayer = None

    def setSourceLayer(self, sourceLayer):
        """Set the source layer for this working layer."""
        assert isinstance(sourceLayer, SourceLayer)
        self.sourceLayer = sourceLayer

    def save(self):
        """Write the content of this layer to a shapefile."""
        ensureDirectory(Path(self.shapefilePath).parent)
        QgsVectorFileWriter.writeAsVectorFormat(self.workingLayer, self.shapefilePath, "utf-8", driverName="ESRI Shapefile")

    def addBurntAreas(self):
        """Add the currently selected burnt areas to this working layer."""

        # Save after adding
        self.save()

    def getSubGroupLayer(self, groupLayer):
        """Get or create the right dMIRBI difference layer group for an NTRRP data layer."""
        subGroupLayerName = "Working layers"
        subGroupLayer = groupLayer.findGroup(subGroupLayerName)
        if subGroupLayer == None:
            groupLayer.insertGroup(0, subGroupLayerName)
            subGroupLayer = groupLayer.findGroup(subGroupLayerName)
        return subGroupLayer

    def addMapLayer(self, groupLayer):
        """Add an NTRRP data layer to the map."""
        QgsProject.instance().addMapLayer(self.workingLayer, False)
        subGroupLayer = self.getSubGroupLayer(groupLayer)
        displayLayer = subGroupLayer.addLayer(self.workingLayer)
        displayLayer.setName(self.getUniqueMapLayerName(groupLayer))

    # TODO does not currently work
    def getUniqueMapLayerName(self, groupLayer):
        if groupLayer is None:
            groupLayer = QgsProject.instance().layerTreeRoot()
        
        existingMapLayers = QgsProject.instance().mapLayersByName(self.getMapLayerName())
        existingDisplayLayers = [groupLayer.findLayer(layer) for layer in existingMapLayers]
        existingDisplayLayers = [layer for layer in existingDisplayLayers if layer is not None]

        while existingDisplayLayers:
            self.index += 1
            qgsDebug(str(existingDisplayLayers))
            qgsDebug(self.getMapLayerName())
            existingMapLayers = QgsProject.instance().mapLayersByName(self.getMapLayerName())
            existingDisplayLayers = [groupLayer.findLayer(layer) for layer in existingMapLayers]
        existingDisplayLayers = [layer for layer in existingDisplayLayers if layer is not None]

        return self.getMapLayerName()

    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        return f"Burnt Areas - Approved #{self.index}"

    def getMapLayer(self, groupLayer = None):
        """Get the QGIS map layer corresponding to this layer, if any."""
        if groupLayer is None:
            groupLayer = QgsProject.instance().layerTreeRoot()

        return self.getSubGroupLayer(groupLayer).findLayer(self.getMapLayerName())