import os
from typing import Any

from qgis.PyQt import uic
from qgis.PyQt.QtCore import QModelIndex, QSize, QSortFilterProxyModel, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QDockWidget

from nafi_hires.src.models import Mapping, Project, Region, WorkspaceMetadata
from nafi_hires.src.services import MappingService, WorkspaceMetadataService
from nafi_hires.src.utils import getRemoteWorkspaceUrl

from .workspace_layer_item import WorkspaceLayerItem
from .workspace_tree_view_model import WorkspaceTreeViewModel

FORM_CLASS: Any
FORM_CLASS, _ = uic.loadUiType(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "dock_widget.ui"))
)


class DockWidget(QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        super(DockWidget, self).__init__(parent)

        self._region: Region = None
        self._mapping: Mapping = None
        self._project: Project = None

        self.setupUi(self)

        # Set up QTreeView
        self.treeView.setHeaderHidden(True)
        self.treeView.setSortingEnabled(True)
        self.treeView.setFocusPolicy(Qt.NoFocus)
        self.treeView.pressed.connect(self.treeViewPressed)

        # Set up base model
        self.treeViewModel = WorkspaceTreeViewModel(getRemoteWorkspaceUrl())

        # Set up proxy model for filtering
        self.proxyModel = QSortFilterProxyModel(self.treeView)
        self.proxyModel.setSourceModel(self.treeViewModel)
        self.proxyModel.setRecursiveFilteringEnabled(True)
        self.treeView.setModel(self.proxyModel)

        self.workspaceService = WorkspaceMetadataService()
        self.workspaceService.workspaceMetadataParsed.connect(self.initProject)

        # Restore the view from source whenever this dock widget is made visible again
        self.visibilityChanged.connect(
            lambda visible: visible and self.refreshRemoteWorkspace()
        )

        self.refreshRemoteWorkspace()

        # Set up comboboxes
        self.regionComboBox.currentIndexChanged.connect(self.regionComboBoxChanged)
        self.mappingComboBox.currentIndexChanged.connect(self.mappingComboBoxChanged)

    def region(self) -> Region:
        return self._region

    def setRegion(self, region: Region) -> None:
        """Set the current region."""
        if region is None:
            return

        # Do not set region if it is already set to the same one
        if self._region is not None and self._region.isSame(region):
            return

        self._region = region
        self.regionComboBox.setCurrentText(self._region.regionName())

        # Update mapping combo box
        self.mappingComboBox.clear()
        self.mappingComboBox.addItems(self._region.mappingNames())

        # Populate tree view
        self.treeViewModel.setRegion(self._region)
        # Set default sort and expansion
        self.proxyModel.sort(0, Qt.AscendingOrder)
        self.expandTreeViewTopLevel()

        # Set first mapping in the region (if any)
        self.setMapping(next(iter(self._region.mappings()), None))

        # Update item visibility in the map and layers panel
        self.updateItemVisibilities()

    def mapping(self) -> Mapping:
        return self.mappingWidget.mapping()

    def setMapping(self, mapping: Mapping) -> None:
        """Set the current mapping."""
        if mapping is None:
            return

        # Do not set mapping if it is already set to the same one
        if self.mapping() is not None and self.mapping().isSame(mapping):
            return

        self.mappingWidget.setMapping(mapping)
        self.mappingWidget.updateToolBar()

        # Update item visibility in the map and layers panel
        self.updateItemVisibilities()

    def initProject(self, workspaceMetadata: WorkspaceMetadata):
        """Initialise a QStandardItemModel from the remtoe workspace."""
        # Stash the parsed capabilities and set up the mapping combobox

        self._project = Project(workspaceMetadata)

        mappingService = MappingService()
        for mapping in self._project.mappings():
            mappingService.addMappingLayers(mapping)

        self.regionComboBox.clear()
        self.regionComboBox.addItems(self._project.regionNames())

        self.setRegion(next(iter(self._project.regions())))

    def refreshCurrentRegion(self):
        """Refresh the current region."""
        if self.region() is not None:
            self.setRegion(self.region())

    def refreshRemoteWorkspace(self):
        """(Re)load the workspace layers."""
        self.wmsUrl = getRemoteWorkspaceUrl()
        self.workspaceService.downloadAndParseWorkspaceMetadata(self.wmsUrl)

    def updateItemVisibilities(self):
        """Update the visibility of the region and mapping items basd on the current mapping."""
        for region in self._project.regions():
            region.setVisibilityChecked(region.isSame(self.region()))
            for mapping in region.mappings():
                mapping.setVisibilityChecked(mapping.isSame(self.mapping()))

    def expandTreeViewTopLevel(self):
        """Expand top level items in the tree view."""
        for row in range(self.proxyModel.rowCount()):
            self.treeView.expand(self.proxyModel.index(row, 0))

    def sizeHint(self):
        return QSize(150, 400)

    def treeViewPressed(self, index: QModelIndex) -> None:
        """Load a workspace layer given an index in the tree view."""
        realIndex = self.proxyModel.mapToSource(index)
        item: WorkspaceLayerItem = self.treeViewModel.itemFromIndex(realIndex)

        # If we've got a layer and not a layer group, add to map
        if item is not None:
            item.itemLayer.addMapLayer()
            self.treeViewModel.refresh()

    def regionComboBoxChanged(self, regionIndex):
        if regionIndex < 0:
            self.setRegion(None)
            return
        regionName = self.regionComboBox.itemText(regionIndex)
        self.setRegion(self._project.regionByName(regionName))

    def mappingComboBoxChanged(self, mappingIndex):
        if mappingIndex < 0:
            self.setMapping(None)
            return
        mappingName = self.mappingComboBox.itemText(mappingIndex)
        self.setMapping(self.region().mappingByName(mappingName))

    def closeEvent(self, event):
        """Handle plug-in close."""
        self.closingPlugin.emit()
        event.accept()
