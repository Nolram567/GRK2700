import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import pandas as pd
from urllib.parse import unquote
import numpy as np
import matplotlib
from geopy import Nominatim


class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    endpoints_to_files = {
        "/karte": "leaflat.nex.html",
        "/html_content": "chart.js_Beipiel.html",
        "/draw": "leaflat_draw_example.html",
        "/regions": "leaflet.js_regions.html",
        "/tabular": "tabular.html",
        "/": "leaflat.nex.html"
    }

    df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    def do_GET(self) -> None:
        print(self.path)
        if self.path.startswith("/data"):
            self.handle_data_endpoint()
        if self.path in self.endpoints_to_files:
            file_name = self.endpoints_to_files[self.path]
            #print(self.path)
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_response(404)

    def handle_data_endpoint(self) -> None:
        path_parts = self.path.split('/')
        if len(path_parts) < 3:
            self.send_error(400, 'Stadtname muss angegeben werden')
            return

        city_name = unquote(path_parts[2])
        filtered_df = self.df[self.df['ort'] == city_name]
        region = self.df[self.df['ort'] == city_name]['Region'].iloc[0].lower()
        #filtered_df2 = self.df[self.df['Region'] == region]

        if filtered_df.empty:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Stadt nicht gefunden'}).encode())
        else:
            data = filtered_df.to_dict('records')
            #data2 = filtered_df2.to_dict('records')
            regional_means = Statistics.calculate_means_for_regions(city_name)
            local_means = Statistics.calculate_means_for_citys(city_name)
            regional_means[0].reset_index(drop=True, inplace=True)
            local_means[0].reset_index(drop=True, inplace=True)
            local_mean_PAM = Statistics.calculate_mean_PAM(local_means[1])
            regional_intragenerational_mean = regional_means[0].to_dict('records')
            regional_intergenerational_mean = regional_means[1].to_dict()
            #regional_mean_PAM = Statistics.calculate_mean_PAM(regional_means[1]).to_dict()
            local_intragenerational_mean = local_means[0].to_dict('records')
            local_intergenerational_mean = local_means[1].to_dict()
            local_general_PAM = Statistics.calculate_mean_local_generation(filtered_df)
            local_general_PAM_intergenerational = np.mean([local_general_PAM['jung'], local_general_PAM['mittel'], local_general_PAM['alt']])
            regional_general_PAM_intergenerational = Statistics.calculate_regional_general_PAM_intergenerational(regional_intergenerational_mean)
            print(regional_general_PAM_intergenerational)

            with open("chart_template.html", "r", encoding="utf-8") as f:
                html_template = f.read()

            # Ersetze die Datenplatzhalter in der HTML-Datei durch die tatsächlichen Daten
            html_content = html_template.replace("{{city}}", f"\"{city_name}\"")\
                .replace("{{current_dataset}}", json.dumps(data, ensure_ascii=False)) \
                .replace("{{region}}", f"\"{region}\"") \
                .replace("{{regional_intragenerational_mean}}", json.dumps(regional_intragenerational_mean, ensure_ascii=False)) \
                .replace("{{regional_intergenerational_mean}}", json.dumps(regional_intergenerational_mean, ensure_ascii=False)) \
                .replace("{{local_intragenerational_mean}}", json.dumps(local_intragenerational_mean, ensure_ascii=False)) \
                .replace("{{local_intergenerational_mean}}", json.dumps(local_intergenerational_mean, ensure_ascii=False)) \
                .replace("{{local_mean_PAM}}", f"{local_general_PAM_intergenerational}") \
                .replace("{{local_young_mean}}", f"{local_general_PAM['jung']}") \
                .replace("{{local_intermediate_mean}}", f"{local_general_PAM['mittel']}") \
                .replace("{{local_old_mean}}", f"{local_general_PAM['alt']}") \
                .replace("{{regional_general_mean}}", f"{json.dumps(regional_general_PAM_intergenerational, ensure_ascii=False)}")
                #.replace("{{full_dataset}}", json.dumps(self.df.to_dict("records"), ensure_ascii=False)) \

            #print(html_content)

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))




