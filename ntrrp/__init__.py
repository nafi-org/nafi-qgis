# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NTRRP
                                 A QGIS plugin
 NAFI Burnt Areas Mapping
                             -------------------
        begin                : 2021-05-27
        copyright            : (C) 2020 by Tom Lynch
        email                : tom@trailmarker.io
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Ntrrp class from file Ntrrp.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ntrrp import Ntrrp
    return Ntrrp(iface)
