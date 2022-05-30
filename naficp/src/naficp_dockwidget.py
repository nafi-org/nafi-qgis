# -*- coding: utf-8 -*-
import os

from qgis.core import QgsMapLayerProxyModel
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface as QgsInterface

from .utils import guiError

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui', 'naficp_dockwidget_base.ui'))

NAFICP_MENUNAME = "NAFI Copy and Paste"
NAFICP_HOTKEY = "Ctrl+Z"


class NafiCpDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(NafiCpDockWidget, self).__init__(parent)

        self.setupUi(self)

        # was having trouble getting this to lay out correctly, so have commented for now
        # self.pasteFeaturesButton.setIcon(QIcon(":/plugins/naficp/images/paintbrush.png"))
        # self.pasteFeaturesButton.updateGeometry()

        self.sourceLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.sourceLayerComboBox.setShowCrs(True)

        self.workingLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.workingLayerComboBox.setShowCrs(True)

        self.pasteFeaturesButton.clicked.connect(
            self.copySelectedFeaturesFromSourceLayer)

        self.pasteAction = QAction("Paste Features", QgsInterface.mainWindow())
        QgsInterface.registerMainWindowAction(self.pasteAction, NAFICP_HOTKEY)
        # won't work without calling this method?
        QgsInterface.addPluginToVectorMenu(
            NAFICP_MENUNAME, self.pasteAction)
        self.pasteAction.triggered.connect(
            self.copySelectedFeaturesFromSourceLayer)

    # miscellaneous sanity checks
    def checkLayersSelected(self, sourceLayer, workingLayer):
        if sourceLayer is None or workingLayer is None:
            guiError(
                "You must select both a source layer and a working layer to paste features.")
            return False
        return True

    def checkLayersHaveSameGeometryType(self, sourceLayer, workingLayer):
        if sourceLayer.geometryType() != workingLayer.geometryType():
            guiError(
                "Your source layer and working layer have different geometry types. Please select different layers.")
            return False
        return True

    def checkNotSameLayer(self, sourceLayer, workingLayer):
        if sourceLayer.id() == workingLayer.id():
            guiError(
                "Your source layer is the same as your working layer. Please select different layers.")
            return False
        return True

    def copySelectedFeaturesFromSourceLayer(self):
        """Paste the currently selected features in the source layer into the working layer."""
        sourceLayer = self.sourceLayerComboBox.currentLayer()
        workingLayer = self.workingLayerComboBox.currentLayer()

        if not self.checkLayersSelected(sourceLayer, workingLayer):
            return
        if not self.checkLayersHaveSameGeometryType(sourceLayer, workingLayer):
            return
        if not self.checkNotSameLayer(sourceLayer, workingLayer):
            return

        QgsInterface.setActiveLayer(sourceLayer)
        QgsInterface.actionCopyFeatures().trigger()
        QgsInterface.setActiveLayer(workingLayer)

        # if not currently editing, start editing this layer
        wasEditing = workingLayer.isEditable()
        if not wasEditing:
            workingLayer.startEditing()

        QgsInterface.actionPasteFeatures().trigger()

        # commit the changes, and stop editing if we weren't before
        workingLayer.commitChanges(stopEditing=(not wasEditing))

        QgsInterface.mainWindow().findChild(QAction, 'mActionDeselectAll').trigger()
        QgsInterface.setActiveLayer(sourceLayer)

        # repopulate the clipboard with no features to avoid re-pasting
        QgsInterface.actionCopyFeatures().trigger()

    def closeEvent(self, event):
        nafiCpMenu = next(a for a in QgsInterface.vectorMenu(
        ).actions() if NAFICP_MENUNAME in a.text())
        QgsInterface.vectorMenu().removeAction(nafiCpMenu)
        self.closingPlugin.emit()
        event.accept()