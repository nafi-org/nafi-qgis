import json
import os
import os.path as path

from qgis.core import Qgis, QgsMessageLog
from qgis.PyQt.QtWidgets import QMessageBox

NAFICP_NAME = "Easy Copy and Paste"
NAFICP_DEFAULT_HOTKEY = "Ctrl+Z"
NAFICP_CONFIG_FILENAME = "naficp.json"


def qgsDebug(message, level=Qgis.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(message, tag=NAFICP_NAME, level=level)


def guiInformation(message):
    """Show an info message box."""
    QMessageBox.information(None, NAFICP_NAME, message)


def guiError(message):
    """Show an error message box."""
    QMessageBox.critical(None, NAFICP_NAME, message)


def guiWarning(message):
    """Show a warning message box."""
    QMessageBox.warning(None, NAFICP_NAME, message)


def resolvePluginPath(relative, base=None):
    """Resolve a relative path in the plug-in deployment directory."""
    if not base:
        base = path.dirname(os.path.realpath(__file__))
        # note this function will break if this code in src/utils.py is moved to a different directory
        base = path.normpath(path.join(base, os.pardir))
    return path.normpath(path.join(base, relative))


def getSetting(setting, default=None):
    """Retrieve an Easy Copy and Paste setting."""
    try:
        with open(resolvePluginPath("naficp.json")) as settingsFile:
            settings = json.load(settingsFile)
            return settings.get(setting, default)
    except:
        qgsDebug(f"Error reading {NAFICP_NAME} settings file.")
        return default


def getConfiguredHotKey():
    """Get the configured hot key."""
    return getSetting("hotkey", NAFICP_DEFAULT_HOTKEY)
