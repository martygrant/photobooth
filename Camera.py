import cv2
import picamera.array # todo check system type
import picamera
import time
from enum import Enum

class Backend(Enum):
    OPENCV = 0
    PICAM = 1

class Camera:
    def __init__(self, backend, width, height, fps, brightness):
        self._backend = backend
        if self._backend == Backend.OPENCV:
            self._camera = cv2.VideoCapture(0)
            self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self._camera.set(cv2.CAP_PROP_FPS, fps)
            self._camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness / 100)
        if self._backend == Backend.PICAM:
            self._camera = picamera.PiCamera()#sensor_mode=2)
            self._camera.resolution = (width,height)
            self._camera.framerate = fps
            self._camera.brightness = brightness
            #camera.contrast = 8
            #camera.video_stabilization = True
            #camera.exposure_mode = 'auto'
            #camera.rotation = 180
            self._rawCapture = picamera.array.PiRGBArray(self._camera, size=(width,height))
            time.sleep(1)

    def set(self, width, height, fps):
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._camera.set(cv2.CAP_PROP_FPS, fps)

    def capture(self):
        if self._backend == Backend.OPENCV:
            ret_val, image = self._camera.read()
            return image
        if self._backend == Backend.PICAM:
            self._camera.capture(self._rawCapture, 'rgb', use_video_port=False)
            img = self._rawCapture.array
            # reset camera
            self._rawCapture.seek(0)
            self._rawCapture.truncate(0)
            return img
         
    #def __del__(self): 
        #self._camera.release() # todo clean up
