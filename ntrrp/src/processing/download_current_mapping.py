# -*- coding: utf-8 -*-
from pathlib import Path
from zipfile import ZipFile

from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFile
import processing

from ..utils import ensureTempDirectories, getNtrrpDataUrl, getTempZipFilename, qgsDebug, NTRRP_REGIONS


class DownloadCurrentMapping(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterEnum('Region', 'Region', options=NTRRP_REGIONS,
                          allowMultiple=False, usesStaticStrings=False, defaultValue=0))
        self.addParameter(QgsProcessingParameterFile('WorkingDirectory', 'Working Directory',
                          behavior=QgsProcessingParameterFile.Folder, fileFilter='All files (*.*)', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {
            'CurrentMappingDirectory': None
        }

        # Ensure all temp directories exist
        ensureTempDirectories()

        # Set up transfer parameters
        region = NTRRP_REGIONS[parameters['Region']]
        regionDataDirectory = Path(parameters['WorkingDirectory']) / region

        # Note: _tif suffix removed by Patrice (BNTQ-57)
        downloadUrl = f"{getNtrrpDataUrl()}/bfnt_{region.lower()}_current_sr3577.zip"
        tempFile = getTempZipFilename()

        qgsDebug(f"Downloading {downloadUrl} to {tempFile}")

        # Download ZIP to temp location
        alg_params = {
            'OUTPUT': tempFile,
            'URL': downloadUrl
        }
        processing.run('native:filedownloader', alg_params,
                       context=context, feedback=feedback, is_child_algorithm=True)

        # Unzip ZIP to region data folder
        if not Path(tempFile).exists():
            return results
        else:
            with ZipFile(Path(tempFile), 'r') as zf:
                zf.extractall(regionDataDirectory)
                zf.close()
                Path(tempFile).unlink()

            results = {
                'CurrentMappingDirectory': regionDataDirectory
            }

        return results

    def name(self):
        return 'DownloadCurrentMapping'

    def displayName(self):
        return 'Download NAFI Current Burnt Areas Mapping'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return DownloadCurrentMapping()
