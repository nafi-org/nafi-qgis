# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\ntrrp_about_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NtrrpAboutDialogBase(object):
    def setupUi(self, NtrrpAboutDialogBase):
        NtrrpAboutDialogBase.setObjectName("NtrrpAboutDialogBase")
        NtrrpAboutDialogBase.resize(1414, 830)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            NtrrpAboutDialogBase.sizePolicy().hasHeightForWidth())
        NtrrpAboutDialogBase.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/ntrrp/images/icon.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NtrrpAboutDialogBase.setWindowIcon(icon)
        self.outerVerticalLayout = QtWidgets.QVBoxLayout(NtrrpAboutDialogBase)
        self.outerVerticalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetFixedSize)
        self.outerVerticalLayout.setObjectName("outerVerticalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.iconLabel = QtWidgets.QLabel(NtrrpAboutDialogBase)
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.iconLabel.setObjectName("iconLabel")
        self.verticalLayout.addWidget(self.iconLabel)
        self.aboutLabel = QtWidgets.QLabel(NtrrpAboutDialogBase)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.aboutLabel.sizePolicy().hasHeightForWidth())
        self.aboutLabel.setSizePolicy(sizePolicy)
        self.aboutLabel.setTextFormat(QtCore.Qt.RichText)
        self.aboutLabel.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.aboutLabel.setWordWrap(True)
        self.aboutLabel.setOpenExternalLinks(True)
        self.aboutLabel.setObjectName("aboutLabel")
        self.verticalLayout.addWidget(self.aboutLabel)
        self.firescarLabel = QtWidgets.QLabel(NtrrpAboutDialogBase)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.firescarLabel.sizePolicy().hasHeightForWidth())
        self.firescarLabel.setSizePolicy(sizePolicy)
        self.firescarLabel.setMaximumSize(QtCore.QSize(16777215, 400))
        self.firescarLabel.setScaledContents(True)
        self.firescarLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.firescarLabel.setObjectName("firescarLabel")
        self.verticalLayout.addWidget(self.firescarLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(NtrrpAboutDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.outerVerticalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(NtrrpAboutDialogBase)
        self.buttonBox.accepted.connect(NtrrpAboutDialogBase.accept)
        QtCore.QMetaObject.connectSlotsByName(NtrrpAboutDialogBase)

    def retranslateUi(self, NtrrpAboutDialogBase):
        _translate = QtCore.QCoreApplication.translate
        NtrrpAboutDialogBase.setWindowTitle(_translate(
            "NtrrpAboutDialogBase", "About NAFI Burnt Areas Mapping"))
        self.iconLabel.setText(
            _translate(
                "NtrrpAboutDialogBase",
                "<html><head/><body><p><img src=\":/plugins/ntrrp/images/icon.png\"/></p></body></html>"))
        self.aboutLabel.setText(_translate("NtrrpAboutDialogBase", "<html><head/><body><p>This plugin is part of a project to provide high resolution burnt area mapping in northern Australia through the active fire season.</p><p>Burnt area mapping is the cornerstone of successful fire management and is essential for assessing planned burn effectiveness and determining what will stop or slow down a wildfire. Current medium resolution mapping available on the Northern Australia Fire Information website (NAFI) is of limited use for fire management in rural subdivisions. </p><p>This plugin helps through facilitating a semi-automated burnt area mapping process that results in freely available burnt area mapping. The mapping is freely available to fire managers and the general public through the NAFI website and the NAFI mobile application and allows users to undertake near real-time assessments of fire spread risk.</p><p><br/><span style=\" font-weight:600;\">Acknowledgment</span>: The development of the plugin was supported by a Northern Territory Government grant (<a href=\"https://cmc.nt.gov.au/supporting-government/northern-territory-risk-reduction-program\"><span style=\" text-decoration: underline; color:#0000ff;\">NTRRP</span></a>) though the <a href=\"https://www.homeaffairs.gov.au/about-us/our-portfolios/emergency-management/resources\"><span style=\" text-decoration: underline; color:#0000ff;\">National Risk Reduction Framework</span></a> initiative. It initially was produced in partnership with <a href=\"https://depws.nt.gov.au/bushfire-information-and-management/about-bushfires-nt/bushfires-nt\"><span style=\" text-decoration: underline; color:#0000ff;\">Bushfires NT</span></a>, <a href=\"https://www.pfes.nt.gov.au\"><span style=\" text-decoration: underline; color:#0000ff;\">NT Police, Fire &amp; Emergency Services</span></a> and the <a href=\"https://bushfireresearch.org.au/\"><span style=\" text-decoration: underline; color:#0000ff;\">Darwin Centre for Bushfire Research</span></a> to support strategic fuel reduction activities and emergency response for the greater Darwin and Katherine areas.</p></body></html>"))
        self.firescarLabel.setText(
            _translate(
                "NtrrpAboutDialogBase",
                "<html><head/><body><p><img src=\":/plugins/ntrrp/images/firescar.jpg\"/></p></body></html>"))
