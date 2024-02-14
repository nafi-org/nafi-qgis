from random import random

from qgis.core import QgsRectangle

from ntrrp.src.api import ApiService
from ntrrp.src.models import HiresSegmentationLayer
from ntrrp.hires_client.models import (
    ApproveSegmentationFeatures,
    UnapproveSegmentationFeatures,
    DifferenceResponse,
    MappingResponse,
    SegmentationDatasetResponse,
)


def getPublishedSegmentationDatasets() -> list[SegmentationDatasetResponse]:
    api = ApiService("http://localhost:8000")
    mappings: list[MappingResponse] = api.get_mappings()
    [mapping] = mappings
    difference: DifferenceResponse = mapping.differences[0]
    datasets: list[SegmentationDatasetResponse] = difference.datasets
    return [sd for sd in datasets if sd.published]


def randomBounds(bounds: list[float]) -> list[float]:
    """Generate a random smaller bounding box within the specified bounds."""
    [xmin, ymin, xmax, ymax] = bounds
    xs = [xmin + random() * (xmax - xmin) for _ in range(2)]
    ys = [ymin + random() * (ymax - ymin) for _ in range(2)]
    return [min(xs), min(ys), max(xs), max(ys)]


def testAddHiresSegmentationLayerToMap() -> HiresSegmentationLayer:
    datasets = getPublishedSegmentationDatasets()
    for dataset in datasets:
        layer = HiresSegmentationLayer(dataset)
        layer.addMapLayer()


def testBoundary():
    datasets = getPublishedSegmentationDatasets()
    for dataset in datasets:
        print(dataset.boundary)


def testApproveSegmentationByBounds():
    datasets = getPublishedSegmentationDatasets()

    for dataset in datasets:
        api = ApiService("http://localhost:8000")

        approvalBounds = randomBounds(dataset.boundary)

        api.approve_segmentation(
            dataset, ApproveSegmentationFeatures(bounds=approvalBounds)
        )


def testUnapproveSegmentationByBounds():
    datasets = getPublishedSegmentationDatasets()

    for dataset in datasets:
        api = ApiService("http://localhost:8000")

        unapprovalBounds = randomBounds(dataset.boundary)

        api.unapprove_segmentation(
            dataset, UnapproveSegmentationFeatures(bounds=unapprovalBounds)
        )
