# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QObject, QUrl
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest, QSslSocket

from qgis.core import QgsBlockingNetworkRequest

from .utils import guiError, qgsDebug

class NafiCapabilitiesReader(QObject):

    # emit this signal with the downloaded capabilities XML
    capabilitiesDownloaded = pyqtSignal(str)

    def __init__(self):
        """Constructor."""
        super(QObject, self).__init__()

    def downloadCapabilities(self, wmsUrl):
        """Download a remote capabilities file."""
        # we get the WMS 1.1.1 XML because OWSLib actually works with it
        capabilitiesUrl = f"{wmsUrl}?request=GetCapabilities&version=1.1.1"
        request = QNetworkRequest(QUrl(capabilitiesUrl))

        # suppress errors from SSL for the capabilities request (NTG network is dodgy)
        sslConfig = request.sslConfiguration()
        sslConfig.setPeerVerifyMode(QSslSocket.VerifyNone)
        request.setSslConfiguration(sslConfig)

        # use a blocking request here
        blockingRequest = QgsBlockingNetworkRequest()
        result = blockingRequest.get(request)
        if result == QgsBlockingNetworkRequest.NoError:
            reply = blockingRequest.reply()
            if reply.error() == QNetworkReply.NoError:
                xml = bytes(reply.content()).decode()
                self.capabilitiesDownloaded.emit(xml)
            else:
                self.connectionError(reply.errorString())
        else:
            self.connectionError(blockingRequest.errorMessage())


    def connectionError(self, logMessage):
        """Raise a connection error."""
        error = (f"Error connecting to NAFI services!\n"
                 f"Check the QGIS NAFI Fire Maps message log for details.")
        guiError(error)
        qgsDebug(logMessage)

