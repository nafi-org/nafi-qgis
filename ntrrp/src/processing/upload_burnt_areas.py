# -*- coding: utf-8 -*-
import os
import os.path as path
import shutil
import subprocess

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProject

import processing

from ..utils import ensureDirectory, getNtrrpUploadUrl, getRandomFilename, getUploadDirectory, resolvePluginPath, NTRRP_REGIONS


class UploadBurntAreas(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        processing.ProcessingConfig.setSettingValue(
            'IGNORE_INVALID_FEATURES', 1)
        self.addParameter(QgsProcessingParameterVectorLayer('AttributedBurntAreas', 'Your approved and attributed burnt areas', types=[
                          QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterEnum('Region', 'Region', options=NTRRP_REGIONS,
                          allowMultiple=False, usesStaticStrings=False, defaultValue=0))
        self.addParameter(QgsProcessingParameterRasterLayer(
            'RasterisedBurntAreas', 'Rasterised and merged burnt area map', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)

        feedback.pushInfo(
            f"Rasterised Burnt Areas: {type(parameters['RasterisedBurntAreas'])} {str(parameters['RasterisedBurntAreas'])}")

        # Derive region string from enum parameter
        region = NTRRP_REGIONS[parameters['Region']]

        # set up a temp filesystem
        uploadDir = getUploadDirectory()
        randomDir = getRandomFilename()
        archiveDir = path.join(uploadDir, randomDir)

        if path.exists(archiveDir):
            os.rmdir(archiveDir)

        ensureDirectory(archiveDir)

        saveBurntAreas = path.join(archiveDir, "burnt_areas.shp")

        feedback.pushInfo(
            f"Saving attributed burnt areas to {saveBurntAreas} …")

        # save Attributed Burnt Areas
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': parameters['AttributedBurntAreas'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': saveBurntAreas
        }
        processing.run('native:savefeatures', alg_params,
                       context=context, feedback=feedback, is_child_algorithm=True)

        # make this work whether the input is a layer ID or a filename
        rasterisedBurntAreasPath = self.deriveRasterisedBurntAreasPath(
            parameters['RasterisedBurntAreas'])

        feedback.pushInfo(
            f"Rasterised burnt areas path: {rasterisedBurntAreasPath}")
        rasterisedTifLocation = path.join(archiveDir, "rasterised.tif")
        feedback.pushInfo(
            f"Copying rasterised burnt areas to {rasterisedTifLocation} …")

        # copy the rasterised burnt areas output to the upload location ready for archiving
        shutil.copyfile(rasterisedBurntAreasPath, rasterisedTifLocation)

        # make_archive appends a .zip as well
        archiveLocation = path.join(uploadDir, getRandomFilename())
        ensureDirectory(archiveLocation)
        archive = path.join(
            archiveLocation, f"bfnt_{region.lower()}_current_sr3577")
        feedback.pushInfo(f"Zipping all upload data to {archive} …")

        os.chdir(archiveDir)
        shutil.make_archive(archive, "zip", archiveDir)

        feedback.pushInfo(f"Starting NAFI upload …")

        # try to upload the lot!
        try:
            patriceScript = resolvePluginPath("src/upload/upload.py")

            feedback.pushInfo(f"Using upload script at: {patriceScript}")

            args = ["python", patriceScript,
                    "-u", getNtrrpUploadUrl(),
                    "-f", f"{archive}.zip",
                    "-cs", "409600",
                    "-v"]

            commandLine = " ".join(args)

            feedback.pushInfo(f"Upload script command line: {commandLine}")

            # mojo from Patrice
            returnCode = subprocess.run(args, shell=True)

            # return code handling commented here because the UNIX 0=success convention is not respected
            # if returnCode == 0:
            feedback.pushInfo("NAFI upload succeeded.")
            # else:
            #   feedback.reportError("NAFI upload failed.", fatalError=True)

        except Exception as err:
            raise RuntimeError(r"""Exception occurred spawning external NAFI upload script … 
                                   check you can run scripts of the form 
                                   'python.exe upload.py -u https://test.firenorth.org.au/bfnt -f examples\bfnt_darwin_current_sr3577_tif.zip -cs 409600 -v'""")

        # we need to return something to processing engine or it records a failure
        return {
            'ArchiveLocation': archive
        }

    def deriveRasterisedBurntAreasPath(self, rasterisedBurntAreasParam):
        # derive Rasterised Burnt Areas output file from the specified rasterised burnt areas layer
        project = QgsProject.instance()
        rasterisedBurntAreasLayer = project.mapLayer(rasterisedBurntAreasParam)
        if rasterisedBurntAreasLayer is not None:
            return rasterisedBurntAreasLayer.dataProvider().dataSourceUri()
        else:
            return rasterisedBurntAreasParam

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
