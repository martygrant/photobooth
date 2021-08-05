import pygame
import pygame.freetype
import cv2
import numpy as np
import time
import datetime
import os
from enum import Enum

SCREEN_W = 600
SCREEN_H = 600

FRAME_W = 400
FRAME_H = 400

CAPTURE_W = 400
CAPTURE_H = 400

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Photobooth v2")
GAME_FONT = pygame.freetype.Font("Castoro-Regular.ttf", 24)


class PhotoboothState(Enum):
    CAPTURE = 0
    COUNTDOWN = 1
    DISPLAY = 2
    PRINT = 4

inputCapture = False
inputReset = False
inputPrint = False

state = PhotoboothState.CAPTURE

cameraFrame = 0
cameraFrameSurface = pygame.Surface((FRAME_W, FRAME_H))

countDown = 5
oldTime = time.time()

"""
class Camera:
    def __init__(self, width, height, fps, brightness):
        self._backend = backend
        if self._backend == Backend.OPENCV:
            self._camera = cv2.VideoCapture(0)
            self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self._camera.set(cv2.CAP_PROP_FPS, fps)
            self._camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness / 100)
    def capture(self):
        ret_val, image = self._camera.read()
        return image
    def __del__(self): 
        self._camera.release()
"""

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_W)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_H)
#camera.set(cv2.CAP_PROP_FPS, 60)
#camera.set(cv2.CAP_PROP_BRIGHTNESS, 1)

PATH = "photos/"

def createLocalDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("SUCCESS: Created directory '%s'" % path)            
    else:
        print("INFO: Directory '%s' already exists" % path)

def savePhotoLocal(photo):
    datetimeStr = "{date:%Y-%m-%d_%H_%M_%S}".format(date=datetime.datetime.now())

    originalFilename = "photobooth_original-{0}.jpg".format(datetimeStr)

    # Save photo locally
    if cv2.imwrite(PATH + originalFilename, photo):
        print("SUCCESS: Saved locally:", originalFilename)
    else:
        print("FAILURE: Did not save:", originalFilename)

def savePhotoExternal(photo):
    print("savePhotoExternal")

def savePhotoOnline(photo):
    print("savePhotoOnline")
    #check connection?
    #try upload 
    #if fail add to retry list

def printPhoto(photo, saveLocal, saveExternal, saveOnline):
    print("printPhoto")
    
    photo=cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    
    if saveLocal == True:
        savePhotoLocal(photo)

    if saveExternal == True:
        savePhotoExternal(photo)

    if saveOnline == True:
        savePhotoOnline(photo)



def getCamFrame(color, camera):
    global cameraFrame
    retval,frame=camera.read()
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if not color:
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame=cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    frame=np.rot90(frame, -1)
    frame = cv2.resize(frame, (FRAME_W, FRAME_H))
    cameraFrame = frame
    frame=pygame.surfarray.make_surface(frame)
    return frame

def blitCamFrame(frame, screen):
    screen.blit(frame,(0,0))
    return screen


def renderTextCentered(string, y):
    text_surface, rect = GAME_FONT.render(string, (0, 0, 0))
    screen.blit(text_surface, (SCREEN_W/2 - rect.centerx, y))
    
def renderText(string, x, y):
    text_surface, rect = GAME_FONT.render(string, (0, 0, 0))
    screen.blit(text_surface, (x, y))


def countdownDisplay():
    currentTime = time.time()

    global countDown
    global oldTime

    # 1 second has passed
    if currentTime - oldTime >= 1:
        print("preview countdown {0}s left".format(str(countDown)))
        countDown -= 1
        oldTime = time.time()

    return countDown


def events():
    global inputCapture
    global inputReset
    global inputPrint
    
    inputCapture = False   
    inputReset = False
    inputPrint = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_c:
                inputCapture = True
            elif event.key == pygame.K_r:
                inputReset = True
            elif event.key == pygame.K_p:
                inputPrint = True
            #else:

    return True



def update():
    global cameraFrameSurface
    global state
    global oldTime

    if state == PhotoboothState.CAPTURE:
        cameraFrameSurface = getCamFrame(True, camera)
        if inputCapture == True:
            oldTime = time.time()
            state = PhotoboothState.COUNTDOWN

    elif state == PhotoboothState.COUNTDOWN:
        cameraFrameSurface = getCamFrame(True, camera)
        if countdownDisplay() < 1:
            global countDown
            countDown = 5
            state = PhotoboothState.DISPLAY 

    elif state == PhotoboothState.DISPLAY:
        if inputReset == True:
            state = PhotoboothState.CAPTURE
        elif inputPrint == True:
            state = PhotoboothState.PRINT

    elif state == PhotoboothState.PRINT:
        printPhoto(cameraFrame, True, True, True)
        state = PhotoboothState.CAPTURE

    else:
        print("blah")


def render(screen):
    screen.fill((255,255,255))

    background = pygame.Surface((410, 410))
    background = background.convert()
    background.fill((255, 0, 0))

    screen.blit(background, (95, 95))

    if state == PhotoboothState.CAPTURE:
        renderTextCentered("CAPTURE", 40)
        renderTextCentered("(C)apture", 65)
        screen.blit(cameraFrameSurface, (100, 100))

    elif state == PhotoboothState.COUNTDOWN:
        renderTextCentered("COUNTDOWN", 40)
        renderTextCentered(str(countDown), 65)
        screen.blit(cameraFrameSurface, (100, 100))

    elif state == PhotoboothState.DISPLAY:
        renderTextCentered("(R)eset | (P)rint", 65)
        renderTextCentered("DISPLAY", 40)
        screen.blit(cameraFrameSurface, (100, 100))

    elif state == PhotoboothState.PRINT:
        renderTextCentered("PRINT", 40)

    else:
        print("Invalid state.")

    pygame.display.flip()


"""
todo:
- save to gdrive
- save to usb
- UI setup
- camera params
- frame/window/display sizes
- rpi cam
- rpi buttons + LEDs
- print
- notifications?
- logging
"""




def main():
    print("Photobooth v2")

    createLocalDirectory(PATH)

    running = True

    while running:
        running = events()
        update()
        render(screen)
    
    camera.release()
    pygame.quit()

if __name__ == "__main__":
    main()
