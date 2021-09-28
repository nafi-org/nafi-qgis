# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from owslib.map.wms111 import ContentMetadata

from .ntrrp_region import NtrrpRegion
from .utils import capabilitiesError, qgsDebug

UNWANTED_LAYERS = ["NODATA_RASTER"]

class NtrrpTreeViewModel(QStandardItemModel):

    def __init__(self, unwantedLayers = UNWANTED_LAYERS):
        """Constructor."""
        super(QStandardItemModel, self).__init__()
        self.unwantedLayers = unwantedLayers
        self.owsLayers = []
        self.region = ""

    def setRegion(self, region):
        """Set the current region for the NTRRP layer model."""
        assert isinstance(region, NtrrpRegion)

        self.region = region

        # clear all rows
        self.removeRows(0, self.rowCount())

        # append all NtrrpItems in the region
        for item in region.getNtrrpItems():
            self.appendRow(item)

