# -*- coding: utf-8 -*-
from urllib.parse import unquote, urlencode

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 
from qgis.core import QgsProject, QgsRasterLayer

from .utils import getOzTopoParams, guiError, qgsDebug

WMTS_LABEL = "Australian Topographic Base Map"

class OzTopoWmtsItem(QStandardItem):
    def __init__(self):
        """Constructor."""
        super(QStandardItem, self).__init__()

        self.setFlags(Qt.ItemIsEnabled)
        self.setText(WMTS_LABEL)
        self.setIcon(QIcon(":/plugins/ntrrp/images/globe.png"))
        
    def addLayer(self):
        """Create a QgsRasterLayer from this one specific WMTS endpoint."""

        wmtsParams = getOzTopoParams()
        wmtsParamsUri = unquote(urlencode(wmtsParams))
        
        wmtsLayer = QgsRasterLayer(wmtsParamsUri, WMTS_LABEL, "wms")
        if wmtsLayer is not None and wmtsLayer.isValid():
            QgsProject.instance().addMapLayer(wmtsLayer)
        else:
            error = (f"An error occurred adding the layer {WMTS_LABEL} to the map.\n"
                     f"Check your QGIS WMS message log for details.")
            guiError(error)
