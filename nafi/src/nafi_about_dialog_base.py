# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\nafi_about_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NafiAboutDialogBase(object):
    def setupUi(self, NafiAboutDialogBase):
        NafiAboutDialogBase.setObjectName("NafiAboutDialogBase")
        NafiAboutDialogBase.resize(1414, 830)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NafiAboutDialogBase.sizePolicy().hasHeightForWidth())
        NafiAboutDialogBase.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/nafi/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NafiAboutDialogBase.setWindowIcon(icon)
        self.outerVerticalLayout = QtWidgets.QVBoxLayout(NafiAboutDialogBase)
        self.outerVerticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.outerVerticalLayout.setObjectName("outerVerticalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.iconLabel = QtWidgets.QLabel(NafiAboutDialogBase)
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.iconLabel.setObjectName("iconLabel")
        self.verticalLayout.addWidget(self.iconLabel)
        self.aboutLabel = QtWidgets.QLabel(NafiAboutDialogBase)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aboutLabel.sizePolicy().hasHeightForWidth())
        self.aboutLabel.setSizePolicy(sizePolicy)
        self.aboutLabel.setTextFormat(QtCore.Qt.RichText)
        self.aboutLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.aboutLabel.setWordWrap(True)
        self.aboutLabel.setOpenExternalLinks(True)
        self.aboutLabel.setObjectName("aboutLabel")
        self.verticalLayout.addWidget(self.aboutLabel)
        self.firescarLabel = QtWidgets.QLabel(NafiAboutDialogBase)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firescarLabel.sizePolicy().hasHeightForWidth())
        self.firescarLabel.setSizePolicy(sizePolicy)
        self.firescarLabel.setMaximumSize(QtCore.QSize(16777215, 400))
        self.firescarLabel.setScaledContents(True)
        self.firescarLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.firescarLabel.setObjectName("firescarLabel")
        self.verticalLayout.addWidget(self.firescarLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(NafiAboutDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.outerVerticalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(NafiAboutDialogBase)
        self.buttonBox.accepted.connect(NafiAboutDialogBase.accept)
        QtCore.QMetaObject.connectSlotsByName(NafiAboutDialogBase)

    def retranslateUi(self, NafiAboutDialogBase):
        _translate = QtCore.QCoreApplication.translate
        NafiAboutDialogBase.setWindowTitle(_translate("NafiAboutDialogBase", "About NAFI Fire Maps"))
        self.iconLabel.setText(_translate("NafiAboutDialogBase", "<html><head/><body><p><img src=\":/plugins/nafi/images/icon.png\"/></p></body></html>"))
        self.aboutLabel.setText(_translate("NafiAboutDialogBase", "<html><head/><body><p>This plugin provides an easy method to search and discover fire mapping layers from the <a href=\"https://firenorth.org.au\"><span style=\" text-decoration: underline; color:#0000ff;\">Northern Australia and rangelands Fire Information</span></a> (NAFI) program, and upload them to the QGIS map window. The Open Geospatial Compliant (OGC) WMS layers represent fire activity based on information from satellites, such as hotspots (locations of recently burning fires) and fire scars (maps of recently burnt country). The maps are displayed to meet the needs of north Australian and remote area fire managers.</p><p>Hotspots are sourced from Landgate Western Australia and Geoscience Australia (from NOAA and NASA satellites). Firescars are sourced from the Darwin Centre for Bushfires Research at Charles Darwin University (for NT and northern WA fire scars) and from FNQ Spatial Data Services (for Queensland).</p><p>The services are hosted at Charles Darwin University and funded by NAFI’s <a href=\"https://firenorth.org.au/nafi3/views/about/supporters.htm\"><span style=\" text-decoration: underline; color:#0000ff;\">supporters</span></a>. This plugin was developed by Gaia Resources.</p><p><br/></p><p><span style=\" font-weight:600;\">Terms of use</span></p><p>The information available from this plugin is to be used as a management tool only, and is dependent on the availability and functioning of satellites. The information is able to determine relative temperature differences or &quot;hotspots&quot;, but is not intended to be able to determine the cause of or identify the nature of such &quot;hotspots&quot;. Reliance on, or actions based on this information must therefore be made with caution.</p><p>This plugin includes a Google Maps base map service, the use of which is subject to <a href=\"https://maps.google.com/help/terms_maps/\"><span style=\" text-decoration: underline; color:#0000ff;\">Google Maps Additional Terms of Service</span></a> and <a href=\"https://www.google.com/policies/privacy/\"><span style=\" text-decoration: underline; color:#0000ff;\">Google Privacy Policy</span></a>.</p><p>To the extent permitted by law, the copyright holders (including its employees and consultants) exclude all liability to any person for any consequences, including but not limited to all losses, damages, costs, expenses and any other compensation, arising directly or indirectly from using these services (in part or in whole) and any information or material contained in it.</p></body></html>"))
        self.firescarLabel.setText(_translate("NafiAboutDialogBase", "<html><head/><body><p><img src=\":/plugins/nafi/images/firescar.jpg\"/></p></body></html>"))

