# -*- coding: utf-8 -*-
import dateutil

from qgis.PyQt.QtCore import QObject
from qgis.core import QgsLayerTreeGroup, QgsProject, QgsVectorLayer

from .abstract_layer import AbstractLayer
from ..utils import resolveStylePath

def parseMetadataFromShapefilePath(shapefilePath):
    """Parse metadata from a segmentation layer shapefile path."""
    segments = shapefilePath.stem.split("_")
    difference = segments[0]
    region = segments[1].capitalize()
    endDate = dateutil.parser.parse(segments[2])
    startDate = dateutil.parser.parse(segments[3])
    
    # Patrice has started adding files with no threshold in the name
    threshold = segments[5][1:] if len(segments) > 5 else None
    differenceGroup = f"{difference} Differences ({endDate.strftime('%b %d')}–{startDate.strftime('%b %d')})"

    return {
        "difference": difference,
        "region": region,
        "endDate": endDate,
        "startDate": startDate,
        "threshold": threshold,
        "differenceGroup": differenceGroup
    }

class SegmentationLayer(QObject, AbstractLayer):

    def __init__(self, region, mappingDate, shapefilePath):
        """Constructor."""
        QObject.__init__(self)
        AbstractLayer.__init__(self)

        self.region = region
        self.mappingDate = mappingDate

        metadata = parseMetadataFromShapefilePath(shapefilePath)
        self.shapefilePath = shapefilePath
        
        # Copy metadata to this object
        self.difference = metadata["difference"]
        self.endDate = metadata["endDate"]
        self.startDate = metadata["startDate"]
        self.threshold = metadata["threshold"]
        self.differenceGroup = metadata["differenceGroup"]

    def getSubGroupLayerItem(self):
        """Get or create the right dMIRBI difference layer group for an NTRRP data layer."""

        groupLayer = self.getMappingGroupLayerItem()

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
        """Load the segmentation layer."""
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
        subGroupLayer = self.getSubGroupLayerItem()
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
