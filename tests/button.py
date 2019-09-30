from signal import pause
from gpiozero import Button

left = Button(4)
mid = Button(22)
right = Button(17)

def btn1():
    print("left")
    
def btn2():
    print("mid")
def btn3():
    print("right")
        
left.when_pressed = btn1
mid.when_pressed = btn2
right.when_pressed = btn3

pause()
