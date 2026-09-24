# Form implementation generated from reading ui file 'ui\nafi_about_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui, QtWidgets

from .scaled_image_label import ScaledImageLabel


class Ui_NafiAboutDialogBase(object):
    def setupUi(self, NafiAboutDialogBase):
        NafiAboutDialogBase.setObjectName("NafiAboutDialogBase")
        NafiAboutDialogBase.resize(960, 860)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            NafiAboutDialogBase.sizePolicy().hasHeightForWidth()
        )
        NafiAboutDialogBase.setSizePolicy(sizePolicy)
        NafiAboutDialogBase.setMinimumSize(QtCore.QSize(680, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/plugins/nafi/images/icon.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        NafiAboutDialogBase.setWindowIcon(icon)
        self.outerVerticalLayout = QtWidgets.QVBoxLayout(NafiAboutDialogBase)
        self.outerVerticalLayout.setObjectName("outerVerticalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.iconLabel = ScaledImageLabel(NafiAboutDialogBase)
        self.iconLabel.setPixmap(QtGui.QPixmap(":/plugins/nafi/images/logo.png"))
        self.iconLabel.setObjectName("iconLabel")
        self.verticalLayout.addWidget(self.iconLabel)
        self.aboutBrowser = QtWidgets.QTextBrowser(NafiAboutDialogBase)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.aboutBrowser.sizePolicy().hasHeightForWidth())
        self.aboutBrowser.setSizePolicy(sizePolicy)
        self.aboutBrowser.setMinimumSize(QtCore.QSize(0, 160))
        self.aboutBrowser.setStyleSheet("background: transparent;")
        self.aboutBrowser.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.aboutBrowser.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.aboutBrowser.setOpenExternalLinks(True)
        self.aboutBrowser.setObjectName("aboutBrowser")
        self.verticalLayout.addWidget(self.aboutBrowser)
        self.firescarLabel = ScaledImageLabel(NafiAboutDialogBase)
        self.firescarLabel.setMaximumSize(QtCore.QSize(16777215, 400))
        self.firescarLabel.setPixmap(QtGui.QPixmap(":/plugins/nafi/images/firescar.jpg"))
        self.firescarLabel.setObjectName("firescarLabel")
        self.verticalLayout.addWidget(self.firescarLabel)
        self.footerLayout = QtWidgets.QHBoxLayout()
        self.footerLayout.setObjectName("footerLayout")
        self.versionLabel = QtWidgets.QLabel(NafiAboutDialogBase)
        self.versionLabel.setStyleSheet("color: palette(mid);")
        self.versionLabel.setObjectName("versionLabel")
        self.footerLayout.addWidget(self.versionLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(NafiAboutDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.footerLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.footerLayout)
        self.outerVerticalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(NafiAboutDialogBase)
        self.buttonBox.accepted.connect(NafiAboutDialogBase.accept)
        QtCore.QMetaObject.connectSlotsByName(NafiAboutDialogBase)

    def retranslateUi(self, NafiAboutDialogBase):
        _translate = QtCore.QCoreApplication.translate
        NafiAboutDialogBase.setWindowTitle(
            _translate("NafiAboutDialogBase", "About NAFI Fire Maps")
        )
        self.aboutBrowser.setHtml(
            _translate(
                "NafiAboutDialogBase",
                '<html><head/><body><p>This plugin provides an easy method to search and discover fire mapping layers from the <a href="https://firenorth.org.au"><span style=" text-decoration: underline; color:#0000ff;">Northern Australia and rangelands Fire Information</span></a> (NAFI) program, and upload them to the QGIS map window. The Open Geospatial Compliant (OGC) WMS layers represent fire activity based on information from satellites, such as hotspots (locations of recently burning fires) and fire scars (maps of recently burnt country). The maps are displayed to meet the needs of north Australian and remote area fire managers.</p><p>Hotspots are sourced from Landgate Western Australia and Geoscience Australia (from NOAA and NASA satellites). Firescars are sourced from the Darwin Centre for Bushfires Research at Charles Darwin University (for NT and northern WA fire scars) and from FNQ Spatial Data Services (for Queensland).</p><p>The services are hosted at Charles Darwin University and funded by NAFI’s <a href="https://firenorth.org.au/nafi4/supporters"><span style=" text-decoration: underline; color:#0000ff;">supporters</span></a>. This plugin was developed by Gaia Resources in 2020 and has been enhanced by Trailmarker since then.</p><p style=" margin-top:24px;"><span style=" font-weight:600;">Terms of use and attributions</span></p><p>The information available from this plugin is to be used as a management tool only, and is dependent on the availability and functioning of satellites. The information is able to determine relative temperature differences or &quot;hotspots&quot;, but is not intended to be able to determine the cause of or identify the nature of such &quot;hotspots&quot;. Reliance on, or actions based on this information must therefore be made with caution.</p><p>This plugin includes a Google Maps base map service, the use of which is subject to <a href="https://maps.google.com/help/terms_maps/"><span style=" text-decoration: underline; color:#0000ff;">Google Maps Additional Terms of Service</span></a> and <a href="https://www.google.com/policies/privacy/"><span style=" text-decoration: underline; color:#0000ff;">Google Privacy Policy</span></a>.</p><p>To the extent permitted by law, the copyright holders (including its employees and consultants) exclude all liability to any person for any consequences, including but not limited to all losses, damages, costs, expenses and any other compensation, arising directly or indirectly from using these services (in part or in whole) and any information or material contained in it.</p><p>The icons in this application were made by <a href="https://www.flaticon.com/authors/dave-gandy"><span style=" text-decoration: underline; color:#0000ff;">Dave Gandy</span></a> and <a href="https://www.flaticon.com/authors/turkkub"><span style=" text-decoration: underline; color:#0000ff;">turkkub</span></a> and used under an open licence from <a href="https://www.flaticon.com"><span style=" text-decoration: underline; color:#0000ff;">Flaticon</span></a>.</p></body></html>',
            )
        )
