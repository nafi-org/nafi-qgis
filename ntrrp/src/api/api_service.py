from typing import Any, Optional

from ntrrp.hires_client.apis import AcquisitionsApi, MappingsApi, SegmentationApi
from ntrrp.hires_client.exceptions import OpenApiException
from ntrrp.hires_client.models import (
    AcquisitionResponse,
    ApproveSegmentationFeatures,
    MappingResponse,
    RefreshTilesResponse,
    SegmentationDatasetResponse,
    UnapproveSegmentationFeatures,
)

from .client import get_client


class ApiService:
    def __init__(self, host_uri: str):
        self.host_uri = host_uri
        self.client = get_client(host_uri)
        self.acquisitions = AcquisitionsApi(self.client)
        self.mappings = MappingsApi(self.client)
        self.segmentation = SegmentationApi(self.client)

    def getAcquisitions(self, region_name: str) -> list[AcquisitionResponse]:
        """Get HiRes Acquisitions for a region."""
        try:
            return self.acquisitions.get_acquisitions_v1_acquisitions_region_name_get(
                region_name
            )
        except OpenApiException as e:
            print(f"Exception on AcquisitionsApi->getAcquisitions: {e}")

    def getMappings(self, region_name: str) -> list[MappingResponse]:
        """Get HiRes Mappings."""
        try:
            return self.mappings.get_mappings_v1_mappings_region_name_get(region_name)
        except OpenApiException as e:
            print(f"Exception on MappingsApi->getMappings: {e}")

    def approveSegmentation(
        self,
        mapping_uuid: str,
        segmentation_dataset_uuid: str,
        bounds: list[float],
        feature_ids: Optional[list[int]] = [],
    ) -> Any:
        """Approve segmentation features."""
        try:
            return self.segmentation.approve_segmentation_v1_segmentation_approve_mapping_uuid_segmentation_dataset_uuid_post(
                mapping_uuid,
                segmentation_dataset_uuid,
                ApproveSegmentationFeatures(bounds=bounds, feature_ids=feature_ids),
            )
        except OpenApiException as e:
            print(f"Exception on SegmentationApi->approveSegmentation: {e}")

    def rejectSegmentation(
        self,
        mapping_uuid: str,
        segmentation_dataset_uuid: str,
        bounds: list[float],
        feature_ids: Optional[list[int]] = [],
    ) -> Any:
        """Reject segmentation features."""
        try:
            return self.segmentation.reject_segmentation_v1_segmentation_reject_mapping_uuid_segmentation_dataset_uuid_post(
                mapping_uuid,
                segmentation_dataset_uuid,
                ApproveSegmentationFeatures(bounds=bounds, feature_ids=feature_ids),
            )
        except OpenApiException as e:
            print(f"Exception on SegmentationApi->rejectSegmentation: {e}")
