from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
import processing


class RasteriseBurntAreas(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        pass

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Rasterize (vector to raster)
        alg_params = {
            'BURN': 0,
            'DATA_TYPE': 5,
            'EXTENT': '-183050.000000000,-132090.000000000,-1360010.000000000,-1309230.000000000 [EPSG:3577]',
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 15,
            'INIT': None,
            'INPUT': 'T1T2_darwin_T20210901_T20210827_seg_sa1_t100_7bfd0640_cec8_424a_8480_ee31e00b2eb6',
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,
            'WIDTH': 15,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
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
        return Rasteriseburntareas()
