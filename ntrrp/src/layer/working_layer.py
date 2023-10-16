# -*- coding: utf-8 -*-
import os.path as path
from pathlib import Path

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsWkbTypes
from qgis.utils import iface as QgsInterface

from .abstract_layer import AbstractLayer
from .segmentation_layer import SegmentationLayer
from ..utils import ensureDirectory, deriveWorkingDirectory, guiError, resolveStylePath


class WorkingLayer(QObject, AbstractLayer):

    def __init__(self, region, mappingDate, templateSegmentationLayer):
        """Constructor."""
        QObject.__init__(self)
        AbstractLayer.__init__(self)

        self.region = region
        self.mappingDate = mappingDate

        self.index = 1
        self.templateSegmentationLayer = templateSegmentationLayer

        # segmentation layer is not initially set
        self.segmentationLayer = None
        self.shapefilePath = self.getShapefilePath()

        self.createShapefile()

    def setSegmentationLayer(self, segmentationLayer):
        """Set the segmentation layer for this working layer."""
        assert isinstance(segmentationLayer, SegmentationLayer)
        self.segmentationLayer = segmentationLayer

    def createShapefile(self):
        """Create a shapefile for this layer."""

        # templateSegmentationLayer sets initial attributes
        if self.templateSegmentationLayer is not None:
            sourceImpl = self.templateSegmentationLayer.impl
            writer = QgsVectorFileWriter(self.shapefilePath, 'UTF-8', self.templateSegmentationLayer.impl.fields(
            ), QgsWkbTypes.Polygon, QgsCoordinateReferenceSystem('EPSG:3577'), 'ESRI Shapefile')
        else:
            guiError("No template segmentation layer!")

    def getShapefilePath(self):
        """Get a path for a working layer shapefile."""
        outputDir = path.normpath(
            path.join(deriveWorkingDirectory(), f"{self.region} Working"))
        ensureDirectory(outputDir)

        return path.normpath(path.join(outputDir, f"{self.getMapLayerName()}.shp"))

    def save(self):
        """Write the content of this layer to a shapefile."""
        ensureDirectory(Path(self.shapefilePath).parent)
        QgsVectorFileWriter.writeAsVectorFormat(
            self.impl, self.shapefilePath, "utf-8", driverName="ESRI Shapefile")

    def copySelectedFeaturesFromSegmentationLayer(self):
        """Add the currently selected features in the segmentation layer to this working layer."""
        if self.segmentationLayer is None or self.segmentationLayer.impl is None:
            guiError("Error occurred: inconsistent state in segmentation layer.")
        elif self.impl is None:
            guiError("Error occurred: inconsistent state in working layer.")
        else:
            QgsInterface.setActiveLayer(self.segmentationLayer.impl)
            QgsInterface.actionCopyFeatures().trigger()
            QgsInterface.setActiveLayer(self.impl)

            # if not currently editing, start editing this layer
            wasEditing = self.impl.isEditable()
            if not wasEditing:
                self.impl.startEditing()

            QgsInterface.actionPasteFeatures().trigger()

            # commit the changes, and stop editing if we weren't before
            self.impl.commitChanges(stopEditing=(not wasEditing))

            QgsInterface.mainWindow().findChild(QAction, 'mActionDeselectAll').trigger()
            QgsInterface.setActiveLayer(self.segmentationLayer.impl)

            # repopulate the clipboard with no features to avoid re-pasting
            QgsInterface.actionCopyFeatures().trigger()

        # Save after adding
        self.save()

    def getSubGroupLayerItem(self):
        """Get or create the right dMIRBI difference layer group for an NTRRP data layer."""
        groupLayer = self.getMappingGroupLayerItem()
        subGroupLayerName = "Approved Burnt Areas"
        subGroupLayer = groupLayer.findGroup(subGroupLayerName)
        if subGroupLayer is None:
            groupLayer.insertGroup(0, subGroupLayerName)
            subGroupLayer = groupLayer.findGroup(subGroupLayerName)
        return subGroupLayer

    def addMapLayer(self):
        """Add an NTRRP data layer to the map."""
        self.impl = QgsVectorLayer(
            self.shapefilePath, self.getMapLayerName(), "ogr")

        QgsProject.instance().addMapLayer(self.impl, False)
        self.impl.willBeDeleted.connect(lambda: self.layerRemoved.emit(self))
        self.loadStyle("approved")
        self.layerAdded.emit(self)
        subGroupLayer = self.getSubGroupLayerItem()
        displayLayer = subGroupLayer.addLayer(self.impl)
        displayLayer.setName(self.getMapLayerName())

    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        return f"Working Layer #{self.index}"

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        if self.impl is not None:
            self.impl.loadNamedStyle(stylePath)
