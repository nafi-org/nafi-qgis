# -*- coding: utf-8 -*-
import os
import webbrowser
from urllib import parse

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, QRegExp, QSortFilterProxyModel, Qt, QModelIndex
from qgis.PyQt.QtGui import QFont, QIcon, QPixmap, QStandardItem, QStandardItemModel 
from qgis.PyQt.QtWidgets import QApplication

from qgis.core import Qgis, QgsRasterLayer, QgsProject

# from .google_xyz_item import GoogleXyzItem
# from .ibra_wms_item import IbraWmsItem
# from .oz_topo_wmts_item import OzTopoWmtsItem

from .ntrrp_about_dialog import NtrrpAboutDialog
from .nafi_capabilities_reader import NafiCapabilitiesReader
from .ntrrp_dockwidget_base import Ui_NtrrpDockWidgetBase
from .nafi_tree_view_model import NafiTreeViewModel
from .utils import getNafiDataUrl, getNafiUrl, qgsDebug
from .wms_item import WmsItem

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
        
        # set up search signal
        self.lineEdit.textChanged.connect(self.searchTextChanged)
        self.searchText = ""

        # set up clear search
        self.clearSearchButton.clicked.connect(self.clearSearch)

        # set up About … dialog
        self.aboutButton.clicked.connect(self.showAboutDialog)

        # set up Download NAFI data … link button
        self.dataButton.clicked.connect(lambda: webbrowser.open(getNafiDataUrl()))

        # set up base model
        self.treeViewModel = NafiTreeViewModel(getNafiUrl())

        # set up proxy model for filtering        
        self.proxyModel = QSortFilterProxyModel(self.treeView)
        self.proxyModel.setSourceModel(self.treeViewModel)
        self.proxyModel.setRecursiveFilteringEnabled(True)
        self.treeView.setModel(self.proxyModel)

        self.reader = NafiCapabilitiesReader()
        # self.reader.capabilitiesDownloaded.connect(lambda xml: self.initModel(xml))

        # restore the view from source whenever this dock widget is made visible again
        self.visibilityChanged.connect(lambda visible: visible and self.loadNafiWms())

        # initialise proxied tree view model from WMS contents
        # self.loadNafiWms()

    def loadNafiWms(self):
        """Load the NAFI WMS and additional layers."""
        self.wmsUrl = getNafiUrl()
        self.reader.downloadCapabilities(self.wmsUrl)

    def initModel(self, wmsXml):
        """Initialise a QStandardItemModel from the NAFI WMS."""
        googSat = GoogleXyzItem()
        googHyb = GoogleXyzItem("y")
        googStr = GoogleXyzItem("m")
        # ibraWms = IbraWmsItem()
        ozTopoWmts = OzTopoWmtsItem()
        self.treeViewModel.loadWms(self.wmsUrl, wmsXml, additionalItems=[googSat, googHyb, googStr, ozTopoWmts])

        # set default sort and expansion
        self.proxyModel.sort(0, Qt.AscendingOrder)
        self.expandTopLevel()        

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
            if isinstance(modelNode, (GoogleXyzItem, IbraWmsItem, OzTopoWmtsItem, WmsItem)):
                modelNode.addLayer()

    def searchTextChanged(self, text):
        """Process a change in the search filter text."""
        # user adding characters and has exceeded 3 or more, or is removing characters
        if len(text) >= 3 or len(self.searchText) > len(text):
            regex = QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp)
            self.proxyModel.setFilterRegExp(regex)
            self.treeView.expandAll()

        # update last search text state 
        self.searchText = text

    def clearSearch(self):
        """Clear search data."""
        self.lineEdit.setText(None)
        self.treeView.collapseAll()

    def sizeHint(self):
        return QtCore.QSize(150, 400)

    def showAboutDialog(self):
        """Show an About … dialog."""
        aboutDialog = NafiAboutDialog()
        aboutDialog.exec_()
    
    def closeEvent(self, event):
        """Handle plug-in close."""
        self.closingPlugin.emit()
        event.accept()
