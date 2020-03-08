import cv2
from PIL import ImageFont, ImageDraw, Image
import cups
import picamera.array
import picamera
from pushover import *
from gpiozero import Button
from signal import pause
from gpiozero import LED
from backup import *
from Camera import *
from globals import *
from GUI import *


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
            draw.text((1400/2-100, 900/2), progStr, font=roboto_font)
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
    
    print("start")

    camera = Camera(WINDOW_W, WINDOW_H, CAPTURE_W, CAPTURE_H, 30, 55, 180, 120)

    running = True
    
    while running:
        cv2.imshow('Photobooth', startScreen())

        k = cv2.waitKey(1)
        if k == BUTTON_CAPTURE:
            smileScreen()
            cv2.waitKey(1)
            
            image = countdownDisplay(COUNTDOWN_TIME, camera)
            outputDisplay(image)

            while True:
                k = cv2.waitKey(1)
                if k == BUTTON_STARTOVER:
                    print("startover")
                    break
                if k == BUTTON_PRINT:
                    print("print")
                    cv2.imshow('Photobooth', printScreen())

                    save(image)
                    
                    cv2.waitKey(3000)
                    break

        if k == BUTTON_EXIT:
            running = False
            
    #camera.__del__
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
def leftButtonAction():
    test = 1
    
def middleButtonAction():
    originalFrame = countdown(COUNTDOWN_TIME)
    
def rightButtonAction():
    test = 1
"""
