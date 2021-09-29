import unittest

from pathlib import Path

from src.layer.working_layer import WorkingLayer
from src.utils import getWorkingDirectory

class TestWorkingLayer(unittest.TestCase):

    def test_create(self):
        workingLayer = WorkingLayer()
        print(workingLayer.shapefilePath)
        self.assertTrue(Path(getWorkingDirectory()) in Path(workingLayer.shapefilePath).parents, "Working layer shapefile is not in working directory!")

    def test_save(self):
        workingLayer = WorkingLayer()
        workingLayer.save()
        self.assertTrue(Path(workingLayer.shapefilePath).exists(), f"Working layer with shapefile {workingLayer.shapefilePath} not created on filesystem!")
