# -*- coding: utf-8 -*-
import html

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsMessageLog, QgsProject, QgsSettings

# NTRRP_URL = "https://test.firenorth.org.au/mapserver/ntrrp/wms"
NTRRP_WMS_URL = "https://test.firenorth.org.au/mapserver/ntrrp/gwc/service/wms"
NTRRP_WMTS_URL = "https://test.firenorth.org.au/mapserver/ntrrp/gwc/service/wmts"
NTRRP_DATA_URL = f"https://test.firenorth.org.au/ntrrp/downloads/drw/area1.zip"
# /wms?service=WMS&version=1.1.0&request=GetCapabilities&layers=ntrrp_test%3AT1T2_darwin_dMIRB
# https://test.firenorth.org.au/mapserver/ntrrp/wms?service=WMS&version=1.1.0&request=GetMap&layers=ntrrp%3AFSHDRW_CURRENT&bbox=-222099.563500943%2C-1441352.91373074%2C-42069.56350094339%2C-1263222.91373074&width=768&height=759&srs=EPSG%3A3577&format=application/openlayers

def getSetting(setting, default = None):
    """Retrieve an NTRRP setting."""
    settings = QgsSettings()
    current = settings.value(f"NTRRP/{setting}", default)

    if current == default:
        settings.setValue(f"NTRRP/{setting}", current)
    return current

def restoreDefaults():
    settings = QgsSettings()
    settings.setValue(f"NTRRP/NTRRP_WMS_URL", NTRRP_WMS_URL)
    settings.setValue(f"NTRRP/NTRRP_WMTS_URL", NTRRP_WMTS_URL)
    settings.setValue(f"NTRRP/NTRRP_DATA_URL", NTRRP_DATA_URL)

def getNtrrpWmsUrl():
    return getSetting("NTRRP_WMS_URL", NTRRP_WMS_URL)

def getNtrrpWmtsUrl():
    return getSetting("NTRRP_WMTS_URL", NTRRP_WMTS_URL)

def getNtrrpDataUrl():
    return getSetting("NTRRP_DATA_URL", NTRRP_DATA_URL)

def qgsDebug(message, level=Qgis.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="NT Risk Reduction Program", level=level)

def guiInformation(message):
    """Show an info message box."""
    QMessageBox.information(None, "NT Risk Reduction Program", message)

def guiError(message):
    """Show an error message box."""
    QMessageBox.critical(None, "NT Risk Reduction Program", message)

def guiWarning(message):
    """Show a warning message box."""
    QMessageBox.warning(None, "NT Risk Reduction Program", message)

def setDefaultProjectCrs(project):
    """Set the Project CRS to the default value of GDA94 geographic."""
    assert isinstance(project, QgsProject)

    ausAlbers = QgsCoordinateReferenceSystem("EPSG:3577")
    warning = (f"A default coordinate system of "
               f"{ausAlbers.userFriendlyIdentifier()} has been applied to interact with "
               f"NAFI map services.")

    guiWarning(warning)
    project.setCrs(ausAlbers)

def connectionError(logMessage):
    """Raise a connection error."""
    error = (f"Error connecting to NAFI services!\n"
             f"Check the QGIS NT Risk Reduction Program message log for details.")
    guiError(error)
    qgsDebug(logMessage, Qgis.Critical)

def capabilitiesError(errorString, capsXml):
    """Raise an error parsing the WMS capabilities file."""
    error = (f"Error parsing the retrieved NAFI WMS capabilities!\n"
             f"Check the QGIS NT Risk Reduction Program message log for details.")
    guiError(error)
    logMessage = f"NAFI WMS capabilities XML parse failure: {errorString}"
    qgsDebug(logMessage, Qgis.Critical)
    logMessage = f"NAFI WMS capabilities XML: {html.escape(capsXml)}"
    qgsDebug(logMessage, Qgis.Critical)