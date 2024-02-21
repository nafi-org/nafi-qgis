from collections import defaultdict
from typing import Any, Optional

from nafi_hires.hires_client import ApiClient, Configuration, OpenApiException
from nafi_hires.hires_client.apis import AcquisitionsApi, MappingsApi, SegmentationApi
from nafi_hires.hires_client.models import (
    AcquisitionResponse,
    ApproveSegmentationFeatures,
    MappingResponse,
    RefreshTilesResponse,
    RejectSegmentationFeatures,
    SegmentationDatasetResponse,
)
from nafi_hires.src.utils import getHiResApiUrl, qgsDebug


class HiResApiService:
    def __init__(self, hostUri: str = getHiResApiUrl()):
        self.hostUri = hostUri

        configuration = Configuration(host=self.hostUri)
        configuration.verify_ssl = False
        configuration.discard_unknown_keys = True
        self.client: ApiClient = ApiClient(configuration)

        self.acquisitionApi = AcquisitionsApi(self.client)
        self.mappingApi = MappingsApi(self.client)
        self.segmentationApi = SegmentationApi(self.client)

    def __del__(self):
        self.client.close()

    def getAcquisitions(self, regionName: str) -> list[AcquisitionResponse]:
        """Get HiRes Acquisitions for a region."""
        try:
            return self.acquisitionApi.get_acquisitions_v1_acquisitions_region_name_get(
                regionName
            )
        except OpenApiException as e:
            print(f"Exception on AcquisitionsApi->getAcquisitions: {e}")

    def getMappings(self, regionName: str) -> list[MappingResponse]:
        """Get HiRes Mappings."""
        try:
            return self.mappingApi.get_mappings_v1_mappings_region_name_get(regionName)
        except OpenApiException as e:
            print(f"Exception on MappingsApi->getMappings: {e}")

    def groupSegmentationDatasets(
        self, mapping: MappingResponse
    ) -> list[SegmentationDatasetResponse]:
        """Get Segmentation Datasets from a Mapping."""

        # First get a list of _all_ the datasets
        datasets: list[SegmentationDatasetResponse] = []
        for difference in mapping.differences:
            difference_datasets: list[SegmentationDatasetResponse] = (
                difference.segmentation_datasets
            )
            assert isinstance(difference_datasets, list)
            datasets.extend(difference_datasets)

        # Then group by when they have the same code, difference code and threshold
        # Only return the groups - no keys
        groups: dict[str, list[SegmentationDatasetResponse]] = defaultdict(list)
        for dataset in datasets:
            key = f"{int(dataset.code)}_{int(dataset.difference_code)}_{int(dataset.threshold)}"
            groups[key].append(dataset)

        return list(groups.values())

    def approveSegmentation(
        self,
        mappingUUID: str,
        segmentationDatasetUUID: str,
        bounds: list[float],
        feature_ids: Optional[list[int]] = [],
    ) -> Any:
        """Approve segmentation features."""
        try:
            return self.segmentationApi.approve_segmentation_v1_segmentation_approve_mapping_uuid_segmentation_dataset_uuid_post(
                mappingUUID,
                segmentationDatasetUUID,
                ApproveSegmentationFeatures(bounds=bounds, feature_ids=feature_ids),
            )
        except OpenApiException as e:
            print(f"Exception on SegmentationApi->approveSegmentation: {e}")

    def rejectSegmentation(
        self,
        mappingUUID: str,
        segmentationDatasetUUID: str,
        bounds: list[float],
        feature_ids: Optional[list[int]] = [],
    ) -> Any:
        """Reject segmentation features."""
        try:
            return self.segmentationApi.reject_segmentation_v1_segmentation_reject_mapping_uuid_segmentation_dataset_uuid_post(
                mappingUUID,
                segmentationDatasetUUID,
                ApproveSegmentationFeatures(bounds=bounds, feature_ids=feature_ids),
            )
        except OpenApiException as e:
            print(f"Exception on SegmentationApi->rejectSegmentation: {e}")
