# -*- coding: utf-8 -*-
import json
import os
import os.path as path

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsMessageLog, QgsProject

NAFICP_CONFIG_FILENAME="naficp.json"

def qgsDebug(message, level=Qgis.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(
        message, tag="NAFI Burnt Areas Mapping", level=level)


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


def deriveWorkingDirectory():
    """Derive the working folder from the current QGS project file."""
    project = QgsProject.instance()
    projectFilePath = project.fileName()
    if projectFilePath is None or projectFilePath == '':
        guiError("Save your burnt areas mapping project before continuing.")
        return None
    return path.dirname(projectFilePath)


def getSetting(setting, default=None):
    """Retrieve a NAFI Copy & Paste setting."""
    try:
        with open(resolvePluginPath("naficp.json")) as settingsFile:
            settings = json.load(settingsFile)
            return settings.get(setting, default)
    except:
        qgsDebug("Error reading NAFI Copy & Paste settings file.")
        return default


