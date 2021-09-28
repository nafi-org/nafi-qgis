import unittest

from pathlib import Path

from src.ntrrp_working_layer import NtrrpWorkingLayer
from src.utils import getWorkingDirectory

class TestWorkingLayer(unittest.TestCase):

    def test_create(self):
        workingLayer = NtrrpWorkingLayer()
        print(workingLayer.shapefilePath)
        self.assertTrue(Path(getWorkingDirectory()) in Path(workingLayer.shapefilePath).parents, "Working layer shapefile is not in working directory!")

    def test_save(self):
        workingLayer = NtrrpWorkingLayer()
        workingLayer.save()
        self.assertTrue(Path(workingLayer.shapefilePath).exists(), f"Working layer with shapefile {workingLayer.shapefilePath} not created on filesystem!")
