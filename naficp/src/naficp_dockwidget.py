# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NafiCpDockWidget
                                 A QGIS plugin
 Easily copy and paste features between QGIS layers
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-04-22
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Trailmarker
        email                : tom@trailmarker.io
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsMapLayerProxyModel
from qgis.utils import iface as QgsInterface

from .utils import guiError

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui', 'naficp_dockwidget_base.ui'))


class NafiCpDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(NafiCpDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.sourceLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.sourceLayerComboBox.setShowCrs(True)

        self.workingLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.workingLayerComboBox.setShowCrs(True)

        self.pasteFeaturesButton.clicked.connect(self.copySelectedFeaturesFromSourceLayer)

        # set up active layer handler
        # QgsInterface.layerTreeView().currentLayerChanged.connect(self.activeLayerChanged)


    def copySelectedFeaturesFromSourceLayer(self):
        """Add the currently selected features in the source layer to this working layer."""
        sourceLayer = self.sourceLayerComboBox.currentLayer()
        workingLayer = self.workingLayerComboBox.currentLayer()

        if sourceLayer is None:
            guiError("Error occurred: no source layer selected.")
        if workingLayer is None:
            guiError("Error occurred: no working layer selected.")
        else:
            QgsInterface.setActiveLayer(sourceLayer)
            QgsInterface.actionCopyFeatures().trigger()
            QgsInterface.setActiveLayer(workingLayer)

            # if not currently editing, start editing this layer
            wasEditing = workingLayer.isEditable()
            if not wasEditing:
                workingLayer.startEditing()

            QgsInterface.actionPasteFeatures().trigger()

            # commit the changes, and stop editing if we weren't before
            workingLayer.commitChanges(stopEditing=(not wasEditing))

            QgsInterface.mainWindow().findChild(QAction, 'mActionDeselectAll').trigger()
            QgsInterface.setActiveLayer(sourceLayer)

            # repopulate the clipboard with no features to avoid re-pasting
            QgsInterface.actionCopyFeatures().trigger()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
