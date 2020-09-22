# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 

from owslib.wms import WebMapService
from owslib.map.wms111 import ContentMetadata, WebMapService_1_1_1

from qgis.core import QgsRasterLayer, QgsProject

from .utils import getIbraUrl

class IbraWmsItem(QStandardItem):
    def __init__(self):
        """Constructor."""
        super(QStandardItem, self).__init__()

        ibra = WebMapService(getIbraUrl())
        ibraOwsLayer = ibra.contents["IBRA7 subregions"]

        self.wmsUrl = getIbraUrl()       
        self.setFlags(Qt.ItemIsEnabled)
        self.setText(ibraOwsLayer.title)
        self.owsLayer = ibraOwsLayer
        self.setIcon(QIcon(":/plugins/nafi/globe.png"))
        
    def createLayer(self):
        """Create a QgsRasterLayer from WMS given an OWS ContentMetadata object."""
        # weirdly true that URL-encoding of the layer ID does not work correctly
        encodedLayer = self.owsLayer.id.replace(" ","%20")
        # this should create "EPSG:28350" for Map Grid of Australia, "EPSG:4326" for WGS84 etc
        encodedSrsId = f"EPSG:{QgsProject.instance().crs().postgisSrid()}"
        wmsParams = f"crs={encodedSrsId}&format=image/png&layers={encodedLayer}&styles&url={self.wmsUrl}"
        wmsLayer = QgsRasterLayer(wmsParams, self.owsLayer.title, "wms")
        return wmsLayer

