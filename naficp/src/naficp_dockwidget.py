import os
from typing import Any

from qgis.core import QgsMapLayerProxyModel
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface as QgsInterface

from .utils import guiError, guiWarning

FORM_CLASS: Any
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(
        os.path.dirname(__file__), os.pardir, "ui", "naficp_dockwidget_base.ui"
    )
)


class NafiCpDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()

    def __init__(
        self,
        pasteFeaturesHotKey,
        pasteFeaturesAction,
        setActiveLayerAsSourceLayerAction,
        setActiveLayerAsWorkingLayerAction,
        parent=None,
    ):
        super(NafiCpDockWidget, self).__init__(parent)

        self.setupUi(self)

        self.pasteFeaturesHotKey = pasteFeaturesHotKey
        self.pasteFeaturesAction = pasteFeaturesAction
        self.setActiveLayerAsSourceLayerAction = setActiveLayerAsSourceLayerAction
        self.setActiveLayerAsWorkingLayerAction = setActiveLayerAsWorkingLayerAction

        # Was having trouble getting this to lay out correctly, so have commented for now
        # self.pasteFeaturesButton.setIcon(QIcon(":/plugins/naficp/images/paintbrush.png"))
        # self.pasteFeaturesButton.updateGeometry()
        self.pasteFeaturesButton.setText(f"Paste Features ({self.pasteFeaturesHotKey})")

        self.sourceLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.sourceLayerComboBox.setShowCrs(True)

        self.workingLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.workingLayerComboBox.setShowCrs(True)

        self.pasteFeaturesAction.triggered.connect(
            self.copySelectedFeaturesFromSourceLayer
        )
        self.pasteFeaturesButton.clicked.connect(
            self.copySelectedFeaturesFromSourceLayer
        )

        self.setActiveLayerAsSourceLayerAction.triggered.connect(
            self.setActiveLayerAsSourceLayer
        )
        self.setActiveLayerAsWorkingLayerAction.triggered.connect(
            self.setActiveLayerAsWorkingLayer
        )

    # Miscellaneous sanity checks
    def checkLayersSelected(self, sourceLayer, workingLayer):
        if sourceLayer is None or workingLayer is None:
            guiError(
                "You must select both a source layer and a working layer to paste features."
            )
            return False
        return True

    def checkLayersHaveSameGeometryType(self, sourceLayer, workingLayer):
        if sourceLayer.geometryType() != workingLayer.geometryType():
            guiError(
                "Your source layer and working layer have different geometry types. Please select different layers."
            )
            return False
        return True

    def checkNotSameLayer(self, sourceLayer, workingLayer):
        if sourceLayer.id() == workingLayer.id():
            guiError(
                "Your source layer is the same as your working layer. Please select different layers."
            )
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

        # If not currently editing, start editing this layer
        wasEditing = workingLayer.isEditable()
        if not wasEditing:
            workingLayer.startEditing()

        QgsInterface.actionPasteFeatures().trigger()

        # Commit the changes, and stop editing if we weren't before
        workingLayer.commitChanges(stopEditing=(not wasEditing))

        QgsInterface.mainWindow().findChild(QAction, "mActionDeselectAll").trigger()
        QgsInterface.setActiveLayer(sourceLayer)

        # Repopulate the clipboard with no features to avoid re-pasting
        QgsInterface.actionCopyFeatures().trigger()

    def setActiveLayerAsSourceLayer(self):
        """Set the currently active layer as the source layer."""
        guiWarning("Setting active layer as source layer.")

        # activeLayer = QgsInterface.activeLayer()
        # if activeLayer is None:
        #     guiWarning("No active layer to set as source layer.")
        #     return
        # self.sourceLayerComboBox.setCurrentLayer(activeLayer)

    def setActiveLayerAsWorkingLayer(self):
        """Set the currently active layer as the working layer."""
        guiWarning("Setting active layer as working layer.")

        # activeLayer = QgsInterface.activeLayer()
        # if activeLayer is None:
        #     guiWarning("No active layer to set as working layer.")
        #     return
        # self.workingLayerComboBox.setCurrentLayer(activeLayer)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
