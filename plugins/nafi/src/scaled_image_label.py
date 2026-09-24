from qgis.PyQt.QtCore import QSize, Qt
from qgis.PyQt.QtGui import QPainter, QPixmap
from qgis.PyQt.QtWidgets import QLabel, QSizePolicy


class ScaledImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QPixmap()
        policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

    def setPixmap(self, pixmap):
        """Show an image scaled to the label's width, keeping its aspect ratio."""
        self.image = QPixmap(pixmap)
        self.updateGeometry()
        self.update()

    def pixmap(self):
        return self.image

    def hasHeightForWidth(self):
        return not self.image.isNull()

    def heightForWidth(self, width):
        if self.image.isNull():
            return 0
        # never scale up past the image's own size
        width = min(width, self.image.width())
        return min(round(width * self.image.height() / self.image.width()), self.maximumHeight())

    def sizeHint(self):
        return self.image.size() if not self.image.isNull() else QSize()

    def minimumSizeHint(self):
        return QSize(0, 0)

    def paintEvent(self, event):
        if self.image.isNull():
            return
        ratio = self.devicePixelRatioF()
        target = QSize(min(self.width(), self.image.width()), self.height())
        scaled = self.image.scaled(
            target * ratio,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        scaled.setDevicePixelRatio(ratio)
        painter = QPainter(self)
        x = round((self.width() - scaled.width() / ratio) / 2)
        y = round((self.height() - scaled.height() / ratio) / 2)
        painter.drawPixmap(x, y, scaled)
