# -*- coding: utf-8 -*-
from pathlib import Path

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer
from qgis.utils import iface as QgsInterface

from .abstract_layer import AbstractLayer
from .source_layer import SourceLayer
from ..utils import ensureDirectory, getWorkingShapefilePath, guiError, resolveStylePath


class WorkingLayer(QObject, AbstractLayer):

    def __init__(self, region, templateSourceLayer):
        """Constructor."""
        super(QObject, self).__init__()

        self.region = region
        self.index = 0
        self.templateSourceLayer = templateSourceLayer

        # source layer is not initially set
        self.sourceLayer = None

    def setSourceLayer(self, sourceLayer):
        """Set the source layer for this working layer."""
        assert isinstance(sourceLayer, SourceLayer)
        self.sourceLayer = sourceLayer

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
            self.impl.startEditing()
            QgsInterface.actionPasteFeatures().trigger()
            self.impl.commitChanges()
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
            "Polygon?crs=epsg:3577", self.getMapLayerName(), "memory")
        self.shapefilePath = getWorkingShapefilePath()

        # templateSourceLayer sets initial attributes
        if self.templateSourceLayer is not None:
            sourceImpl = self.templateSourceLayer.impl
            fields = [sourceImpl.fields()[index]
                      for index in sourceImpl.fields().allAttributesList()]
            self.impl.dataProvider().addAttributes(fields)
            self.impl.updateFields()

        QgsProject.instance().addMapLayer(self.impl, False)
        self.impl.willBeDeleted.connect(lambda: self.layerRemoved.emit(self))
        self.loadStyle("approved")
        self.layerAdded.emit(self)
        subGroupLayer = self.getSubGroupLayer()
        displayLayer = subGroupLayer.addLayer(self.impl)
        displayLayer.setName(self.getUniqueMapLayerName())

    # TODO does not currently work
    def getUniqueMapLayerName(self):
        groupLayer = self.getRegionLayer()

        existingMapLayers = QgsProject.instance().mapLayersByName(self.getMapLayerName())
        existingDisplayLayers = [groupLayer.findLayer(
            layer) for layer in existingMapLayers]
        existingDisplayLayers = [
            layer for layer in existingDisplayLayers if layer is not None]

        while len(existingDisplayLayers) > 0:
            self.index += 1
            # qgsDebug(str(existingDisplayLayers))
            # qgsDebug(self.getMapLayerName())
            existingMapLayers = QgsProject.instance().mapLayersByName(self.getMapLayerName())
            existingDisplayLayers = [groupLayer.findLayer(
                layer) for layer in existingMapLayers]
        existingDisplayLayers = [
            layer for layer in existingDisplayLayers if layer is not None]

        return self.getMapLayerName()

    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        return f"Working Layer #{self.index}"

    # def getMapLayer(self, groupLayer=None):
    #     """Get the QGIS map layer corresponding to this layer, if any."""
    #     if self.impl is None:
    #         return None

    #     if groupLayer is None:
    #         groupLayer = QgsProject.instance().layerTreeRoot()

    #     return self.getSubGroupLayer(groupLayer).findLayer(self.impl)

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        if self.impl is not None:
            self.impl.loadNamedStyle(stylePath)
