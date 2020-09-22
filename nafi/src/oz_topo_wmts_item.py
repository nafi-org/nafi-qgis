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
        self.setIcon(QIcon(":/plugins/nafi/images/globe.png"))
        
    def addLayer(self):
        """Create a QgsRasterLayer from this one specific WMTS endpoint."""

        # see https://github.com/isogeo/isogeo-plugin-qgis/blob/master/tests/dev/qgis_console/dev_wmts.py

        # cut and pasted from QGIS layer properties after manual add:
        # contextualWMSLegend=0&crs=EPSG:3857&dpiMode=7&featureCount=10&format=image/jpgpng&layers=Topographic_Base_Map
        # &styles=default&tileMatrixSet=GoogleMapsCompatible
        # &url=https://services.ga.gov.au/gis/rest/services/Topographic_Base_Map/MapServer/WMTS/1.0.0/WMTSCapabilities.xml        
        wmtsParams = getOzTopoParams()
        wmtsParamsUri = unquote(urlencode(wmtsParams))
        
        # qgsDebug(wmtsParamsUri)

        wmtsLayer = QgsRasterLayer(wmtsParamsUri, WMTS_LABEL, "wms")
        if wmtsLayer is not None and wmtsLayer.isValid():
            QgsProject.instance().addMapLayer(wmtsLayer)
        else:
            error = (f"An error occurred adding the layer {WMTS_LABEL} to the map.\n"
                     f"Check your QGIS WMS message log for details.")
            guiError(error)
