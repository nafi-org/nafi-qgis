# -*- coding: utf-8 -*-
from pathlib import Path
from zipfile import ZipFile
import os
import random
import string

from qgis.PyQt.QtCore import pyqtSignal, QEventLoop, QObject, QUrl

from qgis.core import QgsFileDownloader

from .ntrrp_data_layer import NtrrpDataLayer
from .utils import qgsDebug

class NtrrpDataClient(QObject):

    # dataAdded = pyqtSignal(QObject)
    def __init__(self):
        """Constructor."""
        super(QObject, self).__init__()
        self.dataFile = ""

    def getUrl(self, regionName):
        """Set up the download URL based on the region name."""
        return f"https://test.firenorth.org.au/ntrrp/downloads/drw/area1.zip"

    def downloadData(self, regionName):
        """Download, unzip and process remote data file."""
        loop = QEventLoop()
        dataUrl = self.getUrl(regionName)
        randFilename = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
        unzipLocation = f"{os.environ['TMP']}\\ntrrp\\{randFilename}"
        dataFile = f"{unzipLocation}.zip"
        qgsDebug(f"Data file: {dataFile}")
        downloader = QgsFileDownloader(QUrl(dataUrl), dataFile, delayStart=True)
        downloader.downloadProgress.connect(NtrrpDataClient.downloadProgress)
        downloader.downloadError.connect(NtrrpDataClient.downloadError)
        downloader.downloadCompleted.connect(lambda: self.loadData(dataFile, unzipLocation))

        downloader.startDownload()

        loop.exec_()

    def loadData(self, dataFile, unzipLocation):
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
