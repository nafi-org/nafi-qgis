# -*- coding: utf-8 -*-
import os
import os.path as path
from pathlib import Path
from zipfile import ZipFile

from qgis.PyQt.QtCore import QEventLoop, QObject, QUrl
from qgis.core import QgsFileDownloader

from .ntrrp_data_layer import NtrrpDataLayer
from .utils import ensureDirectory, getNtrrpDataUrl, getTempDownloadPath, qgsDebug

class NtrrpDataClient(QObject):

    def __init__(self):
        """Constructor."""
        super(QObject, self).__init__()
        self.dataFile = ""

    def getUrl(self, regionName):
        """Set up the download URL based on the region name."""
        return getNtrrpDataUrl()

    def downloadData(self, regionName):
        """Download, unzip and process remote data file."""
        loop = QEventLoop()
        dataUrl = self.getUrl(regionName)
        dataFile = getTempDownloadPath()
        ensureDirectory(Path(dataFile).parent)
        qgsDebug(f"Data file: {dataFile}")
        
        downloader = QgsFileDownloader(QUrl(dataUrl), dataFile, delayStart=True)
        downloader.downloadProgress.connect(NtrrpDataClient.downloadProgress)
        downloader.downloadError.connect(NtrrpDataClient.downloadError)
        downloader.downloadCompleted.connect(lambda: self.loadData(dataFile))
        downloader.startDownload()

        loop.exec_()

    def loadData(self, dataFile):
        dataPath = Path(dataFile)
        unzipLocation = path.normpath(path.join(dataPath.parent, os.pardir, dataPath.stem))
        
        with ZipFile(dataFile, 'r') as zf:
            zf.extractall(unzipLocation)

        dataLayers = [NtrrpDataLayer(path) for path in Path(unzipLocation).rglob("*.shp")]

        for layer in dataLayers:
            layer.addToMap()

    @staticmethod
    def downloadProgress(bytesReceived, bytesTotal):
        qgsDebug(f"{bytesReceived / float(bytesTotal)}%")

    @staticmethod
    def downloadError(messages):
        qgsDebug(str(messages))
