import time
import cv2
import numpy as np

COLOUR_WHITE = (255, 255, 255)
FONT_NORMAL = cv2.FONT_HERSHEY_SIMPLEX
WINDOW_W = 1440
WINDOW_H = 900


def createFrameBlack():
    return np.zeros((WINDOW_H, WINDOW_W, 3), np.uint8)

def writeText(frame, text, x, y, font, size, thickness, colour):
    cv2.putText(frame, text, (int(x), int(y)), font, size, colour, thickness, cv2.LINE_AA)

def writeTextCentered(frame, text, font, size, thickness, colour):
    textsize = cv2.getTextSize(text, font, size, thickness)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    textY = (frame.shape[0] + textsize[1]) / 2



class Camera:
    def __init__(self, backend, previewDuration):
        self._backend = backend
        self._previewDuration = previewDuration
        self._previewRunning = False
        self._previewImage = "test"
        self._camera = cv2.VideoCapture(0)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

    def previewCountdown(self):
        print("previewCountdown")

        self.previewRunning = True

        oldTime = time.time()
        timeLeft = self._previewDuration
        while True:
            currentTime = time.time()


            ret_val, img = self._camera.read()

            writeTextCentered(img, str(timeLeft), FONT_NORMAL, 4, 2, COLOUR_WHITE)
            cv2.imshow('Photobooth', img)
            cv2.waitKey(1)
            img = createFrameBlack()

            # 1 second has passed
            if currentTime - oldTime >= 1:
                print("preview countdown {0}s left".format(str(timeLeft)))
                timeLeft -= 1
                oldTime = time.time()

            # countdown finished
            if timeLeft < 1:
                print("finished preview")
                self._previewImage = self._camera.read()
                self._previewRunning = False
                return

    def isPreviewRunning(self):
        return self._previewRunning

    def getPreviewImage(self):
        return self._previewImage

    def capture(self):
        print("capture")