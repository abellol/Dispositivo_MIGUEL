import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def init_df(n_rows):
    # Datos de ejemplo
    theta = np.linspace(0, 2 * np.pi, n_rows)  # Ángulo theta
    R = np.abs(np.sin(theta))  # Radio R, por ejemplo, función seno absoluto
    df = pd.DataFrame({'theta': theta, 'R': R})
    return df


def graph_df(df):
    # Graficar el dataframe en coordenadas polares
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.plot(df['theta'], df['R'])
    ax.set_title(r'Distancia($\theta$)')
    plt.show()


def update_value_df(df, theta, distance):
    # Función para actualizar un único valor R dentro del dataframe
    index = df[df['theta'] == theta].index
    df.loc[index, 'R'] = distance


def blank_df(df):
    # Función para borrar todos los datos de la columna R dentro del dataframe
    df['R'] = np.nan


if __name__ == "__main__":
    # Crea un dataframe de pandas para guardar los datos y los grafica
    df = init_df(52)
    print(df)
    graph_df(df)
