import uiTools
from PySide2 import QtCore, QtGui, QtUiTools, QtWidgets
import vrController
import os
import sys
import vrVariants

def modulePath():
    version = vrController.getVredVersion()
    path = os.path.join(os.path.expanduser('~'), "Documents", "Autodesk", "VRED-" + version, "modules")
    return path

# Add module path to pythons system path to be able to import the custom modules
sys.path.append(modulePath())

# Import plugin specific modules
import logger
from render_snapshots import renderSnapshotsToDirectory
import camera_readout

example_plugin_form, example_plugin_base = uiTools.loadUiType('example_plugin.ui')

class examplePluginInterface(example_plugin_form, example_plugin_base):
    '''
    Main example plugin interface
    '''
    
    def __init__(self, parent=None):
        super(examplePluginInterface, self).__init__(parent)
        parent.layout().addWidget(self)
        self.parent = parent
        self.setupUi(self)
        self.initializeInterface()

    def initializeInterface(self):
        '''
        Initialize the plugins user interface
        '''
        self._render_snapshots_local.clicked.connect(self.renderSnapshotsLocal)
        self._render_snapshots_plugin.clicked.connect(self.renderSnapshotsPlugin)
        self.initializeCameraReadout()

    def renderSnapshotsLocal(self):
        '''
        Render snapshots by calling the variant set tool in the scene
        '''
        logger.info("Render snapshot local", self)
        # vrVariants.selectVariantSet('RenderSnapshots_local')
        vrVariants.selectVariantSet('RenderSnapshots_local')

    def renderSnapshotsPlugin(self):
        '''
        Render snapshots using the plugins imported modules
        '''
        logger.info("Render snapshot plugin", self)
        renderSnapshotsToDirectory()

    def initializeCameraReadout(self):
        '''
        Initialize the camera readout script
        '''
        self.cameraPositionReadout = camera_readout.cameraPositionReadout(lambda a, b, c: self.setCameraPositionReadout(a, b, c))
        self.cameraPositionReadout.setActive(True)

    def setCameraPositionReadout(self, height, lookdown, intersection):
        '''
        Set the camera position readout from the camera readout module in the interface
        '''
        cam_string = "Camera Location:<br/>"
        cam_string = cam_string + "Height: " + ("%.2f" % (height / 1000.0)) + " m<br/>"
        cam_string = cam_string + "Angle: " + ("%.1f" % lookdown) + " deg<br/>"
        cam_string = cam_string + "Distance to Origin: " + ("%.2f" % (intersection / 1000.0)) + " m<br/>"
        self._camera_label.setText(cam_string)

plugin = examplePluginInterface(VREDPluginWidget)