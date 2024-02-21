# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from nafi_hires.hires_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from nafi_hires.hires_client.model.acquisition_response import AcquisitionResponse
from nafi_hires.hires_client.model.approve_segmentation_features import ApproveSegmentationFeatures
from nafi_hires.hires_client.model.difference_response import DifferenceResponse
from nafi_hires.hires_client.model.dmirbi_dataset_response import DmirbiDatasetResponse
from nafi_hires.hires_client.model.error_response import ErrorResponse
from nafi_hires.hires_client.model.http_validation_error import HTTPValidationError
from nafi_hires.hires_client.model.health import Health
from nafi_hires.hires_client.model.login_user_request import LoginUserRequest
from nafi_hires.hires_client.model.mapping_response import MappingResponse
from nafi_hires.hires_client.model.mirbi_dataset_response import MirbiDatasetResponse
from nafi_hires.hires_client.model.natural_colour_dataset_response import NaturalColourDatasetResponse
from nafi_hires.hires_client.model.refresh_tiles_response import RefreshTilesResponse
from nafi_hires.hires_client.model.region_response import RegionResponse
from nafi_hires.hires_client.model.register_user_request import RegisterUserRequest
from nafi_hires.hires_client.model.reject_segmentation_features import RejectSegmentationFeatures
from nafi_hires.hires_client.model.segmentation_dataset_response import SegmentationDatasetResponse
from nafi_hires.hires_client.model.sentinel2_tile_response import Sentinel2TileResponse
from nafi_hires.hires_client.model.task_create import TaskCreate
from nafi_hires.hires_client.model.task_response import TaskResponse
from nafi_hires.hires_client.model.task_state import TaskState
from nafi_hires.hires_client.model.task_type import TaskType
from nafi_hires.hires_client.model.tile import Tile
from nafi_hires.hires_client.model.token import Token
from nafi_hires.hires_client.model.user_response import UserResponse
from nafi_hires.hires_client.model.validation_error import ValidationError
