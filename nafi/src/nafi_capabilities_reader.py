from qgis.PyQt.QtCore import pyqtSignal, QObject, QUrl
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest, QSslSocket

from qgis.core import QgsBlockingNetworkRequest

from .utils import connectionError, guiError, qgsDebug


class NafiCapabilitiesReader(QObject):
    # emit this signal with the downloaded capabilities XML
    capabilitiesDownloaded = pyqtSignal(str)

    def __init__(self):
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
        if result == QgsBlockingNetworkRequest.NoError:  # type: ignore
            reply = blockingRequest.reply()
            if reply.error() == QNetworkReply.NoError:
                xml = bytes(reply.content()).decode()
                self.capabilitiesDownloaded.emit(xml)
            else:
                connectionError(reply.errorString())
        else:
            connectionError(blockingRequest.errorMessage())
