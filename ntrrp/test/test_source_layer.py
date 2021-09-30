import unittest

import os
import os.path as path
from pathlib import Path

from src.layer.source_layer import SourceLayer
from src.utils import getWorkingDirectory

TEST_SOURCE = Path(path.normpath(path.join(path.dirname(__file__), os.pardir, os.pardir, "ntrrp_data", "test", "test_source", "T1T3_darwin_T20210926_T20210916_seg_sa1_t100.shp")))

class TestSourceLayer(unittest.TestCase):

    # a WorkingLayer is created from a template SourceLayer
    def test_create(self):
        sourceLayer = SourceLayer(TEST_SOURCE)
        self.assertIsNotNone(sourceLayer.impl)