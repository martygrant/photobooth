import picamera.array
import picamera
import time
from PIL import Image

class Camera:
    def __init__(self, previewWidth, previewHeight, captureWidth, captureHeight, frameRate, brightness, rotation, textSize):
        self._previewWidth = previewWidth
        self._previewHeight = previewHeight
        self._captureWidth = captureWidth
        self._captureHeight = captureHeight
        self._frameRate = frameRate
        self._brightness = brightness
        self._rotation = rotation
        self._textSize = textSize

        self.setupCamera(self._previewWidth, self._previewHeight, self._frameRate, self._brightness, self._rotation, self._textSize)

        #self.countdown_images = ['countdown_images/5.png', 'countdown_images/4.png', 'countdown_images/3.png', 'countdown_images/2.png', 'countdown_images/1.png']
        self.countdown_images = ['countdown_images/3.png', 'countdown_images/2.png', 'countdown_images/1.png']

    def addoverlay(self, image_path):
        img = Image.open(image_path)
        pad = Image.new('RGBA', (
            ((img.width + 31) // 32) * 32,
            ((img.height + 15) // 16) * 16,
            ))
        pad.paste(img, (0, 0))

        # Create an overlay
        o = self._camera.add_overlay(pad.tobytes(), size=img.size)
        o.alpha = 128  # Transparency of the overlay
        o.layer = 3   # Layer position
        return o

    def countdownCapture(self, leftLED, rightLED, midLED):
        print("countdownCapture")
        self.startPreview()

        count = 0

        LEDS = [leftLED, rightLED, midLED]

        for img_path in self.countdown_images:
            overlay = self.addoverlay(img_path)
            
            if count == 0:
                leftLED.on()
            if count == 1:
                midLED.on()
            if count == 2:
                rightLED.on()
            
            time.sleep(1.0)
            self._camera.remove_overlay(overlay)

            count += 1

        self.stopPreview()

        leftLED.off()
        midLED.off()
        rightLED.off()

        return self.capture(leftLED, rightLED, midLED)

    def startPreview(self):
        self._camera.start_preview()
        time.sleep(1) # allow some time for the camera to calibrate

    def stopPreview(self):
        self._camera.stop_preview()

    def setText(self, text):
        self._camera.annotate_text = text

    def setupCamera(self, width, height, frameRate, brightness, rotation, textSize):
        self._camera = picamera.PiCamera()
        self._camera.resolution = (width, height)
        self._camera.framerate = frameRate
        self._camera.brightness = 60
        self._camera.contrast = 10
        self._camera.iso = 100
        self._camera.exposure_mode = 'auto'
        self._camera.awb_mode = 'auto'
        self._camera.sharpness = 10

        self._camera.rotation = rotation
        self._rawCapture = picamera.array.PiRGBArray(self._camera, size=(width,height))
        self._camera.annotate_text_size = textSize

    def capture(self, leftLED, rightLED, midLED):
        # close and re-open the camera with the capture resolution
        self._camera.close()
        self.setupCamera(self._captureWidth, self._captureHeight, self._frameRate, self._brightness, self._rotation, self._textSize)

        leftLED.on()
        rightLED.on()
        midLED.on()

        time.sleep(1) # allow some time for the camera to calibrate

        # take the image
        self._camera.capture(self._rawCapture, 'bgr', use_video_port=False)
        img = self._rawCapture.array
        # todo can the above be simplified?
        # todo do a second capture with resize param as its more efficient than resizing with opencv later for display
        
        # close and re-open the camera with the preview resolution
        self._camera.close()
        self.setupCamera(self._previewWidth, self._previewHeight, self._frameRate, self._brightness, self._rotation, self._textSize)
        
        return img
         
    def close(self): 
        self._camera.close()
