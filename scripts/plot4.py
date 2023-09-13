import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np

if __name__ == "__main__":
    data = pd.read_csv('../data/d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])
    mess_long = pd.DataFrame(data)

    situations = ['WSS', 'NOSO', 'NOT', 'INT', 'FG', 'WSD']
    generations = ['jung', 'mittel', 'alt']


    # Beispiel-Daten
    np.random.seed(123)
    n = 100

    # Erstellen der Subplots
    fig = sp.make_subplots(rows=2, cols=1, subplot_titles=("Boxplot und Jitter", "Dichteplot"), row_heights=[0.6, 0.4])

    # Boxplot und Jitter für verschiedene Situationen
    for sit in situations:
        col_name = f'PAM-Wert_{sit}'
        for gen in generations:
            subset = mess_long[mess_long['GENERATION'] == gen]
            fig.add_trace(
                go.Box(
                    x=[sit] * len(subset),
                    y=subset[col_name],
                    name=f"Box {sit} {gen}",
                    boxpoints='outliers',
                    jitter=0.3,
                    pointpos=0
                ),
                row=1,
                col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=[sit] * len(subset),
                    y=subset[col_name],
                    mode='markers',
                    name=f"Jitter {sit} {gen}",
                    marker=dict(opacity=0.1)
                ),
                row=1,
                col=1
            )

    # Dichteplot für verschiedene Generationen
    for gen in generations:
        subset = mess_long[mess_long['GENERATION'] == gen]
        for sit in situations:
            col_name = f'PAM-Wert_{sit}'
            fig.add_trace(
                go.Histogram(
                    x=subset[col_name],
                    histnorm='probability density',
                    name=f"Dichte {gen} {sit}",
                    opacity=0.2
                ),
                row=2,
                col=1
            )

    # Horizontale und vertikale Linien hinzufügen
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=-1,
            x1=len(situations),
            y0=0,
            y1=0,
            line=dict(
                color="Grey",
                width=0.4,
                dash="dash"
            )
        ),
        row=1,
        col=1
    )
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=0,
            x1=0,
            y0=0,
            y1=1,
            yref="paper",
            line=dict(
                color="Grey",
                width=0.4,
                dash="dash"
            )
        ),
        row=2,
        col=1
    )

    # Update layout
    fig.update_layout(
        height=700,
        width=900,
        showlegend=False
    )

    fig.show()
