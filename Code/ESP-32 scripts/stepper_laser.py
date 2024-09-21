from machine import Pin, I2C
import machine
import time
from VL53L0X import VL53L0X

# Define los pines
IN1 = machine.Pin(27, machine.Pin.OUT)
IN2 = machine.Pin(26, machine.Pin.OUT)
IN3 = machine.Pin(25, machine.Pin.OUT)
IN4 = machine.Pin(33, machine.Pin.OUT)

# Configuración de los pines I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Función para mover el motor, con direccion a favor de las manecillas(1) y en contra(-1)
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
      print(combination + 1)
      for step in half_step:
          IN1.value(step[0])
          IN2.value(step[1])
          IN3.value(step[2])
          IN4.value(step[3])
          time.sleep_ms(delay)
  else:
    for combination in range(steps):
      print (combination + 1)
      for step in range(len(half_step)-1, -1, -1):
          IN1.value(half_step[step][0])
          IN2.value(half_step[step][1])
          IN3.value(half_step[step][2])
          IN4.value(half_step[step][3])
          time.sleep_ms(delay)


if __name__ == "__main__":
      # Inicializar el sensor VL53L0X
      sensor = VL53L0X(i2c)
      sensor.start()
      valores = [] #25
      for i in range(51):
          motor_half_step(10, 2)
          individual = 0
          for i in range(10):
              distance = sensor.read() + 20
              print(f"Distancia: {distance} mm")
              individual += distance
          valores.append(individual/10)
          
      print(valores)
        
      
      
      
      