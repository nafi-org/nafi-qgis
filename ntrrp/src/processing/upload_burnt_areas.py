# -*- coding: utf-8 -*-
import os.path as path
import shutil
import subprocess

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProject

import processing

from ..utils import ensureDirectory, getNtrrpUploadUrl, getRandomFilename, getUploadDirectory, resolvePluginPath, qgsDebug

class UploadBurntAreas(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        processing.ProcessingConfig.setSettingValue(
            'IGNORE_INVALID_FEATURES', 1)
        self.addParameter(QgsProcessingParameterVectorLayer('AttributedBurntAreas', 'Your approved burnt areas', types=[
                          QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer(
            'RasterisedBurntAreas', 'Your rasterised burnt areas merged with the current mapping', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}

        # set up a temp filesystem
        uploadDir = getUploadDirectory()
        archiveName = getRandomFilename()

        archiveDir = path.join(uploadDir, archiveName)
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

        # derive Rasterised Burnt Areas output file from the specified rasterised burnt areas layer
        project = QgsProject.instance()
        rasterisedBurntAreasLayer = project.mapLayer(
            parameters["RasterisedBurntAreas"])
        rasterisedBurntAreasPath = rasterisedBurntAreasLayer.dataProvider().dataSourceUri()

        feedback.pushInfo(
            f"Rasterised burnt areas path: {rasterisedBurntAreasPath}")
        rasterisedTifLocation = path.join(archiveDir, "rasterised.tif")
        feedback.pushInfo(
            f"Copying rasterised burnt areas to {rasterisedTifLocation} …")

        shutil.copyfile(rasterisedBurntAreasPath, rasterisedTifLocation)

        # make_archive appends a .zip as well
        archive = path.join(uploadDir, f"{archiveName}.zip")
        feedback.pushInfo(f"Zipping all upload data to {archive} …")

        shutil.make_archive(archiveDir, "zip", archiveDir)

        feedback.pushInfo(f"Attempting upload …")

        # try to upload the lot!
        try:
            patriceScript = resolvePluginPath("src/upload/upload.py")

            feedback.pushInfo(f"Patrice's script: {patriceScript}")

            args = ["python", patriceScript,
                    "-u", getNtrrpUploadUrl(),
                    "-f", archive,
                    "-cs", 409600,
                    "-v"]

            feedback.pushInfo(f"Arguments: {str(args)}")

            # mojo from Patrice
            subprocess.run(["python", patriceScript,
                            "-u", getNtrrpUploadUrl(),
                            "-f", archive,
                            "-cs", "409600",
                            "-v"])

        except Exception as err:
            raise RuntimeError(r"""Exception occurred spawning external NAFI upload script … 
                                   check you can run scripts of the form 
                                   'python.exe upload.py -u https://test.firenorth.org.au/bfnt -f examples\bfnt_darwin_current_sr3577_tif.zip -cs 409600 -v'""")
        
        # we need to return something to processing engine or it records a failure
        return {
            'ArchiveLocation': archive
        }

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
