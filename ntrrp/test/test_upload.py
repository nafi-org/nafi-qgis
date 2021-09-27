import os.path as path
import unittest

from src.processing.dissolve_burnt_areas import DissolveBurntAreas
from src.processing.attribute_burnt_areas import AttributeBurntAreas
from src.processing.rasterise_burnt_areas import RasteriseBurntAreas

class TestUpload(unittest.TestCase):

    def test_archive(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you

    def test_upload(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you

    def test_archive_and_upload(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you

