import numpy as np
import cv2
import time
import os
import datetime
import threading
from copy import deepcopy

WINDOW_W = 512
WINDOW_H = 512

OUTPUT_PATH = "photos"

COUNTDOWN_TIME = 3

CAPTURE_TEXT = "Press Button (b)"
CAPTURE_X = (WINDOW_W / 2) - 50
CAPTURE_Y = WINDOW_H / 2
CAPTURE_SIZE = 1
CAPTURE_THICKNESS = 1

STARTOVER_TEXT = "Start Over (s)"
STARTOVER_X = 30
STARTOVER_Y = WINDOW_H - 60
STARTOVER_SIZE = 1
STARTOVER_THICKNESS = 1

PRINT_TEXT = "Print! (p)"
PRINT_TEXT_X = WINDOW_W - 50
PRINT_TEXT_Y = WINDOW_H - 60
PRINT_TEXT_SIZE = 1
PRINT_TEXT_THICKNESS = 1

BUTTON_CAPTURE = 98
BUTTON_STARTOVER = 115
BUTTON_PRINT = 112

""" notes
keep original frame size to export
error checking, output logs
photo meta data
display slideshow after period of inactivity
specific button press to start slideshow
"""


camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

window = cv2.namedWindow("Photobooth")
cv2.moveWindow("Photobooth", 380, 120)

font = cv2.FONT_HERSHEY_SIMPLEX

img = np.zeros((WINDOW_W, WINDOW_H, 3), np.uint8)



def writeTextCentered(frame, text, size, thickness):
    textsize = cv2.getTextSize(text, font, 1, 2)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    textY = (frame.shape[0] + textsize[1]) / 2

    writeText(frame, text, textX, textY, size, thickness)

def writeText(frame, text, x, y, size, thickness):
    cv2.putText(frame, text, (x, y), font, size, (255, 255, 255), thickness, cv2.LINE_AA)

def createFrameBlack():
    return np.zeros((WINDOW_W, WINDOW_H, 3), np.uint8)



def countdown(count):
    oldtime = time.time()
    secs = 0
    while True:
        currenttime = time.time()

        #print(count)
        #img = np.zeros((WINDOW_W, WINDOW_H, 3), np.uint8)
        
        ret_val, img = camera.read()

        writeTextCentered(img, str(count - secs), 4, 2)
        cv2.imshow('Photobooth', img)
        cv2.waitKey(1)
        img = createFrameBlack()

        print(secs)

        if currenttime - oldtime >= 1:
            secs += 1
            oldtime = time.time()

        if secs >= count:
            ret, frame = camera.read()
            #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
            #frame = cv2.resize(frame, (512, 512)) 
            return frame



def createExportDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("Created directory '%s'" % path)
    else:
        print("Directory '%s' already exists" % path)


createExportDirectory(OUTPUT_PATH)
pressButtonFrame = np.zeros((WINDOW_W, WINDOW_H, 3), np.uint8)
writeTextCentered(pressButtonFrame, CAPTURE_TEXT, CAPTURE_SIZE, CAPTURE_THICKNESS)

while (True):
    print("Ready...")

    # show start message
    cv2.imshow('Photobooth', pressButtonFrame)
    # wait for button press
    k = cv2.waitKey(0)
    if k == BUTTON_CAPTURE:
        print("Capture")
        # get camera frame after countdown
        frame = countdown(COUNTDOWN_TIME)
        
        # make a copy of camera frame to 
        dispframe = deepcopy(frame)
        cv2.rectangle(dispframe, (0, WINDOW_H - 100), (800, WINDOW_H), (0, 0, 0), -1)

        alpha = 0.6
        dispframe = cv2.addWeighted(dispframe, alpha, frame, 1 - alpha, 0)

        # write start over and print text
        writeText(dispframe, STARTOVER_TEXT, STARTOVER_X, STARTOVER_Y, STARTOVER_SIZE, STARTOVER_THICKNESS)
        writeText(dispframe, PRINT_TEXT, PRINT_TEXT_X, PRINT_TEXT_Y, PRINT_TEXT_SIZE, PRINT_TEXT_THICKNESS)
        
        # display frame
        cv2.imshow('Photobooth', dispframe)

        # wait until start over or print is selected
        nxt = False
        while not nxt:
            k = cv2.waitKey(0)
            if k == BUTTON_STARTOVER:
                print("Startover")
                nxt = True
            if k == BUTTON_PRINT:
                print("Print")
                filename = '{dir}/photobooth-{date:%Y-%m-%d_%H_%M_%S}.jpeg'.format(dir=OUTPUT_PATH, date=datetime.datetime.now())
                cv2.imwrite(filename, frame)
                nxt = True
        

cv2.waitKey(0)


"""
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    writeText(frame, "yo")

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
"""

cap.release()
cv2.destroyAllWindows()