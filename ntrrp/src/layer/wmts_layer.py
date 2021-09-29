# -*- coding: utf-8 -*-
from qgis.core import QgsProject, QgsRasterLayer

from .abstract_layer import AbstractLayer
from ..utils import getNtrrpWmtsUrl, guiError, setDefaultProjectCrs

class WmtsLayer(AbstractLayer):
    def __init__(self, wmsUrl, owsLayer, item):
        """Constructor."""

        self.wmsUrl = wmsUrl       
        self.owsLayer = owsLayer

        # TODO this is a bit inelegant
        self.item = item

    def getSubGroupLayer(self, groupLayer):
        return groupLayer

    def addMapLayer(self, groupLayer):
        """Create a QgsRasterLayer from WMTS given an OWS ContentMetadata object."""
        # only create a WMTS layer from a child
        # NtrrpItem keeps a reference to any active QgsMapLayer in order to avoid being added twice
        if not self.owsLayer.children and self.item.mapLayerId is None:
            project = QgsProject.instance()
            # weirdly true that URL-encoding of the layer ID does not work correctly
            encodedLayer = self.owsLayer.id.replace(" ","%20")

            # set the project CRS to Australian Albers (EPSG 3577) whenever an NTRRP WMTS layer is added
            srsId = project.crs().postgisSrid()
            if srsId != 3577:
                setDefaultProjectCrs(project)

            wmtsUrl = getNtrrpWmtsUrl()
            wmtsParams = f"crs=EPSG:3577&format=image/png&layers={encodedLayer}&url={wmtsUrl}&styles&tileMatrixSet=EPSG:3577"

            wmtsLayer = QgsRasterLayer(wmtsParams, self.getMapLayerName(), "wms")

            if wmtsLayer is not None and wmtsLayer.isValid():
                wmtsLayer = project.addMapLayer(wmtsLayer, False)
                self.item.linkLayer(wmtsLayer)

                subGroupLayer = self.getSubGroupLayer(groupLayer)
                subGroupLayer.addLayer(wmtsLayer)
                
                # don't show legend initially
                displayLayer = project.layerTreeRoot().findLayer(wmtsLayer)
                displayLayer.setExpanded(False)
            else:
                error = (f"An error occurred adding the layer {self.getMapLayerName()} to the map.\n"
                         f"Check your QGIS WMS message log for details.")
                guiError(error)

    def addWmsMapLayer(self, groupLayer):
        """Create a QgsRasterLayer from WMS given an OWS ContentMetadata object."""
        # only create a WMS layer from a child
        # NtrrpItem keeps a reference to any active QgsMapLayer in order to avoid being added twice
        if not self.owsLayer.children and self.item.mapLayerId is None:
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
            wmsLayer = QgsRasterLayer(wmsParams, self.getMapLayerName(), "wms")

            if wmsLayer is not None and wmsLayer.isValid():
                wmsLayer = project.addMapLayer(wmsLayer, False)
                self.item.linkLayer(wmsLayer)

                subGroupLayer = self.getSubGroupLayer(groupLayer)
                subGroupLayer.addLayer(wmsLayer)
                
                # don't show legend initially
                displayLayer = subGroupLayer.findLayer(wmsLayer)
                displayLayer.setExpanded(False)
            else:
                error = (f"An error occurred adding the layer {self.getMapLayerName()} to the map.\n"
                         f"Check your QGIS WMS message log for details.")
                guiError(error)

    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        return self.owsLayer.title

    def getMapLayer(self, groupLayer = None):
        """Get the QGIS map layer corresponding to this layer, if any."""
        if groupLayer is None:
            groupLayer = QgsProject.instance().layerTreeRoot()

        return self.getSubGroupLayer(groupLayer).findLayer(self.getMapLayerName())

