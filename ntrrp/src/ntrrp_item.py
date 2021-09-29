# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 

from qgis.core import QgsMapLayer

from .layer.wmts_layer import WmtsLayer
from .ows_utils import parseNtrrpLayerDescription, parseNtrrpLayerRegion
from .utils import qgsDebug

class NtrrpItem(QStandardItem):

    def __init__(self, wmsUrl, owsLayer):
        """Constructor."""
        super(QStandardItem, self).__init__()

        self.toggleOff()
        
        # assemble some properties
        self.region = parseNtrrpLayerRegion(owsLayer)
        self.description = parseNtrrpLayerDescription(owsLayer)

        self.itemLayer = WmtsLayer(wmsUrl, owsLayer)
        self.setText(self.description)

        self.setFlags(Qt.ItemIsEnabled)
        self.setCheckable(False)

        self.restoreLayer()

    def restoreLayer(self):
        """Check if a layer is in the map already and set its icon if it is."""
        layer = self.itemLayer.getMapLayer()
        if layer is not None and isinstance(layer, QgsMapLayer):
            self.toggleOn(layer)

    def toggleOn(self, layer):
        """Associate this WMS item with an active map layer."""
        if layer is not None and isinstance(layer, QgsMapLayer):
            self.setIcon(QIcon(":/plugins/ntrrp/images/fire.png"))
            self.itemLayer.layerRemoved.connect(lambda _: self.toggleOff())

    def toggleOff(self):
        self.setIcon(QIcon(":/plugins/ntrrp/images/globe.png"))

