# -*- coding: utf-8 -*-

import socket
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import sys

# Direcciónn IP del servidor (ESP32) y puerto
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


def graph_df_parallel(df, stop_event, update_event, exit_bool):
    # Configurar el gráfico polar
    plt.ion()  # Modo interactivo activado
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
    ax.set_title(r'Distancia($\theta$)')

    # Línea inicial
    line, = ax.plot([], [], 'b-')  # 'b-' es el color azul y línea continua

    # Función para cerrar la ventana al presionar 'q'
    def on_key(event):
        if event.key == 'q':
            update_event.set() # Establecer la señal para que siga corriendo el for dentro del main
            stop_event.set()  # Establecer la señal para detener el gráfico
            exit_bool = True  # Salirse del while principal
        if event.key == 'r':
            blank_df(df)
            update_event.set()  # Señal para empezar a tomar datos de nuevo

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

    # Evento para detener el gráfico, actualizar el gráfico y cerrar el código
    stop_event = threading.Event()
    update_event = threading.Event()
    exit_bool = False
    # Crear y comenzar el hilo para graph_df
    graph_thread = threading.Thread(target=graph_df_parallel, args=(df, stop_event, update_event, exit_bool))
    graph_thread.start()
    update_event.set() # Inicialmente empieza activado

    # Enviar un mensaje al servidor (ESP32) para iniciar la transferencia de datos
    while not exit_bool:
        if(update_event.is_set()):
            update_event.clear() # Se desactiva el evento cada vez que se presiona 'r'
            for i in range(51):
                sk.sendall(b'Enviar valor')
                # Recibir y procesar el dato
                valor_recibido = receive_data()
                dato = eval(valor_recibido) # [distancia, angulo]
                update_value_df(df, i, dato[0])
                # Cerrar la conexión
            print('\nDataframe final:')
            print(df)
        update_event.wait()
    graph_thread.join()

    print("Cerrando conexión")
    sk.close()

