from ntrrp.hires_client import ApiClient
from ntrrp.hires_client.apis import AcquisitionsApi, MappingsApi
from ntrrp.hires_client.exceptions import OpenApiException
from ntrrp.hires_client.models import AcquisitionResponse

from .client import get_client


class ApiService:
    def __init__(self, host_uri: str):
        self.host_uri = host_uri
        self.client = get_client(host_uri)
        self.acquisitions = AcquisitionsApi(self.client)
        self.mappings = MappingsApi(self.client)

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
