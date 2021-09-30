import shutil
import os.path as path
from pathlib import Path

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer, QgsProcessingParameterFile
import processing

from ..upload.client import Client
from ..upload.exceptions import ProcessingException
from ..utils import ensureDirectory, getNtrrpUploadUrl, getRandomFilename, getUploadDirectory, qgsDebug
class UploadBurntAreas(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        processing.ProcessingConfig.setSettingValue('IGNORE_INVALID_FEATURES', 0)
        self.addParameter(QgsProcessingParameterVectorLayer('AttributedBurntAreas', 'Burnt Areas', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('RasterisedBurntAreas', 'Rasterised Burnt Areas', extension="tif", defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}

        # set up a temp filesystem
        uploadDir = getUploadDirectory()
        archiveName = getRandomFilename()

        archiveDir = path.join(uploadDir, archiveName)
        ensureDirectory(archiveDir)
        saveBurntAreas = path.join(archiveDir, "burnt_areas.shp")

        # Save Attributed Burnt Areas
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': parameters['AttributedBurntAreas'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': saveBurntAreas
        }
        results = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        rasterisedBurntAreasPath = parameters['RasterisedBurntAreas']
        attributedBurntAreasPath = results['OUTPUT']

        shutil.copyfile(rasterisedBurntAreasPath, path.join(archiveDir, "rasterised.tif"))
        
        # make_archive appends a .zip as well
        shutil.make_archive(archiveDir, "zip", uploadDir)
        archive = path.join(uploadDir, f"{archiveName}.zip")

        # try to upload the lot!
        try:
            client = Client(getNtrrpUploadUrl(), 1024)
            client.upload_file(archive)

        except ProcessingException as err:
            raise RuntimeError('script terminated due to processing errors...')

        return {}
                                    

    def name(self):
        return 'UploadBurntAreas'

    def displayName(self):
        return 'Upload Burnt Areas'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return UploadBurntAreas()
