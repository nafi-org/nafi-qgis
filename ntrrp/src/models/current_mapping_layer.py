# -*- coding: utf-8 -*-
from typing import Union

from os import PathLike
from pathlib import Path

from qgis.core import QgsLayerTreeLayer, QgsProject, QgsRasterLayer

from ..utils import guiError
from .layer import Layer
from .mapping import Mapping


class CurrentMappingLayer(QgsRasterLayer, Layer):
    """Layer type for the current NAFI Hires mapping image."""

    def __init__(self, mapping: Mapping, rasterFile: Union[str, PathLike]):
        self.rasterPath = Path(rasterFile)        
        QgsRasterLayer.__init__(self, self.rasterPath.as_posix(), f"{mapping.region} Current Mapping", "gdal")
        
        self._mapping = mapping
        
    # Item interface
    @property
    def directory(self) -> Path:
        return self.mapping.directory

    @property
    def layerItemName(self) -> str:
        return f"{self.mapping.region} Current Mapping"

    @property
    def layerItem(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    # Layer interface
    @property
    def mapping(self) -> Mapping:
        return self._mapping

    @mapping.setter
    def mapping(self, mapping: Mapping) -> None:
        self._mapping = mapping

    def addMapLayer(self) -> None:
        if self.isValid():
            project = QgsProject.instance()
            project.addMapLayer(self, False)
            self.willBeDeleted.connect(
                lambda: self.layerRemoved.emit(self.id()))
            self.layerAdded.emit(self.id())
            self.subGroupLayerItem.addLayer(self)

            # don't show legend initially
            self.layerItem.setExpanded(True)
            self.layerItem.setExpanded(False)
        else:
            error = (f"An error occurred adding the layer {self.layerItemName} to the map.\n"
                     f"Check your QGIS WMS message log for details.")
            guiError(error)

