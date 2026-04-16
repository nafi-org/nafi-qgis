from dateutil import parser
from pathlib import Path


class SegmentationMetadata:
    def __init__(self, shapefilePath: Path):
        self.shapefilePath = shapefilePath
        segments = self.shapefilePath.stem.split("_")

        if len(segments) < 6:
            raise ValueError(f"Invalid segmentation filename: {shapefilePath}")

        # the 'difference' code will be eg 'T1T3'
        self.difference = segments[0]

        # the third and fourth segments will be eg '20191001' and '20190901' as dates
        try:
            self.endDate = parser.parse(segments[2])
            self.startDate = parser.parse(segments[3])
        except ValueError:
            raise ValueError(f"Invalid segmentation filename: {shapefilePath}")

        # the sixth segment will be eg 'T100'
        self.threshold = int(segments[5][1:])

        self.differenceGroup = f"{self.difference} Differences ({self.endDate.strftime('%b %d')}–{self.startDate.strftime('%b %d')})"
