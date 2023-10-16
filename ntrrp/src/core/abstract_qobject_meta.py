# -*- coding: utf-8 -*-
from abc import ABCMeta

from qgis.PyQt.QtCore import QObject


class AbstractQObjectMeta(ABCMeta, type(QObject)):
    """Metaclass to manage the requirement that things with signals be QObjects."""
    pass
