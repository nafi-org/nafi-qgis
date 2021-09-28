# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QStandardItem 

from qgis.core import QgsProject, QgsRasterLayer

from .ows_utils import parseNtrrpLayerDescription, parseNtrrpLayerRegion
from .utils import getNtrrpWmtsUrl, guiError, setDefaultProjectCrs

class NtrrpItem(QStandardItem):
    def __init__(self, wmsUrl, owsLayer):
        """Constructor."""
        super(QStandardItem, self).__init__()

        self.unsetLayer()
        
        # assemble some properties
        self.wmsUrl = wmsUrl       
        self.owsLayer = owsLayer
        self.region = parseNtrrpLayerRegion(owsLayer)
        self.description = parseNtrrpLayerDescription(owsLayer)

        self.setText(self.description)

        self.setFlags(Qt.ItemIsEnabled)
        self.setCheckable(False)

        self.restoreLayer()

    def unsetLayer(self):
        self.setIcon(QIcon(":/plugins/ntrrp/images/globe.png"))
        self.mapLayerId = None

    def restoreLayer(self):
        """Check if a layer is in the map already and set its icon if it is."""
        # Python idiom to get first or None
        layer = next(iter(QgsProject.instance().mapLayersByName(self.owsLayer.title)), None)
        if layer is not None and isinstance(layer, QgsRasterLayer):
            self.linkLayer(layer)

    def linkLayer(self, layer):
        """Associate this WMS item with an active map layer."""
        self.setIcon(QIcon(":/plugins/ntrrp/images/fire.png"))
        self.mapLayerId = layer.id()
        layer.willBeDeleted.connect(self.unsetLayer)

    def getSubGroupLayer(self, groupLayer):
        return groupLayer

    def addMapLayer(self, groupLayer):
        """Create a QgsRasterLayer from WMTS given an OWS ContentMetadata object."""
        # only create a WMTS layer from a child
        # NtrrpItem keeps a reference to any active QgsMapLayer in order to avoid being added twice
        if not self.owsLayer.children and self.mapLayerId is None:
            project = QgsProject.instance()
            # weirdly true that URL-encoding of the layer ID does not work correctly
            encodedLayer = self.owsLayer.id.replace(" ","%20")

            # set the project CRS to Australian Albers (EPSG 3577) whenever an NTRRP WMTS layer is added
            srsId = project.crs().postgisSrid()
            if srsId != 3577:
                setDefaultProjectCrs(project)

            wmtsUrl = getNtrrpWmtsUrl()
            wmtsParams = f"crs=EPSG:3577&format=image/png&layers={encodedLayer}&url={wmtsUrl}&styles&tileMatrixSet=EPSG:3577"

            wmtsLayer = QgsRasterLayer(wmtsParams, self.owsLayer.title, "wms")

            if wmtsLayer is not None and wmtsLayer.isValid():
                wmtsLayer = project.addMapLayer(wmtsLayer, False)
                self.linkLayer(wmtsLayer)

                subGroupLayer = self.getSubGroupLayer(groupLayer)
                subGroupLayer.addLayer(wmtsLayer)
                
                # don't show legend initially
                displayLayer = project.layerTreeRoot().findLayer(wmtsLayer)
                displayLayer.setExpanded(False)
            else:
                error = (f"An error occurred adding the layer {self.owsLayer.title} to the map.\n"
                         f"Check your QGIS WMS message log for details.")
                guiError(error)

    def addWmsMapLayer(self, groupLayer):
        """Create a QgsRasterLayer from WMS given an OWS ContentMetadata object."""
        # only create a WMS layer from a child
        # NtrrpItem keeps a reference to any active QgsMapLayer in order to avoid being added twice
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
                wmsLayer = project.addMapLayer(wmsLayer, False)
                self.linkLayer(wmsLayer)

                subGroupLayer = self.getSubGroupLayer(groupLayer)
                subGroupLayer.addLayer(wmsLayer)
                
                # don't show legend initially
                displayLayer = project.layerTreeRoot().findLayer(wmsLayer)
                displayLayer.setExpanded(False)
            else:
                error = (f"An error occurred adding the layer {self.owsLayer.title} to the map.\n"
                         f"Check your QGIS WMS message log for details.")
                guiError(error)

