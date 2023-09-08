import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
'''
Performance Tester
'''

endpoints = [
    '/karte',
    '/html_content',
    '/tabular',
    '/',
    '/Impressum',
    '/data/Kassel',
    '/data/Hildesheim',
]


def make_random_request():
    while True:
        endpoint = random.choice(endpoints)
        start_time = time.time()
        try:
            # Anfrage an den Server senden
            response = requests.get(f'http://localhost:8000{endpoint}')

            # Überprüfen, ob die Anfrage erfolgreich war
            if response.status_code == 200:
                print(f'Endpoint {endpoint} OK, Zeit: {time.time() - start_time} Sekunden')
            else:
                print(f'Endpoint {endpoint} Fehler, Status-Code: {response.status_code}')
        except Exception as e:
            print(f'Fehler bei der Anfrage an {endpoint}: {e}')


with ThreadPoolExecutor(max_workers=64) as executor:
    for _ in range(64):
        executor.submit(make_random_request)
