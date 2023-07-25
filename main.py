from http.server import BaseHTTPRequestHandler, HTTPServer
import pandas as pd
import matplotlib
from geopy.geocoders import Nominatim
import time
from flask import Flask, render_template_string

# Definiere den Handler für den HTTP-Server
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    global my_headers
    global my_endpoints

    my_headers = ["test"]
    my_endpoints = ["/karte", "/html_content", "/draw", "/regions", "/tabular"]


    def do_GET(self):

        with open("chart.js_Beipiel.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        with open("leaflat_draw_example.html", "r", encoding="utf-8") as f:
            draw = f.read()

        with open("leaflat.nex.html", "r", encoding="utf-8") as f:
            karte = f.read()

        with open("leaflet.js_regions.html", "r", encoding="utf-8") as f:
            regions = f.read()

        with open("tabular.html", "r", encoding="utf-8") as f:
            tabular = f.read()

        print(self.path)
        # Setze den Response-Code auf 200 (OK)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        if self.path in my_endpoints:
            self.wfile.write(locals().get(f"{self.path.replace('/', '')}").encode('utf-8'))

# Hauptfunktion
def run_server():

    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print('Server läuft auf Port 8000...')

    # Starte den Server und halte ihn aktiv, bis er unterbrochen wird
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    # Stoppe den Server
    httpd.server_close()
    print('Server gestoppt.')

# Führe die Hauptfunktion aus
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