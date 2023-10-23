# -*- coding: utf-8 -*-
from typing import List

from datetime import datetime
from pathlib import Path

from qgis.core import QgsLayerTreeNode, QgsProject

from ..utils import deriveWorkingDirectory
from .item import Item


class Mapping(Item):
    """Represent a NAFI Hires Mapping activity for a particular time period."""

    def __init__(self, region: str, mappingDate: datetime, wmsUrl: str=None, owsLayers: List[object]=[]):
        Item.__init__(self)
        self.region: str = region
        self.mappingDate: datetime = mappingDate
        self.wmsUrl: str = wmsUrl
        self.owsLayers = owsLayers
        self.segmentationLayers = []
        self.workingLayers = []
        self.currentMappingLayer = None

    @property
    def directory(self):
        workingDirectory = deriveWorkingDirectory()
        return None if workingDirectory is None else Path(
            workingDirectory) / self.mappingDate.strftime('%Y%m%d') / self.region

    @property
    def layerItemName(self):
        return f"{self.region} Burnt Areas Mapping ({self.mappingDate.strftime('%b %d')})"

    @property
    def layerItem(self) -> QgsLayerTreeNode:
        root = QgsProject.instance().layerTreeRoot()
        groupLayer = root.findGroup(self.layerItemName)
        if groupLayer is None:
            root.insertGroup(0, self.layerItemName)
            groupLayer = root.findGroup(self.layerItemName)
        return groupLayer