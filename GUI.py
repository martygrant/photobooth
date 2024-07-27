import numpy as np
import cv2
from PIL import ImageDraw, Image
from globals import *

def createFrame(w, h, colour):
    frame = np.zeros((h, w, 3), np.uint8)
    if colour != 0:
        frame.fill(colour)
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

import cv2
import numpy as np

def overlay_transparent(background, overlay, x, y, rotation_angle=0, scale=1.0):
    background_height, background_width = background.shape[:2]

    # Scale the overlay image if scale is not 1
    if scale != 1.0:
        overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    
    # Get the dimensions of the overlay image
    h, w = overlay.shape[:2]

    # Rotate the overlay image if rotation_angle is not zero
    if rotation_angle != 0:
        # Get the center of the overlay image
        center = (w // 2, h // 2)
        # Compute the rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        # Perform the rotation
        overlay = cv2.warpAffine(overlay, rotation_matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)
        # Recompute dimensions after rotation
        h, w = overlay.shape[:2]

    # Ensure the overlay fits within the background dimensions
    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if x < 0:
        overlay = overlay[:, -x:]
        w += x
        x = 0

    if y < 0:
        overlay = overlay[-y:, :]
        h += y
        y = 0

    # If overlay does not have an alpha channel, add one
    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    # Ensure the area in the background is the same size as the overlay
    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background


def addPolaroidBorder(image):
    # scale image down proportionally
    image = cv2.resize(image, (0, 0), fx=0.95, fy=0.95)

    # place the image against a larger white image so it has white borders
    polaroidFrame = createFrame(CAPTURE_W, CAPTURE_H, 255)
    polaroidFrameCols = polaroidFrame.shape[1]
    polaroidFrameRows = polaroidFrame.shape[0]
    imageCols = image.shape[1]
    imageRows = image.shape[0]
    xoffset = int((polaroidFrameCols - imageCols) / 2)
    yoffset = int((polaroidFrameRows - imageRows) / 2)
    polaroidFrame[yoffset:yoffset+imageRows, xoffset:xoffset+imageCols] = image

    # make the height of the top border the same width as the left/right borders
    polaroidFrame[0:xoffset] = 255

    # make the bottom border larger (2x width of left/right border)
    polaroidFrame[polaroidFrameRows-(xoffset*2):polaroidFrameRows] = 255

    writeTextCenteredHorizontal(polaroidFrame, POLAROID_TEXT, POLAROID_TEXT_Y, FONT_ITALIC, POLAROID_TEXT_SIZE, POLAROID_TEXT_THICKNESS, COLOUR_BLACK)
    
    return polaroidFrame
    
def startScreen():
    pressButtonFrame = createFrame(WINDOW_W, WINDOW_H, 0)
    
    writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT, CAPTURE_Y - 50, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
    writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT2, CAPTURE_Y + 70, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
    
    renderFrame(pressButtonFrame)

def outputScreen(image):
    print("outputScreen")

    blackFrame = createFrame(WINDOW_W, WINDOW_H, 0)
    renderFrame(blackFrame)

    image = cv2.resize(image, (1440, 900))

    x = 0
    y = WINDOW_H - 120
    w = WINDOW_W
    h = 120

    overlay = image.copy()

    cv2.rectangle(image, (x, y), (x+w, y+h), COLOUR_BLACK, -1)
    alpha = 0.4
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

    # write start over and print text
    writeText(image, STARTOVER_TEXT, STARTOVER_X, STARTOVER_Y, FONT_NORMAL, STARTOVER_SIZE, STARTOVER_THICKNESS, COLOUR_WHITE)
    writeText(image, PRINT_TEXT, PRINT_TEXT_X, PRINT_TEXT_Y, FONT_NORMAL, PRINT_TEXT_SIZE, PRINT_TEXT_THICKNESS, COLOUR_WHITE)

    #overlay_transparent(image, arrow, STARTOVER_X + 150, STARTOVER_Y + 20)
    #overlay_transparent(image, arrow, PRINT_TEXT_X + 290, STARTOVER_Y + 20)

    renderFrame(image)

def smileScreen():
    print("smile screen")

    image = createFrame(WINDOW_W, WINDOW_H, 0)

    overlay_transparent(image, arrow, int(WINDOW_W/2) - 120, int(WINDOW_H/2) - 300, 180, 2.5)

    writeText(image, SMILE_TEXT, 350, int(WINDOW_H/2) + 350, FONT_NORMAL, SMILE_TEXT_SIZE, SMILE_TEXT_THICKNESS, COLOUR_WHITE)
    
    renderFrame(image)

def printScreen(progress):
    screen = createFrame(WINDOW_W, WINDOW_H, 0)

    # todo remove hardcoded text positions

    writeTextCenteredHorizontal(screen, "Printing your photo...", 900/2 - 200, FONT_NORMAL, 4, 4, COLOUR_WHITE)    

    # Draw the progress with a better font
    cv2_im_rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im_rgb)
    draw = ImageDraw.Draw(pil_im)
    draw.text((1400/2-100, 900/2 - 50), progress, font=roboto_font)
    screen = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

    writeTextCenteredHorizontal(screen, "Please keep it!", 900/2 + 300, FONT_NORMAL, 4, 4, COLOUR_WHITE)    

    renderFrame(screen)

def renderFrame(frame):
    cv2.imshow('Photobooth', frame)