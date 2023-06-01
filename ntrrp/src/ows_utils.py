# -*- coding: utf-8 -*-
import dateutil
import re


def parseNtrrpLayerRegion(owsTitle):
    """Parse the NTRRP region from a WMS or WMTS layer title. The expected format is T1T2 Difference Image [Darwin_T20210628_dMIRBI_T20210623]."""
    match = re.match("^.*\\[(.*)\\].*$", owsTitle)
    if match is not None:
        ntrrpMeta = match.group(1)
        ntrrpMetaElements = ntrrpMeta.split("_")
        if len(ntrrpMetaElements) > 0:
            return ntrrpMetaElements[0]
    # nothing was found
    return None


def parseNtrrpLayerDescription(owsTitle):
    """Parse the NTRRP description from a WMS or WMTS layer title. The expected format is T1T2 Difference Image [Darwin_T20210628_dMIRBI_T20210623]."""
    match = re.match("^(.*)\\[(.*)\\].*$", owsTitle)
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
    return owsTitle
