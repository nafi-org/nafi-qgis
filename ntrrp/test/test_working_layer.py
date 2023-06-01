# -*- coding: utf-8 -*-
import unittest

import os
import os.path as path
from pathlib import Path

from src.layer.working_layer import WorkingLayer
from layer.segmentation_layer import SegmentationLayer
from src.utils import getWorkingDirectory

TEST_SOURCE = Path(path.normpath(path.join(path.dirname(__file__), os.pardir, os.pardir,
                   "ntrrp_data", "test", "test_source", "T1T3_darwin_T20210926_T20210916_seg_sa1_t100.shp")))


class TestWorkingLayer(unittest.TestCase):

    # a WorkingLayer is created from a template SegmentationLayer
    def getSegmentationLayer(self):
        return SegmentationLayer(TEST_SOURCE)

    def test_create(self):
        workingLayer = WorkingLayer(self.getSegmentationLayer())
        print(workingLayer.shapefilePath)
        self.assertTrue(Path(getWorkingDirectory()) in Path(
            workingLayer.shapefilePath).parents, "Working layer shapefile is not in working directory!")

    def test_save(self):
        workingLayer = WorkingLayer(self.getSegmentationLayer())
        workingLayer.save()
        self.assertTrue(Path(workingLayer.shapefilePath).exists(
        ), f"Working layer with shapefile {workingLayer.shapefilePath} not created on filesystem!")
