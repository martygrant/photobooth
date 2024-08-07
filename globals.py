import os
import cv2
from PIL import ImageFont
from gpiozero import Button
from gpiozero import PWMLED

WINDOW_W = 1440
WINDOW_H = 900

# capture and print resolution (match with aspect ratio of print, using 3:2 for 6x4 print)
CAPTURE_W = 2592#1800
CAPTURE_H = 1728#1200

OUTPUT_PATH = str(os.getcwd()) + "/photos/"
USB_DRIVE_PATH = "/media/martin/MARTIN/photos/"
GDRIVE_FOLDER_ID = "1U1aCTd_K84IdQQ9_z1UUkZt7EbEk9_qT"

COUNTDOWN_TIME = 5
COUNTDOWN_SIZE = 6
COUNTDOWN_THICKNESS = 5
COUNTDOWN_OVERLAY_X = WINDOW_W / 2
COUNTDOWN_OVERLAY_Y = (WINDOW_H / 2)
COUNTDOWN_OVERLAY_W = COUNTDOWN_OVERLAY_X + 200
COUNTDOWN_OVERLAY_H = COUNTDOWN_OVERLAY_Y + 200

CAPTURE_TEXT = "Press the middle button"
CAPTURE_TEXT2 = "below to take a photo!"
CAPTURE_X = (WINDOW_W / 2) - 50
CAPTURE_Y = (WINDOW_H / 2) 
CAPTURE_SIZE = 3.5
CAPTURE_THICKNESS = 3

STARTOVER_TEXT = "Try Again"
STARTOVER_X = 50
STARTOVER_Y = WINDOW_H - 30
STARTOVER_SIZE = 3
STARTOVER_THICKNESS = 3

PRINT_TEXT = "Print!"
PRINT_TEXT_X = WINDOW_W - 350
PRINT_TEXT_Y = WINDOW_H - 30
PRINT_TEXT_SIZE = 3
PRINT_TEXT_THICKNESS = 3

SMILE_TEXT = "SMILE! :)"
SMILE_TEXT_SIZE = 6
SMILE_TEXT_THICKNESS = 3

arrow = cv2.imread('arrow.png', cv2.IMREAD_UNCHANGED)

BUTTON_CAPTURE = ord('c')
BUTTON_STARTOVER = ord('s')
BUTTON_PRINT = ord('p')
BUTTON_EXIT = ord('q')

COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)

FONT_NORMAL = cv2.FONT_HERSHEY_SIMPLEX
FONT_ITALIC = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
roboto_font = ImageFont.truetype("Roboto-Regular.ttf", 148)

POLAROID_STYLE = True
POLAROID_TEXT_Y = CAPTURE_H - 35
POLAROID_TEXT_SIZE = 3
POLAROID_TEXT_THICKNESS = 2
POLAROID_TEXT = "Katrina & Nathan   Crossbasket Castle   28.07.2024"

leftLED = PWMLED(26)
rightLED = PWMLED(21)
midLED = PWMLED(6)

leftButton = Button(17)
midButton = Button(5)
rightButton = Button(22)

def lightsOff():
    leftLED.off()
    midLED.off()
    rightLED.off()

PRINT_ENABLED = True