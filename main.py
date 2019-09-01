import numpy as np
import cv2
import time
import os
import datetime
import threading
from random import randint
from copy import deepcopy
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import socket

WINDOW_W = 512
WINDOW_H = 512

OUTPUT_PATH = "photos"
OUTPUT_STYLE = 0 # 0 = POLAROID, 1 = OVERLAY GRAPHIC

COUNTDOWN_TIME = 2

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

COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)


camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

window = cv2.namedWindow("Photobooth")
cv2.moveWindow("Photobooth", 380, 120)

FONT_NORMAL = cv2.FONT_HERSHEY_SIMPLEX
FONT_ITALIC = cv2.FONT_HERSHEY_SCRIPT_COMPLEX


# GOOGLE DRIVE
#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#drive = GoogleDrive(gauth)




def writeTextCentered(frame, text, font, size, thickness, colour):
    textsize = cv2.getTextSize(text, font, 1, 2)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    textY = (frame.shape[0] + textsize[1]) / 2

    writeText(frame, text, textX, textY, font, size, thickness, colour)

def writeTextCenteredHorizontal(frame, text, y, font, size, thickness, colour):
    textsize = cv2.getTextSize(text, font, 1, 2)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    
    writeText(frame, text, textX, y, font, size, thickness, colour)

def writeText(frame, text, x, y, font, size, thickness, colour):
    cv2.putText(frame, text, (x, y), font, size, colour, thickness, cv2.LINE_AA)

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

        writeTextCentered(img, str(count - secs), FONT_NORMAL, 4, 2, COLOUR_WHITE)
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


def CheckInternetConnection(host="8.8.8.8", port=53, timeout=3):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except socket.error as ex:
    print(ex)
    return False


def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image




pressButtonFrame = np.zeros((WINDOW_W, WINDOW_H, 3), np.uint8)
writeTextCentered(pressButtonFrame, CAPTURE_TEXT, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)


def addOutputOptionsToDisplayFrame(frame):
    cv2.rectangle(frame, (0, WINDOW_H - 100), (800, WINDOW_H), COLOUR_BLACK, -1)
    alpha = 0.6
    frame = cv2.addWeighted(frame, alpha, originalFrame, 1 - alpha, 0)

    # write start over and print text
    writeText(dispframe, STARTOVER_TEXT, STARTOVER_X, STARTOVER_Y, FONT_NORMAL, STARTOVER_SIZE, STARTOVER_THICKNESS, COLOUR_WHITE)
    writeText(dispframe, PRINT_TEXT, PRINT_TEXT_X, PRINT_TEXT_Y, FONT_NORMAL, PRINT_TEXT_SIZE, PRINT_TEXT_THICKNESS, COLOUR_WHITE)
        


def overlayGraphicFrame(frame):
    overlay = cv2.imread('overlay.png', cv2.IMREAD_UNCHANGED)
    overlay_transparent(frame, overlay, 30, WINDOW_H - 120)

def overlayPolaroidFrame(frame):
    top = int(0.05 * frame.shape[0])  # shape[0] = rows
    bottom = int(0.15 * frame.shape[0])
    left = int(0.05 * frame.shape[1])  # shape[1] = cols
    right = left
    newf = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, None, COLOUR_WHITE)
    writeTextCenteredHorizontal(newf, "Rebecca & Harry - Mar Hall - 2019", newf.shape[0] - 30, FONT_ITALIC, STARTOVER_SIZE, STARTOVER_THICKNESS, COLOUR_BLACK)
    return newf
    

def backupToDrive(filename, photo):
    folder_id = "1U1aCTd_K84IdQQ9_z1UUkZt7EbEk9_qT"
    #file1 = drive.CreateFile({'title': 'photobooth/Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
    driveFile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}], "title": filename})

    driveFile.SetContentFile(OUTPUT_PATH + filename)
    #file1.SetContentString('Hello World!') # Set content of the file from given string.
    driveFile.Upload()

    """ get IDs for files/folders
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:       
        print ('title: %s, id: %s' % (file1['title'], file1['id']))
    """


def savePhoto(original, stylised):
    # Save photo locally
    filenameOriginal = 'photobooth-{date:%Y-%m-%d_%H_%M_%S}_original.jpeg'.format(date=datetime.datetime.now())
    cv2.imwrite(OUTPUT_PATH + filenameOriginal, original)
    filenameStylised = 'photobooth-{date:%Y-%m-%d_%H_%M_%S}_stylised.jpeg'.format(date=datetime.datetime.now())
    cv2.imwrite(OUTPUT_PATH + filenameStylised, stylised)

    # Save photo to remote backup
    backupToDrive(filenameOriginal, original)
    backupToDrive(filenameStylised, stylised)


def run():
    while (True):
        print("Ready...")

        # show start message
        cv2.imshow('Photobooth', pressButtonFrame)
        # wait for button press
        k = cv2.waitKey(0)
        if k == BUTTON_CAPTURE:
            print("Capture")
            # get camera frame after countdown
            originalFrame = countdown(COUNTDOWN_TIME)
            overlayFrame = deepcopy(originalFrame)
            
            # add black bar at bottom for button text
            dispframe = deepcopy(originalFrame)
            
            addOutputOptionsToDisplayFrame(dispframe)

            # overlay style
            if OUTPUT_STYLE == 0:
                overlayFrame = overlayPolaroidFrame(overlayFrame)
            else:
                overlayGraphicFrame(overlayFrame)

            
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
                    savePhoto(originalFrame, overlayFrame)
                    nxt = True
            










def main():
    print("Startup")
    # Check if we have an internet connection
    if CheckInternetConnection() == True:
        # Create a local export directory
        createExportDirectory(OUTPUT_PATH)
        
        run()

    else:
        print("not connected")


if __name__ == "__main__":
    main()
    


cv2.waitKey(0)

camera.release()
cv2.destroyAllWindows()