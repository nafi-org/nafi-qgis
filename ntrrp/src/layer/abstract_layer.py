# -*- coding: utf-8 -*-
from abc import ABC, ABCMeta, abstractmethod
from tokenize import group

from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsMapLayer, QgsProject

from ..utils import qgsDebug


class AbstractQObjectMeta(ABCMeta, type(QObject)):
    """Metaclass to manage the requirement that things with signals be QObjects."""
    pass


class AbstractLayer(ABC, metaclass=AbstractQObjectMeta):
    """Abstract base class for burnt areas layers."""
    impl = None
    region = None

    # emit this signal if the map layer is removed
    layerAdded = pyqtSignal(object)
    layerRemoved = pyqtSignal(object)

    @abstractmethod
    def addMapLayer(self):
        """Add an NTRRP layer to the map."""
        pass

    @abstractmethod
    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        pass

    def getSubGroupLayer(self):
        """Get the right layer subgroup within a specified group layer for this layer."""
        return self.getRegionLayer()

    def getRegionLayer(self):
        """Get or create the right layer group for an NTRRP data layer."""
        root = QgsProject.instance().layerTreeRoot()
        regionGroup = f"{self.region} Burnt Areas"
        groupLayer = root.findGroup(regionGroup)
        if groupLayer == None:
            root.insertGroup(0, regionGroup)
            groupLayer = root.findGroup(regionGroup)
        return groupLayer

    def getMapLayer(self):
        """Get the QGIS map layer corresponding to this layer, if any."""
        matches = QgsProject.instance().mapLayersByName(self.getMapLayerName())
        if len(matches) == 0:
            return None
        elif len(matches) >= 1:
            subGroupLayer = self.getSubGroupLayer()
            matches = [layer for layer in matches if subGroupLayer.findLayer(layer) is not None]
            if len(matches) >= 1:
                return matches[0]
            else:
                return None

    def addMapLayerIfNotPresent(self):
        layer = self.getMapLayer()

        if layer is None:
            qgsDebug(f"Did not find layer {self.getMapLayerName()}")
            self.addMapLayer()
        else:
            qgsDebug(f"Found layer {self.getMapLayerName()}")
            self.impl = layer

