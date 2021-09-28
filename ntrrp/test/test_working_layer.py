import unittest

from pathlib import Path

from src.ntrrp_working_layer import NtrrpWorkingLayer
from src.utils import getWorkingDirectory

class TestWorkingLayer(unittest.TestCase):

    # def test_getWorkingDirectory(self):
    #     print(path.join(os.environ["TMP"], "ntrrp", "working"))
    #     print(os.environ["TMP"])
    #     print(getWorkingDirectory())

    # def test_getDownloadDirectory(self):
    #     print(getDownloadDirectory())

    def test_create(self):
        workingLayer = NtrrpWorkingLayer("Darwin", "1")
        print(workingLayer.shapefilePath)
        self.assertTrue(Path(getWorkingDirectory()) in Path(workingLayer.shapefilePath).parents, "Working layer shapefile is not in working directory!")

    def test_save(self):
        workingLayer = NtrrpWorkingLayer("Darwin", "1")
        workingLayer.save()
        self.assertTrue(Path(workingLayer.shapefilePath).exists(), f"Working layer with shapefile {workingLayer.shapefilePath} not created on filesystem!")
