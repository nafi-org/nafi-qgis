# -*- coding: utf-8 -*-
from pathlib import Path

from qgis.PyQt.QtCore import QObject
from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer
from qgis.utils import iface as QgsInterface

from .utils import ensureDirectory, getWorkingShapefilePath

class NtrrpWorkingLayer(QObject):

    def __init__(self):
        """Constructor."""
        super(QObject, self).__init__()
        self.layerName = "Burnt Areas - Approved" # TODO
        self.workingLayer = QgsVectorLayer("Polygon?crs=epsg:3577", self.layerName, "memory")
        self.shapefilePath = getWorkingShapefilePath()

    def setSourceLayer(self, ntrrpDataLayer):
        """Set the source layer for this working layer."""
        self.sourceLayer = ntrrpDataLayer

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
        subGroupLayer.addLayer(self.workingLayer)
