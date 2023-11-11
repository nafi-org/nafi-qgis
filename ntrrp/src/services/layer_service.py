from qgis.PyQt.QtCore import QObject, pyqtSignal

from qgis.core import QgsMapLayer, QgsProject
from qgis.utils import iface


class LayerService(QObject):
    # Emits Optional[QgsMapLayer]
    activeMapLayerChanged = pyqtSignal(QgsMapLayer)
    # Emits List[QgsMapLayer]
    layersChanged = pyqtSignal(list)

    def __init__(self):
        QObject.__init__(self)

        for signal in [
            QgsProject.instance().layersAdded,
            QgsProject.instance().layersRemoved,
        ]:
            signal.connect(lambda *_: self.layersChanged.emit(self.allLayers))

        iface.layerTreeView().currentLayerChanged.connect(
            lambda layer: self.activeMapLayerChanged.emit(layer)
        )

    @property
    def allLayers(self) -> list[QgsMapLayer]:
        """Return a list of all layers in the project."""
        return list(QgsProject.instance().mapLayers().values())

    def layersBy(self, predicate: callable) -> list[QgsMapLayer]:
        """Return a list of layers that match a predicate."""
        return [layer for layer in self.allLayers if predicate(layer)]
