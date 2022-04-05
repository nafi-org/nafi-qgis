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
        NtrrpDockWidgetBase.resize(571, 504)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        NtrrpDockWidgetBase.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/icon.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NtrrpDockWidgetBase.setWindowIcon(icon)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.regionLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.regionLabel.sizePolicy().hasHeightForWidth())
        self.regionLabel.setSizePolicy(sizePolicy)
        self.regionLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.regionLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.regionLabel.setFont(font)
        self.regionLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.regionLabel.setObjectName("regionLabel")
        self.gridLayout.addWidget(self.regionLabel, 0, 1, 1, 1)
        self.regionComboBox = QtWidgets.QComboBox(self.dockWidgetContents)
        self.regionComboBox.setObjectName("regionComboBox")
        self.gridLayout.addWidget(self.regionComboBox, 0, 2, 1, 6)
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 8)
        self.aboutButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.aboutButton.sizePolicy().hasHeightForWidth())
        self.aboutButton.setSizePolicy(sizePolicy)
        self.aboutButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            ":/plugins/ntrrp/images/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutButton.setIcon(icon1)
        self.aboutButton.setObjectName("aboutButton")
        self.gridLayout.addWidget(self.aboutButton, 2, 0, 1, 1)
        self.refreshButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        self.refreshButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(
            ":/plugins/ntrrp/images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon2)
        self.refreshButton.setObjectName("refreshButton")
        self.gridLayout.addWidget(self.refreshButton, 2, 2, 1, 1)
        self.downloadButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy)
        self.downloadButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(
            ":/plugins/ntrrp/images/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton.setIcon(icon3)
        self.downloadButton.setObjectName("downloadButton")
        self.gridLayout.addWidget(self.downloadButton, 2, 3, 1, 1)
        self.currentMappingButton = QtWidgets.QPushButton(
            self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.currentMappingButton.sizePolicy().hasHeightForWidth())
        self.currentMappingButton.setSizePolicy(sizePolicy)
        self.currentMappingButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(
            ":/plugins/ntrrp/images/mapdownload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.currentMappingButton.setIcon(icon4)
        self.currentMappingButton.setObjectName("currentMappingButton")
        self.gridLayout.addWidget(self.currentMappingButton, 2, 4, 1, 1)
        self.createButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.createButton.sizePolicy().hasHeightForWidth())
        self.createButton.setSizePolicy(sizePolicy)
        self.createButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(
            ":/plugins/ntrrp/images/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createButton.setIcon(icon5)
        self.createButton.setObjectName("createButton")
        self.gridLayout.addWidget(self.createButton, 2, 5, 1, 1)
        self.approveButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.approveButton.sizePolicy().hasHeightForWidth())
        self.approveButton.setSizePolicy(sizePolicy)
        self.approveButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(
            ":/plugins/ntrrp/images/approve.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.approveButton.setIcon(icon6)
        self.approveButton.setObjectName("approveButton")
        self.gridLayout.addWidget(self.approveButton, 2, 6, 1, 1)
        self.uploadButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.uploadButton.sizePolicy().hasHeightForWidth())
        self.uploadButton.setSizePolicy(sizePolicy)
        self.uploadButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(
            ":/plugins/ntrrp/images/upload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadButton.setIcon(icon7)
        self.uploadButton.setObjectName("uploadButton")
        self.gridLayout.addWidget(self.uploadButton, 2, 7, 1, 1)
        self.activeSourceLayerLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.activeSourceLayerLabel.sizePolicy().hasHeightForWidth())
        self.activeSourceLayerLabel.setSizePolicy(sizePolicy)
        self.activeSourceLayerLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.activeSourceLayerLabel.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.activeSourceLayerLabel.setFont(font)
        self.activeSourceLayerLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.activeSourceLayerLabel.setObjectName("activeSourceLayerLabel")
        self.gridLayout.addWidget(self.activeSourceLayerLabel, 3, 2, 1, 6)
        self.sourceLayerLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sourceLayerLabel.sizePolicy().hasHeightForWidth())
        self.sourceLayerLabel.setSizePolicy(sizePolicy)
        self.sourceLayerLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.sourceLayerLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.sourceLayerLabel.setFont(font)
        self.sourceLayerLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sourceLayerLabel.setObjectName("sourceLayerLabel")
        self.gridLayout.addWidget(self.sourceLayerLabel, 3, 1, 1, 1)
        self.workingLayerComboBox = QtWidgets.QComboBox(
            self.dockWidgetContents)
        self.workingLayerComboBox.setObjectName("workingLayerComboBox")
        self.gridLayout.addWidget(self.workingLayerComboBox, 4, 2, 1, 6)
        self.workingLayerLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.workingLayerLabel.sizePolicy().hasHeightForWidth())
        self.workingLayerLabel.setSizePolicy(sizePolicy)
        self.workingLayerLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.workingLayerLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.workingLayerLabel.setFont(font)
        self.workingLayerLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.workingLayerLabel.setObjectName("workingLayerLabel")
        self.gridLayout.addWidget(self.workingLayerLabel, 4, 1, 1, 1)
        NtrrpDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(NtrrpDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(NtrrpDockWidgetBase)

    def retranslateUi(self, NtrrpDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        NtrrpDockWidgetBase.setToolTip(_translate(
            "NtrrpDockWidgetBase", "NAFI Burnt Areas Mapping"))
        NtrrpDockWidgetBase.setWindowTitle(_translate(
            "NtrrpDockWidgetBase", "NAFI Burnt Areas Mapping"))
        self.regionLabel.setText(_translate(
            "NtrrpDockWidgetBase", "<html><head/><body><p><span style=\" font-weight:600;\">Current region</span></p></body></html>"))
        self.aboutButton.setToolTip(_translate(
            "NtrrpDockWidgetBase", "About NAFI Burnt Areas Mapping …"))
        self.refreshButton.setToolTip(_translate(
            "NtrrpDockWidgetBase", "Refresh Region Layers"))
        self.downloadButton.setToolTip(_translate(
            "NtrrpDockWidgetBase", "Download Burnt Areas"))
        self.currentMappingButton.setToolTip(_translate(
            "NtrrpDockWidgetBase", "Download Current Mapping"))
        self.createButton.setToolTip(_translate(
            "NtrrpDockWidgetBase", "Create Working Burnt Areas Layer"))
        self.approveButton.setToolTip(_translate(
            "NtrrpDockWidgetBase", "Approve Selected Burnt Areas"))
        self.uploadButton.setToolTip(_translate(
            "NtrrpDockWidgetBase", "Upload Burnt Areas"))
        self.activeSourceLayerLabel.setText(_translate(
            "NtrrpDockWidgetBase", "<html><head/><body><p><span style=\" font-weight:600;\">Select segmentation layer …</span></p></body></html>"))
        self.sourceLayerLabel.setText(_translate(
            "NtrrpDockWidgetBase", "<html><head/><body><p><span style=\" font-weight:600;\">Source layer</span></p></body></html>"))
        self.workingLayerLabel.setText(_translate(
            "NtrrpDockWidgetBase", "<html><head/><body><p><span style=\" font-weight:600;\">Working layer</span></p></body></html>"))
