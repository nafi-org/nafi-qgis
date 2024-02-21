from typing import Optional, cast

from qgis.PyQt.QtCore import QByteArray, QUrl, QJsonDocument
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkProxy

from qgis.core import QgsSettings, QgsNetworkAccessManager


def apiPost(url, params):
    """Post a dictionary to a URL with proxy settings."""
    settings = QgsSettings()

    # Read proxy settings from QGIS
    proxy = QNetworkProxy()
    proxyEnabled = settings.value("proxy/proxyEnabled", "")
    proxyHost = settings.value("proxy/proxyHost", "")
    proxyPort = settings.value("proxy/proxyPort", "")
    proxyUser = settings.value("proxy/proxyUser", "")
    proxyPassword = settings.value("proxy/proxyPassword", "")

    networkAccessManager = QgsNetworkAccessManager()
    networkAccessManager.setTimeout(20000)

    # If proxy is in play, set it up on the outgoing request
    if proxyEnabled == "true":
        proxy.setType(QNetworkProxy.HttpProxy)
        proxy.setHostName(proxyHost)
        if proxyPort != "":
            proxy.setPort(int(proxyPort))
        proxy.setUser(proxyUser)
        proxy.setPassword(proxyPassword)
        QNetworkProxy.setApplicationProxy(proxy)
        networkAccessManager.setupDefaultProxyAndCache()
        networkAccessManager.setFallbackProxyAndExcludes(proxy, [""], [""])

    # Create the request
    request = QNetworkRequest(QUrl(url))

    postData: QByteArray = None

    if params:
        jsonDoc = QJsonDocument(params)
        # this oddly named Qt method returns a QByteArray for some reason
        postData = jsonDoc.toJson()

    # Apply the required headers
    request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
    request.setHeader(QNetworkRequest.ContentLengthHeader, len(postData))
    request.setHeader(QNetworkRequest.UserAgentHeader, "QGIS NAFI Burnt Areas Plug-in")

    # Literally cannot believe this API!
    request.setRawHeader("Accept".encode("utf-8"), "*/*".encode("utf-8"))

    return networkAccessManager.blockingPost(request, postData)
