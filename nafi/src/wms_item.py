# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 
from owslib.map.wms111 import ContentMetadata, WebMapService_1_1_1

from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsRasterLayer

from .utils import guiError, guiWarning

class WmsItem(QStandardItem):
    def __init__(self, wmsUrl, owsLayer):
        """Constructor."""
        super(QStandardItem, self).__init__()

        assert isinstance(owsLayer, ContentMetadata)

        self.wmsUrl = wmsUrl
        self.setFlags(Qt.ItemIsEnabled)
        self.setText(owsLayer.title)
        self.owsLayer = owsLayer
        self.mapLayerId = None
        self.setCheckable(False)

        if owsLayer.children: 
            self.setIcon(QIcon(":/plugins/nafi/images/folder.png"))
        else:
            self.setIcon(QIcon(":/plugins/nafi/images/globe.png"))
        
        self.removeLayer()

    def removeLayer(self):
        self.mapLayerId = None

    @staticmethod
    def setDefaultProjectCrs():
        """Set the Project CRS to the default value of GDA94 geographic."""
        gda94 = QgsCoordinateReferenceSystem("EPSG:4283")
        warning = (f"Because no QGIS project CRS was set, a default coordinate system of "
                   f"{gda94.userFriendlyIdentifier()} has been applied to interact with "
                   f"NAFI map services.")

        guiWarning(warning)
        QgsProject.instance().setCrs(gda94)

    def addLayer(self):
        """Create a QgsRasterLayer from WMS given an OWS ContentMetadata object."""
        # only create a WMS layer from a child WmsItem
        # WmsItem keeps a reference to any active QgsMapLayer in order to avoid being added twice
        if not self.owsLayer.children and self.mapLayerId is None:
            # weirdly true that URL-encoding of the layer ID does not work correctly
            encodedLayer = self.owsLayer.id.replace(" ","%20")

            # this should create "EPSG:28350" for Map Grid of Australia, "EPSG:4326" for WGS84 etc
            srsId = QgsProject.instance().crs().postgisSrid()

            # Make sure we've got a project CRS before proceeding further
            if srsId == 0:
                WmsItem.setDefaultProjectCrs()
                srsId = QgsProject.instance().crs().postgisSrid()

            wmsParams = f"crs=EPSG:{srsId}&format=image/png&layers={encodedLayer}&styles&url={self.wmsUrl}"
            wmsLayer = QgsRasterLayer(wmsParams, self.owsLayer.title, "wms")

            if wmsLayer is not None and wmsLayer.isValid():
                wmsLayer = QgsProject.instance().addMapLayer(wmsLayer)
                self.mapLayerId = wmsLayer.id()
                wmsLayer.willBeDeleted.connect(self.removeLayer)
                # Don't show legend initially
                displayLayer = QgsProject.instance().layerTreeRoot().findLayer(wmsLayer)
                displayLayer.setExpanded(False)
            else:
                error = (f"An error occurred adding the layer {self.owsLayer.title} to the map.\n"
                         f"Check your QGIS WMS message log for details.")
                guiError(error)
