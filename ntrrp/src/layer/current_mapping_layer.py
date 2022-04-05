# -*- coding: utf-8 -*-
from pathlib import Path

from qgis.core import QgsProject, QgsRasterLayer
from qgis.PyQt.QtCore import QObject

from ..utils import guiError, qgsDebug
from .abstract_layer import AbstractLayer


class CurrentMappingLayer(QObject, AbstractLayer):
    def __init__(self, region, rasterFile):
        """Constructor."""
        super(QObject, self).__init__()
        self.rasterFile = Path(rasterFile)
        self.region = region

    def addMapLayer(self):
        """Create a QgsRasterLayer from the location of a TIF of current mapping imagery."""
        self.impl = QgsRasterLayer(
            self.rasterFile.as_posix(), self.getMapLayerName(), "gdal")

        project = QgsProject.instance()

        if self.impl is not None and self.impl.isValid():
            self.impl = project.addMapLayer(self.impl, False)
            self.impl.willBeDeleted.connect(
                lambda: self.layerRemoved.emit(self))
            self.layerAdded.emit(self)
            self.mapLayerId = self.impl.id()

            subGroupLayer = self.getSubGroupLayer()
            subGroupLayer.addLayer(self.impl)

            # don't show legend initially
            displayLayer = project.layerTreeRoot().findLayer(self.impl.id())
            displayLayer.setExpanded(True)
            displayLayer.setExpanded(False)
        else:
            error = (f"An error occurred adding the layer {self.getMapLayerName()} to the map.\n"
                     f"Check your QGIS WMS message log for details.")
            guiError(error)

    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        return f"{self.region} Current Mapping"

