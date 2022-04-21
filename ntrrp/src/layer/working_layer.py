# -*- coding: utf-8 -*-
import os.path as path
from pathlib import Path

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsCoordinateReferenceSystem, QgsFields, QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsWkbTypes
from qgis.utils import iface as QgsInterface

from .abstract_layer import AbstractLayer
from .source_layer import SourceLayer
from ..utils import ensureDirectory, deriveWorkingDirectory, guiError, resolveStylePath


class WorkingLayer(QObject, AbstractLayer):

    def __init__(self, region, templateSourceLayer):
        """Constructor."""
        super(QObject, self).__init__()

        self.region = region
        self.index = 1
        self.templateSourceLayer = templateSourceLayer

        # source layer is not initially set
        self.sourceLayer = None
        self.shapefilePath = self.getShapefilePath()

        self.createShapefile()

    def setSourceLayer(self, sourceLayer):
        """Set the source layer for this working layer."""
        assert isinstance(sourceLayer, SourceLayer)
        self.sourceLayer = sourceLayer

    def createShapefile(self):
        """Create a shapefile for this layer."""

        # templateSourceLayer sets initial attributes
        if self.templateSourceLayer is not None:
            sourceImpl = self.templateSourceLayer.impl
            writer = QgsVectorFileWriter(self.shapefilePath, 'UTF-8', self.templateSourceLayer.impl.fields(
            ), QgsWkbTypes.Polygon, QgsCoordinateReferenceSystem('EPSG:3577'), 'ESRI Shapefile')
        else:
            guiError("No template source layer!")

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

    def copySelectedFeaturesFromSourceLayer(self):
        """Add the currently selected features in the source layer to this working layer."""
        if self.sourceLayer is None or self.sourceLayer.impl is None:
            guiError("Error occurred: inconsistent state in source layer.")
        elif self.impl is None:
            guiError("Error occurred: inconsistent state in working layer.")
        else:
            QgsInterface.setActiveLayer(self.sourceLayer.impl)
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
            QgsInterface.setActiveLayer(self.sourceLayer.impl)

            # repopulate the clipboard with no features to avoid re-pasting
            QgsInterface.actionCopyFeatures().trigger()

        # Save after adding
        self.save()

    def getSubGroupLayer(self):
        """Get or create the right dMIRBI difference layer group for an NTRRP data layer."""
        groupLayer = self.getRegionLayer()
        subGroupLayerName = "Approved Burnt Areas"
        subGroupLayer = groupLayer.findGroup(subGroupLayerName)
        if subGroupLayer == None:
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
        subGroupLayer = self.getSubGroupLayer()
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
