# -*- coding: utf-8 -*-
from datetime import date

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterDateTime
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
import processing

from ..ntrrp_fsid_error import NtrrpFsidError
from ..ntrrp_fsid_service import NtrrpFsidService
from ..utils import getNtrrpApiUrl, NTRRP_REGIONS


class ValidateFullBurntAreasProcess(QgsProcessingAlgorithm):

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
                          type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None)),

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}

        # Mapping Period – Enter the dates of the current image and T1 or T2 image date.
        # Month – do not change
        # Region – the areas mapped (ie a1, a2, a3, a4, Kat)
        # Upload date – enter the date you completed the mapping
        # Curent – enter “yes” for the latest mapping for an area.
        # Comments – add any other additional information about a mapping period – ie note mapping problems due to cloud.

        # Derive region string from enum parameter
        regionName = NTRRP_REGIONS[parameters['Region']]
        author = parameters['Author']
        comments = parameters['Comments']
        startDate = self.parameterAsDateTime(
            parameters, 'StartDate', context).toPyDateTime().strftime('%Y-%m-%d')
        endDate = self.parameterAsDateTime(
            parameters, 'EndDate', context).toPyDateTime().strftime('%Y-%m-%d')
        uploadDate = date.today().strftime("%Y-%m-%d")

        postParams = {
            'author': author,
            'start_date': startDate,
            'end_date': endDate,
            'region': regionName,
            'upload_date': uploadDate,
            'comment': comments
        }

        # Get the next available FSID
        feedback.pushInfo(
            "Retrieving next available FSID from NAFI endpoint …")
        self.fsidService = NtrrpFsidService()

        try:
            fsidRecord = self.fsidService.postNewMapping(
                getNtrrpApiUrl(), regionName, postParams)
            
            nextFsid = fsidRecord.fsid
            feedback.pushInfo("FSID retrieval was successful")
            feedback.pushInfo(f"Next FSID: {nextFsid}")

            # Assemble all results for the next bit of processing
            results['ApprovedBurntAreas'] = parameters['ApprovedBurntAreas']
            results['CurrentMapping'] = parameters['CurrentMapping']
            results['Region'] = parameters['Region']
            results['Author'] = author
            results['Comments'] = comments
            results['StartDate'] = startDate
            results['EndDate'] = endDate
            results['NextFsid'] = nextFsid
            results['AttributedBurntAreas'] = parameters['AttributedBurntAreas']

            # Execute the full burnt areas process with the obtained FSID etc
            results = processing.run('BurntAreas:FullBurntAreasProcess', results, context=context, feedback=feedback, is_child_algorithm=True)

        except NtrrpFsidError as fsidError:
            fsidError.processingFeedbackError(feedback)
            results['FsidError'] = fsidError

        return results

    def name(self):
        return 'ValidateFullBurntAreasProcess'

    def displayName(self):
        return 'Full Burnt Areas Process'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return ValidateFullBurntAreasProcess()
