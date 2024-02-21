from abc import abstractmethod

from qgis.core import QgsLayerTreeLayer, QgsProject
from qgis.PyQt.QtCore import pyqtSignal

from .item import Item


class Layer(Item):
    """Abstract type for a NAFI HiRes Layer within a Mapping."""

    # Emit these signals with layer ID
    layerAdded = pyqtSignal(str)
    layerRemoved = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @abstractmethod
    def id(self) -> str:
        """Stub method to return the QGIS layer ID."""
        pass

    def layerName(self) -> str:
        return self.itemName()

    def layerItem(self) -> QgsLayerTreeLayer:
        """Return the QGIS layer item (in the Layers panel) for this Item."""
        return self.item()

    def addMapLayer(self) -> None:
        """Add this layer to the map and layers panel, removing any existing layer with the same name."""

        project = QgsProject.instance()
        project.addMapLayer(self, False)  # type: ignore

        existingItem = next(
            (
                layer
                for layer in self.subGroup().findLayers()
                if layer.name() == self.layerName()
            ),
            None,
        )
        if existingItem is not None:
            self.subGroup().removeLayer(existingItem.layer())
        self.subGroup().addLayer(self)  # type: ignore
        self.layerAdded.emit(self.id())

        # don't show legend initially
        self.item().setExpanded(True)
        self.item().setExpanded(False)
