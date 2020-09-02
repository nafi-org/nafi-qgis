# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NafiDockWidget
                                 A QGIS plugin
 Northern Australia Fire & Rangelands Map Services
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-08-28
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Tom Lynch
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
from urllib import parse

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, Qt, QModelIndex
from qgis.PyQt.QtGui import QFont, QStandardItem, QStandardItemModel 
from qgis.PyQt.QtWidgets import QApplication, QMessageBox

from qgis.core import QgsRasterLayer, QgsProject

from owslib.wms import WebMapService
from .nafi_dockwidget_base import Ui_NafiDockWidgetBase

NAFI_URL = "https://www.firenorth.org.au/public"

class NafiDockWidget(QtWidgets.QDockWidget, Ui_NafiDockWidgetBase):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(NafiDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.loadLayers()

    def loadLayers(self):
        """Add all NAFI WMS layers."""
        nafiUrl = NAFI_URL
        wms = WebMapService(nafiUrl)

        self.treeViewModel = QStandardItemModel()
        self.treeView.setModel(self.treeViewModel)

        # self.treeViewModel.rootItem.setText("NAFI")
        
        # stash a list of OWS layer objects
        owsLayers = [wms.contents[layerName] for layerName in list(wms.contents)]
        self.layersList = dict(zip([layer.title for layer in owsLayers], owsLayers)) 

        for layer in self.layersList.values():
            self.treeViewModel.appendRow(self.createWmsLayerNode(layer))
        
        self.treeView.pressed.connect(self.handleWmsLayerPressed)

    def createWmsLayerNode(self, layer):
        """Return a QStandardItem targeting a NAFI WMS layer given an OWS ContentMetadata object."""
        modelNode = QStandardItem()

        # need to create and set an icon here
        # modelNode.setIcon(iconFolder)
        modelNode.setFlags(Qt.ItemIsEnabled)
        modelNode.setText(layer.title)

        return modelNode

    def handleWmsLayerPressed(self, index):
        """Load a NAFI WMS layer."""
        assert isinstance(index, QModelIndex), "Supplied parameter is not a QModelIndex"

        mouseState = QApplication.mouseButtons()
        # if (mouseState == Qt.RightButton):
        #     index = self.viewModel.index(0, 0)
        #     self.view.setCurrentIndex(index)
        #     self.view.collapseAll()
        #     return

        modelNode = self.treeViewModel.itemFromIndex(index)
        layer = self.layersList[modelNode.text()]
        wmsLayer = self.createWmsLayer(layer)
        QgsProject.instance().addMapLayer(wmsLayer)

    def createWmsLayer(self, layer):
        """Create a QgsRasterLayer from WMS given an OWS ContentMetadata object."""

        # Weirdly true URL-encoding of the layer ID does not work correctly
        encodedLayer = layer.id.replace(" ","%20")

        # This should create "EPSG:28350" for Map Grid of Australia, "EPSG:4326" for WGS84 etc
        encodedSrsId = f"EPSG:{QgsProject.instance().crs().postgisSrid()}"
        wmsUrl = f"crs={encodedSrsId}&format=image/png&layers={encodedLayer}&styles&url={NAFI_URL}"

        wmsLayer = QgsRasterLayer(wmsUrl, layer.title, 'wms')
        return wmsLayer

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
