from gpiozero import LED
from time import sleep
from signal import pause

mid = LED(6)
left = LED(26)
right = LED(21)

mid.blink()
left.blink()
right.blink()

pause()