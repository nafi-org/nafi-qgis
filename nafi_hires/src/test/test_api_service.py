import unittest
from random import random

from qgis.core import QgsProject

from nafi_hires.src.api import *


def randomBounds(bounds: list[float]) -> list[float]:
    """Generate a random smaller bounding box within the specified bounds."""
    [xmin, ymin, xmax, ymax] = bounds
    xs = [xmin + random() * (xmax - xmin) for _ in range(2)]
    ys = [ymin + random() * (ymax - ymin) for _ in range(2)]
    return [min(xs), min(ys), max(xs), max(ys)]


class TestApiService(unittest.TestCase):
    # Add a fixture for the published segmentation datasets
    def setUp(self):
        self.api = HiResApiService("http://localhost:8000")
        self.mappings = self.api.getMappings("Darwin")
        self.mapping = self.mappings[0]
        self.datasets = self.api.groupSegmentationDatasets(self.mapping)

    def test_getIngestedSegmentationDatasets(self):
        self.assertTrue(len(self.datasets) > 0)
        self.assertTrue(all([sd.ingested for sd in self.datasets]))
