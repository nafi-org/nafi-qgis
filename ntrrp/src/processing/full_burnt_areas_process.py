# -*- coding: utf-8 -*-
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterDateTime
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterString

import processing

from ..utils import NTRRP_REGIONS


class FullBurntAreasProcess(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('ApprovedBurntAreas', 'Your approved burnt areas', types=[
                          QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer(
            'CurrentMapping', 'Current rasterised mapping for your region', defaultValue=None))
        self.addParameter(QgsProcessingParameterEnum('Region', 'Region', options=NTRRP_REGIONS,
                          allowMultiple=False, usesStaticStrings=False, defaultValue=0))

        self.addParameter(QgsProcessingParameterString(
            'Author', 'Mapping author', multiLine=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterString(
            'Comments', 'Comments', multiLine=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterDateTime(
            'StartDate', 'Mapping start date', type=QgsProcessingParameterDateTime.Date, defaultValue=None))
        self.addParameter(QgsProcessingParameterDateTime(
            'EndDate', 'Mapping end date', type=QgsProcessingParameterDateTime.Date, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('AttributedBurntAreas', 'Attributed Burnt Areas',
                          type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

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
        outputs['DissolveBurntAreas'] = processing.run(
            'BurntAreas:DissolveBurntAreas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Attribute Burnt Areas
        alg_params = {
            'Comments': parameters['Comments'],
            'DissolvedBurntAreas': outputs['DissolveBurntAreas']['DissolvedBurntAreas'],
            'Region': parameters['Region'],
            'StartDate': parameters['StartDate'],
            'EndDate': parameters['EndDate'],
            'Author': parameters['Author'],
            'AttributedBurntAreas': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AttributeBurntAreas'] = processing.run(
            'BurntAreas:AttributeBurntAreas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Rasterise Burnt Areas
        alg_params = {
            'BurntAreas': outputs['AttributeBurntAreas']['AttributedBurntAreas'],
            'CurrentMapping': parameters['CurrentMapping'],
            'RasterisedBurntAreas': QgsProcessing.TEMPORARY_OUTPUT
        }

        outputs['RasteriseBurntAreas'] = processing.run(
            'BurntAreas:RasteriseBurntAreas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Upload Burnt Areas
        alg_params = {
            'AttributedBurntAreas': outputs['AttributeBurntAreas']['AttributedBurntAreas'],
            'RasterisedBurntAreas': outputs['RasteriseBurntAreas']['RasterisedBurntAreas'],
            'Region': parameters['Region']
        }
        outputs['UploadBurntAreas'] = processing.run(
            'BurntAreas:UploadBurntAreas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        results['AttributedBurntAreas'] = outputs['AttributeBurntAreas']['AttributedBurntAreas']
        return results

    def name(self):
        return 'FullBurntAreasProcess'

    def displayName(self):
        return 'Process and Upload Burnt Areas'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return FullBurntAreasProcess()
