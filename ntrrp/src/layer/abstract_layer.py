# -*- coding: utf-8 -*-
from abc import ABC, ABCMeta, abstractmethod

from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsMapLayer, QgsProject

class AbstractQObjectMeta(ABCMeta, type(QObject)):
    """Metaclass to manage the requirement that things with signals be QObjects."""
    pass

class AbstractLayer(ABC, metaclass=AbstractQObjectMeta):
    """Abstract base class for burnt areas layers."""

    # emit this signal if the map layer is removed
    layerAdded = pyqtSignal(object)
    layerRemoved = pyqtSignal(object)

    @abstractmethod
    def getSubGroupLayer(self, groupLayer):
        """Get the right layer subgroup within a specified group layer for this layer."""
        return groupLayer

    @abstractmethod
    def addMapLayer(self, groupLayer):
        """Add an NTRRP layer to the map."""
        pass

    @abstractmethod
    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        pass

    def getMapLayer(self, groupLayer = None):
        """Get the QGIS map layer corresponding to this layer, if any."""
        # TODO might be aliased
        matches = QgsProject.instance().mapLayersByName(self.getMapLayerName())

        if len(matches) == 0:
            return None
        elif len(matches) >= 1:
            return matches[0]

