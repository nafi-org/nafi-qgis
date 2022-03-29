# -*- coding: utf-8 -*-
import unittest

import gdal
import os
import os.path as path
from pathlib import Path

from src.processing.color_table import FIRESCAR_COLOR_TABLE, addColorTable, getColorTable
from src.processing.dissolve_burnt_areas import DissolveBurntAreas
from src.processing.attribute_burnt_areas import AttributeBurntAreas
from src.processing.rasterise_burnt_areas import RasteriseBurntAreas

TEST_TIF = Path(path.normpath(path.join(path.dirname(__file__), os.pardir,
                os.pardir, "ntrrp_data", "test", "FSDRW_current_sr3577.tif")))
TEST_APPROVED = Path(path.normpath(path.join(path.dirname(
    __file__), os.pardir, os.pardir, "ntrrp_data", "test", "test_working", "approved.shp")))
NTRRP_DATA = path.normpath(path.join(path.dirname(
    __file__), os.pardir, os.pardir, "ntrrp_data"))


class TestProcess(unittest.TestCase):

    def test_addColorTable(self):
        addColorTable(TEST_TIF)

        table = getColorTable(TEST_TIF)
        self.assertEqual(table, FIRESCAR_COLOR_TABLE)

    def test_approvedExists(self):
        self.assertTrue(TEST_APPROVED.exists(),
                        "Sample approved features path is incorrect!")

    # def test_dissolveBurntAreas(self):
    #     # evaluate
    #     dissolve = DissolveBurntAreas()
    #     dissolve.initAlgorithm()

    #     parameters = {
    #         'BurntAreas': TEST_APPROVED
    #     }

    #     dissolve.processAlgorithm(parameters, None, None)

    #     self.assertEqual(1, 2 - 1)
    #     # todo it makes more sense to compare the actual content of the array, we leave this up to you

    def test_attributeBurntAreas(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you

    def test_rasteriseBurntAreas(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you

    def test_doAll(self):
        # evaluate
        self.assertEqual(1, 2 - 1)
        # todo it makes more sense to compare the actual content of the array, we leave this up to you
