import pandas as pd
import plotly.graph_objects as go
import json

if __name__ == '__main__':
    data = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    df = pd.DataFrame(data)

    data = df.to_dict("records")

    # Eine Liste der PAM-Werte.
    pam_keys = ["PAM-Wert_WSS", "PAM-Wert_NOSO", "PAM-Wert_NOT", "PAM-Wert_INT", "PAM-Wert_FG", "PAM-Wert_WSD"]

    pam_symbols = {
        "Übersetzung in das Standarddeutsche": 'circle',
        "Vorlesen": 'square',
        "Notruf": 'diamond',
        "Interview": 'cross',
        "Freundesgespräch": 'x',
        "Übersetzung in den Dialekt": 'triangle-up'
    }

    pam_titles = {
        "PAM-Wert_WSS": "Übersetzung in das Standarddeutsche",
        "PAM-Wert_NOSO": "Vorlesen",
        "PAM-Wert_NOT": "Notruf",
        "PAM-Wert_INT": "Interview",
        "PAM-Wert_FG": "Freundesgespräch",
        "PAM-Wert_WSD": "Übersetzung in den Dialekt"
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


    # Initialdaten für den ersten Ort.
    initial_data = generate_data_for_ort(orte[0])
    initial_traces = [
        go.Scatter(
            x=["Jung", "Mittel", "Alt"],
            y=initial_data[key],
            mode='markers',
            name=pam_titles[key],
            marker=dict(symbol=pam_symbols[pam_titles[key]], size=20)
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
                y=1.2,
                yanchor="top"
            ),
        ],
        yaxis=dict(range=[0, 3.5]),
        xaxis=dict(title="Generation"),
        legend_title_text='Situationen'
    )

    fig.show()




    '''html_string = fig.to_html(full_html=False)

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
    with open("plotly_grafik_test.html", "w", encoding="utf-8") as f:
        f.write(html_document)'''
