# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QStandardItemModel

from .ntrrp_mapping import NtrrpMapping

UNWANTED_LAYERS = ["NODATA_RASTER"]


class NtrrpTreeViewModel(QStandardItemModel):

    def __init__(self, unwantedLayers=UNWANTED_LAYERS):
        """Constructor."""
        super(QStandardItemModel, self).__init__()
        self.unwantedLayers = unwantedLayers
        self.owsLayers = []
        self.region = ""

    def setMapping(self, region):
        """Set the current region for the NTRRP layer model."""
        assert isinstance(region, NtrrpMapping)

        self.region = region

        # clear all rows
        self.removeRows(0, self.rowCount())

        # append all NtrrpItems in the region
        for item in region.getNtrrpItems():
            self.appendRow(item)

    def refresh(self):
        """Refresh the tree view."""
        if self.region:
            self.setMapping(self.region)
