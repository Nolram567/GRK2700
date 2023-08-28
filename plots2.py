import pandas as pd
import plotly.graph_objects as go

if __name__ == '__main__':
    data = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    df = pd.DataFrame(data)

    data = df.to_dict("records")

    df = pd.DataFrame(data)

    x_values = {
        "ort1": [8.25, 16.5, 24.75],
        "ort2": [41.25, 49.5, 57.75],
        "ort3": [74.25, 82.5, 90.25]
    }

    orte = sorted(df['ort'].unique())
    pam_keys = ["PAM-Wert_WSS", "PAM-Wert_NOSO", "PAM-Wert_NOT", "PAM-Wert_INT", "PAM-Wert_FG", "PAM-Wert_WSD"]

    # Initialdaten
    initial_ort = orte[0]
    initial_data = df[df['ort'] == initial_ort]
    initial_traces = [
        go.Scatter(
            x=x_values["ort1"],  # Ändern Sie dies entsprechend der Stadt
            y=initial_data[initial_data['GENERATION'] == gen][key].values,
            mode='markers',
            name=key
        )
        for key in pam_keys for gen in ['jung', 'mittel', 'alt']
    ]

    fig = go.Figure(data=initial_traces)

    dropdown_buttons = []

    # Dropdown-Menüs für jeden Ort
    for i, ort in enumerate(orte):
        ort_data = df[df['ort'] == ort]
        ort_x_values = x_values.get(f"ort{i + 1}", [0, 0, 0])
        traces = [
            {
                "x": ort_x_values,
                "y": ort_data[ort_data['GENERATION'] == gen][key].values
            }
            for key in pam_keys for gen in ['jung', 'mittel', 'alt']
        ]
        dropdown_buttons.append(
            dict(
                args=[{"x": traces, "y": traces}],
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
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
            dict(
                buttons=dropdown_buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.3,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
            dict(
                buttons=dropdown_buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="left",
                y=1.1,
                yanchor="top"
            )
        ],
        xaxis=dict(
            tickvals=x_values["ort1"] + x_values["ort2"] + x_values["ort3"],
            ticktext=['jung', 'mittel', 'alt'] * 3,
            range=[0, 100]
        ),
        yaxis=dict(range=[0, 3.5])
    )

    fig.show()