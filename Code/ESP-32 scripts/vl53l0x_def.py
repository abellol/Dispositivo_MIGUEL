from machine import Pin, I2C
import time
from VL53L0X import VL53L0X

# Configuración de los pines I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Inicializar el sensor VL53L0X
sensor = VL53L0X(i2c)

# Iniciar el sensor
sensor.start()

try:
    while True:
        # Obtener la distancia en milímetros
        distancia = sensor.read() + 20
        print('Distancia: {} mm'.format(distancia))
        time.sleep(0.2)

except KeyboardInterrupt:
    sensor.stop()
