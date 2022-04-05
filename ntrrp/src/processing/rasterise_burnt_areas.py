# -*- coding: utf-8 -*-
from pathlib import Path

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
import processing

from .color_table import addColorTable


class RasteriseBurntAreas(QgsProcessingAlgorithm):

    currentMappingTif = None

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('BurntAreas', 'Your burnt areas (should be attributed with an FSID)', types=[
                          QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination(
            'RasterisedBurntAreas', 'Rasterised and merged burnt area map', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer(
            'CurrentMapping', 'Current rasterised mapping for your region', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        burntAreasExtent = self.parameterAsExtent(
            parameters, 'BurntAreas', context)

        # Rasterize (vector to raster)
        algParams = {
            'BURN': None,
            'DATA_TYPE': 0,     # Byte
            'EXTENT': burntAreasExtent,
            'EXTRA': '',
            'FIELD': 'FSID',
            'HEIGHT': 10,       # metres
            'INIT': None,
            'INPUT': parameters['BurntAreas'],
            'INVERT': False,
            'NODATA': 0,        # 0 background is also NODATA
            'OPTIONS': '',
            'UNITS': 1,         # Georeferenced units
            'WIDTH': 10,        # metres
            'OUTPUT': parameters['RasterisedBurntAreas']
        }
        processing.ProcessingConfig.setSettingValue(
            'IGNORE_INVALID_FEATURES', 1)
        rasteriseOutput = processing.run(
            "gdal:rasterize", algParams, context=context, feedback=feedback, is_child_algorithm=True)

        rasterisedBurntAreasTif = rasteriseOutput['OUTPUT']

        # Merge with current mapping
        mergeAlgParams = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': [rasterisedBurntAreasTif, parameters['CurrentMapping']],
            'NODATA_INPUT': 0,
            'NODATA_OUTPUT': 0,
            'OPTIONS': '',
            'PCT': False,
            'SEPARATE': False,
            'OUTPUT': parameters['RasterisedBurntAreas']
        }
        outputs['RasterisedBurntAreas'] = processing.run(
            'gdal:merge', mergeAlgParams, context=context, feedback=feedback, is_child_algorithm=True)
        results['RasterisedBurntAreas'] = outputs['RasterisedBurntAreas']['OUTPUT']

        # add a color table using GDAL
        addColorTable(Path(results['RasterisedBurntAreas']))

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
