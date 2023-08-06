import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import pandas as pd
from urllib.parse import unquote
import numpy as np
import matplotlib
from geopy import Nominatim


# Definiere den Handler für den HTTP-Server
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    # Definieren Sie eine explizite Zuordnung der Endpunkte zu den Dateien
    endpoints_to_files = {
        "/karte": "leaflat.nex.html",
        "/html_content": "chart.js_Beipiel.html",
        "/draw": "leaflat_draw_example.html",
        "/regions": "leaflet.js_regions.html",
        "/tabular": "tabular.html",
        "": "leaflat.nex.html"
    }

    df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    def do_GET(self) -> None:
        # Überprüfen Sie, ob der Pfad ein gültiger Endpunkt ist
        print(self.path)
        if self.path.startswith("/data"):
            self.handle_data_endpoint()
        if self.path in self.endpoints_to_files:
            file_name = self.endpoints_to_files[self.path]
            #print(self.path)
            # Öffnen und lesen Sie die Datei nur, wenn der Pfad ein gültiger Endpunkt ist
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_response(404)  # sende "Not Found" Antwort, wenn der Pfad nicht gültig ist

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
            print(local_mean_PAM)
            regional_intragenerational_mean = regional_means[0].to_dict('records')
            regional_intergenerational_mean = regional_means[1].to_dict()
            local_intragenerational_mean = local_means[0].to_dict('records')
            local_intergenerational_mean = local_means[1].to_dict()
            local_mean_PAM = local_mean_PAM.to_dict()
            print(local_mean_PAM)

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
                .replace("{{local_mean_PAM}}", json.dumps(local_mean_PAM, ensure_ascii=False))
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
    def calculate_mean_PAM(s):
        # Entferne die Kontrollwert-Elemente
        s = s.dropna()

        s = s.drop(columns=["Kontrollwert_WSS", "Kontrollwert_NOSO", "Kontrollwert_NOT", "Kontrollwert_INT", "Kontrollwert_FG", "Kontrollwert_WSD"])

        # Berechne den Mittelwert
        mean_PAM = s.mean()

        # Erstelle eine neue Series mit dem berechneten Mittelwert
        mean_series = pd.Series({'Mean_PAM': mean_PAM})

        return mean_series


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
    geolocator = Nominatim(user_agent="geoapiExercises")

    cities = ["Alt Duvenstedt", "Bad Segeberg", "Flensburg", "Lohne",
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

    my_cities = []
    for city in cities:
        location = geolocator.geocode(city + ", Deutschland")
        #print(f"{{name: '{city}', lat: {location.latitude}, lng: {location.longitude}}},")
        try:
            local_means = Statistics.calculate_means_for_citys(city)
            local_mean_PAM = Statistics.calculate_mean_PAM(local_means[1])
            Mean_PAM = local_mean_PAM['Mean_PAM']
        except KeyError:
            Mean_PAM = ""
        my_cities.append(f"{{name: '{city}', lat: {location.latitude}, lng: {location.longitude}, PAM_Mittelwert: {Mean_PAM}}}")
        print(f"{my_cities[-1]}, ")
        time.sleep(1)'''

    #print(data["ort"].unique())