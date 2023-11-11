import html
import json

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtNetwork import QNetworkRequest

from ntrrp.src.utils import qgsDebug

from .api_post import apiPost
from .fsid_service_error import FsidServiceError
from .fsid_record import FsidRecord


class FsidService(QObject):
    # emit this signal with the downloaded FSID data
    fsidsDownloaded = pyqtSignal(str)

    # emit this signal with the parsed capabilities object
    fsidsParsed = pyqtSignal(list)

    def __init__(self):
        super(QObject, self).__init__()

    def postNewMapping(self, apiBaseUrl, regionName, params):
        """Post a new mapping record and retrieve and parse the response as an (incomplete) FsidRecord."""
        postUrl = f"{apiBaseUrl}/mapping/?area={regionName.lower()}"
        # eg https://test.firenorth.org.au/bfnt/api/mapping/?area=darwin

        try:
            response = apiPost(postUrl, params)

            statusCode = response.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            responseContent = str(response.content(), "utf-8")

            qgsDebug(f"FsidService.postNewMapping responseContent: {responseContent}")

            if statusCode == 200:
                try:
                    jsonContent = json.loads(responseContent)
                    if (
                        jsonContent is not None
                        and jsonContent.get("new_record", None) is not None
                    ):
                        # Just hard-coding aspects of this API here
                        fsidJson = jsonContent["new_record"]
                        # Note the response contains no "upload_date" for some reason
                        fsid = FsidRecord(fsidJson)
                        return fsid

                    raise Exception()
                except BaseException:
                    raise FsidServiceError(
                        f"Error parsing the retrieved NAFI FSID data!\n"
                        f"Check the QGIS NAFI Burnt Areas Mapping message log for details.",
                        f"NAFI FSID data retrieved: {html.escape(responseContent)}",
                    )
            elif statusCode == 400:
                # One of Patrice's new style errors
                raise FsidServiceError(responseContent)
            else:
                raise FsidServiceError(
                    f"Error connecting to NAFI services!\n"
                    f"Check the QGIS NAFI Burnt Areas Mapping message log for details.",
                    f"Unexpected HTTP status code {statusCode} returned from server with response content {responseContent}",
                )
        except FsidServiceError:
            raise
        except BaseException:
            raise FsidServiceError("Unknown error posting new mapping record")

    # def downloadFsids(self, apiBaseUrl, regionName):
    #     """Download and parse remote capabilities file."""
    #     fsidsUrl = f"{apiBaseUrl}/mapping/?area={regionName.lower()}"
    #     # https://test.firenorth.org.au/bfnt/api/mapping/?area=darwin
    #     request = QNetworkRequest(QUrl(fsidsUrl))

    #     # suppress errors from SSL for the capabilities request (NTG network is dodgy)
    #     sslConfig = request.sslConfiguration()
    #     sslConfig.setPeerVerifyMode(QSslSocket.VerifyNone)
    #     request.setSslConfiguration(sslConfig)

    #     fsidsJson = ""

    #     # use a blocking request here
    #     blockingRequest = QgsBlockingNetworkRequest()
    #     result = blockingRequest.get(request)
    #     if result == QgsBlockingNetworkRequest.NoError:
    #         reply = blockingRequest.reply()
    #         if reply.error() == QNetworkReply.NoError:
    #             fsidsJson = bytes(reply.content()).decode()
    #             self.fsidsDownloaded.emit(fsidsJson)
    #             return fsidsJson
    #         else:
    #             raise FsidServiceError(f"Error connecting to NAFI services!\n"
    #                                  f"Check the QGIS NAFI Burnt Areas Mapping message log for details.",
    #                                  reply.errorString())
    #     else:
    #         raise FsidServiceError(f"Error connecting to NAFI services!\n"
    #                              f"Check the QGIS NAFI Burnt Areas Mapping message log for details.",
    #                              blockingRequest.errorMessage())

    # def parseFsids(self, fsidsJson):
    #     """Parse the FSID JSON and return as a collection of FsidRecord items."""
    #     try:
    #         fsidArray = json.loads(fsidsJson)

    #         if not isinstance(fsidArray, list):
    #             raise RuntimeError("Expected a list of FSIDs")

    #         fsids = [FsidRecord(fsidJson) for fsidJson in fsidArray]
    #     except:
    #         raise FsidServiceError(f"Error parsing the retrieved NAFI FSID data!\n"
    #                              f"Check the QGIS NAFI Burnt Areas Mapping message log for details.",
    #                              f"NAFI FSID data retrieved: {html.escape(fsidsJson)}")

    #     self.fsidsParsed.emit(fsids)
    #     return fsids

    # def downloadAndParseFsids(self, apiBaseUrl, regionName):
    #     """Download, then parse FSID data."""
    #     fsidsJson = self.downloadFsids(apiBaseUrl, regionName)
    #     return (fsidsJson and self.parseFsids(fsidsJson))
