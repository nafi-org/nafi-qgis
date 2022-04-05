from pathlib import Path
from zipfile import ZipFile

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFile
import processing

from ..utils import getNtrrpDataUrl, getTempDownloadPath, NTRRP_REGIONS

def get_signals(source):
    cls = source if isinstance(source, type) else type(source)
    signal = type(QtCore.pyqtSignal())
    for subcls in cls.mro():
        clsname = f'{subcls.__module__}.{subcls.__name__}'
        for key, value in sorted(vars(subcls).items()):
            if isinstance(value, signal):
                print(f'{key} [{clsname}]')



class DownloadCurrentMapping(QgsProcessingAlgorithm):

    REGIONS = ['Darwin', 'Katherine']

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterEnum('Region', 'Region', options=NTRRP_REGIONS, allowMultiple=False, usesStaticStrings=False, defaultValue=0))
        self.addParameter(QgsProcessingParameterFile('WorkingFolder', 'Working Folder', behavior=QgsProcessingParameterFile.Folder, fileFilter='All files (*.*)', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {
            'CurrentMappingFolder': None
        }

        # Set up transfer parameters
        region = NTRRP_REGIONS[parameters['Region']]
        regionDataFolder = Path(parameters['WorkingFolder']) / region
        downloadUrl = f"{getNtrrpDataUrl()}/bfnt_{region.lower()}_current_sr3577_tif.zip"
        tempFile = getTempDownloadPath()

        # Download ZIP to temp location
        alg_params = {
            'OUTPUT': tempFile,
            'URL': downloadUrl
        }
        processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
     
        # Unzip ZIP to region data folder
        if not Path(tempFile).exists():
            return results
        else: 
            with ZipFile(Path(tempFile), 'r') as zf:
                zf.extractall(regionDataFolder)
                zf.close()
                Path(tempFile).unlink()

            results = {
                'CurrentMappingFolder': regionDataFolder
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