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
        NafiAboutDialogBase.resize(1000, 1200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NafiAboutDialogBase.sizePolicy().hasHeightForWidth())
        NafiAboutDialogBase.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/nafi/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NafiAboutDialogBase.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(NafiAboutDialogBase)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 990, 1190))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NafiAboutDialogBase)
        self.buttonBox.accepted.connect(NafiAboutDialogBase.accept)
        QtCore.QMetaObject.connectSlotsByName(NafiAboutDialogBase)

    def retranslateUi(self, NafiAboutDialogBase):
        _translate = QtCore.QCoreApplication.translate
        NafiAboutDialogBase.setWindowTitle(_translate("NafiAboutDialogBase", "About NAFI Fire Maps"))
        self.label.setText(_translate("NafiAboutDialogBase", "<html><head/><body><p>This plugin provides an easy method to search and discover fire mapping layers from the <a href=\"https://firenorth.org.au\"><span style=\" text-decoration: underline; color:#0000ff;\">Northern Australia and rangelands Fire Information</span></a> (NAFI) program, and upload them to the QGIS map window. The Open Geospatial Compliant (OGC) WMS layers represent fire activity based on information from satellites, such as hotspots (locations of recently burning fires) and fire scars (maps of recently burnt country). The maps are displayed to meet the needs of north Australian and remote area fire managers.</p><p>Hotspots are sourced from Landgate Western Australia and Geoscience Australia (from NOAA and NASA satellites). Firescars are sourced from the Darwin Centre for Bushfires Research at Charles Darwin University (for NT and northern WA fire scars) and from FNQ Spatial Data Services (for Queensland).</p><p>The services are hosted at Charles Darwin University and funded by NAFI’s <a href=\"https://firenorth.org.au/nafi3/views/about/supporters.htm\"><span style=\" text-decoration: underline; color:#0000ff;\">supporters</span></a>. This plugin was developed by Gaia Resources.</p><p><br/></p><p><span style=\" font-weight:600;\">Terms of use</span></p><p>The information available from this plugin is to be used as a management tool only, and is dependent on the availability and functioning of satellites. The information is able to determine relative temperature differences or &quot;hotspots&quot;, but is not intended to be able to determine the cause of or identify the nature of such &quot;hotspots&quot;. Reliance on, or actions based on this information must therefore be made with caution.</p><p>This plugin includes a Google Maps base map service, the use of which is subject to <a href=\"https://maps.google.com/help/terms_maps/\"><span style=\" text-decoration: underline; color:#0000ff;\">Google Maps Additional Terms of Service</span></a> and <a href=\"https://www.google.com/policies/privacy/\"><span style=\" text-decoration: underline; color:#0000ff;\">Google Privacy Policy</span></a>.</p><p>To the extent permitted by law, the copyright holders (including its employees and consultants) exclude all liability to any person for any consequences, including but not limited to all losses, damages, costs, expenses and any other compensation, arising directly or indirectly from using these services (in part or in whole) and any information or material contained in it.</p></body></html>"))

