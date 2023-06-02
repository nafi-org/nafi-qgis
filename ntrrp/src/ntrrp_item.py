# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem

from qgis.core import QgsMapLayer

from .layer.wmts_layer import WmtsLayer
from .ows_utils import parseNtrrpLayerDescription, parseNtrrpLayerRegion


class NtrrpItem(QStandardItem):

    def __init__(self, mappingDate, wmsUrl, owsLayer):
        """Constructor."""
        super(QStandardItem, self).__init__()

        self.setIcon(QIcon(":/plugins/ntrrp/images/globe.png"))

        # assemble some properties
        self.region = parseNtrrpLayerRegion(owsLayer.title)
        self.mappingDate = mappingDate
        self.description = parseNtrrpLayerDescription(owsLayer.title)

        self.itemLayer = WmtsLayer(self.region, self.mappingDate, wmsUrl, owsLayer)
        self.setText(self.description)

        self.setFlags(Qt.ItemIsEnabled)
        self.setCheckable(False)

        self.restoreLayer()

    def restoreLayer(self):
        """Check if a layer is in the map already and set its icon if it is."""
        layer = self.itemLayer.getMapLayer()
        if layer is not None and isinstance(layer, QgsMapLayer):
            # qgsDebug(f"Restoring {self.description}: itemLayer.owsLayer.title = {self.itemLayer.owsLayer.title}, itemLayer.getMapLayerName() = {self.itemLayer.getMapLayerName()}")
            self.toggleOn(layer)

    def toggleOn(self, layer):
        """Associate this WMS item with an active map layer."""
        if layer is not None and isinstance(layer, QgsMapLayer):
            self.setIcon(QIcon(":/plugins/ntrrp/images/fire.png"))
