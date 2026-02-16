import os.path

from qgis.PyQt.QtCore import QCoreApplication, QSettings, Qt, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface as QgsInterface

# Initialize Qt resources from file resources.py
from .resources_rc import *

# Import the code for the DockWidget
from .src.naficp_dockwidget import NafiCpDockWidget
from .src.utils import (
    NAFICP_NAME,
    getConfiguredPasteFeaturesHotKey,
    getConfiguredSetActiveLayerAsSourceLayerHotKey,
    getConfiguredSetActiveLayerAsWorkingLayerHotKey,
    guiWarning,
)


class NafiCp:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # Initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "NafiCp_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("&" + NAFICP_NAME)
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar("NafiCp")
        self.toolbar.setObjectName("NafiCp")

        # print "** INITIALIZING NafiCp"

        self.pluginIsActive = False
        self.dockwidget = None

    # noinspection PyMethodMayBeStatic

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("NafiCp", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ":/plugins/naficp/images/icon.png"
        self.add_action(
            icon_path,
            text=self.tr(NAFICP_NAME),
            add_to_toolbar=True,
            callback=self.run,
            parent=self.iface.mainWindow(),
        )

        self.pasteFeaturesHotKey = getConfiguredPasteFeaturesHotKey()
        self.pasteFeaturesAction = QAction("Paste Features", QgsInterface.mainWindow())

        self.setActiveLayerAsSourceLayerHotKey = (
            getConfiguredSetActiveLayerAsSourceLayerHotKey()
        )
        self.setActiveLayerAsSourceLayerAction = QAction(
            "Set Active Layer as Source Layer", QgsInterface.mainWindow()
        )

        self.setActiveLayerAsWorkingLayerHotKey = (
            getConfiguredSetActiveLayerAsWorkingLayerHotKey()
        )
        self.setActiveLayerAsWorkingLayerAction = QAction(
            "Set Active Layer as Working Layer", QgsInterface.mainWindow()
        )

        QgsInterface.registerMainWindowAction(
            self.pasteFeaturesAction, self.pasteFeaturesHotKey
        )

        QgsInterface.registerMainWindowAction(
            self.setActiveLayerAsSourceLayerAction,
            self.setActiveLayerAsSourceLayerHotKey,
        )

        QgsInterface.registerMainWindowAction(
            self.setActiveLayerAsWorkingLayerAction,
            self.setActiveLayerAsWorkingLayerHotKey,
        )

        # Won't work without calling this method?
        QgsInterface.addPluginToVectorMenu(NAFICP_NAME, self.pasteFeaturesAction)
        QgsInterface.addPluginToVectorMenu(
            NAFICP_NAME, self.setActiveLayerAsSourceLayerAction
        )
        QgsInterface.addPluginToVectorMenu(
            NAFICP_NAME, self.setActiveLayerAsWorkingLayerAction
        )

    # --------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # Disconnect the closingPlugin signal from the dockwidget to this method
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # Remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened

        # Commented next statement since it causes QGIS crash
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        # Remove all 'Easy Copy and Paste' actions
        nafiCpMenuActions = [
            a for a in QgsInterface.vectorMenu().actions() if NAFICP_NAME in a.text()
        ]

        for menuAction in nafiCpMenuActions:
            QgsInterface.vectorMenu().removeAction(menuAction)

        for mainWindowAction in [
            self.pasteFeaturesAction,
            self.setActiveLayerAsSourceLayerAction,
            self.setActiveLayerAsWorkingLayerAction,
        ]:
            if not QgsInterface.unregisterMainWindowAction(mainWindowAction):
                guiWarning(f"Error unregistering '{mainWindowAction.text()}' action.")

        # Remove all plug-in actions
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(NAFICP_NAME), action)
            self.iface.removeToolBarIcon(action)

        # Remove the toolbar
        del self.toolbar

    # --------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # Dockwidget may not exist if:
            #    First run of plugin
            #    Removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = NafiCpDockWidget(
                    self.pasteFeaturesHotKey,
                    self.pasteFeaturesAction,
                    self.setActiveLayerAsSourceLayerAction,
                    self.setActiveLayerAsWorkingLayerAction,
                )

            # Connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # Show the dockwidget
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
