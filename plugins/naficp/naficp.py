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

        # Initialize locale. QSettings().value() may return None headless or on a
        # fresh profile, so fall back to English before slicing.
        locale = (QSettings().value("locale/userLocale") or "en")[0:2]
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

        self.pasteFeaturesAction = QAction("Paste Features", QgsInterface.mainWindow())
        self.setActiveLayerAsSourceLayerAction = QAction(
            "Set Active Layer as Source Layer", QgsInterface.mainWindow()
        )
        self.setActiveLayerAsWorkingLayerAction = QAction(
            "Set Active Layer as Working Layer", QgsInterface.mainWindow()
        )

        self.pasteFeaturesHotKey = None
        self.setActiveLayerAsSourceLayerHotKey = None
        self.setActiveLayerAsWorkingLayerHotKey = None
        self.refreshHotKeys()

        # Vector-menu registration happens once; shortcuts are refreshed per-run.
        QgsInterface.addPluginToVectorMenu(NAFICP_NAME, self.pasteFeaturesAction)
        QgsInterface.addPluginToVectorMenu(
            NAFICP_NAME, self.setActiveLayerAsSourceLayerAction
        )
        QgsInterface.addPluginToVectorMenu(
            NAFICP_NAME, self.setActiveLayerAsWorkingLayerAction
        )

    def refreshHotKeys(self):
        """Re-read naficp.json and re-register any action whose shortcut changed.

        Called from initGui() on startup and from run() on each open, so edits to
        naficp.json are picked up without needing a full plugin reload.
        """
        desired = [
            (self.pasteFeaturesAction, getConfiguredPasteFeaturesHotKey()),
            (
                self.setActiveLayerAsSourceLayerAction,
                getConfiguredSetActiveLayerAsSourceLayerHotKey(),
            ),
            (
                self.setActiveLayerAsWorkingLayerAction,
                getConfiguredSetActiveLayerAsWorkingLayerHotKey(),
            ),
        ]

        for action, shortcut in desired:
            if action.shortcut().toString() != shortcut:
                # Unregister is safe even if the action was never registered.
                QgsInterface.unregisterMainWindowAction(action)
                QgsInterface.registerMainWindowAction(action, shortcut)

        self.pasteFeaturesHotKey = desired[0][1]
        self.setActiveLayerAsSourceLayerHotKey = desired[1][1]
        self.setActiveLayerAsWorkingLayerHotKey = desired[2][1]

    # --------------------------------------------------------------------------

    def onClosePlugin(self):
        """Tear down the dockwidget so the next run() builds a fresh one."""

        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # Drop triggered-signal connections so the old dockwidget can be GC'd.
        for action, slot_name in (
            (self.pasteFeaturesAction, "copySelectedFeaturesFromSourceLayer"),
            (self.setActiveLayerAsSourceLayerAction, "setActiveLayerAsSourceLayer"),
            (self.setActiveLayerAsWorkingLayerAction, "setActiveLayerAsWorkingLayer"),
        ):
            try:
                action.triggered.disconnect(getattr(self.dockwidget, slot_name))
            except TypeError:
                pass  # not connected — nothing to do

        self.iface.removeDockWidget(self.dockwidget)
        self.dockwidget.deleteLater()
        self.dockwidget = None
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

        if self.pluginIsActive:
            return

        self.pluginIsActive = True

        # Re-read naficp.json on every open so edits to hotkeys take effect
        # without a full plugin reload.
        self.refreshHotKeys()

        # Always build a fresh dockwidget — the shortcut text is baked into the
        # label at construction time, so a stale widget would show stale labels.
        self.dockwidget = NafiCpDockWidget(
            self.pasteFeaturesHotKey,
            self.pasteFeaturesAction,
            self.setActiveLayerAsSourceLayerHotKey,
            self.setActiveLayerAsSourceLayerAction,
            self.setActiveLayerAsWorkingLayerHotKey,
            self.setActiveLayerAsWorkingLayerAction,
        )
        self.dockwidget.closingPlugin.connect(self.onClosePlugin)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
        self.dockwidget.show()
