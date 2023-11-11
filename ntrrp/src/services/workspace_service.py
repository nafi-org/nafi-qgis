from typing import Optional

from collections import OrderedDict
import re

from qgis.PyQt.QtCore import QObject, QUrl, pyqtSignal
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest, QSslSocket

from qgis.core import QgsBlockingNetworkRequest

from owslib.etree import etree
from owslib.map.wms111 import ContentMetadata

from ntrrp.src.models import WorkspaceMetadata
from ntrrp.src.utils import capabilitiesError, connectionError


class WorkspaceMetadataService(QObject):
    workspaceMetadataDownloaded = pyqtSignal(str)
    workspaceMetadataParsed = pyqtSignal(WorkspaceMetadata)

    def __init__(self):
        QObject.__init__(self)

    def downloadWorkspaceMetadata(self, wmsUrl: str) -> Optional[str]:
        """Download the remote workspace capabilities file."""

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
        if result == QgsBlockingNetworkRequest.NoError:  # type: ignore
            reply = blockingRequest.reply()
            if reply.error() == QNetworkReply.NoError:
                wmsXml = bytes(reply.content()).decode()
                self.workspaceMetadataDownloaded.emit(wmsXml)
                return wmsXml
            else:
                connectionError(reply.errorString())
        else:
            connectionError(blockingRequest.errorMessage())

        return None

    def parseWorkspaceMetadata(
        self, wmsUrl: str, wmsXml: str
    ) -> Optional[WorkspaceMetadata]:
        """Parse the capabilities XML and signal as a collection of OWSLib ContentMetadata items."""

        # etree.fromstring internally for some reason can't handle the XML declaration,
        # so it gets hacked off
        wmsXml = re.sub("<\\?xml.*\\?>", "", wmsXml)
        contents = OrderedDict()

        try:
            parser = etree.XMLParser(
                dtd_validation=False,
                load_dtd=False,
                no_network=True,
                recover=True,
                resolve_entities=False,
            )
            capabilities = etree.fromstring(wmsXml, parser)

            capabilityElement = capabilities.find("Capability")

            if capabilityElement is None:
                raise RuntimeError(
                    "Missing 'Capability' Element in parsed XML capabilities"
                )

            # recursively gather content metadata for all layer elements, this is stolen
            # from OWSLib because it won't let us configure the parser the way we need to
            # to avoid unwanted network activity, entity resolutions etc
            # see
            # https://github.com/geopython/OWSLib/blob/8a94500c2137082dfc4e59acd15389312bcb63fb/owslib/map/wms111.py#L113
            def gatherLayers(parentElement, parentMetadata):
                layers = []
                for index, elem in enumerate(parentElement.findall("Layer")):
                    cm = ContentMetadata(
                        elem,
                        parent=parentMetadata,
                        index=index + 1,
                        parse_remote_metadata=False,
                    )
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
        workspaceMetadata = WorkspaceMetadata(wmsUrl, owsLayers)
        self.workspaceMetadataParsed.emit(workspaceMetadata)
        return workspaceMetadata

    def downloadAndParseWorkspaceMetadata(self, wmsUrl) -> Optional[WorkspaceMetadata]:
        """Download, then parse remote capabilities."""
        wmsXml = self.downloadWorkspaceMetadata(wmsUrl)
        return wmsXml and self.parseWorkspaceMetadata(wmsUrl, wmsXml)
