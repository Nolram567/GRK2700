# Daten-Dashboard für das Rede-Projekt

Dieses Dashboard veranschaulicht den zur Verfügung gestellten Datnesatz des Redeprojekts, in dem phonetische Abstandsmessungen in verschiedenen Regionen Deutschlands durchgeführt wurden. 

Das Backend umfasst einen multithreaded Python-Server, einige Skripte für die (statistische) Datenverarbeitung, sowie einige HTML-Dokumente, welche zur Laufzeit mit Daten formatiert werden. [^1]

Dieses Projekt nutzt die Open-Source-Bilbliotheken [Chart.js](https://www.chartjs.org/), [Plotly](https://plotly.com/python/) und [Leaflet](https://leafletjs.com/). 

[^1]: Grundsätzlich wäre ein Port auf modernes Framwork wie Flask sinnvoll. Zu Beginn dachte ich jedoch noch, dass dies aufgrund der eigentlichen Einfachheit nicht nötig sei und dann fehlte mir die Zeit, um das Projekt noch einmal mit Flask zu realisieren.

# Übersicht und Benutzung

Die Ordnerstruktur des Projekts sieht folgendermaßen aus:

Rede-Dashboard/
├── .gitignore           # Git-Ignore-Datei zum Ausschließen bestimmter Dateien

├── README.md            # Projektdokumentation und -beschreibung

├── requirements.txt     # Die Abhängigkeiten des Python-Projekts

├──config.ini               # Die Konfigurationsdatei, die die finale URL der Webseite enthalten sollte.

├── Dockerfile        

├── data/             # Die Rohdaten und die verarbeiteten Daten liegen in diesem Verzeichnis.

│   └── ...

├── public/              # In diesem Ordner liegen die HTML-Dateien, die Grafiken, das Favicon. [^2]

│   ├── ...         # Haupt-Server-Datei (oder wie auch immer sie heißt)

├── scripts/              # Dieser Ordner enthält einige Helferskripte: Einen Performance-Tester und einige Skripte

│   └── ...                       mit denen ich die plotly-Grafiken erzeugt habe.

├── Statistics.py    # Das Skript für die Datenverarbeitung. 

├── server.py        # Der Server.


Um die Webseite zu starten muss nur server.py ausgeführt werden.

To-Do an Herrn Engsterhold:
- Ein gültiges Impressum einfügen. 
- Die finale URL des Dashboard muss in der config.ini-Datei eingetragen werden.
- Dei Dockerfile muss getestet und ggf. überabeitet werden.
