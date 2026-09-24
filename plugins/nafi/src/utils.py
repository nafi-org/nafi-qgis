import configparser
import html
import json
import os
import os.path as path

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsMessageLog, QgsCoordinateReferenceSystem

IBRA_URL = "http://www.environment.gov.au/mapping/services/ogc_services/IBRA7_Subregions/MapServer/WMSServer"
NAFI_DATA_URL = "https://firenorth.org.au/nafi4/help/download-nafi-data"
NAFI_SUPPORTERS_URL = "https://firenorth.org.au/nafi4/supporters"
NAFI_URL = "https://firenorth.org.au/public"
NAFI_CONFIG_FILENAME = "nafi.json"
NAFI_METADATA_FILENAME = "metadata.txt"
OZ_TOPO_URL = (
    "https://services.ga.gov.au/gis/rest/services/Topographic_Base_Map"
    "/MapServer/WMTS/1.0.0/WMTSCapabilities.xml"
)


def qgsDebug(message, level=Qgis.MessageLevel.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="NAFI Fire Maps", level=level)


def resolvePluginPath(relative, base=None):
    """Resolve a relative path in the plug-in deployment directory."""
    if not base:
        base = path.dirname(os.path.realpath(__file__))
        base = path.normpath(path.join(base, os.pardir))
    return path.normpath(path.join(base, relative))


def getSetting(setting, default=None):
    """Retrieve a NAFI Fire Maps setting."""
    try:
        with open(resolvePluginPath(NAFI_CONFIG_FILENAME)) as settingsFile:
            settings = json.load(settingsFile)
            return settings.get(setting, default)
    except (OSError, json.JSONDecodeError):
        qgsDebug("Error reading NAFI Fire Maps settings file.")
        return default


def getPluginVersion():
    """Retrieve the NAFI Fire Maps plug-in version."""
    # read the plugin version directly from metadata.txt
    metadata = configparser.ConfigParser(interpolation=None)
    metadata.read(resolvePluginPath(NAFI_METADATA_FILENAME))
    return metadata.get("general", "version", fallback="")


def getNafiDataUrl():
    return getSetting("NAFI_DATA_URL", NAFI_DATA_URL)


def getNafiSupportersUrl():
    return getSetting("NAFI_SUPPORTERS_URL", NAFI_SUPPORTERS_URL)


def getNafiUrl():
    return getSetting("NAFI_URL", NAFI_URL)


def getIbraUrl():
    return IBRA_URL


def getOzTopoParams():
    # see https://github.com/isogeo/isogeo-plugin-qgis/blob/master/tests/dev/qgis_console/dev_wmts.py

    # cut and pasted from QGIS layer properties after manual add:
    # contextualWMSLegend=0&crs=EPSG:3857&dpiMode=7&featureCount=10&format=image/jpgpng&layers=Topographic_Base_Map
    # &styles=default&tileMatrixSet=GoogleMapsCompatible
    # &url=https://services.ga.gov.au/gis/rest/services/Topographic_Base_Map/MapServer/WMTS/1.0.0/WMTSCapabilities.xml
    return {
        "crs": "EPSG:3857",
        "format": "image/png",
        "layers": "Topographic_Base_Map",
        "styles": "default",
        "tileMatrixSet": "GoogleMapsCompatible",
        "url": OZ_TOPO_URL,
    }


def guiInformation(message):
    """Show an info message box."""
    QMessageBox.information(None, "NAFI Fire Maps", message)


def guiError(message):
    """Show an error message box."""
    QMessageBox.critical(None, "NAFI Fire Maps", message)


def guiWarning(message):
    """Show a warning message box."""
    QMessageBox.warning(None, "NAFI Fire Maps", message)


def setDefaultProjectCrs(project):
    """Set the Project CRS to the default value of GDA94 geographic."""
    gda94 = QgsCoordinateReferenceSystem("EPSG:4283")
    warning = (
        f"Because no QGIS project CRS was set, a default coordinate system of "
        f"{gda94.userFriendlyIdentifier()} has been applied to interact with "
        f"NAFI map services."
    )

    guiWarning(warning)
    project.setCrs(gda94)


def connectionError(logMessage):
    """Raise a connection error."""
    error = (
        "Error connecting to NAFI services!\n"
        "Check the QGIS NAFI Fire Maps message log for details."
    )
    guiError(error)
    qgsDebug(logMessage, Qgis.MessageLevel.Critical)


def capabilitiesError(errorString, capsXml):
    """Raise an error parsing the WMS capabilities file."""
    error = (
        "Error parsing the retrieved NAFI WMS capabilities!\n"
        "Check the QGIS NAFI Fire Maps message log for details."
    )
    guiError(error)
    logMessage = f"NAFI WMS capabilities XML parse failure: {errorString}"
    qgsDebug(logMessage, Qgis.MessageLevel.Critical)
    logMessage = f"NAFI WMS capabilities XML: {html.escape(capsXml)}"
    qgsDebug(logMessage, Qgis.MessageLevel.Critical)
