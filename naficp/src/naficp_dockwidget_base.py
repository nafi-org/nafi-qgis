# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\naficp_dockwidget_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NafiCpDockWidgetBase(object):
    def setupUi(self, NafiCpDockWidgetBase):
        NafiCpDockWidgetBase.setObjectName("NafiCpDockWidgetBase")
        NafiCpDockWidgetBase.resize(232, 141)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        NafiCpDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(NafiCpDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(NafiCpDockWidgetBase)

    def retranslateUi(self, NafiCpDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        NafiCpDockWidgetBase.setWindowTitle(_translate("NafiCpDockWidgetBase", "NAFI Copy and Paste"))
        self.label.setText(_translate("NafiCpDockWidgetBase", "Replace this QLabel\n"
"with the desired\n"
"plugin content."))

