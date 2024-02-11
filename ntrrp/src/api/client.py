from ntrrp.hires_client import ApiClient, Configuration


def get_client(host_uri) -> ApiClient:
    """Get a client for the HiRes API."""
    configuration = Configuration(host=host_uri)
    configuration.verify_ssl = False
    return ApiClient(configuration)
