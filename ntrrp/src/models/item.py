# -*- coding: utf-8 -*-
from abc import ABC, abstractproperty

from pathlib import Path

from qgis.core import QgsLayerTreeLayer

from .abstract_qobject_meta import AbstractQObjectMeta


class Item(ABC, metaclass=AbstractQObjectMeta):
    """Abstract representation for any NAFI Hires project item, such as a Mapping,
       SegmentationLayer, WorkingLayer, etc."""

    @abstractproperty
    def directory(self) -> Path:
        """Return the filesystem directory for this Item."""
        pass

    @abstractproperty
    def layerItem(self) -> QgsLayerTreeLayer:
        """Return the QGIS layer item (in the Layers panel) for this Item."""
        pass
    
    @abstractproperty
    def layerItemName(self) -> str:
        """Return the name of the QGIS layer item for this Item."""
        pass
    
    
    