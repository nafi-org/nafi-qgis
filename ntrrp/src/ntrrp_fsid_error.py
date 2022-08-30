# -*- coding: utf-8 -*-
from .utils import guiError, qgsDebug
from qgis.core import Qgis

class NtrrpFsidError(Exception):
    """Throw an error after a failure of the FSID service."""

    def __init__(self, headline, details=None):
        super(NtrrpFsidError, self).__init__()
        self.headline = headline
        self.details = details
        
    def guiError(self):
        """Display a GUI error message."""
        guiError(self.headline)

    def log(self):
        """Log to the console."""
        qgsDebug(self.headline, Qgis.Critical)
        if self.details is not None:
            qgsDebug(self.details, Qgis.Critical)

