# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\ntrrp_dockwidget_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NtrrpDockWidgetBase(object):
    def setupUi(self, NtrrpDockWidgetBase):
        NtrrpDockWidgetBase.setObjectName("NtrrpDockWidgetBase")
        NtrrpDockWidgetBase.resize(689, 504)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        NtrrpDockWidgetBase.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NtrrpDockWidgetBase.setWindowIcon(icon)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 2)
        self.searchLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchLabel.sizePolicy().hasHeightForWidth())
        self.searchLabel.setSizePolicy(sizePolicy)
        self.searchLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.searchLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.searchLabel.setFont(font)
        self.searchLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.searchLabel.setObjectName("searchLabel")
        self.gridLayout.addWidget(self.searchLabel, 0, 0, 1, 1)
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 4)
        self.clearSearchButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearSearchButton.sizePolicy().hasHeightForWidth())
        self.clearSearchButton.setSizePolicy(sizePolicy)
        self.clearSearchButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/backspace.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearSearchButton.setIcon(icon1)
        self.clearSearchButton.setObjectName("clearSearchButton")
        self.gridLayout.addWidget(self.clearSearchButton, 0, 3, 1, 1)
        self.aboutButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aboutButton.sizePolicy().hasHeightForWidth())
        self.aboutButton.setSizePolicy(sizePolicy)
        self.aboutButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutButton.setIcon(icon2)
        self.aboutButton.setObjectName("aboutButton")
        self.gridLayout.addWidget(self.aboutButton, 2, 3, 1, 1)
        self.dataButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataButton.sizePolicy().hasHeightForWidth())
        self.dataButton.setSizePolicy(sizePolicy)
        self.dataButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/greenglobe.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dataButton.setIcon(icon3)
        self.dataButton.setObjectName("dataButton")
        self.gridLayout.addWidget(self.dataButton, 2, 0, 1, 1)
        NtrrpDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(NtrrpDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(NtrrpDockWidgetBase)

    def retranslateUi(self, NtrrpDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        NtrrpDockWidgetBase.setToolTip(_translate("NtrrpDockWidgetBase", "NT Risk Reduction Program"))
        NtrrpDockWidgetBase.setWindowTitle(_translate("NtrrpDockWidgetBase", "NT Risk Reduction Program"))
        self.lineEdit.setPlaceholderText(_translate("NtrrpDockWidgetBase", "start typing layer title …"))
        self.searchLabel.setText(_translate("NtrrpDockWidgetBase", "<html><head/><body><p>Search layers</p></body></html>"))
        self.clearSearchButton.setToolTip(_translate("NtrrpDockWidgetBase", "Clear Search"))
        self.aboutButton.setToolTip(_translate("NtrrpDockWidgetBase", "About NTRRP …"))
        self.dataButton.setToolTip(_translate("NtrrpDockWidgetBase", "Download NTRRP data …"))

