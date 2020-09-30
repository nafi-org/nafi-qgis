# -*- coding: utf-8 -*-
import html

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsMessageLog

IBRA_URL = "http://www.environment.gov.au/mapping/services/ogc_services/IBRA7_Subregions/MapServer/WMSServer"
NAFI_DATA_URL = "https://firenorth.org.au/nafi3/views/data/Download.html"
NAFI_URL = "https://www.firenorth.org.au/public"
OZ_TOPO_URL = "https://services.ga.gov.au/gis/rest/services/Topographic_Base_Map/MapServer/WMTS/1.0.0/WMTSCapabilities.xml"

def qgsDebug(message, level=Qgis.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag="NAFI Fire Maps", level=level)

def getNafiDataUrl():
    return NAFI_DATA_URL

def getNafiUrl():
    # TODO look in QGIS settings
    return NAFI_URL

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
        "format": "image/jpgpng",
        "layers": "Topographic_Base_Map",
        "styles": "default",
        "tileMatrixSet": "GoogleMapsCompatible",
        "url": OZ_TOPO_URL
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
    assert isinstance(project, QgsProject)
    
    gda94 = QgsCoordinateReferenceSystem("EPSG:4283")
    warning = (f"Because no QGIS project CRS was set, a default coordinate system of "
                f"{gda94.userFriendlyIdentifier()} has been applied to interact with "
                f"NAFI map services.")

    guiWarning(warning)
    project.setCrs(gda94)

def connectionError(logMessage):
    """Raise a connection error."""
    error = (f"Error connecting to NAFI services!\n"
             f"Check the QGIS NAFI Fire Maps message log for details.")
    guiError(error)
    qgsDebug(logMessage, Qgis.Critical)

def capabilitiesError(errorString, capsXml):
    """Raise an error parsing the WMS capabilities file."""
    error = (f"Error parsing the retrieved NAFI WMS capabilities!\n"
             f"Check the QGIS NAFI Fire Maps message log for details.")
    guiError(error)
    logMessage = f"NAFI WMS capabilities XML parse failure: {errorString}"
    qgsDebug(logMessage, Qgis.Critical)
    logMessage = f"NAFI WMS capabilities XML: {html.escape(capsXml)}"
    qgsDebug(logMessage, Qgis.Critical)