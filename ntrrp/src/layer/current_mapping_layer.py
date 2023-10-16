# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path

from qgis.core import QgsProject, QgsRasterLayer
from qgis.PyQt.QtCore import QObject

from ..utils import guiError
from .abstract_layer import AbstractLayer


class CurrentMappingLayer(QObject, AbstractLayer):
    def __init__(self, region, rasterFile):
        """Constructor."""
        QObject.__init__(self)
        AbstractLayer.__init__(self)

        self.region = region
        self.mappingDate = datetime.today()
        self.rasterFile = Path(rasterFile)

    @property
    def mappingGroup(self):
        """Return the layer group for this mapping."""
        return f"{self.region} Current Mapping"

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

            subGroupLayer = self.getSubGroupLayerItem()
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
