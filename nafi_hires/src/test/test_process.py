import os
import os.path as path
import unittest
from pathlib import Path

from nafi_hires.src.processing.color_table import (
    FIRESCAR_COLOR_TABLE,
    addColorTable,
    getColorTable,
)

TEST_TIF = Path(
    path.normpath(
        path.join(
            path.dirname(__file__),
            os.pardir,
            os.pardir,
            "nafi_hires_data",
            "test",
            "FSDRW_current_sr3577.tif",
        )
    )
)
TEST_APPROVED = Path(
    path.normpath(
        path.join(
            path.dirname(__file__),
            os.pardir,
            os.pardir,
            "nafi_hires_data",
            "test",
            "test_working",
            "approved.shp",
        )
    )
)
HIRES_DATA = path.normpath(
    path.join(path.dirname(__file__), os.pardir, os.pardir, "nafi_hires_data")
)


class TestProcess(unittest.TestCase):
    def test_addColorTable(self):
        addColorTable(TEST_TIF)

        table = getColorTable(TEST_TIF)
        self.assertEqual(table, FIRESCAR_COLOR_TABLE)

    def test_approvedExists(self):
        self.assertTrue(
            TEST_APPROVED.exists(), "Sample approved features path is incorrect!"
        )
