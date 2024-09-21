import socket

# Dirección y puerto en los que el servidor ESP32 va a escuchar
serverAddressPort = socket.getaddrinfo('0.0.0.0', 3000)[0][-1]

# Cantidad de bytes a recibir
bufferSize  = 128

# Conectar a la red (cambiar a tu configuración)
from wifiAP import connectSTA as connect
connect("mySSID", "myPassword")

# Dato entero que se enviará al cliente
data_value = 42  # Un valor entero

# Crear socket TCP/IP
sk = socket.socket()
sk.bind(serverAddressPort)
sk.listen(1)
print("Listening on: ", serverAddressPort)

while True:
    conn, addr = sk.accept()
    print(f"Conexión establecida con {addr}")

    while True:
        data = conn.recv(bufferSize)
        if data:
            print(f"Recibido: {data.decode()}")  # Mostrar el dato recibido
            # Convertir el entero a cadena para enviarlo
            data_str = str(data_value)
            # Enviar el valor entero convertido a cadena al cliente
            conn.sendall(data_str.encode())
            print(f"Valor enviado: {data_str}")

    conn.close()
