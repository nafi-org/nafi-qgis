from typing import Any, Optional

from nafi_hires.hires_client.apis import AcquisitionsApi, MappingsApi, SegmentationApi
from nafi_hires.hires_client.exceptions import OpenApiException
from nafi_hires.hires_client.models import (
    AcquisitionResponse,
    ApproveSegmentationFeatures,
    MappingResponse,
    RefreshTilesResponse,
    RejectSegmentationFeatures,
    SegmentationDatasetResponse,
)

from .client import get_client


class HiResApiService:
    def __init__(self, hostUri: str = "http://localhost:8000"):
        self.host_uri = hostUri
        self.client = get_client(hostUri)
        self.acquisitions = AcquisitionsApi(self.client)
        self.mappings = MappingsApi(self.client)
        self.segmentation = SegmentationApi(self.client)

    def getAcquisitions(self, regionName: str) -> list[AcquisitionResponse]:
        """Get HiRes Acquisitions for a region."""
        try:
            return self.acquisitions.get_acquisitions_v1_acquisitions_region_name_get(
                regionName
            )
        except OpenApiException as e:
            print(f"Exception on AcquisitionsApi->getAcquisitions: {e}")

    def getMappings(self, regionName: str) -> list[MappingResponse]:
        """Get HiRes Mappings."""
        try:
            return self.mappings.get_mappings_v1_mappings_region_name_get(regionName)
        except OpenApiException as e:
            print(f"Exception on MappingsApi->getMappings: {e}")

    def getIngestedSegmentationDatasets(
        self, mapping: MappingResponse
    ) -> list[SegmentationDatasetResponse]:
        """Get ingested Segmentation Datasets."""
        return [
            sd
            for difference in mapping.differences
            for sd in difference.segmentation_datasets
            if sd.ingested
        ]

    def approveSegmentation(
        self,
        mappingUUID: str,
        segmentationDatasetUUID: str,
        bounds: list[float],
        feature_ids: Optional[list[int]] = [],
    ) -> Any:
        """Approve segmentation features."""
        try:
            return self.segmentation.approve_segmentation_v1_segmentation_approve_mapping_uuid_segmentation_dataset_uuid_post(
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
            return self.segmentation.reject_segmentation_v1_segmentation_reject_mapping_uuid_segmentation_dataset_uuid_post(
                mappingUUID,
                segmentationDatasetUUID,
                ApproveSegmentationFeatures(bounds=bounds, feature_ids=feature_ids),
            )
        except OpenApiException as e:
            print(f"Exception on SegmentationApi->rejectSegmentation: {e}")
