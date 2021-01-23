# -*- coding: utf-8 -*-

__author__ = 'Antonio Masotti'
__version__ = '1.0'
__date__ = '29.03.2019'

'''
DOC: In dieser Datei werden alle Einstellungen definiert, die relevant für das ganze Projekt sind. D.h.:
# Initialisierung der WebApp über Flask 
# Initialisierung der Datenbank
# Einstellungen der DB und der App
# Sicherheitseinstellungen
'''

# IMPORTS
import os # für die Festlegung der Arbeitsverzeichnisse
from flask import Flask,render_template, url_for, redirect  # Hauptklasse dieses Programms. Sie verwaltet die gesamte App
from flask_sqlalchemy import SQLAlchemy # Schnittstelle Python-SQL(ite)
from flask_migrate import Migrate # Motor der Datenbank zur Speicherung bzw. Änderungen der Daten
from flask_bootstrap import Bootstrap # Stil der App

#### HAUPTVERZEICHNIS WIRD ANGELEGT #####
# Wir bilden die Verknüpfung zum Hauptverzeichnis.
#  __file__ wird automatisch ersetzt mit dem aktuellen Modul. In unserem Fall __file__ = "app.py"
# da wir diese Variable __file__ innerhalb der .dirname-Methode abrufen, entspricht der Wert der Variabel "hauptverzeichnis" dem Pfad, in dem wir uns befinden.
hauptverzeichnis = os.path.abspath(os.path.dirname(__file__))

# Eine Instanz der Flaskklasse wird erzeugt (diese ist das Kern des Programms).
# Die Variabel "__name__" ist ein Python magic word und kontrolliert, ob die Module direkt oder über import gestartet werden.

# "app" ist der Name unserer App. Theoretisch könnte diese Variabel beliebig heißen, aber wegen meiner Faulheit habe ich den Standardnamen "app" gelassen.
# Hieße die Anwendung anders als "app", müsste man weitere Befehle schreiben, um Flask und Python zu dem gewählten Anwendungsname umzuleiten.
app = Flask(__name__)

# Die Bootstrapklasse wird abgerufen. Das wird dafür sorgen, dass alle Pythonbefehle,
# die direkt ins HTML übersetzt werden (Tabelle, Suchmaske usw...) Zugriff auf die Stileinstellungen der Bootstrap-library haben können.
Bootstrap(app)

# secret key
''' in unserem Fall spielt diese Key keine große Rolle, da die ganze App "nur" eine lokal ausgeführt wird.
Wir brauchen sie trotzdem, weil einige Funktionen von Flask (wie die wtforms für die Abfrage von Daten) diese verlangen.

Sollte die App allerdings veröffentlicht werden, brauchen wir hier ein etwas komplizierteres Passwort, 
die typischerweise mit spezifischen Python Paketen verschlüsselt wird.
Diese Schritte gewährleisten, dass die Endbenutzer keine Änderung auf dem Server tätigen dürfen.
'''
app.config[ 'SECRET_KEY' ] = "meine_geheimschluessel"

# Die Verbindung mit der Datenbank wird hergestellt
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///' + os.path.join(hauptverzeichnis, 'greekData.sqlite')

# Soll die Datenbank jede einzelne Änderung als Backup speichern (= True) oder nicht (=False)
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

# Die Option "ECHO" erlaubt uns, alle SQL-Queries und Befehle, die zur DB geschickt werden, in der Konsole zu printen.
# In der Debug-Phase ist es sinnvoll, den Wert auf True zu setzen.
app.config['SQLALCHEMY_ECHO'] = True

# Eine DB wird erzeugt
db = SQLAlchemy(app)
# Das Backup-Verzeichnis wird aktiviert. Migrate behält für uns den Überblick über alle Änderungen an der Datenbank.
Migrate(app, db)

