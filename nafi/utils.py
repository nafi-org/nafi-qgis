# -*- coding: utf-8 -*-
from qgis.core import Qgis, QgsMessageLog

IBRA_URL = "http://www.environment.gov.au/mapping/services/ogc_services/IBRA7_Subregions/MapServer/WMSServer"
NAFI_URL = "https://www.firenorth.org.au/public"

def qgsDebug(message):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="Messages", level=Qgis.Info)

def getNafiUrl():
    # TODO look in QGIS settings
    return NAFI_URL

def getIbraUrl():
    return IBRA_URL