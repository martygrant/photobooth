import cv2
from pushover import *
from backup import *
from Camera import *
from globals import *
from GUI import *
from cupsprint import *
import subprocess





# priority todo 
# update polaroid text
# finalise camera settings and resolution - exact 300dpi might be better
# blur round photos? reposition camera
# decide on overlay alpha value
# print or put on screen about loading paper and ink?
# turn off paper type register on printer
# save photo is slow - put on another thread? maybe didnt make difference
# add a "saved" screen if printing is disabled - add a flag for this



# todo
# maybe have a gap between countdown overlays
# maybe add all countdown overlays at start and just swap layers during countdown
# print countdown timing?
# "smile" appears for a sec between screens
# handle ink/paper errors
# try gdrive again and see if auth problem happens again
# gif during countdown?

def hide_mouse():
    # use "unclutter" package to hide mouse after period of inactivity, 0 for right away
    subprocess.Popen(['unclutter', '-idle', '0'])


if __name__ == "__main__":
    hide_mouse()

    createExportDirectory(OUTPUT_PATH)
    #CheckInternetConnection()
    checkUSBConnected(USB_DRIVE_PATH)

    cv2.namedWindow("Photobooth", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Photobooth', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    print("start")
    # todo set a countdown param?
    camera = Camera(WINDOW_W, WINDOW_H, CAPTURE_W, CAPTURE_H, 30, 55, 180, 120)

    midLED.pulse(fade_in_time=0.8, fade_out_time=0.8)

    running = True
    
    while running:
        startScreen()

        k = cv2.waitKey(1)
        if k == BUTTON_CAPTURE or midButton.is_pressed:
            smileScreen()
            cv2.waitKey(1) # keyboard buttons can be pressed more than once and affect the state
            # would be good to add a listener function to buttons
            
            lightsOff()

            image = camera.countdownCapture()
            outputScreen(image)

            midLED.off()
            leftLED.pulse(fade_in_time=0.75, fade_out_time=0.75)
            rightLED.pulse(fade_in_time=0.75, fade_out_time=0.75)

            while True:
                k = cv2.waitKey(1)
                if k == BUTTON_STARTOVER or leftButton.is_pressed:
                    print("startover")
                    midLED.pulse(fade_in_time=0.8, fade_out_time=0.8)
                    leftLED.off()
                    rightLED.off()

                    break
                if k == BUTTON_PRINT or rightButton.is_pressed:
                    print("print")

                    # Save photo and send to printer
                    filename = "photos/"
                    filename += saveImage(image)
                    printImage(filename)
                    
                    cv2.waitKey(2000)
                    midLED.pulse(fade_in_time=0.8, fade_out_time=0.8)
                    leftLED.off()
                    rightLED.off()

                    break
                if k == BUTTON_EXIT:
                    running = False
                    break

        if k == BUTTON_EXIT:
            running = False

    lightsOff()

    camera.close()
    cv2.destroyAllWindows()
