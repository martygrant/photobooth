import cv2
from pushover import *
from backup import *
from Camera import *
from globals import *
from GUI import *
from cupsprint import *
from enum import Enum
import subprocess
import yaml
import argparse


inputCapture = False
inputReset = False
inputPrint = False

class State(Enum):
    START = 0
    COUNTDOWN = 1
    DISPLAY = 2
    PRINT = 3

state = State.START

def switchState(newState):
    # todo exit here?
    if newState not in State._value2member_map_:
        print("ERROR: INVALID STATE")

    global state
    oldState = state
    state = newState
    print("INFO: Switching state FROM {0} TO {1}.".format(oldState, newState))

# priority todo 
# finalise camera settings and resolution - exact 300dpi might be better
# blur round photos? reposition camera
# try changing manual focus
# update readme
#   need PyYAML



# todo
# maybe have a gap between countdown overlays
# maybe add all countdown overlays at start and just swap layers during countdown
# print countdown timing?
# "smile" appears for a sec between screens or wrong screen is shown after countdown etc - maybe to do with waitKey
# handle ink/paper errors
# try gdrive again and see if auth problem happens again
# gif during countdown?
# save photo is slow - put on another thread? maybe didnt make difference

def hide_mouse():
    # use "unclutter" package to hide mouse after period of inactivity, 0 for right away
    subprocess.Popen(['unclutter', '-idle', '0'])



"""
def button_left():
    print("left")
    
def button_middle():
    print("mid")

def button_right():
    print("right")
        
left.when_pressed = button_left
mid.when_pressed = button_middle
right.when_pressed = button_right
"""

def events():
    global inputCapture
    global inputReset
    global inputPrint

    inputCapture = False   
    inputReset = False
    inputPrint = False

    if leftButton.is_pressed: # todo or keyboard
        inputReset = True
    elif middleButton.is_pressed:
        inputCapture = True
    elif rightButton.is_pressed:
        inputPrint = True

    return True # todo return if esc is pressed

def update():
    if state == State.START:

        if inputCapture == True:
            switchState(State.COUNTDOWN)

    elif state == State.COUNTDOWN:
        switchState(State.DISPLAY)

    elif state == State.DISPLAY:
        if inputReset == True:
            switchState(State.START)
        elif inputPrint == True:
            switchState(State.PRINT)

    elif state == State.PRINT:
        switchState(State.START)



"""
def render():
    if state == State.START:

    elif state == State.COUNTDOWN:

    elif state == State.DISPLAY:

    elif state == State.PRINT:

"""

def main():
    hide_mouse()
    createExportDirectory(OUTPUT_PATH)
    #CheckInternetConnection()
    checkUSBConnected(USB_DRIVE_PATH)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to a .yaml configuration file.")
    args = parser.parse_args()

    # todo only proceed if valid config found
    # todo add all globals to config
    # todo log the config values
    with open(args.config) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        print(config)

    running = True
    while running:
        running = events()
        update()
        #render(screen)


    #lightsOff()
    #camera.close()
    #cv2.destroyAllWindows()






if __name__ == "__main__":
    main()
    

    
"""
    cv2.namedWindow("Photobooth", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Photobooth', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    

    # todo set a countdown param?
    camera = Camera(WINDOW_W, WINDOW_H, CAPTURE_W, CAPTURE_H, 30, 55, 180, 120)

    midLED.pulse(fade_in_time=0.8, fade_out_time=0.8)

    running = True
    
    while running:
        startScreen()

        k = cv2.waitKey(1)
        if k == BUTTON_CAPTURE or middleButton.is_pressed:
            #smileScreen()
            renderFrame(createFrame(WINDOW_W, WINDOW_H, 0))
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
                    lightsOff()
                    midLED.pulse(fade_in_time=0.8, fade_out_time=0.8)

                    break
                if k == BUTTON_PRINT or rightButton.is_pressed:
                    renderFrame(createFrame(WINDOW_W, WINDOW_H, 0))
                    lightsOff()

                    # Save photo and send to printer
                    filename = saveImage(image)
                    if PRINT_ENABLED == True:
                        printImage(filename)
                    else:
                        savedScreen()
                    
                    cv2.waitKey(2000)
                    midLED.pulse(fade_in_time=0.8, fade_out_time=0.8)

                    break
"""