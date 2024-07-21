import cv2
import picamera
from pushover import *
from gpiozero import Button
from gpiozero import PWMLED
from gpiozero import LED
from signal import pause
from backup import *
from Camera import *
from globals import *
from GUI import *
from cupsprint import *



# todo 
# read docs on camera specific settings i.e. white balance etc
# turnoff screensaver
# maybe have a gap between countdown overlays
# maybe add all countdown overlays at start and just swap layers during countdown
# print countdown timing?
# "smile" appears for a sec between screens
# handle ink/paper errors
# print a page explaining loading paper
# turn off automatic paper type register on printer
# try gdrive again and see if auth problem happens again
# configure light patterns
# there is a blur around photos, try to reposition camera
# capture banner has no alpha on monitor?
# gif during countdown?


if __name__ == "__main__":
    leftLED = PWMLED(26)
    #leftLED.pulse()

    rightLED = PWMLED(21)
    #rightLED.pulse()

    midLED = PWMLED(6)
    midLED.pulse()

    leftButton = Button(17)
    midButton = Button(5)
    rightButton = Button(22)

    createExportDirectory(OUTPUT_PATH)
    #CheckInternetConnection()
    checkUSBConnected(USB_DRIVE_PATH)

    cv2.namedWindow("Photobooth", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Photobooth', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    print("start")
    # todo set a countdown param?
    camera = Camera(WINDOW_W, WINDOW_H, CAPTURE_W, CAPTURE_H, 30, 55, 180, 120)

    running = True
    
    while running:
        startScreen()

        k = cv2.waitKey(1)
        if k == BUTTON_CAPTURE or midButton.is_pressed:
            smileScreen()
            cv2.waitKey(1) # keyboard buttons can be pressed more than once and affect the state
            # would be good to add a listener function to buttons
            
            midLED.off()
            leftLED.off()
            rightLED.off()

            image = camera.countdownCapture()
            outputScreen(image)

            midLED.off()
            leftLED.blink()
            rightLED.blink()

            while True:
                k = cv2.waitKey(1)
                if k == BUTTON_STARTOVER or leftButton.is_pressed:
                    print("startover")
                    midLED.pulse()
                    break
                if k == BUTTON_PRINT or rightButton.is_pressed:
                    print("print")

                    # Save photo and send to printer
                    filename = "photos/"
                    filename += saveImage(image)
                    #printImage(filename)
                    
                    cv2.waitKey(2000)
                    midLED.pulse()
                    break
                if k == BUTTON_EXIT:
                    running = False
                    break

        if k == BUTTON_EXIT:
            running = False

    camera.close()
    cv2.destroyAllWindows()
