import socket
from machine import Pin, I2C
import time
import machine
from VL53L0X import VL53L0X
from wifiAP import connectSTA as connect

# Configuraciones de red
WIFI_SSID = "WIFI RITIN 2"
WIFI_PASSWORD = "Ritis2021"
SERVER_PORT = 3000
BUFFER_SIZE = 128
NUM_LECTURAS = 10

# Declarar los pines de los motorreductores
in1 = Pin(4, Pin.OUT)
in2 = Pin(2, Pin.OUT)
in3 = Pin(14, Pin.OUT)
in4 = Pin(12, Pin.OUT)
d13 = Pin(13, Pin.OUT)
d15 = Pin(15, Pin.OUT)

# Declarar pines del motor paso
IN1 = machine.Pin(27, machine.Pin.OUT)
IN2 = machine.Pin(26, machine.Pin.OUT)
IN3 = machine.Pin(25, machine.Pin.OUT)
IN4 = machine.Pin(33, machine.Pin.OUT)

# Función para controlar la polaridad de los motores frontales
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
          
# Función para conectar el ESP32 a una red WiFi
def conectar_wifi(ssid, password):
    connect(ssid, password)
    print(f"Conectado a la red {ssid}")

# Función para inicializar el sensor VL53L0X
def inicializar_sensor_vl53l0x():
    i2c = I2C(0, scl=Pin(22), sda=Pin(21))
    sensor = VL53L0X(i2c)
    sensor.start()
    return sensor

# Función para crear un socket servidor
def crear_servidor(port):
    server_address = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    sk = socket.socket()
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permitir reutilización del puerto
    sk.bind(server_address)
    sk.listen(1)
    print(f"Servidor escuchando en {server_address}")
    return sk

# Función para leer distancias del sensor y calcular un promedio
def leer_promedio_distancia(sensor, num_lecturas):
    distancia_total = 0
    for _ in range(num_lecturas):
        distancia = sensor.read() + 13  # Suma constante como calibración
        print(f'Distancia: {distancia} mm')
        distancia_total += distancia
        time.sleep(0.1)
    promedio = distancia_total / num_lecturas
    return promedio

# Función principal para manejar conexiones y enviar datos
def manejar_conexion(conn, sensor, num_lecturas, buffer_size):
    try:
        t = 0
        distancias = []
        for i in range(51):
            data = conn.recv(buffer_size)
            if not data:
                break 
            motor_half_step(10,1)
            print(f"Recibido: {data.decode()}")  # Mostrar el dato recibido
            # Leer el promedio de distancia y calcular el ángulo
            promedio_distancia = leer_promedio_distancia(sensor, num_lecturas)
            data_value = [promedio_distancia, t]
            t += (360 / 51)
            data_str = str(data_value)
            # Enviar el valor al cliente
            conn.sendall(data_str.encode())
            print(f"Datos enviados: {data_str}")
            distancias.append(promedio_distancia)
        motor_half_step(512, 1, -1)
        distancias = sorted(distancias, reverse=True)
        return (distancias[0])
    finally:
        conn.close()  # Cerrar siempre la conexión al final
        print("Conexion cerrada")


# Función principal para el bucle del servidor
def servidor_tcp(sensor, port, buffer_size, num_lecturas):
    sk = crear_servidor(port)
    try:
        conn, addr = sk.accept()
        print(f"Conexión establecida con {addr}")
        distancias = manejar_conexion(conn, sensor, num_lecturas, buffer_size)
        conn.close()
        print(f"Conexión con {addr} cerrada")
        return distancias
    finally:
        sk.close()  # Asegurarse de que el socket del servidor se cierre siempre
        print("Socket del servidor cerrado")

        
# Función para girar el dispositivo hasta que esté orientado hacia la dirección mas lejana
def tomar_lejana(sensor, umbral_distancia):
    while True:
        direction("right")
        distancia = sensor.read() + 13  # Calibración
        print(f'Distancia actual: {distancia} mm')
        if distancia > (umbral_distancia-(umbral_distancia*0.1)):
            direction("stop")
            break
        time.sleep(0.3)
        
# Función para avanzar hasta que la distancia sea menor o igual a un umbral
def avanzar(sensor, distancia_minima):
    while True:
        direction("forward")
        distancia = sensor.read() + 13
        print(f"La distancia actual es de: {distancia}mm")
        if distancia <= distancia_minima:
            direction("stop")
            break
        time.sleep(0.3)
        
# Programa principal
def main():
    conectar_wifi(WIFI_SSID, WIFI_PASSWORD)
    sensor = inicializar_sensor_vl53l0x()

    while True:  # Ciclo infinito para reiniciar el servidor cada vez que finaliza una conexión
        print("Iniciando servidor...")
        # Ejecutar el servidor TCP y obtener la mayor distancia medida
        distancia_maxima = servidor_tcp(sensor, SERVER_PORT, BUFFER_SIZE, NUM_LECTURAS)
        
        # Girar el dispositivo hacia la dirección de la distancia más lejana
        tomar_lejana(sensor, distancia_maxima)
        avanzar(sensor, 100)

        print("Ciclo completo. Reiniciando servidor...")
        time.sleep(2)

# Ejecutar el programa
if __name__ == "__main__":
    main()
