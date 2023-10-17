# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider

from .processing import *


class NtrrpProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """Unload the provider."""
        pass

    def loadAlgorithms(self):
        """Load the algorithms from the provider."""
        self.addAlgorithm(AttributeBurntAreas())
        self.addAlgorithm(DissolveBurntAreas())
        self.addAlgorithm(DownloadCurrentMapping())
        self.addAlgorithm(DownloadSegmentationData())
        self.addAlgorithm(FullBurntAreasProcess())
        self.addAlgorithm(ValidateFullBurntAreasProcess())
        self.addAlgorithm(RasteriseBurntAreas())
        self.addAlgorithm(UploadBurntAreas())

    def id(self):
        """Return the unique provider ID."""
        return 'BurntAreas'

    def name(self):
        """Return the provider display name in the QGIS UX."""
        return self.tr("NAFI Burnt Areas Tools")

    def icon(self):
        """Return the provider toolbox icon."""
        return QIcon(":/plugins/ntrrp/images/icon.png")

    def longName(self):
        return self.name()
