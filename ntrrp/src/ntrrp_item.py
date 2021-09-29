# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 

from qgis.core import QgsProject, QgsRasterLayer

from .layer.wmts_layer import WmtsLayer
from .ows_utils import parseNtrrpLayerDescription, parseNtrrpLayerRegion

class NtrrpItem(QStandardItem):
    def __init__(self, wmsUrl, owsLayer):
        """Constructor."""
        super(QStandardItem, self).__init__()

        self.unsetLayer()
        
        # assemble some properties
        self.region = parseNtrrpLayerRegion(owsLayer)
        self.description = parseNtrrpLayerDescription(owsLayer)
        self.itemLayer = WmtsLayer(wmsUrl, owsLayer, self)

        self.setText(self.description)

        self.setFlags(Qt.ItemIsEnabled)
        self.setCheckable(False)

        self.restoreLayer()

    def unsetLayer(self):
        self.setIcon(QIcon(":/plugins/ntrrp/images/globe.png"))
        self.mapLayerId = None

    def restoreLayer(self):
        """Check if a layer is in the map already and set its icon if it is."""
        # Python idiom to get first or None
        layer = next(iter(QgsProject.instance().mapLayersByName(self.itemLayer.owsLayer.title)), None)
        if layer is not None and isinstance(layer, QgsRasterLayer):
            self.linkLayer(layer)

    def linkLayer(self, layer):
        """Associate this WMS item with an active map layer."""
        self.setIcon(QIcon(":/plugins/ntrrp/images/fire.png"))
        self.mapLayerId = layer.id()
        layer.willBeDeleted.connect(self.unsetLayer)

