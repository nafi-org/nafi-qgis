# -*- coding: utf-8 -*-
import dateutil

from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsProject, QgsVectorLayer

from .abstract_layer import AbstractLayer
from ..utils import resolveStylePath

class SourceLayer(QObject, AbstractLayer):

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
        self.subArea = segments[5][2:]

        # Patrice has started adding files with no threshold in the name
        if len(segments) > 6:
            self.threshold = segments[6][1:]
        else:
            self.threshold = 0

        # self.regionGroup = f"{self.region} Burnt Areas (Area {self.subArea})"
        self.differenceGroup = f"{self.difference} Differences ({self.startDate.strftime('%b %d')}–{self.endDate.strftime('%b %d')})"

        self.load()

    def getSubGroupLayer(self, groupLayer):
        """Get or create the right dMIRBI difference layer group for an NTRRP data layer."""

        subGroupLayer = groupLayer.findGroup(self.differenceGroup)
        if subGroupLayer == None:
            groupLayer.insertGroup(0, self.differenceGroup)
            subGroupLayer = groupLayer.findGroup(self.differenceGroup)
        return subGroupLayer

    def load(self):
        """Load the source layer."""
        self.impl = QgsVectorLayer(self.shapefilePath.as_posix(), self.getMapLayerName(), "ogr")

    def addMapLayer(self, groupLayer):
        """Add an NTRRP data layer to the map."""
        self.impl.willBeDeleted.connect(lambda: self.layerRemoved.emit(self))
        QgsProject.instance().addMapLayer(self.impl, False)
        
        # load one of two styles based on the threshold used to segment these features
        if int(self.threshold) < 200:
            self.loadStyle("lower_threshold")
        else:
            self.loadStyle("higher_threshold")

        self.layerAdded.emit(self)
        subGroupLayer = self.getSubGroupLayer(groupLayer)
        subGroupLayer.addLayer(self.impl)

    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        return f"Threshold {self.threshold}"

    def getDisplayName(self):
        """Get an appropriate UX display name for non-hierarchical widgets like combos."""
        return f"{self.difference} {self.getMapLayerName()}"

    def getMapLayer(self, groupLayer = None):
        """Get the QGIS map layer corresponding to this layer, if any."""
        if self.impl is None:
            return None
        
        if groupLayer is None:
            groupLayer = QgsProject.instance().layerTreeRoot()

        return self.getSubGroupLayer(groupLayer).findLayer(self.impl)

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        if self.impl is not None:
            self.impl.loadNamedStyle(stylePath)
            