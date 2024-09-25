from machine import Pin, I2C
from VL53L0X import VL53L0X
import time

in1 = Pin(4, Pin.OUT)
in2 = Pin(2, Pin.OUT)
in3 = Pin(14, Pin.OUT)
in4 = Pin(12, Pin.OUT)
d13 = Pin(13, Pin.OUT)
d15 = Pin(15, Pin.OUT)

def direction(dire:str):
    d13.value(1)
    d15.value(1)
    if dire == "forward":
        in1.value(1)
        in2.value(0)
        in3.value(1)
        in4.value(0)
    elif dire == "backward":
        in1.value(0)
        in2.value(1)
        in3.value(0)
        in4.value(1)
    elif dire == "left":
        in1.value(0)
        in2.value(1)
        in3.value(1)
        in4.value(0)
    elif dire == "right":
        in1.value(1)
        in2.value(0)
        in3.value(0)
        in4.value(1)
    elif dire == "stop":
        in1.value(0)
        in2.value(0)
        in3.value(0)
        in4.value(0)

# def tomar_lejana(sensor, umbral_distancia):
#     while True:
#         direction("right")
#         distancia = sensor.read() + 13  # Calibración
#         print(f'Distancia actual: {distancia} mm')
#         if distancia > (umbral_distancia-(umbral_distancia*0.1)):
#             direction("stop")
#             break
#         time.sleep(0.5)
# def inicializar_sensor_vl53l0x():
#     i2c = I2C(0, scl=Pin(22), sda=Pin(21))
#     sensor = VL53L0X(i2c)
#     sensor.start()
#     return sensor
# if __name__ == "__main__":
#     sensor = inicializar_sensor_vl53l0x()
#     tomar_lejana(sensor, 90)

direction("forward")
