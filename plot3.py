import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if __name__ == '__main__':
    data = pd.read_csv('data/d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])
    df = pd.DataFrame(data)

    df.rename(columns={
        'GENERATION': 'Generation',
        'PAM-Wert_NOT': 'Notruf',
        'PAM-Wert_INT': 'Interview',
        'PAM-Wert_FG': 'Freudesgespräch',
        'PAM-Wert_NOSO': 'Vorlesen',
        'PAM-Wert_WSD': 'Übersetzung in das Standarddeutsche',
        'PAM-Wert_WSS': 'Übersetzung in den Dialekt'

    }, inplace=True)
    # Erstellen Sie eine Subplot-Figur mit 1 Zeile und 3 Spalten
    fig = make_subplots(rows=1, cols=3, subplot_titles=("Freudesgespräch", "Interview", "Notruf", "Vorlesen", "Übersetzung in das Standarddeutsche", "Übersetzung in den Dialekt"))
    fig2 = make_subplots(rows=1, cols=3, subplot_titles=("Vorlesen", "Übersetzung in das Standarddeutsche", "Übersetzung in den Dialekt"))

    hover_text = df['ort'].apply(lambda x: f'{x}')
    # Füge Boxplots hinzu
    fig.add_trace(
        go.Box(y=df['Freudesgespräch'], x=df["Generation"], boxpoints='all', hovertext=hover_text,  hoverinfo='y+text', boxmean='sd'),
        row=1, col=1
    )
    fig.add_trace(
        go.Box(y=df["Interview"], x=df["Generation"], boxpoints='all', hovertext=hover_text,  hoverinfo='y+text', boxmean='sd'),
        row=1, col=2
    )
    fig.add_trace(
        go.Box(y=df["Notruf"], x=df["Generation"], boxpoints='all', hovertext=hover_text, hoverinfo='y+text', boxmean='sd'),
        row=1, col=3
    )
    fig2.add_trace(
        go.Box(y=df["Vorlesen"], x=df["Generation"], boxpoints='all', hovertext=hover_text,  hoverinfo='y+text', boxmean='sd', ),
        row=1, col=1
    )
    fig2.add_trace(
        go.Box(y=df['Übersetzung in den Dialekt'], x=df["Generation"], boxpoints='all', hovertext=hover_text,  hoverinfo='y+text', boxmean='sd'),
        row=1, col=2
    )
    fig2.add_trace(
        go.Box(y=df["Übersetzung in das Standarddeutsche"], x=df["Generation"], boxpoints='all', hovertext=hover_text,  hoverinfo='y+text', boxmean='sd'),
        row=1, col=3
    )
    # Aktualisieren Sie das Layout
    fig.update_layout(showlegend=False)
    fig2.update_layout(showlegend=False)
    config = {
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'hoverClosestCartesian', 'hoverCompareCartesian', 'toggleSpikelines'],
        'modeBarButtonsToAdd': ['toImage']
    }


    fig.show()
    fig.update_layout(width=1263)
    fig2.update_layout(width=1263)

    html_string = fig.to_html(full_html=False, config=config)
    html_string2 = fig2.to_html(full_html=False, config={'displayModeBar': False})

    html_document = f"""
                <!DOCTYPE html>
            <html lang="de">
            <head>
              <title>Datenübersicht</title>
              <meta charset="UTF-8">
                <link rel="icon" href="{{{{ base_url }}}}/favicon" type="image/x-icon">
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
                <img src="{{{{ base_url }}}}/logo_90.png" alt="Logo">
                <div class="nav-container">
                    <a href="{{{{ base_url }}}}/karte"><i class="fa-solid fa-map"></i> Karte</a>
                    <a href="{{{{ base_url }}}}/tabular"><i class="fa-solid fa-table"></i> Tabelle</a>
                    <a href="{{{{ base_url }}}}/Konfigurator"><i class="fa-solid fa-chart-column"></i> Konfigurator</a>
                </div>
                </div>
            <br>
                {html_string}
                {html_string2}
        
        <br><br><br>
            <footer>
        <div class="social-media">
            <a href="{{{{ base_url }}}}/Impressum">Impressum</a>
        </div>
            <a href="{{{{ x_url }}}}" target="_blank"><i class="fa-brands fa-x-twitter"></i></a>
            <a href="{{{{ instagram_url }}}}" target="_blank"><i class="fa-brands fa-instagram"></i></a>
            <a href="{{{{ facebook_url }}}}" target="_blank"><i class="fa-brands fa-facebook"></i></a>
        </footer>
            </body>
            </html>
            """
    #print(html_document)

    '''# Zum Speichern als HTML-Datei
    with open("public/Datenübersicht.html", "w", encoding="utf-8") as f:
        f.write(html_document)'''
