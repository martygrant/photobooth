import numpy as np
import cv2
import time
import os
import threading
from random import randint
from copy import deepcopy
import platform
from random import randrange
if platform.system() == 'Darwin':
    RASPI = 0
elif platform.system() == 'Raspberry Pi':
    RASPI = 1
    import picamera.array
    import picamera
    from pushover import *
    from gpiozero import Button
    from signal import pause
    from gpiozero import LED
from time import sleep
from PIL import ImageFont, ImageDraw, Image
import cups
from backup import *
from Camera import *
from globals import *
from GUI import *


if RASPI:
    camera = picamera.PiCamera()#sensor_mode=2)
    resw = 3280
    resh = 2464
    camera.resolution = (resw,resh)
    camera.framerate = 15
    camera.brightness = 55
    #camera.contrast = 8
    #camera.video_stabilization = True
    #camera.exposure_mode = 'auto'
    camera.rotation = 180
    rawCapture = picamera.array.PiRGBArray(camera, size=(resw,resh))
    time.sleep(1)

    leftButton = Button(4)
    #leftButton.when_pressed = leftButtonAction

    middleButton = Button(22)
    #middleButton.when_pressed = middleButtonAction

    rightButton = Button(17)
    #rightButton.when_pressed = rightButtonAction

    leftLight = LED(19)
    middleLight = LED(6)
    rightLight = LED(21)

else:
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)


# printing
conn = cups.Connection()
printers = conn.getPrinters()
canonPrinter = list(printers.keys())[0] # 0 for canon, 1 for pdf


def printImage(image):
    screen = createFrameBlack()
        
    image = cv2.resize(image, None, fx=0.12, fy=0.12)
    cv2.imwrite("print/scaled_print.jpg", image)

    #job = conn.printFile(canonPrinter, "//home/pi/Desktop/photobooth/print/scaled_print.jpg", "", {'fit-to-page':'True'})
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
        

# what is this??? either gdrive or pushover
def get_key(filename):
    with open(filename) as f:
        key = f.read().strip()
    return key


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
    
    camera.close()
    
    middleLight.on()
    leftLight.off()
    rightLight.off()


if __name__ == "__main__":
    #main()

    cv2.namedWindow("Photobooth", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Photobooth', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    #cv2.moveWindow("Photobooth", 0, 900)

    camera = Camera("opencv")

    buttonCapture = ord('c')
    buttonStartOver = ord('s')
    buttonPrint = ord('p')

    print("start")

    while True:
        cv2.imshow('Photobooth', startScreen())

        k = cv2.waitKey(1)
        if k == buttonCapture:
            image = countdownDisplay(3, camera)
            outputDisplay(image)
            
            while True:
                k = cv2.waitKey(1)
                if k == buttonStartOver:
                    print("startover")
                    break
                if k == buttonPrint:
                    print("print")
                    cv2.imshow('Photobooth', printScreen())
                    saveThread = threading.Thread(target=savePhoto, args=(image,))
                    saveThread.start() # python threads kill themselves once completed
                    cv2.waitKey(3000)
                    break

cv2.waitKey(0)
#camera.release()
cv2.destroyAllWindows()




"""
press button
    flash buttons until button pressed
    button pressed
        button lights off
        start preview countdown
        update preview display
        take image once preview finishes
        show final image with start over / print
        left/right button lights on
        start over
            reset 
        print
            save to file, external disc and cloud
            check print supplies
            send to printer
            update display with print status
            update print supplies
            send notification if supplies low
            reset
        reset

"""


"""
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
"""



"""
def run():
    old = time.time()
    while (True):
        #print("Ready...")

        # show start message
        cv2.imshow('Photobooth', pressButtonFrame)
        
        if RASPI:
            now = time.time()

            middleLight.on()
            leftLight.off()
            rightLight.off()

            # wait for button press
            # TODOOOO IN MORNING TRY DOING WAITKEY 1000+ TO BLINK LIGHT?
            if now - old >= 1:
                print("1 sec and", randrange(10))
                middleLight.off()
                old = time.time()
        
        
        k = cv2.waitKey(1)
        if k == BUTTON_CAPTURE:# or middleButton.is_pressed:        
            print("Capture")
            # ORIGINAL frame (from camera)
            if RASPI:
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
                if RASPI:
                    leftLight.on()
                    rightLight.on()
                
                if k == BUTTON_STARTOVER:# or leftButton.is_pressed:
                    print("Startover")                    
                    nxt = True
                if k == BUTTON_PRINT:# or rightButton.is_pressed:
                    print("Print")                    
                    savePhoto(originalFrame, stylisedFrame)

                    #printPhoto(originalFrame)
                    #printImage(originalFrame)
                    nxt = True
        if k == 113:
            break
"""


"""
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
"""

"""
def leftButtonAction():
    test = 1
    
def middleButtonAction():
    originalFrame = countdown(COUNTDOWN_TIME)
    
def rightButtonAction():
    test = 1
"""