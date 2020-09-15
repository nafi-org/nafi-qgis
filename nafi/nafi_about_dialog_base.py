# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nafi_about_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NafiAboutDialogBase(object):
    def setupUi(self, NafiAboutDialogBase):
        NafiAboutDialogBase.setObjectName("NafiAboutDialogBase")
        NafiAboutDialogBase.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/nafi/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NafiAboutDialogBase.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(NafiAboutDialogBase)
        self.buttonBox.setGeometry(QtCore.QRect(50, 260, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(NafiAboutDialogBase)
        self.buttonBox.accepted.connect(NafiAboutDialogBase.accept)
        QtCore.QMetaObject.connectSlotsByName(NafiAboutDialogBase)

    def retranslateUi(self, NafiAboutDialogBase):
        _translate = QtCore.QCoreApplication.translate
        NafiAboutDialogBase.setWindowTitle(_translate("NafiAboutDialogBase", "About NAFI Fire Maps"))

