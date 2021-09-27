import os
import os.path as path
import unittest

from src.processing.dissolve_burnt_areas import DissolveBurntAreas
from src.processing.attribute_burnt_areas import AttributeBurntAreas
from src.processing.rasterise_burnt_areas import RasteriseBurntAreas

NTRRP_DATA = path.normpath(path.join(path.dirname(__file__), os.pardir, os.pardir, "ntrrp_data"))

class TestProcess(unittest.TestCase):

    def test_dissolve_burnt_areas(self):
        # evaluate
        print(NTRRP_DATA)
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you

    def test_attribute_burnt_areas(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you

    def test_rasterise_burnt_areas(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you

    def test_burnt_areas(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you