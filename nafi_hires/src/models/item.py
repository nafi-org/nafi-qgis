import uuid
from abc import ABC
from typing import cast

from qgis.core import QgsLayerTreeGroup, QgsLayerTreeNode, QgsProject

from nafi_hires.src.abstract_qobject_meta import AbstractQObjectMeta


class Item(ABC, metaclass=AbstractQObjectMeta):
    """Abstract representation for any NAFI HiRes project item, such as a Mapping,
    SegmentationLayer, WorkingLayer, etc."""

    def __init__(self):
        self._uuid = uuid.uuid4().hex

    def uuid(self) -> str:
        """Return the UUID for this Item."""
        return self._uuid

    # Item interface
    def regionName(self) -> str:
        """Return the region name for this Item."""
        pass

    def itemName(self) -> str:
        """Return the name of the QGIS layer item for this Item."""
        pass

    def item(self):
        """Return the QGIS layer item (in the Layers panel) for this Item."""
        pass

    def groupName(self) -> str:
        """Return the QGIS layer group name for this layer."""
        pass

    def group(self) -> QgsLayerTreeGroup:
        """Return the QGIS layer tree group for this layer."""
        groupName = self.groupName()
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(groupName)
        if group is None:
            root.insertGroup(0, groupName)
            group = root.findGroup(groupName)
        return group

    def subGroupName(self) -> str:
        """Return the QGIS layer tree subgroup name for this layer."""
        return self.groupName()

    def subGroup(self) -> QgsLayerTreeGroup:
        """Return the QGIS layer tree subgroup for this layer."""
        return self.group()

    def visibilityChecked(self) -> bool:
        """Return whether this item is visible in the map and the layers panel."""
        return cast(QgsLayerTreeNode, self.item()).itemVisibilityChecked()

    def setVisibilityChecked(self, value: bool) -> None:
        """Set the visibility of this item in the map and the layers panel."""
        cast(QgsLayerTreeNode, self.item()).setItemVisibilityChecked(value)

    def isSame(self, other) -> bool:
        """Return True if the layer is the same as the one in the project."""
        return other and self.uuid() == other.uuid()
