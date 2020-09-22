# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsMessageLog

IBRA_URL = "http://www.environment.gov.au/mapping/services/ogc_services/IBRA7_Subregions/MapServer/WMSServer"
NAFI_URL = "https://www.firenorth.org.au/public"
OZ_TOPO_URL = "https://services.ga.gov.au/gis/rest/services/Topographic_Base_Map/MapServer/WMTS/1.0.0/WMTSCapabilities.xml"

def qgsDebug(message):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="NAFI Fire Maps", level=Qgis.Info)

def getNafiUrl():
    # TODO look in QGIS settings
    return NAFI_URL

def getIbraUrl():
    return IBRA_URL

def getOzTopoParams():
    return {
        "crs": "EPSG:3857",
        "format": "image/jpgpng",
        "layers": "Topographic_Base_Map",
        "styles": "default",
        "tileMatrixSet": "GoogleMapsCompatible",
        "url": OZ_TOPO_URL
    }

def guiInformation(message):
    QMessageBox.information(None, "NAFI Fire Maps", message)

def guiError(message):
    QMessageBox.critical(None, "NAFI Fire Maps", message)

def guiWarning(message):
    QMessageBox.warning(None, "NAFI Fire Maps", message)