from gpiozero import LED
from time import sleep

mid = LED(6)
left = LED(19)
right = LED(21)

while True:
    #mid.on()
    right.on()
    #left.on()
    sleep(1)
    left.off()
    #mid.off()
    right.off()
    sleep(1)
    
light.off()
light2.off()
light3.off()