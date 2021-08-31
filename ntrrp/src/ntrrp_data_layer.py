# -*- coding: utf-8 -*-
from pathlib import Path
import dateutil

from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsProject, QgsVectorLayer

class NtrrpDataLayer(QObject):

    # dataAdded = pyqtSignal(QObject)
    def __init__(self, shapefilePath):
        """Constructor."""
        super(QObject, self).__init__()
        self.shapefilePath = shapefilePath

        # Layer name will be similar to: T1T3_darwin_T20210827_T20210817_seg_sa1_t300
        segments = shapefilePath.stem.split("_")
        self.difference = segments[0]
        self.region = segments[1].capitalize()
        self.endDate = dateutil.parser.parse(segments[2])
        self.startDate = dateutil.parser.parse(segments[3])
        self.threshold = segments[6][1:]
        self.layerName = f"Threshold {self.threshold}"
        self.regionGroup = f"{self.region} Burnt Areas"
        self.differenceGroup = f"{self.difference} Differences ({self.startDate.strftime('%b %d')}–{self.endDate.strftime('%b %d')})"

    def getRegionGroup(self):
        """Get or create the right layer group for an NTRRP data layer."""
        groupLayer = QgsProject.instance().layerTreeRoot().findGroup(self.regionGroup)
        if groupLayer == None:
            QgsProject.instance().layerTreeRoot().insertGroup(0, self.regionGroup)
            groupLayer = QgsProject.instance().layerTreeRoot().findGroup(self.regionGroup)
        return groupLayer

    def getDifferenceGroup(self):
        """Get or create the right dMIRBI difference layer group for an NTRRP data layer."""
        regionGroupLayer = self.getRegionGroup()

        groupLayer = regionGroupLayer.findGroup(self.differenceGroup)
        if groupLayer == None:
            regionGroupLayer.insertGroup(0, self.differenceGroup)
            groupLayer = regionGroupLayer.findGroup(self.differenceGroup)
        return groupLayer

    def addToMap(self):
        """Add an NTRRP data layer to the map."""
        layer = QgsVectorLayer(self.shapefilePath.as_posix(), self.layerName, "ogr")
        groupLayer = self.getDifferenceGroup()

        QgsProject.instance().addMapLayer(layer, False)
        groupLayer.addLayer(layer)