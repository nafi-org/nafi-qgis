# -*- coding: utf-8 -*-
from typing import Union

import dateutil
from os import PathLike
from pathlib import Path

from qgis.core import QgsLayerTreeLayer, QgsProject, QgsVectorLayer

from ..utils import guiError, resolveStylePath
from .layer import Layer
from .mapping import Mapping


class SegmentationLayer(QgsVectorLayer, Layer):
    """Layer type for the current NAFI Hires mapping image."""

    def __init__(self, mapping: Mapping, shapefile: Union[str, PathLike]):
        self.shapefilePath = Path(shapefile)

        segments = self.shapefilePath.stem.split("_")
        self.difference = segments[0]
        self.endDate = dateutil.parser.parse(segments[2])
        self.startDate = dateutil.parser.parse(segments[3])

        # Patrice has started adding files with no threshold in the name
        self.threshold = segments[5][1:] if len(segments) > 5 else None
        self.differenceGroup = f"{self.difference} Differences ({self.endDate.strftime('%b %d')}–{self.startDate.strftime('%b %d')})"
   
        QgsVectorLayer.__init__(self, self.shapefilePath.as_posix(), f"{self.difference} Threshold {self.threshold}", "ogr")        
        self._mapping = mapping
        
    # Item interface
    @property
    def directory(self) -> Path:
        return self.mapping.directory

    @property
    def displayName(self) -> str:
        return f"{self.difference} Threshold {self.threshold}"

    @property
    def layerItemName(self) -> str:
        return f"Threshold {self.threshold}"

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
            self.willBeDeleted.connect(lambda: self.layerRemoved.emit(self.id()))
            
            # load one of two styles based on the threshold used to segment these features
            if int(self.threshold) < 200:
                self.loadStyle("lower_threshold")
            else:
                self.loadStyle("higher_threshold")

            self.layerAdded.emit(self.id())
            self.subGroupLayerItem.addLayer(self)
            
            # don't show legend initially
            self.layerItem.setExpanded(True)
            self.layerItem.setExpanded(False)
        else:
            error = (f"An error occurred adding the layer {self.layerItemName} to the map.\n"
                     f"Check your QGIS WMS message log for details.")
            guiError(error)

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        self.loadNamedStyle(stylePath)