class Statistics():
    @staticmethod
    def calculate_means_for_regions(city_name):
        df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

        region = df[df['ort'] == city_name]['Region'].iloc[0]
        df = df[df['Region'] == region]

        df = df.drop(columns=["gid", "ort", "Informant"])

        mean_df = df.groupby('GENERATION').mean(numeric_only=True).reset_index()

        mean_all = mean_df.mean(numeric_only=True)

        return [mean_df, mean_all]

    @staticmethod
    def calculate_means_for_citys(city_name):
        df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

        df = df[df['ort'] == city_name]

        df = df.drop(columns=["gid", "ort", "Informant"])

        mean_df = df.groupby('GENERATION').mean(numeric_only=True).reset_index()

        mean_all = mean_df.mean(numeric_only=True)

        return [mean_df, mean_all]

    @staticmethod
    def calculate_mean_local_generation(df):

        df = df[[col for col in df.columns if 'PAM-Wert' in col or 'GENERATION' in col]]

        mean_pam_values = df.groupby('GENERATION').mean()

        mean_pam_values = mean_pam_values.mean(axis=1)

        return mean_pam_values

    @staticmethod
    def calculate_mean_PAM(s):
        # Entferne die Kontrollwert-Elemente
        s = s.dropna()

        s = s.drop(columns=["Kontrollwert_WSS", "Kontrollwert_NOSO", "Kontrollwert_NOT", "Kontrollwert_INT", "Kontrollwert_FG", "Kontrollwert_WSD"])

        # Berechne den Mittelwert
        mean_PAM = s.mean()

        # Erstelle eine neue Series mit dem berechneten Mittelwert
        mean_series = pd.Series({'Mean_PAM': mean_PAM})

        return mean_series

    @staticmethod
    def calculate_regional_general_PAM_intergenerational(d: dict) -> dict:
        filtered_values = [value for key, value in d.items() if
                           not key.startswith('Kontrollwert') and not np.isnan(value)]
        average_pam = np.mean(filtered_values)
        return average_pam

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print('Server läuft auf Port 8000...')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print('Server gestoppt.')


