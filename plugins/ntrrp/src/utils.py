import html
import json
import os
import os.path as path
import random
import string
from pathlib import Path
from tempfile import gettempdir

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsMessageLog, QgsProject

NTRRP_REGIONS = ["Darwin", "Katherine"]

NTRRP_WMS_URL = "https://test.firenorth.org.au/mapserver/bfnt/gwc/service/wms"
NTRRP_WMTS_URL = "https://test.firenorth.org.au/mapserver/bfnt/gwc/service/wmts"
NTRRP_DATA_URL = f"https://test.firenorth.org.au/bfnt/downloads"
NTRRP_UPLOAD_URL = "https://test.firenorth.org.au/bfnt/upload.php"
NTRRP_API_URL = "https://test.firenorth.org.au/bfnt/api"


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


def deriveWorkingDirectory():
    """Derive the working folder from the current QGS project file."""
    projectFilePath = resolveProjectFile()
    if not projectFilePath:
        guiError("Save your burnt areas mapping project before continuing.")
        return None
    return path.dirname(projectFilePath)


def doFullSegmentationDownload() -> bool:
    """Return whether to download the full segmentation."""
    return bool(getSetting("NTRRP_DO_FULL_SEGMENTATION_DOWNLOAD", False))


def getSetting(setting, default=None):
    """Retrieve an NTRRP setting."""
    try:
        with open(resolvePluginPath("ntrrp.json")) as settingsFile:
            settings = json.load(settingsFile)
            return settings.get(setting, default)
    except BaseException:
        qgsDebug("Error reading NTRRP settings file.")
        return default


def getRemoteWorkspaceUrl():
    return getSetting("NTRRP_WMS_URL", NTRRP_WMS_URL)


def getNtrrpWmtsUrl():
    return getSetting("NTRRP_WMTS_URL", NTRRP_WMTS_URL)


def getNtrrpDataUrl():
    return getSetting("NTRRP_DATA_URL", NTRRP_DATA_URL)


def getNtrrpUploadUrl():
    return getSetting("NTRRP_UPLOAD_URL", NTRRP_UPLOAD_URL)


def getNtrrpApiUrl():
    return getSetting("NTRRP_API_URL", NTRRP_API_URL)


def getDownloadDirectory():
    """Get the directory location to store NAFI burnt areas data."""
    return path.normpath(path.join(gettempdir(), "ntrrp", "downloads"))


def getWorkingDirectory():
    """Get the directory location to output and save NAFI burnt areas working data."""
    return path.normpath(path.join(gettempdir(), "ntrrp", "working"))


def getUploadDirectory():
    """Get a random upload directory."""
    return path.normpath(path.join(gettempdir(), "ntrrp", "uploads"))


def ensureDirectory(dir):
    """Ensure a particular directory exists."""
    Path(dir).mkdir(parents=True, exist_ok=True)


def ensureTempDirectories():
    """Ensure the download and working directories exist."""
    ensureDirectory(getDownloadDirectory())
    ensureDirectory(getWorkingDirectory())
    ensureDirectory(getUploadDirectory())


def getRandomFilename():
    """Get a random 8-character filename."""
    return "".join(random.choice(string.ascii_lowercase) for i in range(8))


def getTempDirectory():
    """Get a temporary download path."""
    return path.normpath(path.join(getDownloadDirectory(), getRandomFilename()))


def getTempZipFilename():
    """Get a temporary download ZIP path."""
    tempDir = getTempDirectory()
    zipFile = f"{tempDir}.zip"
    return zipFile


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
        f"Error connecting to NAFI services!\n"
        f"Check the QGIS NAFI Burnt Areas Mapping message log for details."
    )
    # guiError(error)
    qgsDebug(logMessage, Qgis.Critical)


def capabilitiesError(errorString, capsXml):
    """Raise an error parsing the WMS capabilities file."""
    error = (
        f"Error parsing the retrieved NAFI WMS capabilities!\n"
        f"Check the QGIS NAFI Burnt Areas Mapping message log for details."
    )
    # guiError(error)
    logMessage = f"NAFI WMS capabilities XML parse failure: {errorString}"
    qgsDebug(logMessage, Qgis.Critical)
    logMessage = f"NAFI WMS capabilities XML: {html.escape(capsXml)}"
    qgsDebug(logMessage, Qgis.Critical)
