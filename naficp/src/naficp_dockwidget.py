# -*- coding: utf-8 -*-
import os

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsMapLayerProxyModel
from qgis.utils import iface as QgsInterface

from .utils import guiError

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

        self.pasteFeaturesButton.setIcon(QIcon(":/plugins/naficp/images/approve.png"))

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


    def copySelectedFeaturesFromSourceLayer(self):
        """Add the currently selected features in the source layer to this working layer."""
        sourceLayer = self.sourceLayerComboBox.currentLayer()
        workingLayer = self.workingLayerComboBox.currentLayer()

        if sourceLayer is None:
            guiError("Error occurred: no source layer selected.")
        if workingLayer is None:
            guiError("Error occurred: no working layer selected.")
        else:
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
