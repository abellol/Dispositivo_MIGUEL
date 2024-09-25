import machine
from machine import Pin
import time

IN1 = machine.Pin(27, machine.Pin.OUT)
IN2 = machine.Pin(26, machine.Pin.OUT)
IN3 = machine.Pin(25, machine.Pin.OUT)
IN4 = machine.Pin(33, machine.Pin.OUT)

def motor_half_step(steps, delay, direction = 1):
  half_step = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
    ]
  if direction == 1:
    for combination in range(steps):
      for step in half_step:
          IN1.value(step[0])
          IN2.value(step[1])
          IN3.value(step[2])
          IN4.value(step[3])
          time.sleep_ms(delay)
  else:
    for combination in range(steps):
      
      for step in range(len(half_step)-1, -1, -1):
          IN1.value(half_step[step][0])
          IN2.value(half_step[step][1])
          IN3.value(half_step[step][2])
          IN4.value(half_step[step][3])
          time.sleep_ms(delay)

