from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer, QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFeatureSink
import processing


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
        outputs = {}

        # # Dissolve
        # alg_params = {
        #     'FIELD': [''],
        #     'INPUT': parameters['BurntAreas'],
        #     'OUTPUT': parameters['DissolvedBurntAreas']
        # }
        # outputs['Dissolve'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # results['DissolvedBurntAreas'] = outputs['Dissolve']['OUTPUT']
        return results

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