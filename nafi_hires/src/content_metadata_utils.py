import re
from typing import Optional

import dateutil.parser
from owslib.map.wms111 import ContentMetadata


def parseContentMetadataRegion(metadata: ContentMetadata) -> Optional[str]:
    """Parse the region from a HiRes WMS or WMTS layer title. The expected format is T1T2 Difference Image [Darwin_T20210628_dMIRBI_T20210623]."""
    match = re.match("^.*\\[(.*)\\].*$", metadata.title)
    if match is not None:
        nafi_hiresMeta = match.group(1)
        nafi_hiresMetaElements = nafi_hiresMeta.split("_")
        if len(nafi_hiresMetaElements) > 0:
            return nafi_hiresMetaElements[0]
    return None


def parseContentMetadataDescription(metadata: ContentMetadata) -> str:
    """Parse the description from a HiRes WMS or WMTS layer title. The expected format is T1T2 Difference Image [Darwin_T20210628_dMIRBI_T20210623]."""
    match = re.match("^(.*)\\[(.*)\\].*$", metadata.title)
    if match is not None:
        freeText = match.group(1) or ""
        metadata = match.group(2) or ""
        elems = metadata.split("_")

        if len(elems) == 4:  # eg dMIRBI layer
            endDate = dateutil.parser.parse(elems[1])
            startDate = dateutil.parser.parse(elems[3])
            return f"{freeText} ({startDate.strftime('%b %d')}–{endDate.strftime('%b %d')})"
        elif len(elems) == 3:  # eg RGB layer
            date = dateutil.parser.parse(elems[1])
            return f"{freeText} ({date.strftime('%b %d')})"
        else:
            return freeText

    # nothing was found
    return metadata.title