if __name__ == '__main__':
    run_server()



    '''# Beispiel DataFrame erstellen
    df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    df.replace(['n. d.', np.nan], '-', inplace=True)

    # DataFrame als HTML exportieren
    html_string = df.to_html(index=False, escape=False)

    # Die HTML-String in eine Datei schreiben mit utf-8 Encoding
    with open('', 'w', encoding='utf-8') as f:
        f.write(html_string)'''
    '''data = [{'GENERATION': 'alt', 'PAM-Wert_WSS': 1.1, 'Kontrollwert_WSS': 0.7, 'PAM-Wert_NOSO': 1.15,
             'Kontrollwert_NOSO': 0.8, 'PAM-Wert_NOT': np.nan, 'PAM-Wert_INT': 1.58, 'Kontrollwert_INT': 1.0,
             'PAM-Wert_FG': 1.62, 'Kontrollwert_FG': 1.0, 'PAM-Wert_WSD': 1.69, 'Kontrollwert_WSD': 1.3},
            {'GENERATION': 'jung', 'PAM-Wert_WSS': 0.79, 'Kontrollwert_WSS': 0.6, 'PAM-Wert_NOSO': 1.05,
             'Kontrollwert_NOSO': 0.8, 'PAM-Wert_NOT': np.nan, 'PAM-Wert_INT': 1.35, 'Kontrollwert_INT': 1.1,
             'PAM-Wert_FG': 1.43, 'Kontrollwert_FG': 1.1, 'PAM-Wert_WSD': 1.31, 'Kontrollwert_WSD': 1.1},
            {'GENERATION': 'mittel', 'PAM-Wert_WSS': 1.01, 'Kontrollwert_WSS': 0.8, 'PAM-Wert_NOSO': 1.34,
             'Kontrollwert_NOSO': 1.0, 'PAM-Wert_NOT': np.nan, 'PAM-Wert_INT': 1.83, 'Kontrollwert_INT': 1.2,
             'PAM-Wert_FG': 1.78, 'Kontrollwert_FG': 1.4, 'PAM-Wert_WSD': 1.38, 'Kontrollwert_WSD': 1.0}]
    # Erzeugen des DataFrames
    # Erzeugen des DataFrames
    df = pd.DataFrame(data)

    # Behalten nur der Spalten, die 'PAM-Wert' oder 'GENERATION' enthalten
    df = df[[col for col in df.columns if 'PAM-Wert' in col or 'GENERATION' in col]]

    # Berechnen des Durchschnitts der 'PAM-Wert'-Spalten für jede 'GENERATION'
    mean_pam_values = df.groupby('GENERATION').mean()

    # Berechnen des Durchschnitts dieser Mittelwerte für jede 'GENERATION'
    mean_pam_values = mean_pam_values.mean(axis=1)

    # Ausgabe der Ergebnisse
    print(mean_pam_values)'''

    '''data = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    filtered_df = df[df['ort'] == "Kassel"]
    region = df[df['ort'] == "Kassel"]['Region'].iloc[0]
    df = df[df['Region'] == region]

    df = df.drop(columns=["gid", "ort", "Informant"])

    mean_df = df.groupby('GENERATION').mean(numeric_only=True).reset_index()

    mean_all = mean_df.mean(numeric_only=True)

    print([mean_df, mean_all])
    print(type([mean_df, mean_all][0]))


    #print(str(data["ort"].unique()).replace("\'", "").replace("[", "").replace("]", ""). replace(" ", ", "))
    print(data.loc[(data["ort"] == "Alt Duvenstedt") & (data["GENERATION"] == "alt"), "PAM-Wert_WSS"])
    geolocator = Nominatim(user_agent="geoapiExercises")'''

    '''cities = ["Alt Duvenstedt", "Bad Segeberg", "Flensburg", "Lohne",
              "Oldenburg", "Lüneburg", "Neustadt am Rübenberge", "Rostock",
              "Schwerin", "Stralsund", "Bergen", "Pasewalk",
              "Frankfurt an der Oder", "Fürstenwalde", "Potsdam", "Pritzwalk",
              "Lüderitz", "Brandenburg an der Havel", "Neuruppin", "Borken",
              "Hagen", "Gütersloh", "Horn-Bad Meinberg", "Drolshagen",
              "Halberstadt", "Hildesheim", "Northeim", "Magdeburg",
              "Bergisch-Gladbach", "Düren", "Troisdorf", "Krefeld",
              "Mönchengladbach", "Montabaur", "Schweich", "Wittlich",
              "Altenkirchen", "Heidelberg", "Kaiserslautern", "Erbach",
              "Reinheim", "Kirkel", "Merzig", "Mainz", "Heilbronn",
              "Frankfurt am Main", "Kleve", "Homberg", "Kassel",
              "Bad Nauheim", "Büdingen", "Gießen", "Ulrichstein",
              "Hofbieber", "Erfurt", "Heilbad Heiligenstadt",
              "Sondershausen", "Gera", "Halle", "Dresden", "Reichenbach",
              "Dessau", "Ansbach", "Bamberg", "Würzburg", "Hirschau",
              "Weiden", "Ingolstadt", "Regensburg", "München", "Passau",
              "Trostberg", "Farchant", "Augsburg", "Calw", "Kaufbeuren",
              "Ulm", "Balingen", "Rudersberg", "Blindheim", "Waldshut",
              "Steinen", "Bräunlingen", "Ravensburg", "Tuttlingen", "Ohlsbach"]

    my_mean_values = []
    for city in cities:
        #location = geolocator.geocode(city + ", Deutschland")
        #print(f"{{name: '{city}', lat: {location.latitude}, lng: {location.longitude}}},")
        local_means = Statistics.calculate_means_for_citys(city)
        New_value = Statistics.calculate_mean_PAM(Statistics.calculate_mean_PAM(local_means[1]))['Mean_PAM']
        if not np.isnan(New_value):
            my_mean_values.append(New_value)
        print(np.mean(my_mean_values))
        time.sleep(1)'''

    #print(data["ort"].unique())