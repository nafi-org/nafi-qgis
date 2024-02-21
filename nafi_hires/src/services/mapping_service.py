from nafi_hires.src.api import HiResApiService
from nafi_hires.src.models import (
    CurrentMappingLayer,
    Mapping,
    MappingFeatureLayer,
    SegmentationLayer,
)
from nafi_hires.src.utils import HIRES_API_URL, guiError
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface


class MappingService(QObject):
    dataDownloadFinished = pyqtSignal()
    currentMappingDownloadFinished = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        self.api = HiResApiService(HIRES_API_URL)

    def addMappingFeatureLayer(self, mapping: Mapping):
        """Create a new working layer for this region."""
        if mapping.mappingLayer is None:
            mapping.mappingLayer = MappingFeatureLayer(mapping)
        # workingLayer.layerRemoved.connect(
        #     lambda layer: self.removeWorkingLayer(layer))
        mapping.mappingLayer.addMapLayer()
        return mapping.mappingLayer

    def addCurrentMappingLayer(self, mapping: Mapping):
        """Add the current mapping layer to the map."""
        mapping.currentMappingLayer = CurrentMappingLayer(mapping)
        mapping.currentMappingLayer.addMapLayer()

    def addMappingLayers(self, mapping: Mapping):
        self.addSegmentationLayers(mapping, mapping.segmentationDirectory)

        if mapping.segmentationLayers:
            self.addMappingFeatureLayer(mapping, mapping.segmentationLayers[0])

    def addSegmentationLayers(self, mapping: Mapping):
        """Add all shapefiles in a directory as data layers to the region group."""

        mapping.segmentationLayers = [
            SegmentationLayer(segmentationDataset)
            for segmentationDataset in self.api.getIngestedSegmentationDatasets(
                mapping.data
            )
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
        if mapping.mappingLayer is None:
            guiError("Error occurred: inconsistent state in working layer.")
        else:
            pass
            # TODO convert the selection into meaningful client side behaviour

            # self.api.approveSegmentation()

            # iface.setActiveLayer(mapping.currentSegmentationLayer)
            # iface.actionCopyFeatures().trigger()
            # iface.setActiveLayer(mapping.mappingLayer)

            # # If not currently editing, start editing this layer
            # wasEditing = self.isEditable()
            # if not wasEditing:
            #     self.startEditing()

            # iface.actionPasteFeatures().trigger()

            # # Commit the changes, and stop editing if we weren't before
            # self.commitChanges(stopEditing=(not wasEditing))

            # iface.mainWindow().findChild(QAction, "mActionDeselectAll").trigger()
            # iface.setActiveLayer(self.segmentationLayer)

            # # Repopulate the clipboard with no features to avoid re-pasting
            # iface.actionCopyFeatures().trigger()

        # TODO wait for the operation to finish then refresh the HiResMappingFeatureLayer?
