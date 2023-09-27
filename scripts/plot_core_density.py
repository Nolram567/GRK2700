import math

import numpy as np
from sklearn.neighbors import KernelDensity
import plotly.graph_objects as go
import pandas as pd

if __name__ == "__main__":

    data = pd.read_csv('../data/d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])
    df = pd.DataFrame(data)

    situations = ['WSS', 'NOSO', 'NOT', 'INT', 'FG', 'WSD']
    generations = ['jung', 'mittel', 'alt']

    # Extrahieren der Spalten, die mit "PAM" beginnen
    pam_columns = [col for col in df.columns if col.startswith('PAM')]

    # Extrahieren der numerischen Werte aus diesen Spalten
    values_list = []

    for col in pam_columns:
        values_list.extend(df[col].tolist())


    values_list = [entry for entry in values_list if not math.isnan(entry)]

    print(values_list)

    # Generieren Sie Beispieldaten
    X = np.array(values_list).reshape(-1, 1)

    # Erstellen Sie das KDE-Modell
    kde = KernelDensity(kernel='gaussian', bandwidth=1.0)
    kde.fit(X)

    # Generieren Sie Datenpunkte für die Visualisierung
    X_plot = np.linspace(-10, 10, 1000)[:, np.newaxis]

    # Berechnen Sie die Dichtewerte
    log_density = kde.score_samples(X_plot)

    # Visualisierung mit plotly
    fig = go.Figure(data=[go.Scatter(x=X_plot.squeeze(), y=np.exp(log_density), mode='lines')])

    fig.update_layout(
        title='Kerndichteschätzung',
        xaxis=dict(title='X'),
        yaxis=dict(title='Dichte')
    )

    fig.show()