from typing import cast

from abc import ABC, abstractproperty

import uuid
from pathlib import Path

from qgis.core import QgsLayerTreeGroup, QgsLayerTreeNode, QgsProject

from ntrrp.src.abstract_qobject_meta import AbstractQObjectMeta


class Item(ABC, metaclass=AbstractQObjectMeta):
    """Abstract representation for any NAFI Hires project item, such as a Mapping,
    SegmentationLayer, WorkingLayer, etc."""

    def __init__(self):
        self._uuid = uuid.uuid4().hex

    @property
    def uuid(self) -> str:
        """Return the UUID for this Item."""
        return self._uuid

    @abstractproperty
    def directory(self) -> Path:
        """Return the filesystem directory for this Item."""
        pass

    @abstractproperty
    def regionName(self) -> str:
        """Return the region name for this Item."""
        pass

    @abstractproperty
    def item(self):
        """Return the QGIS layer item (in the Layers panel) for this Item."""
        pass

    @abstractproperty
    def itemName(self) -> str:
        """Return the name of the QGIS layer item for this Item."""
        pass

    @abstractproperty
    def groupName(self) -> str:
        """Return the QGIS layer group name for this layer."""
        pass

    @property
    def group(self) -> QgsLayerTreeGroup:
        """Return the QGIS layer tree group for this layer."""
        groupName = self.groupName
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(groupName)
        if group is None:
            root.insertGroup(0, groupName)
            group = root.findGroup(groupName)
        return group

    @property
    def subGroupName(self) -> str:
        """Return the QGIS layer tree subgroup name for this layer."""
        return self.groupName

    @property
    def subGroup(self) -> QgsLayerTreeGroup:
        """Return the QGIS layer tree subgroup for this layer."""
        return self.group

    @property
    def visibilityChecked(self) -> bool:
        """Return whether this item is visible in the map and the layers panel."""
        return cast(QgsLayerTreeNode, self.item).itemVisibilityChecked()

    @visibilityChecked.setter
    def visibilityChecked(self, value: bool) -> None:
        """Set the visibility of this item in the map and the layers panel."""
        cast(QgsLayerTreeNode, self.item).setItemVisibilityChecked(value)

    def isSame(self, other) -> bool:
        """Return True if the layer is the same as the one in the project."""
        return other and self.uuid == other.uuid
