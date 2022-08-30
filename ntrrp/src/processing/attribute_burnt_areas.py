# -*- coding: utf-8 -*-
from datetime import date

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterDateTime
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterVectorLayer
import processing

from ..utils import NTRRP_REGIONS


class AttributeBurntAreas(QgsProcessingAlgorithm):

    nextFsid = -1

    def initAlgorithm(self, config=None):
        processing.ProcessingConfig.setSettingValue(
            'IGNORE_INVALID_FEATURES', 1)
        self.addParameter(QgsProcessingParameterVectorLayer('DissolvedBurntAreas', 'Your burnt areas (should already be dissolved)', types=[
                          QgsProcessing.TypeVectorPolygon], defaultValue=None))
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
        self.addParameter(QgsProcessingParameterString(
            'NextFsid', 'Fire Scar ID', multiLine=False, defaultValue=None))

        self.addParameter(QgsProcessingParameterFeatureSink('AttributedBurntAreas', 'Burnt areas attributed with FSID and other NAFI attributes',
                          type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Mapping Period – Enter the dates of the current image and T1 or T2 image date.
        # Month – do not change
        # Region – the areas mapped (ie a1, a2, a3, a4, Kat)
        # Upload date – enter the date you completed the mapping
        # Current – enter “yes” for the latest mapping for an area.
        # Comments – add any other additional information about a mapping period – ie note mapping problems due to cloud.

        # Derive region string from enum parameter
        regionName = NTRRP_REGIONS[parameters['Region']]
        comments = parameters['Comments']
        startDate = self.parameterAsDateTime(
            parameters, 'StartDate', context).toPyDateTime().strftime('%Y-%m-%d')
        nextFsid = parameters['NextFsid']

        feedback.pushInfo(
            "Adding FSID, Mapping Period, Month, Region, Upload Date, Curent, and Comments attributes to your burnt areas …")
        
        # add FSID
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'FSID',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,
            # hack to apply calculator from number input
            'FORMULA': f'value = {nextFsid}',
            'GLOBAL': '',
            'INPUT': parameters['DissolvedBurntAreas'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddFSID'] = processing.run(
            'qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # add Mapping Period
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'map_period',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': f'value = "{startDate}"',
            'GLOBAL': '',
            'INPUT': outputs['AddFSID']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddMappingPeriod'] = processing.run(
            'qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # add Month
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'month',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': 'value = month',
            'GLOBAL': 'from datetime import date\n\nmonth = date.today().strftime(r\"%m\")',
            'INPUT': outputs['AddMappingPeriod']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddMonth'] = processing.run(
            'qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # add Region
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'region',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': f'value = "{regionName}"',
            'GLOBAL': '',
            'INPUT': outputs['AddMonth']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddRegion'] = processing.run(
            'qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # add Upload Date
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'up_date',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': f'value = today',
            'GLOBAL': 'from datetime import date\n\ntoday = date.today().strftime(r\"%Y-%m-%d\")',
            'INPUT': outputs['AddRegion']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddUploadDate'] = processing.run(
            'qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # add Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'current',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': f'value = "yes"',
            'GLOBAL': '',
            'INPUT': outputs['AddUploadDate']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddCurrent'] = processing.run(
            'qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # add Comments
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'current',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': f'value = "{comments}"',
            'GLOBAL': '',
            'INPUT': outputs['AddCurrent']['OUTPUT'],
            'OUTPUT': parameters['AttributedBurntAreas'],
        }
        outputs['AddComments'] = processing.run(
            'qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        results['AttributedBurntAreas'] = outputs['AddComments']['OUTPUT']
        return results

    def name(self):
        return 'AttributeBurntAreas'

    def displayName(self):
        return 'Attribute Burnt Areas (add FSID)'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return AttributeBurntAreas()
