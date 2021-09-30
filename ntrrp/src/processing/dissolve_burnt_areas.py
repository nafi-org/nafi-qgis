import os.path as path
from pathlib import Path

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink

import processing

from ..utils import qgsDebug

class DissolveBurntAreas(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        processing.ProcessingConfig.setSettingValue('IGNORE_INVALID_FEATURES', 0)
        self.addParameter(QgsProcessingParameterVectorLayer('BurntAreas', 'Burnt Areas', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('DissolvedBurntAreas', 'Dissolved Burnt Areas', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def getParameters(self, shapefilePath):
        """Create processing algorithm parameters given the shapefile associated with a working layer."""
        assert isinstance(shapefilePath, Path), "Input to DissolveBurntAreas should be a Path value"
        assert shapefilePath.exists(), "Input to DissolveBurntAreas must exist on the filesystem"

        params = {
            'FIELD': [''],
            'INPUT': str(shapefilePath),
            'OUTPUT': path.normpath(path.join(str(shapefilePath.parent),"output.shp"))
        }

        qgsDebug(str(params))

        return params

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Dissolve
        alg_params = self.getParameters(parameters["BurntAreas"])
        outputs['Dissolve'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DissolvedBurntAreas'] = outputs['Dissolve']['OUTPUT']
        return results

    def name(self):
        return 'DissolveBurntAreas'

    def displayName(self):
        return 'Dissolve Burnt Areas'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return DissolveBurntAreas()
