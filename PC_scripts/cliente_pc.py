import socket

# Dirección IP del servidor (ESP32) y puerto
serverIP = "192.168.1.68"  # Cambia esto por la IP de tu ESP32
serverPort = 3000

# Crear un socket TCP/IP
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor (ESP32)
sk.connect((serverIP, serverPort))
print("Conectado al servidor")

# Función para recibir el dato entero del servidor
def receive_data():
    # Recibir datos del servidor
    data = sk.recv(128).decode()  # Convertir los bytes recibidos a cadena
    # Convertir la cadena en un entero
    data_value = (data)  # Convertir el dato recibido a entero
    print(f"Valor entero procesado: {data_value}")
    
    return data_value

if __name__ == "__main__":
# Enviar un mensaje al servidor (ESP32) para iniciar la transferencia de datos
  datos = []
  for i in range(52):
    sk.sendall(b'Enviar valor')

    # Recibir y procesar el dato
    valor_recibido = receive_data()
    dato = eval(valor_recibido)
    datos.append(dato)
    # Cerrar la conexión
  print("Cerrando conexión")
  sk.close()

