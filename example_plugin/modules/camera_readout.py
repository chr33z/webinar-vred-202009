from vrAEBase import vrAEBase
import vrCamera
import math

class cameraPositionReadout(vrAEBase):
    '''
    Camera Position Readout:
    Read camera position in 3D space and update pass it to the action function
    '''

    def __init__(self, action):
        vrAEBase.__init__(self)
        self.action = action
        self.addLoop()

    def recEvent(self, state):
        vrAEBase.recEvent(self, state)

    def loop(self):
        camera = vrCamera.getActiveCameraNode()

        height = camera.getLocalTranslation()[2]
        lookdown = 90 - camera.getRotation()[0]

        x = camera.getLocalTranslation()[0]
        y = camera.getLocalTranslation()[1]
        distance_to_origin = math.sqrt(x ** 2 + y ** 2)

        try:
            self.action(height, lookdown, distance_to_origin)
        except:
            pass