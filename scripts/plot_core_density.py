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

    pam_columns = [col for col in df.columns if col.startswith('PAM')]

    values_list = []

    for col in pam_columns:
        values_list.extend(df[col].tolist())


    values_list = [entry for entry in values_list if not math.isnan(entry)]

    print(values_list)

    X = np.array(values_list).reshape(-1, 1)

    kde = KernelDensity(kernel='gaussian', bandwidth=1.0)
    kde.fit(X)


    X_plot = np.linspace(-10, 10, 1000)[:, np.newaxis]

    log_density = kde.score_samples(X_plot)

    fig = go.Figure(data=[go.Scatter(x=X_plot.squeeze(), y=np.exp(log_density), mode='lines')])

    fig.update_layout(
        title='Kerndichteschätzung',
        xaxis=dict(title='X'),
        yaxis=dict(title='Dichte')
    )

    fig.show()