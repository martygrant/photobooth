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

if __name__ == "__main__":
    leftLED = PWMLED(26)
    leftLED.pulse()

    rightLED = PWMLED(21)
    rightLED.pulse()

    midLED = LED(6)
    midLED.blink()

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
                    break
                if k == BUTTON_PRINT or rightButton.is_pressed:
                    print("print")

                    # Save photo and send to printer
                    filename = "photos/"
                    filename += saveImage(image)
                    #printImage(filename)
                    
                    cv2.waitKey(2000)
                    break
                if k == BUTTON_EXIT:
                    running = False
                    break

        if k == BUTTON_EXIT:
            running = False

    camera.close()
    cv2.destroyAllWindows()
