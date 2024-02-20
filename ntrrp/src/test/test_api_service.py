import unittest
from random import random

from ntrrp.hires_client.models import (
    ApproveSegmentationFeatures,
    DifferenceResponse,
    MappingResponse,
    SegmentationDatasetResponse,
    UnapproveSegmentationFeatures,
)
from ntrrp.src.api import ApiService
from ntrrp.src.models import HiResSegmentationLayer


def getPublishedSegmentationDatasets() -> list[SegmentationDatasetResponse]:
    api = ApiService("http://localhost:8000")
    mappings: list[MappingResponse] = api.getMappings("Darwin")
    [mapping] = mappings
    difference: DifferenceResponse = mapping.differences[0]
    datasets: list[SegmentationDatasetResponse] = difference.datasets
    assert len(datasets) > 0
    return [sd for sd in datasets if sd.published]


def randomBounds(bounds: list[float]) -> list[float]:
    """Generate a random smaller bounding box within the specified bounds."""
    [xmin, ymin, xmax, ymax] = bounds
    xs = [xmin + random() * (xmax - xmin) for _ in range(2)]
    ys = [ymin + random() * (ymax - ymin) for _ in range(2)]
    return [min(xs), min(ys), max(xs), max(ys)]


def addHiResSegmentationLayerToMap(
    dataset: SegmentationDatasetResponse,
) -> HiResSegmentationLayer:
    layer = HiResSegmentationLayer(dataset)
    layer.addMapLayer()
    return layer


def testApproveSegmentationByBounds():
    datasets = getPublishedSegmentationDatasets()

    for dataset in datasets:
        api = ApiService("http://localhost:8000")


def testUnapproveSegmentationByBounds():
    datasets = getPublishedSegmentationDatasets()

    for dataset in datasets:
        api = ApiService("http://localhost:8000")

        unapprovalBounds = randomBounds(dataset.boundary)

        api.rejectSegmentation(
            dataset, UnapproveSegmentationFeatures(bounds=unapprovalBounds)
        )


class TestApiService(unittest.TestCase):
    # Add a fixture for the published segmentation datasets
    def setUp(self):
        self.datasets = getPublishedSegmentationDatasets()
        self.api = ApiService("http://localhost:8000")

    def test_getPublishedSegmentationDatasets(self):
        self.assertTrue(len(self.datasets) > 0)
        self.assertTrue(all([sd.published for sd in self.datasets]))
        self.assertTrue(
            all([sd.boundary and len(sd.boundary) == 4 for sd in self.datasets])
        )

    def test_addHiResSegmentationLayerToMap(self):
        layer = addHiResSegmentationLayerToMap(self.datasets[0])
        self.assertTrue(layer.isValid())
        self.assertTrue(isinstance(layer, HiResSegmentationLayer))

    def test_approveSegmentationByBounds(self):
        approvalBounds = randomBounds(self.datasets[0].boundary)
        self.api.approveSegmentation(
            self.datasets[0], ApproveSegmentationFeatures(bounds=approvalBounds)
        )

    def test_unapproveSegmentationByBounds(self):
        unapprovalBounds = randomBounds(self.datasets[0].boundary)
        self.api.rejectSegmentation(
            self.datasets[0], UnapproveSegmentationFeatures(bounds=unapprovalBounds)
        )
