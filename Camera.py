import cv2
from enum import Enum

class Backend(Enum):
    OPENCV = 1
    PICAM = 2

class Camera:
    def __init__(self, backend):
        self._backend = backend
        self._camera = cv2.VideoCapture(0)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

    def capture(self):
        ret_val, image = self._camera.read()
        return image
        print("capture")    