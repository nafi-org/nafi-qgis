import html
import json
import os
import os.path as path

from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsMessageLog, QgsProject
from qgis.PyQt.QtWidgets import QMessageBox

HIRES_API_URL = "http://localhost:8000"
HIRES_REGIONS = ["Darwin", "Katherine"]
HIRES_WMS_URL = "https://test.firenorth.org.au/mapserver/bfnt/gwc/service/wms"
HIRES_WMTS_URL = "https://test.firenorth.org.au/mapserver/bfnt/gwc/service/wmts"


def qgsDebug(message, level=Qgis.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="NAFI HiRes", level=level)


def guiInformation(message):
    """Show an info message box."""
    QMessageBox.information(None, "NAFI HiRes", message)


def guiError(message):
    """Show an error message box."""
    QMessageBox.critical(None, "NAFI HiRes", message)


def guiWarning(message):
    """Show a warning message box."""
    QMessageBox.warning(None, "NAFI HiRes", message)


def resolvePluginPath(relative, base=None):
    """Resolve a relative path in the plug-in deployment directory."""
    if not base:
        base = path.dirname(os.path.realpath(__file__))
        # note this function will break if this code in src/utils.py is moved to a different directory
        base = path.normpath(path.join(base, os.pardir))
    return path.normpath(path.join(base, relative))


def resolveProjectFile():
    """Get the QGIS project file."""
    return QgsProject.instance().fileName()


def getSetting(setting, default=None):
    """Retrieve a NAFI HiRes setting."""
    try:
        with open(resolvePluginPath("nafi_hires.json")) as settingsFile:
            settings = json.load(settingsFile)
            return settings.get(setting, default)
    except BaseException:
        qgsDebug("Error reading NAFI HiRes settings file.")
        return default


def getRemoteWorkspaceUrl():
    return getSetting("HIRES_WMS_URL", HIRES_WMS_URL)


def getHiResWmtsUrl():
    return getSetting("HIRES_WMTS_URL", HIRES_WMTS_URL)


def getHiResApiUrl():
    return getSetting("HIRES_API_URL", HIRES_API_URL)


def resolveStylePath(styleName):
    """Load a style file packaged with the plug-in."""
    styleDir = resolvePluginPath("styles")
    return path.join(styleDir, f"{styleName}.qml")


def setDefaultProjectCrs(project):
    """Set the Project CRS to the default value of GDA94 geographic."""
    ausAlbers = QgsCoordinateReferenceSystem("EPSG:3577")
    warning = (
        f"A default coordinate system of "
        f"{ausAlbers.userFriendlyIdentifier()} has been applied to interact with "
        f"NAFI map services."
    )

    guiWarning(warning)
    project.setCrs(ausAlbers)


def connectionError(logMessage):
    """Raise a connection error."""
    error = (
        f"Error connecting to NAFI HiRes services!\n"
        f"Check the QGIS NAFI HiRes: Mapping Burnt Areas message log for details."
    )
    qgsDebug(logMessage, Qgis.Critical)


def capabilitiesError(errorString, capsXml):
    """Raise an error parsing the WMS capabilities file."""
    error = (
        f"Error parsing the retrieved NAFI HiRes WMS capabilities!\n"
        f"Check the QGIS NAFI HiRes message log for details."
    )
    logMessage = f"NAFI HiRes WMS capabilities XML parse failure: {errorString}"
    qgsDebug(logMessage, Qgis.Critical)
    logMessage = f"NAFI HiRes WMS capabilities XML: {html.escape(capsXml)}"
    qgsDebug(logMessage, Qgis.Critical)
