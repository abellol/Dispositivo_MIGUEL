# -*- coding: utf-8 -*-

import socket
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import threading

# DirecciÃ³n IP del servidor (ESP32) y puerto
serverIP = "172.20.10.3"  # Cambia esto por la IP de tu ESP32
serverPort = 3000

# Crear un socket TCP/IP
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor (ESP32)
sk.connect((serverIP, serverPort))
print("Conectado al servidor")

# FunciÃ³n para recibir el dato entero del servidor
def receive_data():
    # Recibir datos del servidor
    data = sk.recv(128).decode()  # Convertir los bytes recibidos a cadena
    # Convertir la cadena en un entero
    data_value = (data)  # Convertir el dato recibido a entero
    print(f"Valor entero procesado: {data_value}")
    return data_value


def init_df(n_rows):
    # Datos de ejemplo
    theta = np.degrees(np.linspace(0, 2 * np.pi, n_rows, endpoint=False))  # Ángulo theta
    R = np.full(n_rows, np.nan)
    df = pd.DataFrame({'theta': theta, 'R': R})
    return df


def graph_df(df):
    # Graficar el dataframe en coordenadas polares
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.plot(np.radians(df['theta']), df['R'])
    ax.set_title(r'Distancia($\theta$)')
    plt.show()


def graph_df_parallel(df, stop_event):
    # Configurar el gráfico polar
    plt.ion()  # Modo interactivo activado
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
    ax.set_title(r'Distancia($\theta$)')

    # Línea inicial
    line, = ax.plot([], [], 'b-')  # 'b-' es el color azul y línea continua

    # Función para cerrar la ventana al presionar 'q'
    def on_key(event):
        if event.key == 'q':
            stop_event.set()  # Establecer la señal para detener el gráfico

    # Conectar la función de control de teclado
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Bucle para actualizar el gráfico
    while not stop_event.is_set():
        # Actualizar los datos de la línea
        line.set_data(np.radians(df['theta']), df['R'])

        # Ajustar los límites de las coordenadas polares si es necesario
        ax.relim()
        ax.autoscale_view()

        # Dibujar y pausar para permitir la actualización de la gráfica
        plt.draw()
        plt.pause(0.1)  # Pausar para actualizar el gráfico

    plt.close(fig)  # Cerrar la ventana al salir del bucle


def update_value_df(df, index, distance):
    # Función para actualizar un único valor R dentro del dataframe
    df.loc[index, 'R'] = distance


def blank_df(df):
    # Función para borrar todos los datos de la columna R dentro del dataframe
    df['R'] = np.nan


if __name__ == "__main__":
    # Dataframe donde se almacenarán los datos
    df = init_df(51)
    print('Dataframe inicial:')
    print(df)

    # Evento para detener el gráfico
    stop_event = threading.Event()
    # Crear y comenzar el hilo para graph_df
    graph_thread = threading.Thread(target=graph_df_parallel, args=(df, stop_event))
    graph_thread.start()

    # Enviar un mensaje al servidor (ESP32) para iniciar la transferencia de datos
    for i in range(51):
        sk.sendall(b'Enviar valor')

        # Recibir y procesar el dato
        valor_recibido = receive_data()
        dato = eval(valor_recibido) # [distancia, angulo]
        update_value_df(df, i, dato[0])
        # Cerrar la conexiÃ³n
    
    #stop_event.set()  # Comentada para terminar con 'q', descomentada para terminar automáticamente
    graph_thread.join()
    #graph_df(df)

    print('\nDataframe final:')
    print(df)
    print("Cerrando conexiÃ³n")
    sk.close()

