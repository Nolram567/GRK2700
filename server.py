import configparser
import json
import math
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import pandas as pd
from urllib.parse import unquote
from Statistics import Statistics


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def format_header(html_content: str) -> str:
    """
    Formats all hyperlinks according to the link specified in config.ini.

    :param html_content
    :return:
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    base_url = config.get('Settings', 'base_url')
    return html_content.replace("{{ base_url }}", base_url)


def format_footer(html_content: str) -> str:
    """
    Formats all hyperlinks according to the link specified in config.ini.

    :param html_content:
    :return:
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    x_url = config.get('Settings', 'x_url')
    instagram_url = config.get('Settings', 'instagram_url')
    facebook_url = config.get('Settings', 'facebook_url')
    return html_content.replace("{{ x_url }}", x_url) \
        .replace("{{ instagram_url }}", instagram_url) \
        .replace("{{ facebook_url }}", facebook_url)


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    My original plan was to build a prototype with a simple http server and request handler and port it to flask later on.
    But since I was short on time and the whole webpage is rather simple I decided to leave the backend like that since it's
    fully functional.

    Nevertheless, the code is a little messy...

    """

    endpoints_to_files = {
        "/karte": "leaflat.nex.html",
        "/tabular": "tabular.html",
        "/": "leaflat.nex.html",
        "/impressum": "impressum.html",
        "/datenuebersicht": "Datenuebersicht.html",
        "/ueber": "Ueber.html"
    }

    df = pd.read_csv('data/d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

    local_means_intergenerational, local_mean_intragenerational, \
        local_situational_means, regional_means_intergenerational, \
        regional_situational_means, regional_situational_means_intragenerational = Statistics.deserialization()

    def do_GET(self) -> None:
        print(self.path)
        if self.path.startswith("/data"):
            self.handle_data_endpoint()
        if self.path == "/logo_90.png":
            self.send_image_response()
        if self.path == "/favicon":
            self.send_favicon()
        if self.path == "/konfigurator":
            self.handle_konfigurator()
        if self.path in self.endpoints_to_files:
            file_name = self.endpoints_to_files[self.path]
            with open(f"public/{file_name}", "r", encoding="utf-8") as f:
                content = f.read()

            content = format_header(content)
            content = format_footer(content)
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

        city_name = unquote(path_parts[-1])
        filtered_df_ort = self.df[self.df['ort'] == city_name]
        region = self.df[self.df['ort'] == city_name]['Region'].iloc[0]
        filtered_df_region = self.df[self.df['Region'] == region]

        (local_mean, local_mean_young, local_mean_intermediate, local_mean_old,
         regional_mean, regional_mean_intra) = Statistics.pick_runtime_data(
            city_name,
            region,
            self.local_means_intergenerational,
            self.local_mean_intragenerational,
            self.regional_means_intergenerational,
            self.regional_situational_means_intragenerational
        )

        if filtered_df_ort.empty:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Stadt nicht gefunden'}).encode())
        else:
            with open("public/chart_template.html", "r", encoding="utf-8") as f:
                html_template = f.read()

            html_content = format_header(html_template)
            html_content = format_footer(html_content)
            html_content = html_content.replace("{{city}}", f"\"{city_name}\"") \
                .replace("{{title}}", city_name) \
                .replace("{{current_dataset}}", json.dumps(filtered_df_ort.to_dict('records'), ensure_ascii=False)) \
                .replace("{{regional_dataset}}", json.dumps(filtered_df_region.to_dict('records'), ensure_ascii=False)) \
                .replace("{{region}}", f"\"{region.lower()}\"") \
                .replace("{{local_intergenerational_mean_situational}}",
                         json.dumps(self.local_situational_means[city_name], ensure_ascii=False)) \
                .replace("{{regional_intergenerational_mean_situational}}",
                         json.dumps(self.regional_situational_means[region], ensure_ascii=False)) \
                .replace("{{regional_intragenerational_mean}}", json.dumps(regional_mean_intra, ensure_ascii=False)) \
                .replace("{{local_mean_PAM}}", f"{local_mean if not math.isnan(local_mean) else 0}") \
                .replace("{{local_young_mean}}", f"{local_mean_young if not math.isnan(local_mean_young) else 0}") \
                .replace("{{local_intermediate_mean}}",
                         f"{local_mean_intermediate if not math.isnan(local_mean_intermediate) else 0}") \
                .replace("{{local_old_mean}}", f"{local_mean_old if not math.isnan(local_mean_old) else 0}") \
                .replace("{{regional_general_mean}}", f"{regional_mean if not math.isnan(regional_mean) else 0}")

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

    def handle_konfigurator(self) -> None:
        with open("public/Konfigurator.html", 'r', encoding='utf-8') as f:
            html_template = f.read()

        html_content = format_header(html_template)
        html_content = format_footer(html_content)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def send_image_response(self) -> None:
        image_path = 'public/logo_90.png'
        if os.path.exists(image_path):
            with open(image_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'File Not Found')

    def send_favicon(self) -> None:
        image_path = 'public/favicon.ico'
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
