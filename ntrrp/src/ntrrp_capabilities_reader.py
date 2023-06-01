# -*- coding: utf-8 -*-
from collections import OrderedDict
import re

from qgis.PyQt.QtCore import pyqtSignal, QObject, QUrl
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest, QSslSocket

from qgis.core import QgsBlockingNetworkRequest

from owslib.etree import etree
from owslib.map.wms111 import ContentMetadata

from .ntrrp_capabilities import NtrrpCapabilities
from .utils import capabilitiesError, connectionError


class NtrrpCapabilitiesReader(QObject):

    # emit this signal with the downloaded capabilities XML
    capabilitiesDownloaded = pyqtSignal(str)

    # emit this signal with the parsed capabilities object
    capabilitiesParsed = pyqtSignal(NtrrpCapabilities)

    def __init__(self):
        """Constructor."""
        super(QObject, self).__init__()

    def downloadCapabilities(self, wmsUrl):
        """Download and parse remote capabilities file."""

        # we get the WMS 1.1.1 XML because OWSLib actually works with it
        capabilitiesUrl = f"{wmsUrl}?request=GetCapabilities&version=1.1.1"
        request = QNetworkRequest(QUrl(capabilitiesUrl))

        # suppress errors from SSL for the capabilities request (NTG network is dodgy)
        sslConfig = request.sslConfiguration()
        sslConfig.setPeerVerifyMode(QSslSocket.VerifyNone)
        request.setSslConfiguration(sslConfig)

        wmsXml = ""

        # use a blocking request here
        blockingRequest = QgsBlockingNetworkRequest()
        result = blockingRequest.get(request)
        if result == QgsBlockingNetworkRequest.NoError:
            reply = blockingRequest.reply()
            if reply.error() == QNetworkReply.NoError:
                wmsXml = bytes(reply.content()).decode()
                self.capabilitiesDownloaded.emit(wmsXml)
                return wmsXml
            else:
                connectionError(reply.errorString())
        else:
            connectionError(blockingRequest.errorMessage())

        return None

    def parseCapabilities(self, wmsUrl, wmsXml):
        """Parse the capabilities XML and return as a collection of OWSLib ContentMetadata items."""

        # etree.fromstring internally for some reason can't handle the XML declaration,
        # so it gets hacked off
        wmsXml = re.sub("<\\?xml.*\\?>", "", wmsXml)
        contents = OrderedDict()

        try:
            parser = etree.XMLParser(dtd_validation=False, load_dtd=False,
                                     no_network=True, recover=True, resolve_entities=False)
            capabilities = etree.fromstring(wmsXml, parser)

            capabilityElement = capabilities.find("Capability")

            if capabilityElement is None:
                raise RuntimeError(
                    "Missing 'Capability' Element in parsed XML capabilities")

            # recursively gather content metadata for all layer elements, this is stolen
            # from OWSLib because it won't let us configure the parser the way we need to
            # to avoid unwanted network activity, entity resolutions etc
            # see
            # https://github.com/geopython/OWSLib/blob/8a94500c2137082dfc4e59acd15389312bcb63fb/owslib/map/wms111.py#L113
            def gatherLayers(parentElement, parentMetadata):
                layers = []
                for index, elem in enumerate(parentElement.findall('Layer')):
                    cm = ContentMetadata(elem, parent=parentMetadata,
                                         index=index + 1,
                                         parse_remote_metadata=False)
                    if cm.id:
                        layers.append(cm)
                        contents[cm.id] = cm
                    cm.children = gatherLayers(elem, cm)
                return layers
            gatherLayers(capabilityElement, None)
        except (etree.ParserError, RuntimeError) as pe:
            capabilitiesError(str(pe), wmsXml)
            return None

        # the OWSLib structure is not properly organised via its "children" properties, need to fix it up
        owsLayers = [contents[layerName] for layerName in list(contents)]
        caps = NtrrpCapabilities(wmsUrl, owsLayers)
        self.capabilitiesParsed.emit(caps)
        return caps

    def downloadAndParseCapabilities(self, wmsUrl):
        """Download, then parse remote capabilities."""
        wmsXml = self.downloadCapabilities(wmsUrl)

        return (wmsXml and self.parseCapabilities(wmsUrl, wmsXml))
