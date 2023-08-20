import pandas as pd
import plotly.graph_objects as go
import json

if __name__ == '__main__':
    data = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    df = pd.DataFrame(data)

    data = df.to_dict("records")
    '''# Ihre Daten

    # Extrahieren Sie einzigartige Werte für die Spaltennamen, die "PAM-Wert_" enthalten
    features = [col for col in df.columns if "PAM-Wert_" in col]

    # Plot initialisieren
    fig = go.Figure()

    # Für jedes Feature einen scatter plot erstellen
    for feature in features:
        for gen in df['GENERATION'].unique():
            df_gen = df[df['GENERATION'] == gen]
            fig.add_trace(
                go.Scatter(x=df_gen['ort'], y=df_gen[feature],
                           mode='markers', name=gen, visible=(gen == 'alt')))

    # Dropdown Menü erstellen
    buttons = []
    for gen in df['GENERATION'].unique():
        visible = [g == gen for feature in features for g in df['GENERATION'].unique()]
        button = dict(label=gen,
                      method="update",
                      args=[{"visible": visible}])
        buttons.append(button)

    # Menü zum Plot hinzufügen
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=buttons,
            )
        ])

    fig.show()'''

    '''generations = df['GENERATION'].unique()
    orte = df['ort'].unique()

    # PAM-Spaltennamen finden
    pam_columns = [col for col in df.columns if 'PAM-Wert' in col]

    # Scatterplot Daten für jede Kombination von Generation und Ort erstellen
    traces = []
    for generation in generations:
        for ort in orte:
            df_filtered = df[(df['GENERATION'] == generation) & (df['ort'] == ort)]
            if not df_filtered.empty:
                for pam_col in pam_columns:
                    traces.append(
                        go.Scatter(
                            x=[pam_col.split("_")[1] for _ in df_filtered[pam_col]],
                            y=df_filtered[pam_col],
                            mode='markers',
                            name=f"{generation} - {ort}",
                            visible=(generation == generations[0] and ort == orte[0])
                            # Erster trace sichtbar, rest unsichtbar
                        )
                    )

    # Dropdown-Menüs erstellen
    generation_buttons = [
        {
            "args": [{"visible": [(gen == generation) & (o == ort) for gen in generations for o in orte for _ in
                                  pam_columns]}],
            "label": generation,
            "method": "restyle"
        }
        for generation in generations
    ]

    ort_buttons = [
        {
            "args": [{"visible": [(gen == generation) & (o == ort) for gen in generations for o in orte for _ in
                                  pam_columns]}],
            "label": ort,
            "method": "restyle"
        }
        for ort in orte
    ]

    # Scatterplot mit Dropdown-Menüs
    layout = go.Layout(
        xaxis={"title": "Varianten der PAM-Werte"},
        yaxis={"title": "Wert", "range": [0, 3.0]},
        updatemenus=[
            {
                "buttons": generation_buttons,
                "direction": "down",
                "showactive": True,
                "x": 0.1,
                "xanchor": "left",
                "y": 1.1,
                "yanchor": "top"
            },
            {
                "buttons": ort_buttons,
                "direction": "down",
                "showactive": True,
                "x": 0.4,
                "xanchor": "left",
                "y": 1.1,
                "yanchor": "top"
            }
        ]
    )

    fig = go.Figure(data=traces, layout=layout)
    fig.show()'''

    # Eine Liste der PAM-Werte.
    pam_keys = ["PAM-Wert_WSS", "PAM-Wert_NOSO", "PAM-Wert_NOT", "PAM-Wert_INT", "PAM-Wert_FG", "PAM-Wert_WSD"]

    pam_symbols = {
        "PAM-Wert_WSS": 'circle',
        "PAM-Wert_NOSO": 'square',
        "PAM-Wert_NOT": 'diamond',
        "PAM-Wert_INT": 'cross',
        "PAM-Wert_FG": 'x',
        "PAM-Wert_WSD": 'triangle-up'
    }

    orte = list(set(entry["ort"] for entry in data))


    # Erzeugt die sichtbaren Daten für eine bestimmte Stadt.
    def generate_data_for_ort(ort_name):
        ort_data = [entry for entry in data if entry["ort"] == ort_name]
        y_data = {}
        for entry in ort_data:
            for key in pam_keys:
                y_data.setdefault(key, []).append(entry[key])
        return y_data


    # Initialdaten für den ersten Ort.
    initial_data = generate_data_for_ort(orte[0])
    initial_traces = [
        go.Scatter(
            x=["jung", "mittel", "alt"],
            y=initial_data[key],
            mode='markers',
            name=key,
            marker=dict(symbol=pam_symbols[key],
                        size= 20)  # Setzen Sie das Symbol mit dem Dictionary
        )
        for key in pam_keys
    ]

    # Erstellt das Diagramm.
    fig = go.Figure(data=initial_traces)

    # Dropdown-Menü.
    dropdown_buttons = []

    for ort in orte:
        ort_data = generate_data_for_ort(ort)
        dropdown_buttons.append(
            dict(
                args=[{"y": [ort_data[key] for key in pam_keys]}],
                label=ort,
                method="restyle"
            )
        )

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=dropdown_buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="center",
                y=1.15,
                yanchor="top"
            ),
        ],
        yaxis=dict(range=[0, 3.0])
    )

    html_string = fig.to_html(full_html=False)

    html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plotly Grafik</title>
    </head>
    <body>
        <h1>Meine Plotly Grafik</h1>
        {html_string}
    </body>
    </html>
    """

    # Zum Speichern als HTML-Datei
    with open("plotly_grafik.html", "w", encoding="utf-8") as f:
        f.write(html_document)
