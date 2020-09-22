# -*- coding: utf-8 -*-
from urllib.parse import unquote, urlencode

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 
from qgis.core import QgsProject, QgsRasterLayer

from .utils import qgsDebug

WMTS_LABEL = "Australian Topographic WMTS"

class OzTopoWmtsItem(QStandardItem):
    def __init__(self):
        """Constructor."""
        super(QStandardItem, self).__init__()

        self.setFlags(Qt.ItemIsEnabled)
        self.setText(WMTS_LABEL)
        self.setIcon(QIcon(":/plugins/nafi/globe.png"))
        
    def addLayer(self):
        """Create a QgsRasterLayer from this one specific WMTS endpoint."""

        # see https://github.com/isogeo/isogeo-plugin-qgis/blob/master/tests/dev/qgis_console/dev_wmts.py

        # cut and pasted from QGIS layer properties after manual add:
        # contextualWMSLegend=0&crs=EPSG:3857&dpiMode=7&featureCount=10&format=image/jpgpng&layers=Topographic_Base_Map
        # &styles=default&tileMatrixSet=GoogleMapsCompatible
        # &url=https://services.ga.gov.au/gis/rest/services/Topographic_Base_Map/MapServer/WMTS/1.0.0/WMTSCapabilities.xml        
        wmtsParams = {
            "crs": "EPSG:3857",
            "format": "image/jpgpng",
            "layers": "Topographic_Base_Map",
            "styles": "default",
            "tileMatrixSet": "GoogleMapsCompatible",
            "url": "https://services.ga.gov.au/gis/rest/services/Topographic_Base_Map/MapServer/WMTS/1.0.0/WMTSCapabilities.xml"
        }
        wmtsParamsUri = unquote(urlencode(wmtsParams))
        
        qgsDebug(wmtsParamsUri)

        wmtsLayer = QgsRasterLayer(wmtsParamsUri, WMTS_LABEL, "wms")
        if wmtsLayer is not None:
            QgsProject.instance().addMapLayer(wmtsLayer)
