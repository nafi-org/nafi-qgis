from pathlib import Path

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing

from .color_table import addColorTable
from ..utils import qgsDebug

class RasteriseBurntAreas(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('BurntAreas', 'Burnt Areas', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('RasterisedBurntAreas', 'Rasterised Burnt Areas', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Rasterize (vector to raster)
        alg_params = {
            'BURN': None,
            #'DATA_TYPE': 0,
            'EXTENT': parameters['BurntAreas'],
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 10,
            'INIT': None,
            'INPUT': parameters['BurntAreas'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,
            'WIDTH': 10,
            'OUTPUT': parameters['RasterisedBurntAreas']
        }
        outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RasterisedBurntAreas'] = outputs['RasterizeVectorToRaster']['OUTPUT']

        # add a color table using GDAL
        addColorTable(Path(results['RasterisedBurntAreas']))

        qgsDebug(f"RasterisedBurntAreas: {results['RasterisedBurntAreas']}")

        return results

    def name(self):
        return 'RasteriseBurntAreas'

    def displayName(self):
        return 'Rasterise Burnt Areas'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return RasteriseBurntAreas()
