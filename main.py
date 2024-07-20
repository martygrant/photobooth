import cv2
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
from cupsprint import *
import os

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
    #CheckInternetConnection()
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
    # todo set a countdown param?
    camera = Camera(WINDOW_W, WINDOW_H, CAPTURE_W, CAPTURE_H, 30, 55, 180, 120)

    running = True
    
    while running:
        cv2.imshow('Photobooth', startScreen())

        k = cv2.waitKey(1)
        if k == BUTTON_CAPTURE:
            smileScreen()
            cv2.waitKey(1)
            
            image = camera.countdownCapture()
            outputDisplay(image)

            while True:
                k = cv2.waitKey(1)
                if k == BUTTON_STARTOVER:
                    print("startover")
                    break
                if k == BUTTON_PRINT:
                    print("print")

                    # Save photo and send to printer
                    filename = "photos/"
                    filename += saveImage(image)
                    printImage(filename)
                    
                    cv2.waitKey(2000)
                    break
                if k == BUTTON_EXIT:
                    running = False
                    break

        if k == BUTTON_EXIT:
            running = False

    camera.close()
    cv2.destroyAllWindows()


"""
def leftButtonAction():
    test = 1
    
def middleButtonAction():
    originalFrame = countdown(COUNTDOWN_TIME)
    
def rightButtonAction():
    test = 1
"""
