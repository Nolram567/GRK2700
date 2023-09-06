import configparser
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import pandas as pd
from urllib.parse import unquote
import numpy as np
import matplotlib
from geopy import Nominatim
from Statistics import Statistics

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    endpoints_to_files = {
        "/karte": "leaflat.nex.html",
        "/html_content": "chart.js_Beipiel.html",
        "/draw": "leaflat_draw_example.html",
        "/regions": "leaflet.js_regions.html",
        "/tabular": "tabular.html",
        "/": "leaflat.nex.html",
        #"/Konfigurator": "plotly_grafik.html",
        "/Impressum": "impressum.html"
    }

    df = pd.read_csv('data/d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    local_means_intergenerational, local_mean_intragenerational,\
        local_situational_means, regional_means_intergenerational,\
        regional_situational_means, regional_situational_means_intragenerational = Statistics.deserialization()

    def do_GET(self) -> None:
        print(self.path)
        if self.path.startswith("/data"):
            self.handle_data_endpoint()
        if self.path == "/logo_90.png":
            self.send_image_response()
        if self.path == "/favicon":
            self.send_favicon()
        if self.path == "/Konfigurator":
            self.handle_Konfigurator()
        if self.path in self.endpoints_to_files:
            file_name = self.endpoints_to_files[self.path]
            # print(self.path)
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()

            content = self.format_header(content)
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
        region = self.df[self.df['ort'] == city_name]['Region'].iloc[0]

        (local_mean, local_mean_young, local_mean_intermediate, local_mean_old,
         regional_mean, regional_mean_intra) = Statistics.pick_runtime_data(
        city_name,
        region,
        self.local_means_intergenerational,
        self.local_mean_intragenerational,
        self.regional_means_intergenerational,
        self.regional_situational_means_intragenerational
        )

        if filtered_df.empty:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Stadt nicht gefunden'}).encode())
        else:
            with open("chart_template.html", "r", encoding="utf-8") as f:
                html_template = f.read()


            html_content = self.format_header(html_template)
            html_content = html_content.replace("{{city}}", f"\"{city_name}\"") \
                .replace("{{title}}", city_name) \
                .replace("{{current_dataset}}", json.dumps(filtered_df.to_dict('records'), ensure_ascii=False)) \
                .replace("{{region}}", f"\"{region.lower()}\"") \
                .replace("{{local_intergenerational_mean_situational}}",
                         json.dumps(self.local_situational_means[city_name], ensure_ascii=False)) \
                .replace("{{regional_intergenerational_mean_situational}}",
                         json.dumps(self.regional_situational_means[region], ensure_ascii=False)) \
                .replace("{{regional_intragenerational_mean}}", json.dumps(regional_mean_intra, ensure_ascii=False)) \
                .replace("{{local_mean_PAM}}", f"{local_mean}") \
                .replace("{{local_young_mean}}", f"{local_mean_young}") \
                .replace("{{local_intermediate_mean}}", f"{local_mean_intermediate}") \
                .replace("{{local_old_mean}}", f"{local_mean_old}") \
                .replace("{{regional_general_mean}}", f"{regional_mean}") \
                # .replace("{{full_dataset}}", json.dumps(self.df.to_dict("records"), ensure_ascii=False))

            # print(html_content)

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

    def format_data_template(self):
        pass

    def format_header(self, html_content):
        config = configparser.ConfigParser()
        config.read('config.ini')
        base_url = config.get('Settings', 'base_url')
        return html_content.replace("{{ base_url }}", base_url)

    def handle_Konfigurator(self):

        with open("plotly_grafik.html", 'r', encoding='utf-8') as f:
            html_template = f.read()

        html_content = html_template.replace("{{full_dataset}}", json.dumps(self.df.to_dict("records"), ensure_ascii=False))
        html_content = self.format_header(html_content)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def send_image_response(self):
        image_path = 'logo_90.png'
        if os.path.exists(image_path):
            with open(image_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'File Not Found')

    def send_favicon(self):
        image_path = 'favicon.ico'
        if os.path.exists(image_path):
            with open(image_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'image/x-icon')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'File Not Found')


def run_server():
    server_address = ('', 8000)
    httpd = ThreadingSimpleServer(server_address, MyHTTPRequestHandler)
    print(f"Server läuft auf Port 8000, Thread {threading.current_thread().name}...")

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

    # print(data["ort"].unique())
