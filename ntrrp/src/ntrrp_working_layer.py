# -*- coding: utf-8 -*-
from pathlib import Path

from qgis.PyQt.QtCore import QObject
from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer
from qgis.utils import iface as QgsInterface

from .utils import ensureDirectory, getWorkingShapefilePath

class NtrrpWorkingLayer(QObject):

    def __init__(self, region, subArea):
        """Constructor."""
        super(QObject, self).__init__()
        self.workingLayer = QgsVectorLayer("Polygon?crs=epsg:3577", "Burnt Areas - Approved", "memory")
        self.shapefilePath = getWorkingShapefilePath()
        self.region = region
        self.subArea = subArea
        self.regionGroup = f"{self.region} Burnt Areas (Area {self.subArea})"

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

    def getRegionGroup(self):
        """Get or create the right layer group for an NTRRP data layer."""
        groupLayer = QgsProject.instance().layerTreeRoot().findGroup(self.regionGroup)
        if groupLayer == None:
            QgsProject.instance().layerTreeRoot().insertGroup(0, self.regionGroup)
            groupLayer = QgsProject.instance().layerTreeRoot().findGroup(self.regionGroup)
        return groupLayer

    def addToMap(self):
        """Add an NTRRP working layer to the map."""
        # layer = QgsVectorLayer(self.shapefilePath.as_posix(), self.layerName, "ogr")
        # groupLayer = self.getDifferenceGroup()

        QgsProject.instance().addMapLayer(self.workingLayer, False)
        self.getRegionGroup().addLayer(self.workingLayer)
        # groupLayer.addLayer(layer)