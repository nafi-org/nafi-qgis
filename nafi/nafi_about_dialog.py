# -*- coding: utf-8 -*-
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, QRegExp, QSortFilterProxyModel, Qt, QModelIndex
from qgis.PyQt.QtGui import QFont, QIcon, QPixmap, QStandardItem, QStandardItemModel 
from qgis.PyQt.QtWidgets import QDialog, QApplication, QMessageBox

from qgis.core import Qgis, QgsRasterLayer, QgsProject

from .nafi_about_dialog_base import Ui_NafiAboutDialogBase


class NafiAboutDialog(QtWidgets.QDialog, Ui_NafiAboutDialogBase):

    def __init__(self, parent=None):
        """Constructor."""
        super(NafiAboutDialog, self).__init__(parent)

        self.setupUi(self)

    def accept(self):
        self.close()
