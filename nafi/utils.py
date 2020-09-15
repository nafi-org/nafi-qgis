# -*- coding: utf-8 -*-
from qgis.core import Qgis, QgsMessageLog

def qgsDebug(message):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="Messages", level=Qgis.Info)
