from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
import processing

class FullBurntAreasProcess(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('ApprovedBurntAreas', 'Approved Burnt Areas', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Dissolve Burnt Areas
        alg_params = {
            'BurntAreas': parameters['ApprovedBurntAreas'],
            'DissolvedBurntAreas': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DissolveBurntAreas'] = processing.run('BurntAreas:DissolveBurntAreas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Rasterise Burnt Areas
        alg_params = {
            'BurntAreas': outputs['DissolveBurntAreas']['DissolvedBurntAreas'],
            'RasterisedBurntAreas': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasteriseBurntAreas'] = processing.run('BurntAreas:RasteriseBurntAreas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Attribute Burnt Areas
        alg_params = {
            'BurntAreas': outputs['DissolveBurntAreas']['DissolvedBurntAreas'],
            'AttributedBurntAreas': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AttributeBurntAreas'] = processing.run('BurntAreas:AttributeBurntAreas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Upload Burnt Areas
        alg_params = {
            'AttributedBurntAreas': outputs['AttributeBurntAreas']['AttributedBurntAreas'],
            'RasterisedBurntAreas': outputs['RasteriseBurntAreas']['RasterisedBurntAreas']
        }
        outputs['UploadBurntAreas'] = processing.run('BurntAreas:UploadBurntAreas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'FullBurntAreasProcess'

    def displayName(self):
        return 'Full Burnt Areas Process'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return FullBurntAreasProcess()
