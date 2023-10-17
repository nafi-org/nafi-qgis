# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsProject

from ..core.abstract_qobject_meta import AbstractQObjectMeta


class AbstractLayer(ABC, metaclass=AbstractQObjectMeta):
    """Abstract base class for burnt areas layers."""
    impl = None
    region = None

    # emit this signal if the map layer is removed
    layerAdded = pyqtSignal(object)
    layerRemoved = pyqtSignal(object)

    def layerGroup(self):
        """Return the layer group for this mapping."""
        if self.mappingDate:
            return f"{self.region} Burnt Areas ({self.mappingDate.strftime('%b %d')})"
        else:
            return f"{self.region} Burnt Areas"

    @abstractmethod
    def addMapLayer(self):
        """Add an NTRRP layer to the map."""
        pass

    @abstractmethod
    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        pass

    def getLayerGroupLayerItem(self):
        """Get or create the right layer group for an NTRRP data layer."""
        root = QgsProject.instance().layerTreeRoot()
        groupLayer = root.findGroup(self.layerGroup())
        if groupLayer is None:
            root.insertGroup(0, self.layerGroup())
            groupLayer = root.findGroup(self.layerGroup())
        return groupLayer

    def getSubGroupLayerItem(self):
        """Get the right layer subgroup within a specified group layer for this layer."""
        return self.getLayerGroupLayerItem()

    def getMapLayer(self):
        """Get the QGIS map layer corresponding to this layer, if any."""
        matches = QgsProject.instance().mapLayersByName(self.getMapLayerName())
        if len(matches) == 0:
            return None
        elif len(matches) >= 1:
            subGroupLayer = self.getSubGroupLayerItem()
            matches = [layer for layer in matches if subGroupLayer.findLayer(
                layer) is not None]
            if len(matches) >= 1:
                return matches[0]
            else:
                return None

    def addMapLayerIfNotPresent(self):
        layer = self.getMapLayer()

        if layer is None:
            self.addMapLayer()
        else:
            self.impl = layer
