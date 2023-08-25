import plotly.express as px
import pandas as pd

if __name__ == "__main__":
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    # Ihre Daten als DataFrame
    data = pd.DataFrame([
        {'name': 'Alt Duvenstedt', 'lat': 54.3586037, 'lng': 9.6437579, 'PAM_Mittelwert': 1.216},
        {'name': 'Bad Segeberg', 'lat': 53.9422672, 'lng': 10.3137943, 'PAM_Mittelwert': 1.332},
        {'name': 'Flensburg', 'lat': 54.7833021, 'lng': 9.4333264, 'PAM_Mittelwert': 1.598},
        # ... weitere Einträge
    ])

    # Entfernen Sie Zeilen mit NaN-Werten im PAM_Mittelwert
    data = data.dropna(subset=['PAM_Mittelwert'])

    # Scatter-Geo-Plot erstellen
    fig = go.Figure(data=go.Scattergeo(
        lon=data['lng'],
        lat=data['lat'],
        text=data['name'],
        mode='markers',
        marker=dict(
            size=8,
            opacity=0.8,
            reversescale=True,
            autocolorscale=False,
            symbol='circle',
            line=dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale='Blues',
            cmin=data['PAM_Mittelwert'].min(),
            color=data['PAM_Mittelwert'],
            cmax=data['PAM_Mittelwert'].max(),
            colorbar_title="PAM Mittelwert"
        )))

    # Fügen Sie Layout-Optionen hinzu, um nur Deutschland anzuzeigen
    fig.update_geos(
        projection_type="mercator",
        lonaxis=dict(range=[5, 16]),
        lataxis=dict(range=[47, 56])
    )

    fig.update_layout(
        title='PAM Mittelwerte in verschiedenen Städten Deutschlands',
        geo=dict(
            scope='europe',
            projection_type='mercator',
            showland=True,
            landcolor="rgb(250, 250, 250)"
        )
    )

    fig.show()
