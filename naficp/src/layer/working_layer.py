# -*- coding: utf-8 -*-
import os.path as path
from pathlib import Path

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QAction
# from qgis.core import QgsCoordinateReferenceSystem, QgsFields, QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsWkbTypes
from qgis.utils import iface as QgsInterface

from .abstract_layer import AbstractLayer
from .source_layer import SourceLayer
from ..utils import guiError


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

