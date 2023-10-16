# -*- coding: utf-8 -*-
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QModelIndex, QSortFilterProxyModel, QSize, Qt, pyqtSignal
from qgis.core import QgsProject
from qgis.utils import iface as QgsInterface

from .ntrrp_about_dialog import NtrrpAboutDialog
from .ntrrp_capabilities_reader import NtrrpCapabilitiesReader
from .ntrrp_dockwidget_base import Ui_NtrrpDockWidgetBase
from .ntrrp_item import NtrrpItem
from .ntrrp_mapping import NtrrpMapping
from .ntrrp_tree_view_model import NtrrpTreeViewModel
from .utils import getNtrrpWmsUrl, guiInformation, qgsDebug


class NtrrpDockWidget(QtWidgets.QDockWidget, Ui_NtrrpDockWidgetBase):
    closingPlugin = pyqtSignal()
    updateState = pyqtSignal()

    NO_SELECTION_TEXT = "Select layer …"

    def __init__(self, parent=None):
        """Constructor."""
        super(NtrrpDockWidget, self).__init__(parent)

        self.setupUi(self)

        # set up QTreeView
        self.treeView.setHeaderHidden(True)
        self.treeView.setSortingEnabled(True)
        self.treeView.setFocusPolicy(Qt.NoFocus)
        self.treeView.pressed.connect(self.treeViewPressed)

        # set up base model
        self.treeViewModel = NtrrpTreeViewModel(getNtrrpWmsUrl())

        # set up proxy model for filtering
        self.proxyModel = QSortFilterProxyModel(self.treeView)
        self.proxyModel.setSourceModel(self.treeViewModel)
        self.proxyModel.setRecursiveFilteringEnabled(True)
        self.treeView.setModel(self.proxyModel)

        # respond to layers being removed
        QgsProject.instance().layerRemoved.connect(
            lambda: self.treeViewModel.refresh())

        # set up active layer handler
        QgsInterface.layerTreeView().currentLayerChanged.connect(self.activeLayerChanged)

        # set up mapping combobox
        self.mappingComboBox.currentIndexChanged.connect(
            self.mappingComboBoxChanged)

        # set up segmentation layer combobox
        # self.segmentationLayerComboBox.currentIndexChanged.connect(
        #     self.segmentationLayerComboBoxChanged)

        # set up working layer combobox
        self.workingLayerComboBox.currentIndexChanged.connect(
            self.workingLayerComboBoxChanged)

        # set up About … dialog
        self.aboutButton.clicked.connect(self.showAboutDialog)

        # set up refresh button
        self.refreshButton.clicked.connect(self.loadNtrrpWms)

        # set up download button
        self.downloadButton.clicked.connect(lambda: self.downloadSegmentationData())

        # set up download current mapping button
        self.currentMappingButton.clicked.connect(
            lambda: self.downloadCurrentMapping())

        # set up create button
        self.createButton.clicked.connect(
            lambda: self.selectedMapping.createWorkingLayer(self.activeSegmentationLayer))

        # set up approve button
        self.approveButton.clicked.connect(
            lambda: self.activeWorkingLayer.copySelectedFeaturesFromSegmentationLayer())

        # set up upload button
        self.uploadButton.clicked.connect(lambda: self.runUpload())

        self.activeSegmentationLayer = None
        self.activeWorkingLayer = None

        # set up state management
        self.updateState.connect(lambda: self.enableDisable())

        self.reader = NtrrpCapabilitiesReader()
        self.reader.capabilitiesParsed.connect(
            lambda caps: self.initModel(caps))

        # restore the view from source whenever this dock widget is made visible again
        self.visibilityChanged.connect(
            lambda visible: visible and self.loadNtrrpWms())

        # initialise proxied tree view model from WMS contents
        self.loadNtrrpWms()

    def loadNtrrpWms(self):
        """Load the NAFI WMS and additional layers."""
        self.wmsUrl = getNtrrpWmsUrl()
        self.reader.downloadAndParseCapabilities(self.wmsUrl)

    def initModel(self, ntrrpCapabilities):
        """Initialise a QStandardItemModel from the NAFI WMS."""
        # stash the parsed capabilities and set up the mapping combobox
        self.ntrrpCapabilities = ntrrpCapabilities

        # get the region names for the combo
        self.mappingComboBox.clear()
        regionNames = sorted(region for region in self.ntrrpCapabilities.mappings)

        self.mappingComboBox.addItems(regionNames)

        initMapping = next(iter(self.ntrrpCapabilities.mappings))
        initMapping = self.ntrrpCapabilities.mappings[initMapping]

        if initMapping is not None:
            self.setMapping(initMapping)
            self.enableDisable()

    def isSelectedMapping(self, mapping):
        """Check if a mapping is the currently selected mapping."""
        return mapping and self.selectedMapping and (mapping.region == self.selectedMapping.region)

    def setMapping(self, mapping):
        """Set the current mapping."""
        if mapping is None:
            return

        assert (isinstance(mapping, NtrrpMapping))
        # disconnect signal handlers?
        # if self.region is not None:
        #    try:
        #        self.region.dataLayersChanged.disconnect()
        # …

        # clear some stuff
        self.activeSegmentationLayer = None
        self.activeWorkingLayer = None

        # set up signal handlers
        mapping.segmentationLayersChanged.connect(
            lambda _: self.updateSegmentationLayerLabel(self.activeSegmentationLayer))
        mapping.workingLayersChanged.connect(
            lambda workingLayers: self.updateWorkingLayerComboBox(workingLayers))
        mapping.ntrrpItemsChanged.connect(
            lambda: self.refreshCurrentMapping(mapping))

        self.selectedMapping = mapping
        self.updateSegmentationLayerLabel(self.activeSegmentationLayer)
        self.updateWorkingLayerComboBox(mapping.workingLayers)

        # populate tree view
        self.treeViewModel.setMapping(mapping)

        # set default sort and expansion
        self.proxyModel.sort(0, Qt.AscendingOrder)
        self.expandTopLevel()

    def refreshCurrentMapping(self, mapping):
        """If a mapping is the current mapping, refresh its tree view."""
        if self.isSelectedMapping(mapping):
            self.treeViewModel.setMapping(mapping)

    def sizeHint(self):
        return QSize(150, 400)

    def runUpload(self):
        """Convert the currently active working layer to a raster, attribute it and upload to NAFI."""
        self.selectedMapping.processAndUploadBurntAreas(self.activeWorkingLayer)

    def downloadSegmentationData(self):
        """Download the segmentation data."""
        self.selectedMapping.downloadSegmentationData()

    def downloadCurrentMapping(self):
        """Download the current mapping data."""
        self.selectedMapping.downloadCurrentMapping()

    # handlers
    def activeLayerChanged(self):
        """Update the active segmentation layer based on clicks in the Layers Panel."""
        activeLayer = QgsInterface.activeLayer()
        if activeLayer is not None:
            matchingSegmentationLayer = self.selectedMapping.getSegmentationLayerByMapLayer(
                activeLayer)
            if matchingSegmentationLayer is not None:
                self.activeSegmentationLayer = matchingSegmentationLayer
                self.updateSegmentationLayerLabel(self.activeSegmentationLayer)
                self.updateState.emit()

    def mappingComboBoxChanged(self, mappingIndex):
        """Switch the active mapping."""
        region = self.mappingComboBox.itemText(mappingIndex)
        mapping = self.ntrrpCapabilities.mappings.get(region, None)

        if mapping is not None:
            self.setMapping(mapping)

    def workingLayerComboBoxChanged(self, workingLayerIndex):
        """Switch the active segmentation layer."""
        workingLayerDisplayName = self.workingLayerComboBox.itemText(
            workingLayerIndex)
        if len(workingLayerDisplayName) > 0 and workingLayerDisplayName != self.NO_SELECTION_TEXT:
            self.activeWorkingLayer = self.selectedMapping.getWorkingLayerByName(
                workingLayerDisplayName)
            QgsInterface.setActiveLayer(self.activeWorkingLayer.impl)
        else:
            self.activeWorkingLayer = None
        self.updateState.emit()

    def updateSegmentationLayerLabel(self, segmentationLayer):
        """Update the segmentation layer label."""
        if segmentationLayer is None:
            self.activeSegmentationLayerLabel.setText(self.NO_SELECTION_TEXT)
            self.activeSegmentationLayerLabel.setStyleSheet(None)
        else:
            self.activeSegmentationLayerLabel.setText(segmentationLayer.getDisplayName())
            self.activeSegmentationLayerLabel.setStyleSheet(("color: rgb(158,16,21); "
                                                             "border: 1px solid black;"))

    # TODO: factor this into a custom ComboBox widget

    def updateWorkingLayerComboBox(self, workingLayers):
        """Update the working layers."""
        currentActiveItem = self.workingLayerComboBox.currentText()
        items = [workingLayer.getMapLayerName()
                 for workingLayer in workingLayers]
        items.insert(0, "")

        oldItems = [self.workingLayerComboBox.itemText(
            i) for i in range(self.workingLayerComboBox.count())]

        self.workingLayerComboBox.clear()
        self.workingLayerComboBox.addItems(items)

        # new item?
        if len(items) > len(oldItems):
            newItems = list(set(items) - set(oldItems))
            newItem = newItems[0]

            index = self.workingLayerComboBox.findText(
                newItem, Qt.MatchFixedString)
            if index > 0:
                self.workingLayerComboBox.setCurrentIndex(index)
        else:
            # restore working layer if present
            index = self.workingLayerComboBox.findText(
                currentActiveItem, Qt.MatchFixedString)
            if index > 0:
                self.workingLayerComboBox.setCurrentIndex(index)

    def expandTopLevel(self):
        """Exppand top level items in the tree view."""
        for row in range(self.proxyModel.rowCount()):
            self.treeView.expand(self.proxyModel.index(row, 0))

    def showAboutDialog(self):
        """Show an About … dialog."""
        aboutDialog = NtrrpAboutDialog()
        aboutDialog.exec_()

    def treeViewPressed(self, index):
        """Load a NAFI WMS layer given an index in the tree view."""
        assert isinstance(
            index, QModelIndex), "Supplied parameter is not a QModelIndex"

        realIndex = self.proxyModel.mapToSource(index)
        modelNode = self.treeViewModel.itemFromIndex(realIndex)

        # if we've got a layer and not a layer group, add to map
        if modelNode is not None:
            if isinstance(modelNode, NtrrpItem):
                self.selectedMapping.addWmtsLayer(modelNode)
                self.treeViewModel.refresh()

    def enableDisable(self):
        "Enable or disable UI elements based on current state."
        haveSegmentationLayers = bool(
            self.selectedMapping.segmentationLayers and len(self.selectedMapping.segmentationLayers) > 0)
        haveWorkingLayers = bool(
            self.selectedMapping.workingLayers and len(self.selectedMapping.workingLayers) > 0)

        if not haveSegmentationLayers:
            self.activeSegmentationLayerLabel.setText(
                "Download segmentation …")

        # need a selection
        self.workingLayerComboBox.setEnabled(haveWorkingLayers)
        if haveWorkingLayers:
            self.workingLayerComboBox.setItemText(0, self.NO_SELECTION_TEXT)
        elif not haveWorkingLayers and haveSegmentationLayers:
            self.workingLayerComboBox.setItemText(
                0, "Create a working layer first …")
            self.workingLayerComboBox.setCurrentIndex(0)

        # need to template working layers off segmentation layers, so we can't enable create until there is one
        haveSegmentationLayer = bool(self.activeSegmentationLayer)
        self.createButton.setEnabled(haveSegmentationLayer)

        # if we have both source and working, we can start approving
        haveBoth = bool(self.activeSegmentationLayer and self.activeWorkingLayer)
        if haveBoth:
            self.activeWorkingLayer.setSegmentationLayer(self.activeSegmentationLayer)
        self.approveButton.setEnabled(haveBoth)

        # we can upload when we've got an active working layer (might need to check for features later)
        haveWorkingLayer = bool(self.activeWorkingLayer)
        # self.uploadButton.setEnabled(haveWorkingLayer)
        self.uploadButton.setEnabled(True)

    def closeEvent(self, event):
        """Handle plug-in close."""
        self.closingPlugin.emit()
        event.accept()
