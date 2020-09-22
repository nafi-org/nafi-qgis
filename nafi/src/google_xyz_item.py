# -*- coding: utf-8 -*-
import requests

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 

from qgis.core import QgsProject, QgsRasterLayer

from .utils import guiError

LABELS = { "s": "Satellite",
           "m": "Streets",
           "y": "Hybrid" }

class GoogleXyzItem(QStandardItem):

    def __init__(self, googleMapType="s"):
        """Constructor."""
        super(QStandardItem, self).__init__()

        # y - hybrid
        # s - satellite (default)
        # m - road map
        self.googleMapType = googleMapType
        self.setFlags(Qt.ItemIsEnabled)
        self.setText(f"Google {LABELS[googleMapType]}")
        self.setIcon(QIcon(":/plugins/nafi/images/globe.png"))
        
    def addLayer(self):
        """Create a QgsRasterLayer from Google XYZ tiles."""
        # See https://gis.stackexchange.com/questions/270871/adding-google-maps-with-pyqgis

        googUrl = f"mt1.google.com/vt/lyrs={self.googleMapType}&x={{x}}&y={{y}}&z={{z}}" 
        googParams = f"type=xyz&zmin=0&zmax=21&url=https://{requests.utils.quote(googUrl)}"

        title = f"Google {LABELS[self.googleMapType]}"
        tmsLayer = QgsRasterLayer(googParams, title, "wms")

        if tmsLayer is not None and tmsLayer.isValid():
            QgsProject.instance().addMapLayer(tmsLayer)
        else:
            error = (f"An error occurred adding the layer title to the map.\n"
                     f"Check your QGIS WMS message log for details.")
            guiError(error)
