# -*- coding: utf-8 -*-
from pathlib import Path
import dateutil

from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsProject, QgsVectorLayer

class NtrrpDataLayer:

    def __init__(self, shapefilePath):
        """Constructor."""
        self.shapefilePath = shapefilePath

        # Layer name will be similar to: T1T3_darwin_T20210827_T20210817_seg_sa1_t300
        segments = shapefilePath.stem.split("_")
        self.difference = segments[0]
        self.region = segments[1].capitalize()
        self.endDate = dateutil.parser.parse(segments[2])
        self.startDate = dateutil.parser.parse(segments[3])
        self.subArea = segments[5][2:]
        self.threshold = segments[6][1:]
        self.layerName = f"Threshold {self.threshold}"
        # self.regionGroup = f"{self.region} Burnt Areas (Area {self.subArea})"
        self.differenceGroup = f"{self.difference} Differences ({self.startDate.strftime('%b %d')}–{self.endDate.strftime('%b %d')})"

    def getSubGroupLayer(self, groupLayer):
        """Get or create the right dMIRBI difference layer group for an NTRRP data layer."""

        subGroupLayer = groupLayer.findGroup(self.differenceGroup)
        if subGroupLayer == None:
            groupLayer.insertGroup(0, self.differenceGroup)
            subGroupLayer = groupLayer.findGroup(self.differenceGroup)
        return subGroupLayer

    def addMapLayer(self, groupLayer):
        """Add an NTRRP data layer to the map."""
        layer = QgsVectorLayer(self.shapefilePath.as_posix(), self.layerName, "ogr")

        QgsProject.instance().addMapLayer(layer, False)
        subGroupLayer = self.getSubGroupLayer(groupLayer)

        subGroupLayer.addLayer(layer)
            