# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject
from qgis.core import QgsProject, QgsRasterLayer

from .abstract_layer import AbstractLayer
from ..ows_utils import parseNtrrpLayerDescription
from ..utils import getNtrrpWmtsUrl, guiError, setDefaultProjectCrs


class WmtsLayer(QObject, AbstractLayer):
    def __init__(self, region, mappingDate, wmsUrl, owsLayer):
        """Constructor."""
        QObject.__init__(self)
        AbstractLayer.__init__(self)
        self.region = region
        self.mappingDate = mappingDate
        
        self.wmsUrl = wmsUrl
        self.owsLayer = owsLayer
        self.mapLayerId = None
        self.impl = None
        
    def addMapLayer(self):
        """Create a QgsRasterLayer from WMTS given an OWS ContentMetadata object."""
        # only create a WMTS layer from a child
        # NtrrpItem keeps a reference to any active QgsMapLayer in order to avoid being added twice
        if not self.owsLayer.children and self.mapLayerId is None:
            project = QgsProject.instance()
            # weirdly true that URL-encoding of the layer ID does not work correctly
            encodedLayer = self.owsLayer.id.replace(" ", "%20")

            # set the project CRS to Australian Albers (EPSG 3577) whenever an NTRRP WMTS layer is added
            srsId = project.crs().postgisSrid()
            if srsId != 3577:
                setDefaultProjectCrs(project)

            wmtsUrl = getNtrrpWmtsUrl()
            wmtsParams = f"crs=EPSG:3577&format=image/png&layers={encodedLayer}&url={wmtsUrl}&styles&tileMatrixSet=EPSG:3577"

            self.impl = QgsRasterLayer(
                wmtsParams, self.getMapLayerName(), "wms")

            if self.impl is not None and self.impl.isValid():
                self.impl = project.addMapLayer(self.impl, False)
                self.impl.willBeDeleted.connect(
                    lambda: self.layerRemoved.emit(self))
                self.layerAdded.emit(self)
                self.mapLayerId = self.impl.id()

                subGroupLayer = self.getSubGroupLayerItem()
                subGroupLayer.addLayer(self.impl)

                # don't show legend initially
                displayLayer = project.layerTreeRoot().findLayer(self.impl)
                displayLayer.setExpanded(True)
                displayLayer.setExpanded(False)
            else:
                error = (f"An error occurred adding the layer {self.getMapLayerName()} to the map.\n"
                         f"Check your QGIS WMS message log for details.")
                guiError(error)

    # def addWmsMapLayer(self, groupLayer):
    #     """Create a QgsRasterLayer from WMS given an OWS ContentMetadata object."""
    #     # only create a WMS layer from a child
    #     # NtrrpItem keeps a reference to any active QgsMapLayer in order to avoid being added twice
    #     if not self.owsLayer.children and self.mapLayerId is None:
    #         project = QgsProject.instance()

    #         # weirdly true that URL-encoding of the layer ID does not work correctly
    #         encodedLayer = self.owsLayer.id.replace(" ","%20")

    #         # this call should get "28350" for Map Grid of Australia, "4326" for WGS84 etc
    #         # make sure we've got a project CRS before proceeding further
    #         srsId = project.crs().postgisSrid()
    #         if srsId == 0:
    #             setDefaultProjectCrs(project)
    #             srsId = project.crs().postgisSrid()

    #         wmsParams = f"crs=EPSG:{srsId}&format=image/png&layers={encodedLayer}&styles&url={self.wmsUrl}"
    #         wmsLayer = QgsRasterLayer(wmsParams, self.getMapLayerName(), "wms")

    #         if wmsLayer is not None and wmsLayer.isValid():
    #             wmsLayer = project.addMapLayer(wmsLayer, False)
    #             wmsLayer.willBeDeleted.connect(lambda: self.layerRemoved.emit(wmsLayer))
    #             self.layerAdded.emit(wmsLayer)
    #             self.mapLayerId = wmsLayer.id()

    #             subGroupLayer = self.getSubGroupLayerItem(groupLayer)
    #             subGroupLayer.addLayer(wmsLayer)

    #             # don't show legend initially
    #             displayLayer = subGroupLayer.findLayer(wmsLayer)
    #             displayLayer.setExpanded(False)
    #         else:
    #             error = (f"An error occurred adding the layer {self.getMapLayerName()} to the map.\n"
    #                      f"Check your QGIS WMS message log for details.")
    #             guiError(error)

    def getMapLayerName(self):
        """Get an appropriate map layer name for this layer."""
        return parseNtrrpLayerDescription(self.owsLayer.title)

    # def getMapLayer(self, groupLayer=None):
    #     """Get the QGIS map layer corresponding to this layer, if any."""

    #     matches = QgsProject.instance().mapLayersByName(self.getMapLayerName())
    #     return matches and matches[0]
