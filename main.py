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
import picamera.array
import picamera
from pushover import *
from gpiozero import Button
from signal import pause
from gpiozero import LED
from time import sleep
from PIL import ImageFont, ImageDraw, Image
import cups

WINDOW_W = 1440
WINDOW_H = 900

OUTPUT_PATH = str(os.getcwd()) + "/photos/"
OUTPUT_STYLE = 0 # 0 = POLAROID, 1 = OVERLAY GRAPHIC

COUNTDOWN_TIME = 3
COUNTDOWN_SIZE = 6
COUNTDOWN_THICKNESS = 5
COUNTDOWN_OVERLAY_X = WINDOW_W / 2
COUNTDOWN_OVERLAY_Y = (WINDOW_H / 2)
COUNTDOWN_OVERLAY_W = COUNTDOWN_OVERLAY_X + 200
COUNTDOWN_OVERLAY_H = COUNTDOWN_OVERLAY_Y + 200

CAPTURE_TEXT = "Press the middle button"
CAPTURE_TEXT2 = "below to take a photo!"
CAPTURE_TEXT3 = "You have " + str(COUNTDOWN_TIME) + " seconds to pose!"
CAPTURE_X = (WINDOW_W / 2) - 50
CAPTURE_Y = (WINDOW_H / 2) 
CAPTURE_SIZE = 3.5
CAPTURE_THICKNESS = 3

STARTOVER_TEXT = "Start Over"
STARTOVER_X = 50
STARTOVER_Y = WINDOW_H - 130
STARTOVER_SIZE = 3
STARTOVER_THICKNESS = 3

PRINT_TEXT = "Print Photo!"
PRINT_TEXT_X = WINDOW_W - 600
PRINT_TEXT_Y = WINDOW_H - 130
PRINT_TEXT_SIZE = 3
PRINT_TEXT_THICKNESS = 3

arrow = cv2.imread('arrow.png', cv2.IMREAD_UNCHANGED)
arrow = cv2.resize(arrow, None, fx=0.4, fy=0.4)


BUTTON_CAPTURE = 98
BUTTON_STARTOVER = 115
BUTTON_PRINT = 112

COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)


resw = 3280
resh = 2464

camera = picamera.PiCamera()#sensor_mode=2)
camera.resolution = (resw,resh)
camera.framerate = 15
#camera.brightness = 60
camera.rotation = 180
rawCapture = picamera.array.PiRGBArray(camera, size=(resw,resh))
time.sleep(1)


window = cv2.namedWindow("Photobooth", cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Photobooth', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#cv2.moveWindow("Photobooth", 0, 900)

FONT_NORMAL = cv2.FONT_HERSHEY_SIMPLEX
FONT_ITALIC = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
roboto = ImageFont.truetype("Roboto-Regular.ttf", 148)


# GOOGLE DRIVE
#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#drive = GoogleDrive(gauth)



# printing
conn = cups.Connection()
printers = conn.getPrinters()
canonPrinter = list(printers.keys())[0] # 0 for canon, 1 for pdf

"""
def leftButtonAction():
    test = 1
    
def middleButtonAction():
    originalFrame = countdown(COUNTDOWN_TIME)
    
def rightButtonAction():
    test = 1
"""

leftButton = Button(4)
#leftButton.when_pressed = leftButtonAction

middleButton = Button(22)
#middleButton.when_pressed = middleButtonAction

rightButton = Button(17)
#rightButton.when_pressed = rightButtonAction



leftLight = LED(21)
middleLight = LED(6)
rightLight = LED(19)

def writeTextCentered(frame, text, font, size, thickness, colour):
    textsize = cv2.getTextSize(text, font, size, thickness)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    textY = (frame.shape[0] + textsize[1]) / 2

    writeText(frame, text, textX, textY, font, size, thickness, colour)

def writeTextCenteredHorizontal(frame, text, y, font, size, thickness, colour):
    textsize = cv2.getTextSize(text, font, size, thickness)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    
    writeText(frame, text, textX, y, font, size, thickness, colour)

def writeText(frame, text, x, y, font, size, thickness, colour):
    cv2.putText(frame, text, (int(x), int(y)), font, size, colour, thickness, cv2.LINE_AA)

def createFrameBlack():
    return np.zeros((WINDOW_H, WINDOW_W, 3), np.uint8)
    

def countdown(countdown):
    oldtime = time.time()
    
    img = None
    firstRun = True

    while True:
        currenttime = time.time()
        #print(dir(camera))

        if currenttime - oldtime >= 1 or firstRun == True:
            countdown -= 1
            oldtime = time.time()
            print(countdown)

            # get image from camera
            camera.capture(rawCapture, 'bgr')#, use_video_port=False)
            img = rawCapture.array

            # make preview fit window
            img = cv2.resize(img, (1440, 900))

            # write countdown on image
            overlay = img.copy()
            if countdown != 0:
                cv2.rectangle(overlay, (620, 550), (820, 750), COLOUR_BLACK, -1)
                alpha = 0.3
                cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
                writeTextCenteredHorizontal(img, str(countdown), 710, FONT_NORMAL, COUNTDOWN_SIZE, COUNTDOWN_THICKNESS, COLOUR_WHITE)
            else:
                cv2.rectangle(overlay, (320, 550), (1120, 750), COLOUR_BLACK, -1)
                alpha = 0.3
                cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
                writeTextCenteredHorizontal(img, "Cheese!", 710, FONT_NORMAL, COUNTDOWN_SIZE, COUNTDOWN_THICKNESS+1, COLOUR_WHITE)


            # display image
            cv2.imshow('Photobooth', img)
            cv2.waitKey(1)

            # reset camera
            rawCapture.seek(0)
            rawCapture.truncate(0)

            if firstRun == True:
                firstRun = False

        if countdown < 1:     
            camera.capture(rawCapture, 'bgr', use_video_port=False)
            rawCapture.seek(0)
            rawCapture.truncate(0)
            return rawCapture.array



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



pressButtonFrame = np.zeros((WINDOW_H, WINDOW_W, 3), np.uint8)
writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT, CAPTURE_Y - 50, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT2, CAPTURE_Y + 70, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT3, CAPTURE_Y + 300, FONT_NORMAL, 2.5, CAPTURE_THICKNESS, COLOUR_WHITE)


