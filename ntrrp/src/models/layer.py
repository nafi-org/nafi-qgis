# -*- coding: utf-8 -*-
from abc import abstractmethod

from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject, QgsLayerTreeGroup, QgsMapLayer

from .item import Item
from .mapping import Mapping


class Layer(Item):
    """Abstract type for a NAFI Hires Layer within a Mapping."""

    # emit this signal if the map layer is removed
    layerAdded = pyqtSignal(QgsMapLayer)
    layerRemoved = pyqtSignal(QgsMapLayer)

    @property
    def groupName(self) -> str:
        """Return the QGIS layer group name for this Layer."""
        return self.mapping and self.mapping.layerItemName

    @property
    def groupLayerItem(self) -> QgsLayerTreeGroup:
        """Return the QGIS layer group layer item for this Layer."""
        groupName = self.groupName
        if not groupName:
            return None
        
        root = QgsProject.instance().layerTreeRoot()
        groupLayer = root.findGroup(groupName)
        if groupLayer is None:
            root.insertGroup(0, groupName)
            groupLayer = root.findGroup(groupName)
        return groupLayer

    @property
    def subGroupLayerItem(self) -> QgsLayerTreeGroup:
        """Return the QGIS layer subgroup item for this Layer."""
        return self.groupLayerItem

    @property
    @abstractmethod
    def mapping(self) -> Mapping:
        """Return the Mapping for this Layer."""
        pass

    @mapping.setter
    @abstractmethod
    def mapping(self, mapping: Mapping) -> None:
        """Set the Mapping for this Layer."""
        pass

    @abstractmethod
    def addMapLayer(self) -> None:
        """Constract and add this Layer to the QGIS map and the Layers panel."""
        pass
