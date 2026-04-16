from typing import Any
from abc import ABCMeta

from qgis.PyQt.QtCore import QObject

# mypy prefers this to using type(QObject) directly
QObjectType: Any = type(QObject)


class AbstractQObjectMeta(ABCMeta, QObjectType):
    """Metaclass to manage the requirement that things with signals be QObjects."""

    pass
