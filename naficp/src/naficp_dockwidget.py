# -*- coding: utf-8 -*-
import os

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsMapLayerProxyModel
from qgis.utils import iface as QgsInterface

from .utils import guiError, guiWarning
from ..resources_rc import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), os.pardir, 'ui', 'naficp_dockwidget_base.ui'))


class NafiCpDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(NafiCpDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # self.pasteFeaturesButton.setIcon(QIcon(":/plugins/naficp/images/paintbrush.png"))
        # self.pasteFeaturesButton.updateGeometry()

        self.sourceLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.sourceLayerComboBox.setShowCrs(True)

        self.workingLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.workingLayerComboBox.setShowCrs(True)

        self.pasteFeaturesButton.clicked.connect(self.copySelectedFeaturesFromSourceLayer)

        self.pasteAction = QAction("Paste Features", QgsInterface.mainWindow())
        QgsInterface.registerMainWindowAction(self.pasteAction, "Ctrl+Z")  
        # won't work without calling this method?
        QgsInterface.addPluginToVectorMenu("NAFI Copy and Paste", self.pasteAction)
        self.pasteAction.triggered.connect(self.copySelectedFeaturesFromSourceLayer)

    # miscellaneous sanity checks
    def checkLayersSelected(self, sourceLayer, workingLayer):
        if sourceLayer is None or workingLayer is None:
            guiError("You must select both a source layer and a working layer to paste features.")
            return False
        return True

    def checkLayersHaveSameGeometryType(self, sourceLayer, workingLayer):
        if sourceLayer.geometryType() != workingLayer.geometryType():
            guiError("Your source layer and working layer have different geometry types. Please select different layers.")
            return False
        return True

    def checkNotSameLayer(self, sourceLayer, workingLayer):
        if sourceLayer.id() == workingLayer.id():
            guiError("Your source layer is the same as your working layer. Please select different layers.")
            return False
        return True

    def copySelectedFeaturesFromSourceLayer(self):
        """Add the currently selected features in the source layer to this working layer."""
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
        QgsInterface.removePluginVectorMenu("NAFI Copy and Paste", self.pasteAction)
        self.closingPlugin.emit()
        event.accept()
