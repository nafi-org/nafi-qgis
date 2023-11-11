from qgis.core import Qgis, QgsProcessingFeedback

from ntrrp.src.utils import guiError, qgsDebug


class FsidServiceError(Exception):
    """Throw an error after a failure of the FSID service."""

    def __init__(self, headline, details=None):
        super(FsidServiceError, self).__init__()
        self.headline = headline
        self.details = details

    def guiError(self):
        """Display a GUI error message."""
        guiError(self.headline)

    def processingFeedbackError(self, feedback):
        """Report a processing feedback error."""
        if feedback is not None and isinstance(feedback, QgsProcessingFeedback):
            feedback.reportError(self.headline)
            if self.details:
                feedback.reportError(self.details)

    def log(self):
        """Log to the console."""
        qgsDebug(self.headline, Qgis.Critical)
        if self.details:
            qgsDebug(self.details, Qgis.Critical)
