# -*- coding: utf-8 -*-
from urllib import parse

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, QRegExp, QSortFilterProxyModel, Qt, QModelIndex
from qgis.PyQt.QtGui import QFont, QIcon, QPixmap, QStandardItem, QStandardItemModel 
from qgis.PyQt.QtWidgets import QApplication

from qgis.core import Qgis, QgsRasterLayer, QgsProject

from .ntrrp_about_dialog import NtrrpAboutDialog
from .ntrrp_capabilities import NtrrpCapabilities
from .ntrrp_capabilities_reader import NtrrpCapabilitiesReader
from .ntrrp_data_client import NtrrpDataClient
from .ntrrp_dockwidget_base import Ui_NtrrpDockWidgetBase
from .ntrrp_item import NtrrpItem
from .ntrrp_tree_view_model import NtrrpTreeViewModel
from .utils import getNtrrpWmsUrl, qgsDebug

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
        self.regionComboBox.currentIndexChanged.connect(self.regionChanged)

        # set up download button
        self.dataClient = NtrrpDataClient()
        self.downloadButton.clicked.connect(lambda: self.dataClient.downloadData(self.treeViewModel.region))

        self.reader = NtrrpCapabilitiesReader()
        self.reader.capabilitiesParsed.connect(lambda caps: self.initModel(caps))

        # restore the view from source whenever this dock widget is made visible again
        self.visibilityChanged.connect(lambda visible: visible and self.loadNtrrpWms())

        # initialise proxied tree view model from WMS contents
        self.loadNtrrpWms()

    def loadNtrrpWms(self):
        """Load the NAFI WMS and additional layers."""
        qgsDebug("Calling parseCapabilities")
        self.wmsUrl = getNtrrpWmsUrl()
        self.reader.parseCapabilities(self.wmsUrl)

    def initModel(self, ntrrpCapabilities):
        """Initialise a QStandardItemModel from the NAFI WMS."""
        # stash the parsed capabilities and set up the region combobox
        self.ntrrpCapabilities = ntrrpCapabilities
        self.regionComboBox.clear()
        self.regionComboBox.addItems(ntrrpCapabilities.regions)
        self.treeViewModel.setRegion(ntrrpCapabilities.regions[0], ntrrpCapabilities)

    def expandTopLevel(self):
        # expand the top level items
        for row in range(self.proxyModel.rowCount()):
            self.treeView.expand(self.proxyModel.index(row, 0))

    def treeViewPressed(self, index):
        """Load a NAFI WMS layer given an index in the tree view."""
        assert isinstance(index, QModelIndex), "Supplied parameter is not a QModelIndex"

        realIndex = self.proxyModel.mapToSource(index)
        modelNode = self.treeViewModel.itemFromIndex(realIndex)
       
        # if we've got a layer and not a layer group, add to map
        if modelNode is not None:
            if isinstance(modelNode, NtrrpItem):
                modelNode.addWmtsLayer()

    def regionChanged(self, regionIndex):
        """Switch the active region."""
        self.treeViewModel.setRegion(self.regionComboBox.itemText(regionIndex), self.ntrrpCapabilities)
        # set default sort and expansion
        self.proxyModel.sort(0, Qt.AscendingOrder)
        self.expandTopLevel()        

    def sizeHint(self):
        return QtCore.QSize(150, 400)

    def showAboutDialog(self):
        """Show an About … dialog."""
        aboutDialog = NtrrpAboutDialog()
        aboutDialog.exec_()
    
    def closeEvent(self, event):
        """Handle plug-in close."""
        self.closingPlugin.emit()
        event.accept()
