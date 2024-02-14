from typing import Any
from ntrrp.hires_client.apis import AcquisitionsApi, MappingsApi, SegmentationApi
from ntrrp.hires_client.exceptions import OpenApiException
from ntrrp.hires_client.models import (
    AcquisitionResponse,
    ApproveSegmentationFeatures,
    RefreshTilesResponseResponse,
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

    def get_acquisitions(self, region_name: str) -> list[AcquisitionResponse]:
        """Get Hires Acquisitions for a region."""
        try:
            return self.acquisitions.get_acquisitions_v1_acquisitions_region_name_get(
                region_name
            )
        except OpenApiException as e:
            print(f"Exception when calling AcquisitionsApi->get_acquisitions: {e}")

    def get_mappings(self) -> list[AcquisitionResponse]:
        """Get Hires Mappings."""
        try:
            return self.mappings.get_mappings_v1_mappings_get()
        except OpenApiException as e:
            print(f"Exception when calling MappingsApi->get_mappings: {e}")

    def approve_segmentation(
        self,
        segmentation_dataset: SegmentationDatasetResponse,
        features: ApproveSegmentationFeatures,
    ) -> Any:
        """Approve segmentation features."""
        try:
            return self.segmentation.approve_segmentation_v1_segmentationapprove_segmentation_dataset_uuid_post(
                segmentation_dataset.uuid, features
            )
        except OpenApiException as e:
            print(f"Exception when calling SegmentationApi->approve_segmentation: {e}")

    def unapprove_segmentation(
        self,
        segmentation_dataset: SegmentationDatasetResponse,
        features: ApproveSegmentationFeatures,
    ) -> Any:
        """Unapprove segmentation features."""
        try:
            return self.segmentation.unapprove_segmentation_v1_segmentationunapprove_segmentation_dataset_uuid_post(
                segmentation_dataset.uuid, features
            )
        except OpenApiException as e:
            print(
                f"Exception when calling SegmentationApi->unapprove_segmentation: {e}"
            )
