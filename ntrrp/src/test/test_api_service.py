import unittest
from random import random

from qgis.core import QgsProject

from ntrrp.hires_client.models import (
    ApproveSegmentationFeatures,
    DifferenceResponse,
    MappingResponse,
    RejectSegmentationFeatures,
    SegmentationDatasetResponse,
)
from ntrrp.src.api import ApiService
from ntrrp.src.models import HiResSegmentationLayer


def randomBounds(bounds: list[float]) -> list[float]:
    """Generate a random smaller bounding box within the specified bounds."""
    [xmin, ymin, xmax, ymax] = bounds
    xs = [xmin + random() * (xmax - xmin) for _ in range(2)]
    ys = [ymin + random() * (ymax - ymin) for _ in range(2)]
    return [min(xs), min(ys), max(xs), max(ys)]


class TestApiService(unittest.TestCase):
    # Add a fixture for the published segmentation datasets
    def setUp(self):
        self.api = ApiService("http://localhost:8000")
        self.mappings = self.api.getMappings("Darwin")
        self.mapping = self.mappings[0]
        self.datasets = self.api.getIngestedSegmentationDatasets(self.mapping)

    def test_getIngestedSegmentationDatasets(self):
        self.assertTrue(len(self.datasets) > 0)
        self.assertTrue(all([sd.ingested for sd in self.datasets]))

    def test_addHiResSegmentationLayer(self):
        layer = self.api.addHiResSegmentationLayer(self.datasets[0])
        self.assertTrue(layer.isValid())
        self.assertTrue(isinstance(layer, HiResSegmentationLayer))
        QgsProject.instance().removeMapLayer(layer)

    def test_addHiResSegmentationLayers(self):
        layers = self.api.addHiResSegmentationLayers(self.mapping)
        self.assertTrue(len(layers) > 0)
        self.assertTrue(all([layer.isValid() for layer in layers]))
        for layer in layers:
            QgsProject.instance().removeMapLayer(layer)

    # def test_addHiResSegmentationLayers(self):
    #     approvalBounds = randomBounds(self.datasets[0].boundary)
    #     self.api.approveSegmentation(
    #         self.datasets[0], ApproveSegmentationFeatures(bounds=approvalBounds)
    #     )

    # def test_unapproveSegmentationByBounds(self):
    #     unapprovalBounds = randomBounds(self.datasets[0].boundary)
    #     self.api.rejectSegmentation(
    #         self.datasets[0], RejectSegmentationFeatures(bounds=unapprovalBounds)
    #     )
