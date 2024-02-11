from typing import Any

from pathlib import Path
from shutil import copytree
from zipfile import ZipFile

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFolderDestination,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterEnum,
)
import processing

from ntrrp.src.utils import (
    ensureDirectory,
    ensureTempDirectories,
    getNtrrpDataUrl,
    getTempDirectory,
    getTempZipFilename,
    qgsDebug,
    NTRRP_REGIONS,
)


class DownloadSegmentationData(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterEnum(
                "Region",
                "Region",
                options=NTRRP_REGIONS,
                allowMultiple=False,
                usesStaticStrings=False,
                defaultValue=0,
            )
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                "SegmentationDirectory",
                "Segmentation data download directory",
                defaultValue=None,
            )
        )

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results: dict[str, Any] = {"SegmentationDirectory": None}

        # Ensure segmentation data directory exists
        segmentationDirectory = Path(parameters["SegmentationDirectory"])
        ensureDirectory(segmentationDirectory)

        # Ensure all temp directories exist
        ensureTempDirectories()

        # Set up transfer parameters
        region = NTRRP_REGIONS[parameters["Region"]]
        downloadUrl = f"{getNtrrpDataUrl()}/{region.lower()}/{region.lower()}.zip"
        tempFile = getTempZipFilename()
        unzipLocation = getTempDirectory()

        qgsDebug(f"Downloading {downloadUrl} to {tempFile}")

        # Download ZIP to temp location
        alg_params = {"OUTPUT": tempFile, "URL": downloadUrl}
        processing.run(
            "native:filedownloader",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        # Unzip ZIP to region data folder
        if not Path(tempFile).exists():
            return results
        else:
            with ZipFile(Path(tempFile), "r") as zf:
                zf.extractall(unzipLocation)
                zf.close()
                Path(tempFile).unlink()

                # Copy the tree from the original unzip location to the segmentation data
                # directory (may overwrite stuff)
                copytree(unzipLocation, segmentationDirectory, dirs_exist_ok=True)

            results = {"SegmentationDirectory": segmentationDirectory}

        return results

    def name(self):
        return "DownloadSegmentationData"

    def displayName(self):
        return "Download NAFI Segmentation Data"

    def group(self):
        return ""

    def groupId(self):
        return ""

    def createInstance(self):
        return DownloadSegmentationData()