def addOutputOptionsToDisplayFrame(frame):
    x = 0
    y = WINDOW_H - 230
    w = WINDOW_W
    h = 300

    overlay = frame.copy()
    
    cv2.rectangle(overlay, (x, y), (x+w, y+h), COLOUR_BLACK, -1)
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # write start over and print text
    writeText(frame, STARTOVER_TEXT, STARTOVER_X, STARTOVER_Y, FONT_NORMAL, STARTOVER_SIZE, STARTOVER_THICKNESS, COLOUR_WHITE)
    writeText(frame, PRINT_TEXT, PRINT_TEXT_X, PRINT_TEXT_Y, FONT_NORMAL, PRINT_TEXT_SIZE, PRINT_TEXT_THICKNESS, COLOUR_WHITE)

    overlay_transparent(frame, arrow, STARTOVER_X + 150, STARTOVER_Y + 20)
    overlay_transparent(frame, arrow, PRINT_TEXT_X + 290, STARTOVER_Y + 20)


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


def createExportDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("SUCCESS: Created directory '%s'" % path)
            
    else:
        print("INFO: Directory '%s' already exists" % path)


def CheckInternetConnection(host="8.8.8.8", port=53, timeout=3):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    print("SUCCESS: Connected to internet.")
    return True
  except socket.error as ex:
    print("ERROR: No internet connection:", ex)
    return False
    

def backupToGoogleDrive(filename, photo):
    if CheckInternetConnection():
        http = drive.auth.Get_Http_Object()
        
        folder_id = "1U1aCTd_K84IdQQ9_z1UUkZt7EbEk9_qT"
        #file1 = drive.CreateFile({'title': 'photobooth/Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
        driveFile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}], "title": filename})

        driveFile.SetContentFile(OUTPUT_PATH + filename)
        #file1.SetContentString('Hello World!') # Set content of the file from given string.
        driveFile.Upload(param={"http": http})
            
        print("SUCCESS: Uploaded to GDrive:", filename)
    else:
        print("ERROR: Did not save to GDrive. No internet connection.")

    """ get IDs for files/folders
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:       
        print ('title: %s, id: %s' % (file1['title'], file1['id']))
    """

def checkUSBConnected():
    if not os.path.exists("/media/pi/2A47-4A89/photobooth/"):
        print("ERROR: USB Drive not found.")
        return False
    else:
        print("SUCCESS: USB Drive connected.")
        return True


def saveToUSB(filename, image):
    path = "/media/pi/2A47-4A89/photobooth/"
    if checkUSBConnected() == True:
        cv2.imwrite(path + filename, image)
        print("SUCCESS: Saved to USB Drive:", filename)
    else:
        print("ERROR: Did not save to USB Drive:", filename) 


def savePhoto(original, stylised):
    # Save photo locally
    filenameOriginal = 'photobooth-{date:%Y-%m-%d_%H_%M_%S}_original.jpeg'.format(date=datetime.datetime.now())
    cv2.imwrite(OUTPUT_PATH + filenameOriginal, original)
    print("SUCCESS: Saved locally:", filenameOriginal)
    
    filenameStylised = 'photobooth-{date:%Y-%m-%d_%H_%M_%S}_stylised.jpeg'.format(date=datetime.datetime.now())
    cv2.imwrite(OUTPUT_PATH + filenameStylised, stylised)
    print("SUCCESS: Saved locally:", filenameStylised)

    old = time.time()
    
    # Save photo to remote backup
    # todo check if drive object exists
    uploadThreadOne = threading.Thread(target=backupToGoogleDrive, args=(filenameOriginal, original))
    uploadThreadOne.start()
    uploadThreadTwo = threading.Thread(target=backupToGoogleDrive, args=(filenameStylised, stylised))
    uploadThreadTwo.start()

    # TODO PROBABLY DON'T NEED TO WAIT, TAKES ~2SECS, RESEARCH THIS
    uploadThreadOne.join()
    uploadThreadTwo.join()

    now = time.time()
    print("upload took", now - old)
        
    # Save photo to external usb drive
    saveToUSB(filenameOriginal, original)
    saveToUSB(filenameStylised, stylised)


