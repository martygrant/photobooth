import picamera
from PIL import Image
from time import sleep
import keyboard

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 24
camera.start_preview()

img = Image.open('countdown_images/5.png')
pad = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
pad.paste(img, (0, 0))
#o = camera.add_overlay(pad.tobytes(), size=img.size)
#o.alpha = 50
#o.layer = 0


img2 = Image.open('countdown_images/4.png')
pad2 = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
pad2.paste(img2, (0, 0))
#o2 = camera.add_overlay(pad2.tobytes(), size=img2.size)
#o2.alpha = 50
#o2.layer = 0

img3 = Image.open('countdown_images/3.png')
pad3 = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
pad.paste(img3, (0, 0))
#o3 = camera.add_overlay(pad.tobytes(), size=img3.size)
#o3.alpha = 50
#o3.layer = 1


img4 = Image.open('countdown_images/2.png')
pad4 = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
pad4.paste(img4, (0, 0))
#o4 = camera.add_overlay(pad4.tobytes(), size=img4.size)
#o4.alpha = 50
#o4.layer = 0

img5 = Image.open('countdown_images/1.png')
pad5 = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
pad5.paste(img5, (0, 0))
#o5 = camera.add_overlay(pad5.tobytes(), size=img5.size)
#o5.alpha = 50
#o5.layer = 0


count = 0

while True:
    sleep(1)
    
    count += 1
    print(count)

    camera.annotate_text = str(5-count)
    camera.annotate_text_size = 160

    """if (count > 2):
        o = camera.add_overlay(pad.tobytes(), size=img.size)
        o.alpha = 50
        o.layer = 0"""
    """elif (count < 3):
        camera.remove_overlay(o)
        o = camera.add_overlay(pad2.tobytes(), size=img2.size)
        o.alpha = 50
        o.layer = 0
    elif (count < 4):
        camera.remove_overlay(o)
        o = camera.add_overlay(pad3.tobytes(), size=img3.size)
        o.alpha = 50
        o.layer = 0"""
    """elif (count < 5):
        camera.overlays[0].layer = 0"""
    

    
    
