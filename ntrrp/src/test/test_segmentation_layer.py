# import unittest

# import os
# import os.path as path
# from pathlib import Path

# from ..models import SegmentationLayer

# TEST_SOURCE = Path(
#     path.normpath(
#         path.join(
#             path.dirname(__file__),
#             os.pardir,
#             os.pardir,
#             "ntrrp_data",
#             "test",
#             "test_source",
#             "T1T3_darwin_T20210926_T20210916_seg_sa1_t100.shp",
#         )
#     )
# )


# class TestSegmentationLayer(unittest.TestCase):
#     def test_create(self):
#         segmentationLayer = SegmentationLayer(TEST_SOURCE)
#         assert segmentationLayer.isValid()
