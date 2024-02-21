# -*- coding: utf-8 -*-
import re

from qgis.gui import QgsAttributeTableDelegate
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor


class SegmentationLayerDelegate(QgsAttributeTableDelegate):
    """An item delegate for the segmentation layer chooser."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        """Paint the cell."""
        try:
            painter.save()

            # painter.drawText(option.rect, Qt.AlignCenter, index.data())

            # Since this is a layer chooser, the data is the layer name
            layerName = index.data(role=Qt.DisplayRole)

            abbreviatedLayerName = re.sub("[\(\[].*?[\)\]]", "", layerName)

            # cellSelected = (self._tableView.selectionModel().currentIndex().row() == index.row())

            # painter.setBrush(option.palette.highlight())
            # painter.setPen(option.palette.highlightedText().color())

            # painter.setPen(Qt.NoPen)
            # if cellSelected:
            # painter.setBrush(option.palette.highlight())
            # else:
            # painter.setBrush(QColor(*fieldDomainValue.toColour()))
            # painter.fillRect(option.rect, painter.brush())
            # if cellSelected:
            #     painter.setPen(option.palette.highlightedText().color())
            # else:
            # painter.setPen(QColor(*fieldDomainValue.toForegroundColour()))
            painter.drawText(option.rect, Qt.AlignCenter, abbreviatedLayerName)

            painter.restore()
        except BaseException:
            pass
