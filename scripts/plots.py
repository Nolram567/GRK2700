import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

if __name__ == '__main__':


    data = pd.read_csv('../data/d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    df = pd.DataFrame(data)

    data = df.to_dict("records")

    # Eine Liste der PAM-Werte.
    pam_keys = ["PAM-Wert_WSS", "PAM-Wert_NOSO", "PAM-Wert_NOT", "PAM-Wert_INT", "PAM-Wert_FG", "PAM-Wert_WSD"]

    pam_symbols = {
        "Übersetzung in das Standarddeutsche": 'star-triangle-down',
        "Vorlesen": 'x',
        "Notruf": 'square',
        "Interview": 'triangle-up',
        "Freundesgespräch": 'circle',
        "Übersetzung in den Dialekt": 'star'
    }

    pam_titles = {
        "PAM-Wert_WSS": "Übersetzung in das Standarddeutsche",
        "PAM-Wert_NOSO": "Vorlesen",
        "PAM-Wert_NOT": "Notruf",
        "PAM-Wert_INT": "Interview",
        "PAM-Wert_FG": "Freundesgespräch",
        "PAM-Wert_WSD": "Übersetzung in den Dialekt"
    }

    x_values = {
        "first": [8.25, 16.5, 24.75],
        "second": [41.25, 49.5, 57.75],
        "third": [74.25, 82.5, 90.25]
    }

    orte = sorted(list(set(entry["ort"] for entry in data)))


    # Erzeugt die sichtbaren Daten für eine bestimmte Stadt.
    def generate_data_for_ort(ort_name):
        ort_data = [entry for entry in data if entry["ort"] == ort_name]
        y_data = {}
        for entry in ort_data:
            for key in pam_keys:
                y_data.setdefault(key, []).append(entry[key])
        return y_data


    dropdown_buttons1, dropdown_buttons2, dropdown_buttons3 = [], [], []

    for i, ort in enumerate(orte):
        ort_data = generate_data_for_ort(ort)
        args_dict = {"y": [ort_data[key] for key in pam_keys]}

        btn_dict = dict(args=[args_dict, [i]], label=ort, method="restyle")

        if i == 0:
            dropdown_buttons1.append(btn_dict)
        elif i == 1:
            dropdown_buttons2.append(btn_dict)
        elif i == 2:
            dropdown_buttons3.append(btn_dict)

    # Erzeugung der initialen Scatter-Traces
    initial_traces = []
    for i, ort in enumerate(['first', 'second', 'third']):
        initial_data = generate_data_for_ort(orte[0])
        for key in pam_keys:
            initial_traces.append(
                go.Scatter(
                    x=x_values[ort],
                    y=initial_data[key] if i == 0 else None,
                    mode='markers',
                    name=f"{pam_titles[key]} ({ort})",
                    marker=dict(symbol=pam_symbols[pam_titles[key]], size=13)
                )
            )

    fig = go.Figure(data=initial_traces)
    fig.update_layout(
        updatemenus=[
            dict(buttons=dropdown_buttons1, direction="down", x=0.1, xanchor="left", y=1.2, yanchor="top"),
            dict(buttons=dropdown_buttons2, direction="down", x=0.5, xanchor="left", y=1.2, yanchor="top"),
            dict(buttons=dropdown_buttons3, direction="down", x=0.9, xanchor="left", y=1.2, yanchor="top")
        ],
        yaxis=dict(range=[0, 3.5]),
        xaxis=dict(
            title="Generation",
            tickvals=x_values['first'] + x_values['second'] + x_values['third'],
            ticktext=["Jung", "Mittel", "Alt"] * 3,  # Dreimal, da es drei Städte gibt
            range=[0, 100]
        ),
        legend_title_text='Situationen',
        annotations=[
            dict(
                x=1,  # x-Position, die Sie anpassen können
                y=-0.3,  # y-Position, die Sie anpassen können
                xref='paper',  # x-Position ist relativ zur Breite des Diagramms
                yref='paper',  # y-Position ist relativ zur Höhe des Diagramms
                text="Dieser Konfigurator veranschaulicht die Abweichung vom Standarddeutschen der Gewehrpersonen nach Situation, Generation und Stadt.",  # Ihr Text
                showarrow=False  # Kein Pfeil, nur Text
            )
        ]
    )

    fig.show()

    html_string = fig.to_html(full_html=False, config={'displayModeBar': True,
                                                       "modeBarButtonsToRemove": ['zoom2d', 'pan2d', 'select2d', 'lasso2d']})

    html_document = f"""
            <!DOCTYPE html>
        <html lang="de">
        <head>
          <title>Konfigurator</title>
          <meta charset="UTF-8">
            <link rel="icon" href="http://localhost:8000/favicon" type="image/x-icon">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.4"></script>
            <script src="https://unpkg.com/chartjs-chart-box-and-violin-plot"></script>

           <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            /* Remove outline*/
            body, html {{
                  margin: 0;
                  padding: 0;
            }}

            .header {{
                background-color: #174d88;
                height: 95px;
                width: 100%;
                display: flex;
                align-items: center;
                box-shadow: 0px 3px 6px 0px rgba(0,0,0,0.16);
            }}
            .header img {{
                margin-left: 10px; /* Abstand zum linken Rand */
            }}
            .nav-container {{
                display: flex;
                justify-content: space-around;
                flex-grow: 1; /* Nimmt den verfügbaren Platz im Header auf */
                padding: 0 20px; /* Raum um die Links */
            }}
            .nav-container a {{
                background-color: #f8f9fa;
                text-decoration: none;
                color: black;
                font-size: 20px;
                padding: 10px 20px;
                border: 1px solid #333;
                border-radius: 5px;
                transition: 0.3s;
            }}
            .nav-container a:hover {{
                color: #fff;
                background-color: #333;
            }}
            footer {{
                background-color: #174d88;
                color: white; /* Farbe des Textes, in diesem Fall weiß */
                padding: 20px 0; /* Vertikales Padding */
                text-align: center; /* Zentrierung des Inhalts */
                width: 100%; /* Volle Breite */
                position: relative; /* Relative Positionierung */
                z-index: 1; /* Stellt sicher, dass die Fußzeile über anderen Inhalten angezeigt wird */
            }}
            .social-media {{
                position: absolute;
                right: 20px;
                top: 50%;
                transform: translateY(-50%);
            }}
        
            footer a, .social-media a {{
                color: white;
                text-decoration: none;
                margin-right: 10px;  /* Etwas Abstand zwischen den Symbolen */
            }}
        
            footer a:hover, .social-media a:hover {{
                text-decoration: underline;
                color: black;  /* Ändern Sie die Farbe beim Überfahren in schwarz */
            }}
        
            .social-media i {{  /* Ändern Sie die Farbe des Symbols selbst, nicht nur des Links */
                color: white;
            }}
        
            .social-media i:hover {{
                color: black;
            }}
          </style>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" rel="stylesheet">
        </head>
        <body>
          <div class="header">
                <img src="http://127.0.0.1:8000/logo_90.png" alt="Logo">
                <div class="nav-container">
                    <a href="http://127.0.0.1:8000/karte"><i class="fa-solid fa-map"></i> Karte</a>
                    <a href="http://127.0.0.1:8000/tabular"><i class="fa-solid fa-table"></i> Tabelle</a>
                    <a href="http://127.0.0.1:8000/Konfigurator"><i class="fa-solid fa-chart-column"></i> Konfigurator</a>
                </div>
          </div>
        <br>
            {html_string}
        <br><br><br>
        <footer>
        <div class="social-media">
            <a href="http://localhost:8000/Impressum">Impressum</a>
        </div>
            <a href="https://twitter.com/regionalsprache?lang=de" target="_blank"><i class="fa-brands fa-x-twitter"></i></a>
            <a href="https://www.instagram.com/deutschersprachatlas/" target="_blank"><i class="fa-brands fa-instagram"></i></a>
            <a href="https://www.facebook.com/DeutscherSprachatlas" target="_blank"><i class="fa-brands fa-facebook"></i></a>
        </footer>
        </body>
        </html>
        """
    # Zum Speichern als HTML-Datei
    with open("Konfigurator.html", "w", encoding="utf-8") as f:
        f.write(html_document)
