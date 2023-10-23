# -*- coding: utf-8 -*-
from datetime import datetime

from qgis.core import QgsProject

from .src.models import *


def test_Mapping() -> None:
    mapping = Mapping('Darwin', datetime.today())
    assert mapping.directory is not None
    assert mapping.layerItemName is not None
    assert mapping.layerItem is not None


def test_CurrentMappingLayer() -> None:
    mapping = Mapping('Darwin', datetime.today())
    currentMapping = CurrentMappingLayer(
        mapping, '/Users/tom/Documents/Development/trm/nafi/data/Scratch/Darwin/rasterised.tif')    
    currentMapping.addMapLayer()
    # QgsProject.instance().removeMapLayer(currentMapping)


def test_SegmentationLayer() -> None:
    mapping = Mapping('Darwin', datetime.today())
    segmentation = SegmentationLayer(
        mapping, '/Users/tom/Documents/Development/trm/nafi/data/Scratch/20231016/Darwin/darwin/T1T2/T1T2_darwin_T20231016_T20231011_seg_t150.shp')    
    segmentation.addMapLayer()
    # QgsProject.instance().removeMapLayer(segmentation)


def test_all() -> None:
    test_Mapping()
    test_CurrentMappingLayer()
    test_SegmentationLayer()
