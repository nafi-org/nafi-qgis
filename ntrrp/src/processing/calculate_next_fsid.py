# -*- coding: utf-8 -*-
from pathlib import Path
import json

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFile
import processing

from ..ntrrp_fsid_record import NtrrpFsidRecord
from ..utils import getNtrrpApiUrl, fsidsError, NTRRP_REGIONS


class CalculateNextFsid(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterEnum('Region', 'Region', options=NTRRP_REGIONS,
                          allowMultiple=False, usesStaticStrings=False, defaultValue=0))
        self.addParameter(QgsProcessingParameterFile('WorkingFolder', 'Working Folder',
                          behavior=QgsProcessingParameterFile.Folder, fileFilter='All files (*.*)', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {
            'NextFSID': None
        }

        # Set up transfer parameters
        region = NTRRP_REGIONS[parameters['Region']]
        regionDataFolder = Path(parameters['WorkingFolder']) / region
        downloadUrl = fsidsUrl = f"{getNtrrpApiUrl()}/mapping/?area={region.lower()}"
        fsidsFile = regionDataFolder / "fsids.json"

        # Download ZIP to temp location
        alg_params = {
            'OUTPUT': fsidsFile,
            'URL': downloadUrl
        }
        processing.run('native:filedownloader', alg_params,
                       context=context, feedback=feedback, is_child_algorithm=True)

        # Parse FSID data
        if not Path(fsidsFile).exists():
            return results
        else:
            try:
                fsidArray = json.load(fsidsFile)

                if not isinstance(fsidArray, list):
                    raise RuntimeError("Expected a list of FSIDs")

                fsids = [NtrrpFsidRecord(fsidJson) for fsidJson in fsidArray]
                fsids.sort(key=lambda x: int(x.fsid), reverse=True)
                lastFsid = int(fsids[0].fsid)
                results['NextFSID'] = lastFsid + 1

            except:
                fsidsError()

        return results

    def name(self):
        return 'CalculateNextFSID'

    def displayName(self):
        return 'Calculate Next Fire Scar ID'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return DownloadCurrentMapping()
