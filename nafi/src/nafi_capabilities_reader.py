# -*- coding: utf-8 -*-
from re import sub

from qgis.PyQt.QtCore import pyqtSignal, QObject, QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply, QSslSocket

from qgis.core import QgsNetworkAccessManager

from .utils import guiError, qgsDebug

class NafiCapabilitiesReader(QObject):

    # emit this signal with the downloaded capabilities XML
    capabilitiesDownloaded = pyqtSignal(str)

    def __init__(self):
        """Constructor."""
        super(QObject, self).__init__()
        self.httpClient = QgsNetworkAccessManager.instance()

    def downloadCapabilities(self, wmsUrl):
        """Download a remote capabilities file."""
        # we get the WMS 1.1.1 XML because OWSLib actually works with it
        capabilitiesUrl = f"{wmsUrl}?request=GetCapabilities&version=1.1.1"
        request = QNetworkRequest(QUrl(capabilitiesUrl))

        # suppress errors from SSL for the capabilities request (NTG network is dodgy)
        sslConfig = request.sslConfiguration()
        sslConfig.setPeerVerifyMode(QSslSocket.VerifyNone)
        request.setSslConfiguration(sslConfig)
        
        self.httpClient.finished.connect(self.processCapabilities)
        self.httpClient.get(request)

    def processCapabilities(self, reply):
        """Handle the reply from the WMS capabilities request."""
        try:
            if reply.error() == QNetworkReply.NoError:
                xml = reply.content().data().decode("utf-8")
                self.capabilitiesDownloaded.emit(xml)
            else:
                self.connectionError(reply.errorString())
        finally:
            # doing this with QgsNetworkAccessManager turns out to be important!
            self.httpClient.finished.disconnect()

    def connectionError(self, logMessage):
        """Raise a connection error."""
        error = (f"Error connecting to NAFI services!\n"
                 f"Check the QGIS NAFI Fire Maps message log for details.")
        guiError(error)
        qgsDebug(logMessage)

