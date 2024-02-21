
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.acquisitions_api import AcquisitionsApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from nafi_hires.hires_client.api.acquisitions_api import AcquisitionsApi
from nafi_hires.hires_client.api.health_api import HealthApi
from nafi_hires.hires_client.api.mappings_api import MappingsApi
from nafi_hires.hires_client.api.regions_api import RegionsApi
from nafi_hires.hires_client.api.segmentation_api import SegmentationApi
from nafi_hires.hires_client.api.tasks_api import TasksApi
from nafi_hires.hires_client.api.users_api import UsersApi