def printImage(image):
    screen = createFrameBlack()
    
    job = conn.printTestPage(canonPrinter)
    print("print job " + str(job))
    
    while True:
        if conn.getJobs().get(job, None) is not None:
            jobProgress = conn.getJobAttributes(job)['job-media-progress']
            print(jobProgress)
            time.sleep(2)
            
            writeTextCenteredHorizontal(screen, "Printing your photo...", 900/2 - 100, FONT_NORMAL, 4, 4, COLOUR_WHITE)    
            progStr = "{0}%".format(str(jobProgress))

            cv2_im_rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im_rgb)
            draw = ImageDraw.Draw(pil_im)
            draw.text((1400/2-100, 900/2), progStr, font=roboto)
            screen = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
            
            cv2.imshow('Photobooth', screen)
            cv2.waitKey(1000)
            screen = createFrameBlack()
                        
        else:
            # should wait for 5 secs or so
            # TODO IN MORNING MODIFY THE LAST SLEEP HERE
            print("done printing, finishing!")
            
            cv2.waitKey(5000)
            writeTextCenteredHorizontal(screen, "Collect your photo below!", 900/2, FONT_NORMAL, 3.5, 4, COLOUR_WHITE)
            cv2.imshow('Photobooth', screen)
            cv2.waitKey(4000)
            break
        

def get_key(filename):
    with open(filename) as f:
        key = f.read().strip()
    return key

from random import randrange

def run():
    old = time.time()
    while (True):
        #print("Ready...")

        now = time.time()

        middleLight.on()
        leftLight.off()
        rightLight.off()

        # show start message
        cv2.imshow('Photobooth', pressButtonFrame)
        # wait for button press
        
        # TODOOOO IN MORNING TRY DOING WAITKEY 1000+ TO BLINK LIGHT?
        if now - old >= 1:
            print("1 sec and", randrange(10))
            middleLight.off()
            old = time.time()
        
        
        k = cv2.waitKey(1)
        if k == BUTTON_CAPTURE or middleButton.is_pressed:        
            print("Capture")
            # ORIGINAL frame (from camera)
            middleLight.off()
            originalFrame = countdown(COUNTDOWN_TIME)

            # STYLISED frame (for printing)
            stylisedFrame = deepcopy(originalFrame)
            if OUTPUT_STYLE == 0:
                stylisedFrame = overlayPolaroidFrame(stylisedFrame)
            else:
                overlayGraphicFrame(stylisedFrame)

            # DISPLAY frame (for screen)
            dispframe = deepcopy(originalFrame)            
            # add black bar at bottom for button text
            dispframe = cv2.resize(dispframe, (1440, 900))
            addOutputOptionsToDisplayFrame(dispframe)
            
            cv2.imshow('Photobooth', dispframe)

            # wait until start over or print is selected
            nxt = False
            while not nxt:
                k = cv2.waitKey(1)
                leftLight.on()
                rightLight.on()
                
                if k == BUTTON_STARTOVER or leftButton.is_pressed:
                    print("Startover")                    
                    nxt = True
                if k == BUTTON_PRINT or rightButton.is_pressed:
                    print("Print")                    
                    savePhoto(originalFrame, stylisedFrame)
                    printImage(originalFrame)
                    nxt = True
        if k == 113:
            break
                            

def main():
    # Check if we have an internet connection
    """if CheckInternetConnection() == True:
        
        
        # Create a local export directory
        createExportDirectory(OUTPUT_PATH)

        checkUSBConnected()
        
        run()

    else:
        run()
        print("not connected")
    """

    createExportDirectory(OUTPUT_PATH)
    CheckInternetConnection()
    checkUSBConnected()

    run()
    """
    push_user = get_key(os.path.join(os.path.dirname(__file__), 'pushuser.key'))
    push_api = get_key(os.path.join(os.path.dirname(__file__), 'pushapi.key'))
    
    pusher = PushoverSender(push_user, push_api)
    pusher.send("from rpi")"""
    
    camera.close()
    
    middleLight.on()
    leftLight.off()
    rightLight.off()


if __name__ == "__main__":
    main()
    


cv2.waitKey(0)

#camera.release()
cv2.destroyAllWindows()
