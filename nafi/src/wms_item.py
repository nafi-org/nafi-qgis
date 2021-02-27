# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 
from owslib.map.wms111 import ContentMetadata, WebMapService_1_1_1

from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsRasterLayer

from .utils import guiError, guiWarning, setDefaultProjectCrs

class WmsItem(QStandardItem):
    def __init__(self, wmsUrl, owsLayer):
        """Constructor."""
        super(QStandardItem, self).__init__()

        assert isinstance(owsLayer, ContentMetadata)

        self.unsetLayer()
        
        self.wmsUrl = wmsUrl       
        self.setFlags(Qt.ItemIsEnabled)
        self.setText(owsLayer.title)
        self.owsLayer = owsLayer
        self.setCheckable(False)

        if owsLayer.children: 
            self.setIcon(QIcon(":/plugins/nafi/images/folder.png"))
        else:
            self.setIcon(QIcon(":/plugins/nafi/images/globe.png"))
            self.restoreLayer()

    def unsetLayer(self):
        self.setIcon(QIcon(":/plugins/nafi/images/globe.png"))
        self.mapLayerId = None

    def restoreLayer(self):
        """Check if a layer is in the map already and set its icon if it is."""
        # Python idiom to get first or None
        layer = next(iter(QgsProject.instance().mapLayersByName(self.owsLayer.title)), None)
        if layer is not None and isinstance(layer, QgsRasterLayer):
            self.linkLayer(layer)

    def linkLayer(self, layer):
        """Associate this WMS item with an active map layer."""
        self.setIcon(QIcon(":/plugins/nafi/images/fire.png"))
        self.mapLayerId = layer.id()
        layer.willBeDeleted.connect(self.unsetLayer)

    def addLayer(self):
        """Create a QgsRasterLayer from WMS given an OWS ContentMetadata object."""
        # only create a WMS layer from a child WmsItem
        # WmsItem keeps a reference to any active QgsMapLayer in order to avoid being added twice
        if not self.owsLayer.children and self.mapLayerId is None:
            project = QgsProject.instance()
            
            # weirdly true that URL-encoding of the layer ID does not work correctly
            encodedLayer = self.owsLayer.id.replace(" ","%20")

            # this call should get "28350" for Map Grid of Australia, "4326" for WGS84 etc
            # make sure we've got a project CRS before proceeding further
            srsId = project.crs().postgisSrid()
            if srsId == 0:
                setDefaultProjectCrs(project)
                srsId = project.crs().postgisSrid()

            wmsParams = f"crs=EPSG:{srsId}&format=image/png&layers={encodedLayer}&styles&url={self.wmsUrl}"
            wmsLayer = QgsRasterLayer(wmsParams, self.owsLayer.title, "wms")

            if wmsLayer is not None and wmsLayer.isValid():
                wmsLayer = project.addMapLayer(wmsLayer)
                self.linkLayer(wmsLayer) 
                
                # don't show legend initially
                displayLayer = project.layerTreeRoot().findLayer(wmsLayer)
                displayLayer.setExpanded(False)
            else:
                error = (f"An error occurred adding the layer {self.owsLayer.title} to the map.\n"
                         f"Check your QGIS WMS message log for details.")
                guiError(error)
