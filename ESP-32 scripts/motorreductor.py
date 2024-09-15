from machine import Pin,PWM

in1 = Pin(27, Pin.OUT)
in2 = Pin(26, Pin.OUT)
in3 = Pin(25, Pin.OUT)
in4 = Pin(33, Pin.OUT)

def direction(dire:int):
    if dire == 1:
        in1.value(1)
        in2.value(0)
        in3.value(1)
        in4.value(0)
    elif dire == -1:
        in1.value(0)
        in2.value(1)
        in3.value(0)
        in4.value(1)
    elif dire == 0:
        in1.value(0)
        in2.value(0)
        in3.value(0)
        in4.value(0)

direction(1)