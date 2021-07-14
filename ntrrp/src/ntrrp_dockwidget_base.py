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
        icon.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NtrrpDockWidgetBase.setWindowIcon(icon)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.refreshButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        self.refreshButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon1)
        self.refreshButton.setObjectName("refreshButton")
        self.gridLayout.addWidget(self.refreshButton, 2, 3, 1, 1)
        self.downloadButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy)
        self.downloadButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton.setIcon(icon2)
        self.downloadButton.setObjectName("downloadButton")
        self.gridLayout.addWidget(self.downloadButton, 2, 4, 1, 1)
        self.approveButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.approveButton.sizePolicy().hasHeightForWidth())
        self.approveButton.setSizePolicy(sizePolicy)
        self.approveButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/approve.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.approveButton.setIcon(icon3)
        self.approveButton.setObjectName("approveButton")
        self.gridLayout.addWidget(self.approveButton, 2, 5, 1, 1)
        self.uploadButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uploadButton.sizePolicy().hasHeightForWidth())
        self.uploadButton.setSizePolicy(sizePolicy)
        self.uploadButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/upload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadButton.setIcon(icon4)
        self.uploadButton.setObjectName("uploadButton")
        self.gridLayout.addWidget(self.uploadButton, 2, 6, 1, 1)
        self.aboutButton = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aboutButton.sizePolicy().hasHeightForWidth())
        self.aboutButton.setSizePolicy(sizePolicy)
        self.aboutButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutButton.setIcon(icon5)
        self.aboutButton.setObjectName("aboutButton")
        self.gridLayout.addWidget(self.aboutButton, 2, 0, 1, 1)
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 7)
        self.regionComboBox = QtWidgets.QComboBox(self.dockWidgetContents)
        self.regionComboBox.setObjectName("regionComboBox")
        self.gridLayout.addWidget(self.regionComboBox, 0, 2, 1, 5)
        self.regionLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regionLabel.sizePolicy().hasHeightForWidth())
        self.regionLabel.setSizePolicy(sizePolicy)
        self.regionLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.regionLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.regionLabel.setFont(font)
        self.regionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.regionLabel.setObjectName("regionLabel")
        self.gridLayout.addWidget(self.regionLabel, 0, 1, 1, 1)
        self.sourceFeaturesComboBox = QtWidgets.QComboBox(self.dockWidgetContents)
        self.sourceFeaturesComboBox.setObjectName("sourceFeaturesComboBox")
        self.gridLayout.addWidget(self.sourceFeaturesComboBox, 3, 2, 1, 5)
        self.sourceFeaturesLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sourceFeaturesLabel.sizePolicy().hasHeightForWidth())
        self.sourceFeaturesLabel.setSizePolicy(sizePolicy)
        self.sourceFeaturesLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.sourceFeaturesLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.sourceFeaturesLabel.setFont(font)
        self.sourceFeaturesLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sourceFeaturesLabel.setObjectName("sourceFeaturesLabel")
        self.gridLayout.addWidget(self.sourceFeaturesLabel, 3, 1, 1, 1)
        self.finalFeaturesComboBox = QtWidgets.QComboBox(self.dockWidgetContents)
        self.finalFeaturesComboBox.setObjectName("finalFeaturesComboBox")
        self.gridLayout.addWidget(self.finalFeaturesComboBox, 4, 2, 1, 5)
        self.finalFeaturesLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finalFeaturesLabel.sizePolicy().hasHeightForWidth())
        self.finalFeaturesLabel.setSizePolicy(sizePolicy)
        self.finalFeaturesLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.finalFeaturesLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.finalFeaturesLabel.setFont(font)
        self.finalFeaturesLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.finalFeaturesLabel.setObjectName("finalFeaturesLabel")
        self.gridLayout.addWidget(self.finalFeaturesLabel, 4, 1, 1, 1)
        NtrrpDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(NtrrpDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(NtrrpDockWidgetBase)

    def retranslateUi(self, NtrrpDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        NtrrpDockWidgetBase.setToolTip(_translate("NtrrpDockWidgetBase", "NAFI Burnt Areas Mapping"))
        NtrrpDockWidgetBase.setWindowTitle(_translate("NtrrpDockWidgetBase", "NAFI Burnt Areas Mapping"))
        self.refreshButton.setToolTip(_translate("NtrrpDockWidgetBase", "Refresh Region Layers"))
        self.downloadButton.setToolTip(_translate("NtrrpDockWidgetBase", "Download Burnt Areas"))
        self.approveButton.setToolTip(_translate("NtrrpDockWidgetBase", "Approve Selected Burnt Areas"))
        self.uploadButton.setToolTip(_translate("NtrrpDockWidgetBase", "Upload Burnt Areas"))
        self.aboutButton.setToolTip(_translate("NtrrpDockWidgetBase", "About NTRRP …"))
        self.regionLabel.setText(_translate("NtrrpDockWidgetBase", "<html><head/><body><p><span style=\" font-weight:600;\">Current region</span></p></body></html>"))
        self.sourceFeaturesLabel.setText(_translate("NtrrpDockWidgetBase", "<html><head/><body><p><span style=\" font-weight:600;\">Source features</span></p></body></html>"))
        self.finalFeaturesLabel.setText(_translate("NtrrpDockWidgetBase", "<html><head/><body><p><span style=\" font-weight:600;\">Final features</span></p></body></html>"))

