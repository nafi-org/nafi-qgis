
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsProject

from .ntrrp_data_client import NtrrpDataClient
from .ntrrp_data_layer import NtrrpDataLayer
from .ntrrp_item import NtrrpItem
from .ntrrp_working_layer import NtrrpWorkingLayer
from .utils import getNtrrpDataUrl, guiWarning

class NtrrpRegion(QObject):
     # emit this signal with the downloaded data layers
    dataLayersChanged = pyqtSignal(list)
    
    # emit this signal with the created working layer
    workingLayerCreated = pyqtSignal(NtrrpWorkingLayer)

    def __init__(self, region, wmsUrl, owsLayers):
        """Constructor."""
        super(QObject, self).__init__()

        self.name = region
        self.wmsUrl = wmsUrl
        self.owsLayers = owsLayers
        self.dataLayers = []
        self.workingLayer = None
        self.regionGroup = f"{self.name} Burnt Areas"

    # arrange data
    def getNtrrpItems(self):
        """Return a set of NtrrpItem objects corresponding to this region's layers."""
        return [NtrrpItem(self.wmsUrl, owsLayer) for owsLayer in self.owsLayers]
    
    def getDataUrl(self):
        """Get the distinctive URL used for the data layers for this region."""
        return getNtrrpDataUrl()

    def downloadData(self):
        client = NtrrpDataClient()
        client.dataDownloaded.connect(lambda unzipLocation: self.addDataLayers(unzipLocation))
        client.downloadData(self.getDataUrl())

    # add things to the map
    def getSubGroupLayer(self):
        """Get or create the right layer group for an NTRRP data layer."""
        root = QgsProject.instance().layerTreeRoot()
        groupLayer = root.findGroup(self.regionGroup)
        if groupLayer == None:
            root.insertGroup(0, self.regionGroup)
            groupLayer = root.findGroup(self.regionGroup)
        return groupLayer
    
    def createWorkingLayer(self):
        """Create a new working layer for this region."""
        self.workingLayer = NtrrpWorkingLayer()
        self.workingLayer.addMapLayer(self.getSubGroupLayer())
        self.workingLayerCreated.emit(self.workingLayer)

    def addDataLayers(self, unzipLocation):
        """Add all shapefiles in a directory as data layers to the region group."""
        self.dataLayers = [NtrrpDataLayer(path) for path in unzipLocation.rglob("*.shp")]

        for dataLayer in self.dataLayers:
            dataLayer.addMapLayer(self.getSubGroupLayer())

        self.dataLayersChanged.emit(self.dataLayers)

    def addNtrrpLayer(self, item):
        """Add an NTRRP remote layer for this region to the map."""
        assert(isinstance(item, NtrrpItem))

        item.addMapLayer(self.getSubGroupLayer())

    # upload data
    def uploadData(self):
        """Upload the curated working layer to NAFI."""
        guiWarning("Upload under construction!")