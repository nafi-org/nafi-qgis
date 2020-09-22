# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 
from owslib.map.wms111 import ContentMetadata, WebMapService_1_1_1

from qgis.core import QgsRasterLayer, QgsProject

class WmsItem(QStandardItem):
    def __init__(self, wmsUrl, owsLayer):
        """Constructor."""
        super(QStandardItem, self).__init__()

        assert isinstance(owsLayer, ContentMetadata)

        self.wmsUrl = wmsUrl       
        self.setFlags(Qt.ItemIsEnabled)
        self.setText(owsLayer.title)
        self.owsLayer = owsLayer
        
        if owsLayer.children: 
            self.setIcon(QIcon(":/plugins/nafi/folder.png"))
        else:
            self.setIcon(QIcon(":/plugins/nafi/globe.png"))
        
    def createLayer(self):
        """Create a QgsRasterLayer from WMS given an OWS ContentMetadata object."""
        # only create a WMS layer from a child WmsItem
        if not self.owsLayer.children:
            # weirdly true that URL-encoding of the layer ID does not work correctly
            encodedLayer = self.owsLayer.id.replace(" ","%20")
            # this should create "EPSG:28350" for Map Grid of Australia, "EPSG:4326" for WGS84 etc
            encodedSrsId = f"EPSG:{QgsProject.instance().crs().postgisSrid()}"
            wmsParams = f"crs={encodedSrsId}&format=image/png&layers={encodedLayer}&styles&url={self.wmsUrl}"
            wmsLayer = QgsRasterLayer(wmsParams, self.owsLayer.title, "wms")
            return wmsLayer
        else:
            return None

