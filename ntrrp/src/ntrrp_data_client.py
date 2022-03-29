# -*- coding: utf-8 -*-
import os
import os.path as path
from pathlib import Path
from zipfile import ZipFile

from qgis.PyQt.QtCore import QEventLoop, QObject, QUrl, pyqtSignal
from qgis.core import QgsFileDownloader

from .utils import ensureDirectory, getNtrrpDataUrl, getTempDownloadPath, qgsDebug


class NtrrpDataClient(QObject):
    # emit this signal with the downloaded data
    dataDownloaded = pyqtSignal(Path)

    def __init__(self):
        """Constructor."""
        super(QObject, self).__init__()
        self.dataFile = ""

    def downloadData(self, dataUrl):
        """Download, unzip and process remote data file."""
        loop = QEventLoop()
        dataFile = getTempDownloadPath()
        ensureDirectory(Path(dataFile).parent)
        qgsDebug(f"Data file: {dataFile}")

        downloader = QgsFileDownloader(
            QUrl(dataUrl), dataFile, delayStart=True)
        downloader.downloadProgress.connect(NtrrpDataClient.downloadProgress)
        downloader.downloadError.connect(NtrrpDataClient.downloadError)
        downloader.downloadCompleted.connect(lambda: self.unzipData(dataFile))
        downloader.startDownload()

        loop.exec_()

    def unzipData(self, dataFile):
        """Unzip the downloaded data and signal the process is complete."""
        qgsDebug(f"Unzipping data file: {dataFile}")
        dataPath = Path(dataFile)
        unzipLocation = path.normpath(
            path.join(dataPath.parent, os.pardir, dataPath.stem))

        with ZipFile(dataFile, 'r') as zf:
            zf.extractall(unzipLocation)

        self.dataDownloaded.emit(Path(unzipLocation))

    @staticmethod
    def downloadProgress(bytesReceived, bytesTotal):
        qgsDebug(f"{bytesReceived / float(bytesTotal)}%")

    @staticmethod
    def downloadError(messages):
        qgsDebug(str(messages))
