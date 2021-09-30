# -*- coding: utf-8 -*-
import html
import os
import os.path as path
import random
import string
from pathlib import Path

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

def getDownloadDirectory():
    """Get the directory location to store NAFI burnt areas data."""
    return path.normpath(path.join(os.environ["TMP"], "ntrrp", "downloads"))

def getWorkingDirectory():
    """Get the directory location to output and save NAFI burnt areas working data."""
    return path.normpath(path.join(os.environ["TMP"], "ntrrp", "working"))

def ensureDirectory(dir):
    """Ensure a particular directory exists."""
    Path(dir).mkdir(parents=True, exist_ok=True)

def ensureTempDirectories():
    """Ensure the download and working directories exist."""
    ensureDirectory(getDownloadDirectory())
    ensureDirectory(getWorkingDirectory())

def getRandomFilename():
    """Get a random 8-character filename."""
    return ''.join(random.choice(string.ascii_lowercase) for i in range(8))

def getTempDownloadPath():
    """Get a temporary download path."""
    unzipLocation = path.normpath(path.join(getDownloadDirectory(), getRandomFilename()))
    dataFile = f"{unzipLocation}.zip"
    return dataFile

def getWorkingShapefilePath():
    """Get a path for a working layer shapefile."""
    outputDir = path.normpath(path.join(getWorkingDirectory(), getRandomFilename()))
    return path.normpath(path.join(outputDir, "working.shp"))

def resolvePluginPath(relative, base = None):
    """Resolve a relative path in the plug-in deployment directory."""
    if not base:
        base = path.dirname(os.path.realpath(__file__))
        # note this function will break if this code in src/utils.py is moved to a different directory
        base = path.normpath(path.join(base, os.pardir))    
    return path.normpath(path.join(base, relative))

def resolveStylePath(styleName):
    """Load a style file packaged with the plug-in."""
    relative = f"styles\\{styleName}.qml"
    return resolvePluginPath(relative)

def qgsDebug(message, level=Qgis.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="NAFI Burnt Areas Mapping", level=level)

def guiInformation(message):
    """Show an info message box."""
    QMessageBox.information(None, "NAFI Burnt Areas Mapping", message)

def guiError(message):
    """Show an error message box."""
    QMessageBox.critical(None, "NAFI Burnt Areas Mapping", message)

def guiWarning(message):
    """Show a warning message box."""
    QMessageBox.warning(None, "NAFI Burnt Areas Mapping", message)

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
             f"Check the QGIS NAFI Burnt Areas Mapping message log for details.")
    guiError(error)
    qgsDebug(logMessage, Qgis.Critical)

def capabilitiesError(errorString, capsXml):
    """Raise an error parsing the WMS capabilities file."""
    error = (f"Error parsing the retrieved NAFI WMS capabilities!\n"
             f"Check the QGIS NAFI Burnt Areas Mapping message log for details.")
    guiError(error)
    logMessage = f"NAFI WMS capabilities XML parse failure: {errorString}"
    qgsDebug(logMessage, Qgis.Critical)
    logMessage = f"NAFI WMS capabilities XML: {html.escape(capsXml)}"
    qgsDebug(logMessage, Qgis.Critical)