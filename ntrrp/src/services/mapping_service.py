from typing import Any

from pathlib import Path
from ntrrp.src.utils import guiError

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface

import processing

from ntrrp.src.models import (
    CurrentMappingLayer,
    Mapping,
    SegmentationLayer,
    SegmentationMetadata,
    WorkingLayer,
)
from ntrrp.src.utils import (
    NTRRP_REGIONS,
    doFullSegmentationDownload,
    deriveWorkingDirectory,
    ensureDirectory,
    getDownloadDirectory,
    qgsDebug,
)


class MappingService(QObject):
    dataDownloadFinished = pyqtSignal()
    currentMappingDownloadFinished = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

    def downloadCurrentMapping(self, mapping: Mapping):
        """Download current mapping for the region and add it to the map."""
        qgsDebug("Downloading current NAFI burnt areas mapping …")

        if deriveWorkingDirectory() is None:
            return None

        params = {
            "Region": NTRRP_REGIONS.index(mapping.regionName),
            "WorkingDirectory": deriveWorkingDirectory(),
        }
        dialog = processing.createAlgorithmDialog(
            "BurntAreas:DownloadCurrentMapping", params
        )
        dialog.algorithmFinished.connect(
            lambda _: self.addCurrentMappingLayer(
                mapping, dialog.results()["CurrentMappingDirectory"]
            )
        )
        for signal in [
            dialog.algorithmFinished,
            dialog.accepted,
            dialog.rejected,
            dialog.destroyed,
        ]:
            signal.connect(lambda: self.currentMappingDownloadFinished.emit())
        dialog.show()
        dialog.runButton().click()

        return True

    def downloadSegmentationData(self, mapping: Mapping):
        """Download segmentation features from NAFI and call back to add them to the map."""
        if doFullSegmentationDownload():
            if deriveWorkingDirectory() is None:
                return None

            params = {
                "Region": NTRRP_REGIONS.index(mapping.region.regionName),
                "SegmentationDirectory": mapping.segmentationDirectory.as_posix(),
            }
            dialog = processing.createAlgorithmDialog(
                "BurntAreas:DownloadSegmentationData", params
            )
            dialog.algorithmFinished.connect(
                lambda _: self.addSegmentationLayers(
                    mapping, dialog.results()["SegmentationDirectory"]
                )
            )
            for signal in [
                dialog.algorithmFinished,
                dialog.accepted,
                dialog.rejected,
                dialog.destroyed,
            ]:
                signal.connect(lambda: self.dataDownloadFinished.emit())
            dialog.show()
            dialog.runButton().click()

        self.addMappingLayers(mapping)

    def addWorkingLayer(
        self, mapping: Mapping, templateSegmentationLayer: SegmentationLayer
    ):
        """Create a new working layer for this region."""
        if mapping.workingLayer is None:
            mapping.workingLayer = WorkingLayer(mapping, templateSegmentationLayer)
        # workingLayer.layerRemoved.connect(
        #     lambda layer: self.removeWorkingLayer(layer))
        mapping.workingLayer.addMapLayer()
        return mapping.workingLayer

    def addCurrentMappingLayer(self, mapping: Mapping, unzipLocation):
        """Add the current mapping layer to the map."""
        if unzipLocation is None:
            return
        rasterFile = next(Path(unzipLocation).rglob("*.tif"))
        mapping.currentMappingLayer = CurrentMappingLayer(mapping, rasterFile)
        mapping.currentMappingLayer.addMapLayer()

    def addMappingLayers(self, mapping: Mapping):
        self.addSegmentationLayers(mapping, mapping.segmentationDirectory)

        if mapping.segmentationLayers:
            self.addWorkingLayer(mapping, mapping.segmentationLayers[0])

    def addSegmentationLayers(self, mapping: Mapping, segmentationDirectory: Path):
        """Add all shapefiles in a directory as data layers to the region group."""
        if segmentationDirectory is None:
            return

        ensureDirectory(segmentationDirectory)

        shapefilePaths = [path for path in segmentationDirectory.rglob("*.shp")]

        # Determine the mapping date from what's been downloaded
        mapping.mappingDate = max(
            [SegmentationMetadata(path).endDate for path in shapefilePaths]
        )

        mapping.segmentationLayers = [
            SegmentationLayer(mapping, path) for path in shapefilePaths
        ]

        for segmentationLayer in mapping.segmentationLayers:
            # segmentationLayer.layerRemoved.connect(
            #     lambda layer: self.removeSegmentationLayer(layer))
            segmentationLayer.addMapLayer()

    def removeSegmentationLayer(
        self, mapping: Mapping, segmentationLayer: SegmentationLayer
    ):
        """Remove a segmentation layer and inform subscribers."""
        mapping.segmentationLayers.remove(segmentationLayer)

    def approveSelectedFeatures(self, mapping: Mapping):
        """Add the currently selected features in the segmentation layer to the working layer."""
        if mapping.currentSegmentationLayer is None:
            guiError("Error occurred: inconsistent state in segmentation layer.")
        if mapping.workingLayer is None:
            guiError("Error occurred: inconsistent state in working layer.")
        else:
            iface.setActiveLayer(mapping.currentSegmentationLayer)
            iface.actionCopyFeatures().trigger()
            iface.setActiveLayer(mapping.workingLayer)

            # If not currently editing, start editing this layer
            wasEditing = self.isEditable()
            if not wasEditing:
                self.startEditing()

            iface.actionPasteFeatures().trigger()

            # Commit the changes, and stop editing if we weren't before
            self.commitChanges(stopEditing=(not wasEditing))

            iface.mainWindow().findChild(QAction, "mActionDeselectAll").trigger()
            iface.setActiveLayer(self.segmentationLayer)

            # Repopulate the clipboard with no features to avoid re-pasting
            iface.actionCopyFeatures().trigger()

        # Save after adding
        mapping.workingLayer.saveFeatures()

    # Upload data
    def processAndUploadBurntAreas(self, mapping: Mapping):
        """Upload the curated working layer to NAFI."""

        params: dict[str, Any] = {
            "Region": NTRRP_REGIONS.index(mapping.regionName),
        }

        if mapping.workingLayer is not None:
            params["ApprovedBurntAreas"] = mapping.workingLayer.id()

        # Default current mapping layer if present
        if mapping.currentMappingLayer is not None:
            params["CurrentMapping"] = mapping.currentMappingLayer.id()

        paramsWithFsid = processing.execAlgorithmDialog(
            "BurntAreas:ValidateFullBurntAreasProcess", params
        )

        if paramsWithFsid.get("FsidServiceError", None) is not None:
            FsidServiceError = paramsWithFsid["FsidServiceError"]
            FsidServiceError.guiError()
            FsidServiceError.log()
