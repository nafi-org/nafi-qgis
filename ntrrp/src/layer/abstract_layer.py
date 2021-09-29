# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class AbstractLayer(ABC):
    """Abstract base class for burnt areas layers."""

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

    @abstractmethod
    def getMapLayer(self, groupLayer = None):
        """Get the QGIS map layer corresponding to this layer, if any."""
        pass
            