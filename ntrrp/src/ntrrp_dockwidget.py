# -*- coding: utf-8 -*-
from random import randint

from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSignal, QSortFilterProxyModel, Qt, QModelIndex
from qgis.utils import iface as QgsInterface

from .ntrrp_about_dialog import NtrrpAboutDialog
from .ntrrp_capabilities_reader import NtrrpCapabilitiesReader
from .ntrrp_dockwidget_base import Ui_NtrrpDockWidgetBase
from .ntrrp_item import NtrrpItem
from .ntrrp_region import NtrrpRegion
from .ntrrp_tree_view_model import NtrrpTreeViewModel
from .processing.upload import Upload
from .utils import getNtrrpWmsUrl, getWorkingShapefilePath, guiInformation, qgsDebug


class NtrrpDockWidget(QtWidgets.QDockWidget, Ui_NtrrpDockWidgetBase):
    closingPlugin = pyqtSignal()
    updateState = pyqtSignal()

    NO_SELECTION_TEXT = "Select …"

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

        # set up region combobox
        self.regionComboBox.currentIndexChanged.connect(self.regionComboBoxChanged)

        # set up source layer combobox
        self.sourceLayerComboBox.currentIndexChanged.connect(self.sourceLayerComboBoxChanged)

        # set up working layer combobox
        self.workingLayerComboBox.currentIndexChanged.connect(self.workingLayerComboBoxChanged)

        # set up About … dialog
        self.aboutButton.clicked.connect(self.showAboutDialog)

        # set up refresh button
        self.refreshButton.clicked.connect(self.loadNtrrpWms)

        # set up download button
        self.downloadButton.clicked.connect(lambda: self.region.downloadData())

        # set up create button
        self.createButton.clicked.connect(lambda: self.region.createWorkingLayer(self.activeSourceLayer))

        # set up approve button
        self.approveButton.clicked.connect(lambda: self.activeWorkingLayer.copySelectedFeaturesFromSourceLayer())

        # set up upload button
        self.uploadButton.clicked.connect(lambda: self.runUpload())

        self.activeSourceLayer = None
        self.activeWorkingLayer = None

        # set up state management
        self.updateState.connect(lambda: self.enableDisable())

        self.reader = NtrrpCapabilitiesReader()
        self.reader.capabilitiesParsed.connect(lambda caps: self.initModel(caps))

        # restore the view from source whenever this dock widget is made visible again
        self.visibilityChanged.connect(lambda visible: visible and self.loadNtrrpWms())

        # initialise proxied tree view model from WMS contents
        self.loadNtrrpWms()

    def loadNtrrpWms(self):
        """Load the NAFI WMS and additional layers."""
        self.wmsUrl = getNtrrpWmsUrl()
        self.reader.downloadAndParseCapabilities(self.wmsUrl)

    def initModel(self, ntrrpCapabilities):
        """Initialise a QStandardItemModel from the NAFI WMS."""
        # stash the parsed capabilities and set up the region combobox
        self.ntrrpCapabilities = ntrrpCapabilities

        # get the region names for the combo
        self.regionComboBox.clear()
        regions = [region for region in self.ntrrpCapabilities.regions]
        regions.sort()

        self.regionComboBox.addItems(regions)

        initRegionName = next(iter(self.ntrrpCapabilities.regions))
        initRegion = self.ntrrpCapabilities.regions[initRegionName]

        if initRegion is not None:
            self.setRegion(initRegion)
            self.enableDisable()

    def isCurrentRegion(self, region):
        """Check if a region is the current NTRRP region."""
        return region and self.region and (region.name == self.region.name)

    def setRegion(self, region):
        """Set the current NTRRP region."""
        if region is None:
            return

        assert(isinstance(region, NtrrpRegion))
        # disconnect signal handlers?
        # if self.region is not None:
        #    try:
        #        self.region.dataLayersChanged.disconnect()
        # …

        # clear some stuff
        self.activeSourceLayer = None
        self.activeWorkingLayer = None

        # set up signal handlers
        region.sourceLayersChanged.connect(lambda sourceLayers: self.updateSourceLayerComboBox(sourceLayers))
        region.workingLayersChanged.connect(lambda workingLayers: self.updateWorkingLayerComboBox(workingLayers))
        region.ntrrpItemsChanged.connect(lambda: self.refreshCurrentRegion(region))

        self.region = region
        self.updateSourceLayerComboBox(region.sourceLayers)
        self.updateWorkingLayerComboBox(region.workingLayers)
        
        # populate tree view
        self.treeViewModel.setRegion(region)
        
        # set default sort and expansion
        self.proxyModel.sort(0, Qt.AscendingOrder)
        self.expandTopLevel()

    def refreshCurrentRegion(self, region):
        """If a region is the current region, refresh the tree view."""
        if self.isCurrentRegion(region):
            self.treeViewModel.setRegion(region)

    def sizeHint(self):
        return QtCore.QSize(150, 400)

    # handlers    

    def regionComboBoxChanged(self, regionIndex):
        """Switch the active region."""
        regionName = self.regionComboBox.itemText(regionIndex)
        region = self.ntrrpCapabilities.regions.get(regionName, None)

        if region is not None:
            self.setRegion(region)

    def sourceLayerComboBoxChanged(self, sourceLayerIndex):
        """Switch the active source layer."""
        sourceLayerDisplayName = self.sourceLayerComboBox.itemText(sourceLayerIndex)
        if len(sourceLayerDisplayName) > 0 and sourceLayerDisplayName != self.NO_SELECTION_TEXT:
            self.activeSourceLayer = self.region.getSourceLayerByDisplayName(sourceLayerDisplayName)
            QgsInterface.setActiveLayer(self.activeSourceLayer.impl)
        else:
            self.activeSourceLayer = None
        self.updateState.emit()
    
    def workingLayerComboBoxChanged(self, workingLayerIndex):
        """Switch the active source layer."""
        workingLayerDisplayName = self.workingLayerComboBox.itemText(workingLayerIndex)
        if len(workingLayerDisplayName) > 0 and workingLayerDisplayName != self.NO_SELECTION_TEXT:
            self.activeWorkingLayer = self.region.getWorkingLayerByName(workingLayerDisplayName)
            QgsInterface.setActiveLayer(self.activeWorkingLayer.impl)
        else:
            self.activeWorkingLayer = None
        self.updateState.emit()

    def updateSourceLayerComboBox(self, sourceLayers):
        """Update the source layers."""
        current = self.sourceLayerComboBox.currentText()
        self.sourceLayerComboBox.clear()
        items = [sourceLayer.getDisplayName() for sourceLayer in sourceLayers]
        items.insert(0, "")
        self.sourceLayerComboBox.addItems(items)

        # restore source layer if present
        index = self.sourceLayerComboBox.findText(current, Qt.MatchFixedString)
        if index > 0:
            self.sourceLayerComboBox.setCurrentIndex(index)

    # TODO: factor this into a custom ComboBox widget
    def updateWorkingLayerComboBox(self, workingLayers):
        """Update the source layers."""
        currentActiveItem = self.workingLayerComboBox.currentText()
        items = [workingLayer.getMapLayerName() for workingLayer in workingLayers]
        items.insert(0, "")      
        
        oldItems = [self.workingLayerComboBox.itemText(i) for i in range(self.workingLayerComboBox.count())]

        self.workingLayerComboBox.clear()
        self.workingLayerComboBox.addItems(items)

        # new item?
        if len(items) > len(oldItems):
            newItems = list(set(items) - set(oldItems))
            newItem = newItems[0]

            index = self.workingLayerComboBox.findText(newItem, Qt.MatchFixedString)
            if index > 0:
                self.workingLayerComboBox.setCurrentIndex(index)
        else: 
            # restore working layer if present
            index = self.workingLayerComboBox.findText(currentActiveItem, Qt.MatchFixedString)
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
        assert isinstance(index, QModelIndex), "Supplied parameter is not a QModelIndex"

        realIndex = self.proxyModel.mapToSource(index)
        modelNode = self.treeViewModel.itemFromIndex(realIndex)
       
        # if we've got a layer and not a layer group, add to map
        if modelNode is not None:
            if isinstance(modelNode, NtrrpItem):
                self.region.addWmtsLayer(modelNode)

    def runUpload(self):
        """Convert the currently active working layer to a raster, attribute it and upload to NAFI."""

        fsid = randint(100, 200)
        results = Upload.run(self.activeWorkingLayer.impl, fsid, self.region.name, getWorkingShapefilePath())
        guiInformation(results)

    def enableDisable(self):
        "Enable or disable UI elements based on current state."
        haveSourceLayers = bool(self.region.sourceLayers and len(self.region.sourceLayers) > 0)
        haveWorkingLayers = bool(self.region.workingLayers and len(self.region.workingLayers) > 0)
        
        # need a selection of source layers before we can start choosing
        self.sourceLayerComboBox.setEnabled(haveSourceLayers)
        if haveSourceLayers:
            self.sourceLayerComboBox.setItemText(0, self.NO_SELECTION_TEXT)
        else:
            self.sourceLayerComboBox.setItemText(0, "Download NAFI burnt areas first …")
            self.sourceLayerComboBox.setCurrentIndex(0)

        # need a selection
        self.workingLayerComboBox.setEnabled(haveWorkingLayers)
        if haveWorkingLayers:
            self.workingLayerComboBox.setItemText(0, self.NO_SELECTION_TEXT)
        elif not haveWorkingLayers and haveSourceLayers:
            self.workingLayerComboBox.setItemText(0, "Create a working layer first …")
            self.workingLayerComboBox.setCurrentIndex(0)

        # need to template working layers off source layers, so we can't enable create until there is one
        haveSourceLayer = bool(self.activeSourceLayer)
        self.createButton.setEnabled(haveSourceLayer)

        # if we have both source and working, we can start approving
        haveBoth = bool(self.activeSourceLayer and self.activeWorkingLayer)
        if haveBoth:
            self.activeWorkingLayer.setSourceLayer(self.activeSourceLayer)
        self.approveButton.setEnabled(haveBoth)

        # we can upload when we've got an active working layer (might need to check for features later)
        haveWorkingLayer = bool(self.activeWorkingLayer)
        self.uploadButton.setEnabled(haveWorkingLayer)


    def closeEvent(self, event):
        """Handle plug-in close."""
        self.closingPlugin.emit()
        event.accept()
