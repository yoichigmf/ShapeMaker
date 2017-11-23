# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShapeMaker
                                 A QGIS plugin
 Make a Polgon Shape Layer
                             -------------------
        begin                : 2017-11-21
        copyright            : (C) 2017 by Yoichi Kayama
        email                : yoichi.kayama@gmail.com
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
    """Load ShapeMaker class from file ShapeMaker.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ShapeMaker import ShapeMaker
    return ShapeMaker(iface)
