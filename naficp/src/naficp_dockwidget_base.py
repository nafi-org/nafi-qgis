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
        NafiCpDockWidgetBase.resize(464, 297)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.sourceLayerLayout = QtWidgets.QHBoxLayout()
        self.sourceLayerLayout.setObjectName("sourceLayerLayout")
        self.sourceLayerLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sourceLayerLabel.sizePolicy().hasHeightForWidth())
        self.sourceLayerLabel.setSizePolicy(sizePolicy)
        self.sourceLayerLabel.setObjectName("sourceLayerLabel")
        self.sourceLayerLayout.addWidget(self.sourceLayerLabel)
        self.sourceLayerComboBox = QgsMapLayerComboBox(self.dockWidgetContents)
        self.sourceLayerComboBox.setObjectName("sourceLayerComboBox")
        self.sourceLayerLayout.addWidget(self.sourceLayerComboBox)
        self.gridLayout.addLayout(self.sourceLayerLayout, 0, 0, 1, 1)
        self.workingLayerLayout = QtWidgets.QHBoxLayout()
        self.workingLayerLayout.setObjectName("workingLayerLayout")
        self.workingLayerLabel = QtWidgets.QLabel(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workingLayerLabel.sizePolicy().hasHeightForWidth())
        self.workingLayerLabel.setSizePolicy(sizePolicy)
        self.workingLayerLabel.setObjectName("workingLayerLabel")
        self.workingLayerLayout.addWidget(self.workingLayerLabel)
        self.workingLayerComboBox = QgsMapLayerComboBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workingLayerComboBox.sizePolicy().hasHeightForWidth())
        self.workingLayerComboBox.setSizePolicy(sizePolicy)
        self.workingLayerComboBox.setObjectName("workingLayerComboBox")
        self.workingLayerLayout.addWidget(self.workingLayerComboBox)
        self.gridLayout.addLayout(self.workingLayerLayout, 1, 0, 1, 1)
        self.pasteFeaturesButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pasteFeaturesButton.setObjectName("pasteFeaturesButton")
        self.gridLayout.addWidget(self.pasteFeaturesButton, 2, 0, 1, 1)
        NafiCpDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(NafiCpDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(NafiCpDockWidgetBase)

    def retranslateUi(self, NafiCpDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        NafiCpDockWidgetBase.setWindowTitle(_translate("NafiCpDockWidgetBase", "NAFI Copy and Paste"))
        self.sourceLayerLabel.setText(_translate("NafiCpDockWidgetBase", "Select source layer"))
        self.workingLayerLabel.setText(_translate("NafiCpDockWidgetBase", "Select working layer"))
        self.pasteFeaturesButton.setToolTip(_translate("NafiCpDockWidgetBase", "Click, or press the \'Q\' key to paste features"))
        self.pasteFeaturesButton.setText(_translate("NafiCpDockWidgetBase", "Paste features (Ctrl+Z)"))

from qgsmaplayercombobox import QgsMapLayerComboBox
