import cv2
from pushover import *
from backup import *
from Camera import *
import globals
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

    if globals.leftButton.is_pressed: # todo or keyboard
        inputReset = True
    elif globals.middleButton.is_pressed:
        inputCapture = True
    elif globals.rightButton.is_pressed:
        inputPrint = True

    # todo be careful state can't be advanced when it shouldn't be

    return True # todo return if esc is pressed

def update():
    if state == State.START:

        #if inputCapture == True:
            switchState(State.COUNTDOWN)

    #elif state == State.COUNTDOWN:
        #switchState(State.DISPLAY)
        

    elif state == State.DISPLAY:
        if inputReset == True:
            switchState(State.START)
        elif inputPrint == True:
            switchState(State.PRINT)

    elif state == State.PRINT:
        switchState(State.START)




def render(camera):
    if state == State.START:
        startScreen()

    elif state == State.COUNTDOWN:
        #smileScreen()
        renderFrame(createFrame(globals.config["window"]["width"], globals.config["window"]["width"], 0))
        cv2.waitKey(1) # keyboard buttons can be pressed more than once and affect the state
        # would be good to add a listener function to buttons
        image = camera.countdownCapture()
        outputScreen(image)

        cv2.imwrite("test.jpg", image)
        exit(0)

    elif state == State.DISPLAY:
        vox = 1

    elif state == State.PRINT:
        vox = 1


def main():
    hide_mouse()
    createExportDirectory(globals.OUTPUT_PATH)
    #CheckInternetConnection()
    checkUSBConnected(globals.USB_DRIVE_PATH)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to a .yaml configuration file.")
    args = parser.parse_args()

    # todo only proceed if valid config found
    # todo add all globals to config
    # todo log the config values
    with open(args.config) as f:
        globals.config = yaml.load(f, Loader=yaml.FullLoader)
        print(globals.config)

    # todo set a countdown param?
    # todo magic numbers
    camera = Camera(globals.config["window"]["width"], globals.config["window"]["width"], globals.config["camera"]["width"], globals.config["camera"]["height"], 30, 55, 180, 120)

    cv2.namedWindow(globals.config["window"]["title"], cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty(config["window"]["title"], cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(globals.config["window"]["title"], createFrame(1440, 900, 0)) 
    #cv2.imshow(config["window"]["title"], createFrame(200, 200, 0)) 

    #cv2.waitKey(0)

    running = True
    while running:
        running = events()
        update()
        render(camera)


    lightsOff()
    #camera.close()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()
"""
    # todo set a countdown param?
    camera = Camera(globals.config["window"]["width"], globals.config["window"]["width"], CAPTURE_W, CAPTURE_H, 30, 55, 180, 120)

    midLED.pulse(fade_in_time=0.8, fade_out_time=0.8)

    running = True
    
    while running:
        startScreen()

        k = cv2.waitKey(1)
        if k == BUTTON_CAPTURE or middleButton.is_pressed:
            #smileScreen()
            renderFrame(createFrame(globals.config["window"]["width"], globals.config["window"]["width"], 0))
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
                    renderFrame(createFrame(globals.config["window"]["width"], globals.config["window"]["width"], 0))
                    lightsOff()

                    # Save photo and send to printer
                    filename = saveImage(image)
                    if config["print_enabled"] == True:
                        printImage(filename)
                    else:
                        savedScreen()
                    
                    cv2.waitKey(2000)
                    midLED.pulse(fade_in_time=0.8, fade_out_time=0.8)

                    break
"""