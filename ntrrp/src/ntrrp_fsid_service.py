# -*- coding: utf-8 -*-
import json
import re
from collections import OrderedDict

from owslib.etree import etree
from owslib.map.wms111 import ContentMetadata
from qgis.core import QgsBlockingNetworkRequest
from qgis.PyQt.QtCore import QObject, QUrl, pyqtSignal
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest, QSslSocket

from .ntrrp_capabilities import NtrrpCapabilities
from .ntrrp_fsid_record import NtrrpFsidRecord
from .utils import capabilitiesError, connectionError, fsidsError, qgsDebug


class NtrrpFsidService(QObject):

    # emit this signal with the downloaded FSID data
    fsidsDownloaded = pyqtSignal(str)

    # emit this signal with the parsed capabilities object
    fsidsParsed = pyqtSignal(list)

    def __init__(self):
        """Constructor."""
        super(QObject, self).__init__()

    def downloadFsids(self, apiBaseUrl, regionName):
        """Download and parse remote capabilities file."""

        fsidsUrl = f"{apiBaseUrl}/mapping/?area={regionName.lower()}"
        # https://test.firenorth.org.au/bfnt/api/mapping/?area=darwin f"{wmsUrl}?request=GetCapabilities&version=1.1.1"

        request = QNetworkRequest(QUrl(fsidsUrl))

        # suppress errors from SSL for the capabilities request (NTG network is dodgy)
        sslConfig = request.sslConfiguration()
        sslConfig.setPeerVerifyMode(QSslSocket.VerifyNone)
        request.setSslConfiguration(sslConfig)

        fsidsJson = ""

        # use a blocking request here
        blockingRequest = QgsBlockingNetworkRequest()
        result = blockingRequest.get(request)
        if result == QgsBlockingNetworkRequest.NoError:
            reply = blockingRequest.reply()
            if reply.error() == QNetworkReply.NoError:
                fsidsJson = bytes(reply.content()).decode()
                self.fsidsDownloaded.emit(fsidsJson)
                return fsidsJson
            else:
                connectionError(reply.errorString())
        else:
            connectionError(blockingRequest.errorMessage())

        return None

    def parseFsids(self, fsidsJson):
        """Parse the FSID JSON and return as a collection of NtrrpFsidRecord items."""

        try:
            fsidArray = json.loads(fsidsJson)

            if not isinstance(fsidArray, list):
                raise RuntimeError("Expected a list of FSIDs")

            fsids = [NtrrpFsidRecord(fsidJson) for fsidJson in fsidArray]
        except:
            fsidsError()
            return None

        self.fsidsParsed.emit(fsids)
        return fsids

    def downloadAndParseFsids(self, apiBaseUrl, regionName):
        """Download, then parse FSID data."""

        qgsDebug("Downloading FSIDs")

        fsidsJson = self.downloadFsids(apiBaseUrl, regionName)

        qgsDebug(f"Got FSIDs {fsidsJson}")

        qgsDebug("Parsing FSIDs")

        return (fsidsJson and self.parseFsids(fsidsJson))


