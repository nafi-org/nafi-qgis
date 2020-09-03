# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nafi_dockwidget_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NafiDockWidgetBase(object):
    def setupUi(self, NafiDockWidgetBase):
        NafiDockWidgetBase.setObjectName("NafiDockWidgetBase")
        NafiDockWidgetBase.resize(618, 254)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        NafiDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(NafiDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(NafiDockWidgetBase)

    def retranslateUi(self, NafiDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        NafiDockWidgetBase.setWindowTitle(_translate("NafiDockWidgetBase", "NAFI Maps"))
        self.label.setText(_translate("NafiDockWidgetBase", "<html><head/><body><p><img src=\":/plugins/nafi/icon.png\"/></p></body></html>"))

