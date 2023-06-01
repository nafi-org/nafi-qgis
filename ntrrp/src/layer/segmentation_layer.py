# -*- coding: utf-8 -*-
import dateutil

from qgis.PyQt.QtCore import QObject
from qgis.core import QgsLayerTreeGroup, QgsProject, QgsVectorLayer

from .abstract_layer import AbstractLayer
from ..utils import resolveStylePath


class SegmentationLayer(QObject, AbstractLayer):

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
        # self.subArea = segments[5][2:]

        # Patrice has started adding files with no threshold in the name
        if len(segments) > 5:
            self.threshold = segments[5][1:]
        else:
            self.threshold = None

        # self.regionGroup = f"{self.region} Burnt Areas (Area {self.subArea})"
        # if self.subArea is not None:
        #    self.subAreaGroup = f"Subarea {self.subArea}"

        self.differenceGroup = f"{self.difference} Differences ({self.endDate.strftime('%b %d')}–{self.startDate.strftime('%b %d')})"

    def getSubGroupLayer(self):
        """Get or create the right dMIRBI difference layer group for an NTRRP data layer."""

        groupLayer = self.getRegionLayer()

        differenceGroupLayer = groupLayer.findGroup(self.differenceGroup)
        if differenceGroupLayer is None:
            groupLayer.insertGroup(0, self.differenceGroup)
            differenceGroupLayer = groupLayer.findGroup(self.differenceGroup)

        return differenceGroupLayer
        # if self.subArea is not None:
        #     subAreaLayer = differenceGroupLayer.findGroup(self.subAreaGroup)
        #     if subAreaLayer == None:
        #         # put the subareas in in numerical order
        #         differenceGroupLayer.addChildNode(
        #             QgsLayerTreeGroup(self.subAreaGroup))
        #         subAreaLayer = differenceGroupLayer.findGroup(
        #             self.subAreaGroup)
        #     return subAreaLayer
        # else:
        #     return differenceGroupLayer

    def load(self):
        """Load the source layer."""
        self.impl = QgsVectorLayer(
            self.shapefilePath.as_posix(), self.getMapLayerName(), "ogr")

    def addMapLayer(self):
        """Add an NTRRP data layer to the map."""
        # create the QgsVectorLayer object
        self.load()

        self.impl.willBeDeleted.connect(lambda: self.layerRemoved.emit(self))
        QgsProject.instance().addMapLayer(self.impl, False)

        # load one of two styles based on the threshold used to segment these features
        if int(self.threshold) < 200:
            self.loadStyle("lower_threshold")
        else:
            self.loadStyle("higher_threshold")

        self.layerAdded.emit(self)
        subGroupLayer = self.getSubGroupLayer()
        subGroupLayer.addLayer(self.impl)

    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        return f"Threshold {self.threshold}"

    def getDisplayName(self):
        """Get an appropriate UX display name for non-hierarchical widgets like combos."""
        # if self.subArea is not None:
        #     return f"Subarea {self.subArea} {self.difference} Threshold {self.threshold}"
        # else:
        return f"{self.difference} Threshold {self.threshold}"

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        if self.impl is not None:
            self.impl.loadNamedStyle(stylePath)
