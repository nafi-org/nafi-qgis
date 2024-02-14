from ntrrp.src.api import ApiService
from ntrrp.src.models import MartinLayer
from ntrrp.hires_client.models import (
    DifferenceResponse,
    MappingResponse,
    SegmentationDatasetResponse,
)


def getPublishedSegmentationDatasets() -> list[SegmentationDatasetResponse]:
    api = ApiService("http://localhost:8000")
    mappings: list[MappingResponse] = api.get_mappings()
    [mapping] = mappings
    difference: DifferenceResponse = mapping.differences[0]
    segmentation_datasets: list[SegmentationDatasetResponse] = (
        difference.segmentation_datasets
    )
    return [sd for sd in segmentation_datasets if sd.published]


def testMartinLayer() -> MartinLayer:
    segmentation_datasets = getPublishedSegmentationDatasets()
    for segmentation_dataset in segmentation_datasets:
        martin_layer = MartinLayer(segmentation_dataset)
        martin_layer.addMapLayer()
        # return martin_layer


def testBoundary():
    segmentation_datasets = getPublishedSegmentationDatasets()
    for segmentation_dataset in segmentation_datasets:
        print(segmentation_dataset.boundary)
