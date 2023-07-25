from http.server import BaseHTTPRequestHandler, HTTPServer
import pandas as pd
import matplotlib
from geopy.geocoders import Nominatim
import time
from flask import Flask, render_template_string

# Definiere den Handler für den HTTP-Server
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    # Definieren Sie eine explizite Zuordnung der Endpunkte zu den Dateien
    endpoints_to_files = {
        "/karte": "leaflat.nex.html",
        "/html_content": "chart.js_Beipiel.html",
        "/draw": "leaflat_draw_example.html",
        "/regions": "leaflet.js_regions.html",
        "/tabular": "tabular.html",
    }

    def do_GET(self):
        # Überprüfen Sie, ob der Pfad ein gültiger Endpunkt ist
        if self.path in self.endpoints_to_files:
            file_name = self.endpoints_to_files[self.path]

            # Öffnen und lesen Sie die Datei nur, wenn der Pfad ein gültiger Endpunkt ist
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_response(404)  # sende "Not Found" Antwort, wenn der Pfad nicht gültig ist

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


    '''#print(str(data["ort"].unique()).replace("\'", "").replace("[", "").replace("]", ""). replace(" ", ", "))
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
            PAM_Alt = data.loc[(data["ort"] == city) & (data["GENERATION"] == "alt"), "PAM-Wert_WSS"].item()
            PAM_Mittel = data.loc[(data["ort"] == city) & (data["GENERATION"] == "mittel"), "PAM-Wert_WSS"].item()
            PAM_Jung = data.loc[(data["ort"] == city) & (data["GENERATION"] == "jung"), "PAM-Wert_WSS"].item()
        except KeyError:
            PAM_Alt = ""
            PAM_Mittel = ""
            PAM_Jung = ""
        my_cities.append(f"{{name: '{city}', lat: {location.latitude}, lng: {location.longitude}, PAM_Wert_Alt: {PAM_Alt}, PAM_Wert_Mittel: {PAM_Mittel}, PAM_Wert_Jung: {PAM_Jung}}}")
        print(f"{my_cities[-1]}, ")
        time.sleep(1)'''

    #print(data["ort"].unique())