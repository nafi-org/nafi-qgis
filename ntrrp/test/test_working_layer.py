import unittest

import os
import os.path as path
from pathlib import Path

from src.layer.working_layer import WorkingLayer
from src.layer.source_layer import SourceLayer
from src.utils import getWorkingDirectory

TEST_SOURCE = Path(path.normpath(path.join(path.dirname(__file__), os.pardir, os.pardir, "ntrrp_data", "test", "test_source", "T1T3_darwin_T20210926_T20210916_seg_sa1_t100.shp")))

class TestWorkingLayer(unittest.TestCase):

    # a WorkingLayer is created from a template SourceLayer
    def getSourceLayer(self):
        return SourceLayer(TEST_SOURCE)

    def test_create(self):
        workingLayer = WorkingLayer(self.getSourceLayer())
        print(workingLayer.gpkgPath)
        self.assertTrue(Path(getWorkingDirectory()) in Path(workingLayer.gpkgPath).parents, "Working layer shapefile is not in working directory!")

    def test_save(self):
        workingLayer = WorkingLayer(self.getSourceLayer())
        workingLayer.save()
        self.assertTrue(Path(workingLayer.gpkgPath).exists(), f"Working layer with shapefile {workingLayer.gpkgPath} not created on filesystem!")
