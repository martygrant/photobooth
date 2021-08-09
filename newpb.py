import pygame
import pygame.freetype
import cv2
import numpy as np
import time
import datetime
import os
from enum import Enum
from gpiozero import LED

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

PATH = "photos/"

class PhotoboothState(Enum):
    CAPTURE = 0
    COUNTDOWN = 1
    DISPLAY = 2
    PRINT = 4

state = PhotoboothState.CAPTURE

inputCapture = False
inputReset = False
inputPrint = False

countDown = 5
oldTime = time.time()

cameraFrame = 0
cameraFrameSurface = pygame.Surface((FRAME_W, FRAME_H))

# Inputs - Photobooth buttons (and LEDs) and keyboard
capturePB = -1
captureLED = LED(6)
captureKB = pygame.K_c

resetPB = -1
resetLED = LED(19)
resetKB = pygame.K_r

printPB = -1
printLED = LED(21)
printKB = pygame.K_p

quitKB = pygame.K_ESCAPE



def createLocalDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("INFO: Created directory '%s'" % path)            
    else:
        print("INFO: Directory '%s' already exists" % path)

def savePhotoLocal(photo):
    datetimeStr = "{date:%Y-%m-%d_%H_%M_%S}".format(date=datetime.datetime.now())

    originalFilename = "photobooth_original-{0}.jpg".format(datetimeStr)

    # Save photo locally
    if cv2.imwrite(PATH + originalFilename, photo):
        print("INFO: Saved locally:", originalFilename)
    else:
        print("ERROR: Did not save:", originalFilename)

def savePhotoExternal(photo):
    print("savePhotoExternal")

def savePhotoOnline(photo):
    print("savePhotoOnline")
    #check connection?
    #try upload 
    #if fail add to retry list

def printPhoto(photo, saveLocal, saveExternal, saveOnline):
    print("printPhoto")

    if saveLocal == True:
        savePhotoLocal(photo)
    """
    if saveExternal == True:
        savePhotoExternal(photo)

    if saveOnline == True:
        savePhotoOnline(photo)
    """


def getCamFrame(color, camera):
    global cameraFrame
    retval,frame=camera.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    if not color:
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
    frame=np.rot90(frame)
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

def switchState(newState):
    global state
    oldState = state
    state = newState
    print("INFO: Switching state FROM {0} to {1}.".format(oldState, newState))


def countdownDisplay():
    currentTime = time.time()

    global countDown
    global oldTime

    # 1 second has passed
    if currentTime - oldTime >= 1:
        print("INFO: Capturing photo - {0}s left".format(str(countDown)))
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
            if event.key == quitKB:
                return False
            elif event.key == captureKB:
                inputCapture = True
            elif event.key == resetKB:
                inputReset = True
            elif event.key == printKB:
                inputPrint = True
            #else:

    return True



def update():
    global cameraFrameSurface
    global oldTime

    if state == PhotoboothState.CAPTURE:
        #cameraFrameSurface = getCamFrame(True, camera)
        
        captureLED.on()
        resetLED.off()
        printLED.off()

        if inputCapture == True:
            oldTime = time.time()
            switchState(PhotoboothState.COUNTDOWN)

    elif state == PhotoboothState.COUNTDOWN:
        #cameraFrameSurface = getCamFrame(True, camera)

        captureLED.off()
        resetLED.off()
        printLED.off()

        if countdownDisplay() < 1:
            global countDown
            countDown = 5
            switchState(PhotoboothState.DISPLAY)

    elif state == PhotoboothState.DISPLAY:

        captureLED.off()
        resetLED.on()
        printLED.on()

        if inputReset == True:
            switchState(PhotoboothState.CAPTURE)
        elif inputPrint == True:
            switchState(PhotoboothState.PRINT)

    elif state == PhotoboothState.PRINT:
        printPhoto(cameraFrame, True, True, True)
        switchState(PhotoboothState.CAPTURE)

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
- try new camera?
"""




def main():
    print("Photobooth v2")

    createLocalDirectory(PATH)

    running = True

    while running:
        running = events()
        update()
        render(screen)
    
    #camera.release()
    pygame.quit()

if __name__ == "__main__":
    main()