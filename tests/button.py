from signal import pause
from gpiozero import Button

mid = Button(5)
left = Button(17)
right = Button(22)

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
