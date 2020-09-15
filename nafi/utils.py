# -*- coding: utf-8 -*-
from qgis.core import Qgis, QgsMessageLog

NAFI_URL = "https://www.firenorth.org.au/public"

def qgsDebug(message):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="Messages", level=Qgis.Info)

def getNafiUrl():
    # TODO look in QGIS settings
    return NAFI_URL