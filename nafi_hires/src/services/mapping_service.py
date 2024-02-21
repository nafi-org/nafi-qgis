from qgis.core import Qgis
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface

from nafi_hires.src.api import HiResApiService
from nafi_hires.src.models import (
    CurrentMappingLayer,
    Mapping,
    MappingFeatureLayer,
    SegmentationLayer,
)
from nafi_hires.src.utils import HIRES_API_URL, guiError, qgsDebug


class MappingService(QObject):
    dataDownloadFinished = pyqtSignal()
    currentMappingDownloadFinished = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        self.api = HiResApiService(HIRES_API_URL)

    def addMappingFeatureLayer(self, mapping: Mapping):
        """Create a new working layer for this region."""
        qgsDebug(
            "MappingService.addMappingFeatureLayer not yet implemented",
            level=Qgis.Critical,
        )
        # if mapping.mappingFeatureLayer() is None:
        #     mapping.setMappingFeatureLayer(MappingFeatureLayer(mapping))
        # workingLayer.layerRemoved.connect(
        #     lambda layer: self.removeWorkingLayer(layer))
        # mapping.mappingFeatureLayer().addMapLayer()
        # return mapping.mappingFeatureLayer()

    def addCurrentMappingLayer(self, mapping: Mapping):
        """Add the current mapping layer to the map."""
        mapping.setCurrentMappingLayer(CurrentMappingLayer(mapping, mapping.data))
        mapping.currentMappingLayer().addMapLayer()

    def addMappingLayers(self, mapping: Mapping):
        self.addSegmentationLayers(mapping)

        if mapping.segmentationLayers():
            self.addMappingFeatureLayer(mapping)

    def addSegmentationLayers(self, mapping: Mapping):
        """Add all shapefiles in a directory as data layers to the region group."""

        # Because we have several SegmentationDataset objects for every actual
        # source table, we need to group them by the keys that determine the source
        # table name to avoid creating lots of duplicate layers.

        segmentationGroups = self.api.groupSegmentationDatasets(mapping.data)
        segmentationLayers = [
            SegmentationLayer(mapping, list(group)[0]) for group in segmentationGroups
        ]

        for segmentationLayer in segmentationLayers:
            segmentationLayer.addMapLayer()
        mapping.setSegmentationLayers(segmentationLayers)

    def removeSegmentationLayer(
        self, mapping: Mapping, segmentationLayer: SegmentationLayer
    ):
        """Remove a segmentation layer and inform subscribers."""
        mapping.segmentationLayers().remove(segmentationLayer)

    def approveSelectedFeatures(self, mapping: Mapping):
        """Add the currently selected features in the segmentation layer to the working layer."""
        if mapping.currentSegmentationLayer() is None:
            guiError("Error occurred: inconsistent state in segmentation layer.")
        if mapping.mappingFeatureLayer() is None:
            guiError("Error occurred: inconsistent state in working layer.")
        else:
            pass
            # TODO convert the selection into meaningful client side behaviour

            # self.api.approveSegmentation()

            # iface.setActiveLayer(mapping.currentSegmentationLayer())
            # iface.actionCopyFeatures().trigger()
            # iface.setActiveLayer(mapping.mappingLayer())

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
