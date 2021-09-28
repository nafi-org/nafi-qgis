# -*- coding: utf-8 -*-
from urllib import parse

from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSignal, QSortFilterProxyModel, Qt, QModelIndex

from .ntrrp_about_dialog import NtrrpAboutDialog
from .ntrrp_capabilities_reader import NtrrpCapabilitiesReader
from .ntrrp_data_client import NtrrpDataClient
from .ntrrp_dockwidget_base import Ui_NtrrpDockWidgetBase
from .ntrrp_item import NtrrpItem
from .ntrrp_region import NtrrpRegion
from .ntrrp_tree_view_model import NtrrpTreeViewModel
from .utils import getNtrrpWmsUrl, guiInformation, qgsDebug

class NtrrpDockWidget(QtWidgets.QDockWidget, Ui_NtrrpDockWidgetBase):
    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(NtrrpDockWidget, self).__init__(parent)
        
        self.setupUi(self)

        # set up QTreeView        
        self.treeView.setHeaderHidden(True)
        self.treeView.setSortingEnabled(True)
        self.treeView.setFocusPolicy(Qt.NoFocus)
        self.treeView.pressed.connect(self.treeViewPressed)

        # set up About … dialog
        self.aboutButton.clicked.connect(self.showAboutDialog)

        # set up base model
        self.treeViewModel = NtrrpTreeViewModel(getNtrrpWmsUrl())

        # set up proxy model for filtering        
        self.proxyModel = QSortFilterProxyModel(self.treeView)
        self.proxyModel.setSourceModel(self.treeViewModel)
        self.proxyModel.setRecursiveFilteringEnabled(True)
        self.treeView.setModel(self.proxyModel)

        # set up region combobox
        self.regionComboBox.currentIndexChanged.connect(self.regionComboBoxChanged)

        # set up download button
        self.downloadButton.clicked.connect(lambda: self.region.downloadData())

        # set up create button
        self.createButton.clicked.connect(lambda: self.region.createWorkingLayer())

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

        self.regionComboBox.addItems(regions)

        initRegionName = next(iter(self.ntrrpCapabilities.regions))
        initRegion = self.ntrrpCapabilities.regions[initRegionName]

        if initRegion is not None:
            self.setRegion(initRegion)

    def setRegion(self, region):
        """Set the current NTRRP region."""
        if region is None:
            return

        # disconnect signal handlers?
        # if self.region is not None:
        #    try:
        #        self.region.dataLayersChanged.disconnect()
        # …

        # set up signal handlers
        region.dataLayersChanged.connect(lambda dataLayers: self.updateSourceLayerComboBox(dataLayers))
        region.workingLayerCreated.connect(lambda workingLayer: self.updateWorkingLayerComboBox(workingLayer))
        self.region = region
        
        # populate tree view
        self.treeViewModel.setRegion(region)
        
        # set default sort and expansion
        self.proxyModel.sort(0, Qt.AscendingOrder)
        self.expandTopLevel()

    def sizeHint(self):
        return QtCore.QSize(150, 400)

    # handlers    

    def regionComboBoxChanged(self, regionIndex):
        """Switch the active region."""
        regionName = self.regionComboBox.itemText(regionIndex)
        region = self.ntrrpCapabilities.regions.get(regionName, None)

        if region is not None:
            self.setRegion(region)

    def updateSourceLayerComboBox(self, dataLayers):
        """Update the source layers."""
        self.sourceLayerComboBox.clear()
        self.sourceLayerComboBox.addItems([dataLayer.layerName for dataLayer in dataLayers])

    def updateWorkingLayerComboBox(self, workingLayer):
        """Update the source layers."""
        self.workingLayerComboBox.clear()
        self.workingLayerComboBox.addItem(workingLayer.layerName)

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
                self.region.addNtrrpLayer(modelNode)

    def closeEvent(self, event):
        """Handle plug-in close."""
        self.closingPlugin.emit()
        event.accept()
