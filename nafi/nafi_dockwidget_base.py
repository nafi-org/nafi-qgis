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
        NafiDockWidgetBase.resize(689, 451)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        NafiDockWidgetBase.setFont(font)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 3)
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 4)
        self.searchLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchLabel.sizePolicy().hasHeightForWidth())
        self.searchLabel.setSizePolicy(sizePolicy)
        self.searchLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.searchLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.searchLabel.setFont(font)
        self.searchLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.searchLabel.setObjectName("searchLabel")
        self.gridLayout.addWidget(self.searchLabel, 0, 0, 1, 1)
        self.nafiLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.nafiLabel.setObjectName("nafiLabel")
        self.gridLayout.addWidget(self.nafiLabel, 2, 0, 1, 1)
        NafiDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(NafiDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(NafiDockWidgetBase)

    def retranslateUi(self, NafiDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        NafiDockWidgetBase.setWindowTitle(_translate("NafiDockWidgetBase", "NAFI Fire Maps"))
        self.lineEdit.setPlaceholderText(_translate("NafiDockWidgetBase", "(not implemented)"))
        self.searchLabel.setText(_translate("NafiDockWidgetBase", "<html><head/><body><p>Search layers</p></body></html>"))
        self.nafiLabel.setText(_translate("NafiDockWidgetBase", "<html><head/><body><p><a href=\"https://firenorth.org.au\"><span style=\" text-decoration: underline; color:#0000ff;\">Visit the NAFI website</span></a></p></body></html>"))

