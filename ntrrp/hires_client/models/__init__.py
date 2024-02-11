# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from ntrrp.hires_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from ntrrp.hires_client.model.acquisition_response import AcquisitionResponse
from ntrrp.hires_client.model.difference_response import DifferenceResponse
from ntrrp.hires_client.model.dmirbi_dataset_response import DmirbiDatasetResponse
from ntrrp.hires_client.model.error_response import ErrorResponse
from ntrrp.hires_client.model.http_validation_error import HTTPValidationError
from ntrrp.hires_client.model.health import Health
from ntrrp.hires_client.model.login_user_request import LoginUserRequest
from ntrrp.hires_client.model.mapping_response import MappingResponse
from ntrrp.hires_client.model.mirbi_dataset_response import MirbiDatasetResponse
from ntrrp.hires_client.model.natural_colour_dataset_response import (
    NaturalColourDatasetResponse,
)
from ntrrp.hires_client.model.region_response import RegionResponse
from ntrrp.hires_client.model.register_user_request import RegisterUserRequest
from ntrrp.hires_client.model.segmentation_dataset_response import (
    SegmentationDatasetResponse,
)
from ntrrp.hires_client.model.sentinel2_tile_response import Sentinel2TileResponse
from ntrrp.hires_client.model.task_create import TaskCreate
from ntrrp.hires_client.model.task_response import TaskResponse
from ntrrp.hires_client.model.task_type import TaskType
from ntrrp.hires_client.model.token import Token
from ntrrp.hires_client.model.user_response import UserResponse
from ntrrp.hires_client.model.validation_error import ValidationError
