from typing import cast

from pathlib import Path

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsProject,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsWkbTypes,
)

from ntrrp.src.utils import ensureDirectory, guiError, resolveStylePath
from .item import Item
from .layer import Layer
from .segmentation_layer import SegmentationLayer


class WorkingLayer(QgsVectorLayer, Layer):
    @classmethod
    def createWorkingLayerShapefile(
        cls, shapefilePath: Path, templateLayer: SegmentationLayer
    ):
        """Create a shapefile for this layer."""

        ensureDirectory(shapefilePath.parent)

        # template SegmentationLayer sets initial attributes
        writer = QgsVectorFileWriter(
            shapefilePath.as_posix(),
            "utf-8",
            templateLayer.fields(),
            QgsWkbTypes.Polygon,
            QgsCoordinateReferenceSystem("EPSG:3577"),
            "ESRI Shapefile",
        )

    def __init__(self, mapping: Item, templateLayer: SegmentationLayer):
        self.mapping = mapping

        # Target segmentation layer is not initially set
        self.segmentationLayer = None
        self.shapefilePath: Path = Path(
            self.mapping.directory, "Working", "Working.shp"
        )

        # Create underlying shapefile if it does not exist
        if not self.shapefilePath.exists():
            WorkingLayer.createWorkingLayerShapefile(self.shapefilePath, templateLayer)

        # Init vector layer
        QgsVectorLayer.__init__(
            self, self.shapefilePath.as_posix(), f"Working Layer", "ogr"
        )

    def saveFeatures(self):
        """Write the content of this layer to the shapefile."""
        ensureDirectory(Path(self.shapefilePath).parent)
        QgsVectorFileWriter.writeAsVectorFormat(  # typing: ignore
            self, self.shapefilePath.as_posix(), "utf-8", driverName="ESRI Shapefile"
        )

    def addMapLayer(self):
        """Add an NTRRP data layer to the map."""
        if self.isValid():
            Layer.addMapLayer(self)
            self.loadStyle("approved")
            self.item.setName(self.itemName)
        else:
            error = (
                f"An error occurred adding the layer {self.itemName} to the map.\n"
                f"Check your QGIS logs for details."
            )
            guiError(error)

    # Item interface
    @property
    def directory(self) -> Path:
        return Path(self.mapping.directory, "Working")

    @property
    def regionName(self) -> str:
        return self.mapping.regionName

    @property
    def itemName(self):
        """Get an appropriate map layer name for this layer."""
        return f"Working Layer"

    @property
    def item(self) -> QgsLayerTreeLayer:
        return QgsProject.instance().layerTreeRoot().findLayer(self.id())

    @property
    def groupName(self) -> str:
        return self.mapping.itemName

    @property
    def group(self) -> QgsLayerTreeGroup:
        return self.mapping.item

    def loadStyle(self, styleName):
        """Apply a packaged style to this layer."""
        stylePath = resolveStylePath(styleName)
        self.loadNamedStyle(stylePath)
