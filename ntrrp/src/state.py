# -*- coding: utf-8 -*-
import json
import os.path as path

from qgis.core import QgsProject

from .utils import guiError, getSetting, setSetting

class NtrrpState(object):

    # Fully qualified Windows path of the current working folder (which should be the QGS project file area)
    workingFolder = None

    # Map layer name of the active working layer
    workingLayerName = None

    # Map layer name of the active source layer
    sourceLayerName = None

    # Current mapping region
    region = None

    def deriveWorkingFolder(self):
        """Derive the working folder from the current QGS project file."""
        project = QgsProject.instance()
        projectFilePath = project.fileName()
        if projectFilePath is None or projectFilePath == '':
            self.workingFolder = None
            guiError("Save your burnt areas mapping project before continuing.")
        else:
            self.workingFolder = path.dirname(projectFilePath)
        return self.workingFolder

    def saveState(self):
        """Save the current state to QGIS settings."""
        setSetting("NTRRP_STATE", json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))      

    def loadState(self):
        """Load the current state from QGIS settings."""
        state = json.load(getSetting("NTRRP_STATE", "{}"))
        self.__dict__.update(state)
        # self.workingFolder = state["workingFolder"]
        # self.workingLayerName = state["workingLayerName"]
        # self.sourceLayerName = state["sourceLayerName"]
        # self.region = state["region"]
     

State = NtrrpState()
