import numpy as np
import cv2
import time
from PIL import ImageFont, ImageDraw, Image
from globals import *

def createFrameBlack(w, h):
    return np.zeros((WINDOW_H, WINDOW_W, 3), np.uint8)

def createFrameWhite(w, h):
    frame = np.zeros((1728, 2592, 3), np.uint8)
    frame.fill(255)
    return frame

def writeText(frame, text, x, y, font, size, thickness, colour):
    cv2.putText(frame, text, (int(x), int(y)), font, size, colour, thickness, cv2.LINE_AA)

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

def addPolaroidBorder(image):
    # scale image down proportionally
    image = cv2.resize(image, (0, 0), fx=0.95, fy=0.95)

    # place the image against a larger white image so it has white borders
    polaroidFrame = createFrameWhite(CAPTURE_W, CAPTURE_H)
    polaroidFrameCols = polaroidFrame.shape[1]
    polaroidFrameRows = polaroidFrame.shape[0]
    imageCols = image.shape[1]
    imageRows = image.shape[0]
    xoffset = (polaroidFrameCols - imageCols) / 2
    yoffset = (polaroidFrameRows - imageRows) / 2
    polaroidFrame[yoffset:yoffset+imageRows, xoffset:xoffset+imageCols] = image

    # make the height of the top border the same width as the left/right borders
    polaroidFrame[0:xoffset] = 255

    # make the bottom border larger (2x width of left/right border)
    polaroidFrame[polaroidFrameRows-(xoffset*2):polaroidFrameRows] = 255

    writeTextCenteredHorizontal(polaroidFrame, POLAROID_TEXT, POLAROID_TEXT_Y, FONT_ITALIC, POLAROID_TEXT_SIZE, POLAROID_TEXT_THICKNESS, COLOUR_BLACK)
    
    return polaroidFrame
    

def startScreen():
    pressButtonFrame = createFrameBlack(WINDOW_W, WINDOW_H)
    
    writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT, CAPTURE_Y - 50, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
    writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT2, CAPTURE_Y + 70, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
    writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT3, CAPTURE_Y + 300, FONT_NORMAL, 2.5, CAPTURE_THICKNESS, COLOUR_WHITE)
    
    return pressButtonFrame


def outputDisplay(image):
    print("outputDisplay")

    image = cv2.resize(image, (1440, 900))

    x = 0
    y = WINDOW_H - 230
    w = WINDOW_W
    h = 300

    cv2.rectangle(image, (x, y), (x+w, y+h), COLOUR_BLACK, -1)
    alpha = 0.6
    cv2.addWeighted(image, alpha, image, 1 - alpha, 0, image)

    # write start over and print text
    writeText(image, STARTOVER_TEXT, STARTOVER_X, STARTOVER_Y, FONT_NORMAL, STARTOVER_SIZE, STARTOVER_THICKNESS, COLOUR_WHITE)
    writeText(image, PRINT_TEXT, PRINT_TEXT_X, PRINT_TEXT_Y, FONT_NORMAL, PRINT_TEXT_SIZE, PRINT_TEXT_THICKNESS, COLOUR_WHITE)

    overlay_transparent(image, arrow, STARTOVER_X + 150, STARTOVER_Y + 20)
    overlay_transparent(image, arrow, PRINT_TEXT_X + 290, STARTOVER_Y + 20)

    cv2.imshow('Photobooth', image)


def smileScreen():
    print("smile screen")

    image = createFrameBlack(WINDOW_W, WINDOW_H)

    writeTextCentered(image, "SMILE!", FONT_NORMAL, STARTOVER_SIZE, STARTOVER_THICKNESS, COLOUR_WHITE)
    cv2.imshow('Photobooth', image)


def printScreen(progress):
    screen = createFrameBlack(WINDOW_W, WINDOW_H)

    # todo remove hardcoded text positions

    writeTextCenteredHorizontal(screen, "Printing your photo...", 900/2 - 200, FONT_NORMAL, 4, 4, COLOUR_WHITE)    

    # Draw the progress with a better font
    cv2_im_rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im_rgb)
    draw = ImageDraw.Draw(pil_im)
    draw.text((1400/2-100, 900/2 - 50), progress, font=roboto_font)
    screen = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

    writeTextCenteredHorizontal(screen, "Collect below!", 900/2 + 300, FONT_NORMAL, 4, 4, COLOUR_WHITE)    

    return screen


def countdownDisplay(countDown, camera):
    print("countdownDisplay")
    oldTime = time.time()
    camera.startPreview()
    while True:
        currentTime = time.time()

        camera.setText(str(countDown))

        # 1 second has passed
        if currentTime - oldTime >= 1:
            print("preview countdown {0}s left".format(str(countDown)))
            countDown -= 1
            oldTime = time.time()

        if countDown < 1:
            camera.stopPreview()
            return camera.capture()
