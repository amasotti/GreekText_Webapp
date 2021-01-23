# -*- coding: utf-8 -*-
__author__ = 'Antonio Masotti'

'''
Die SQL-Tabellen sind in diesem Pythonprogramm eigentlich Python-Klassen. 
Wir können auf diese Weise die Vorteile der Objekt-Orientierte-Programmierung ausnutzen, um Tabelle zu bilden.
Die Klasse an sich stellt die SQL-Tabelle dar; ihre Attribute entsprechen den Spalten der Tabelle.

Jede Zeile in der Tabelle wird von einer spezifischen Istanz der Klasse definiert. 
In unserem Fall ist z.B. Aristoteles eine Instanz der Klasse "Autoren" d.h. eine Zeile der Tabelle Autoren.
'''

# Die initialisierte DB muss importiert werden
from common.grund_einstellungen import db


#######################################################################################

# Tabelle der Autoren
class Autoren(db.Model):

    # Name der SQLite-Tabelle
    __tablename__ = "Autoren"

    # Spalten der Tabelle
    id_autor = db.Column(db.Integer, primary_key=True) # der ID stellt die Primary Key der Tabelle.
    name = db.Column(db.Text, nullable=False) # nullable=False entspricht dem SQL-Constraint "NOT NULL".
    link = db.Column(db.Text)
    werke = db.relationship('Werken', backref='id_autor') # Eine Beziehung mit der Tabelle der Werken wird erstellt. Werken wird "autor" als Foreign Key verwenden.
    
    # Konstruktor der Klasse. Um einen Autor in der DB zu speichern, benötigen wir den Name und den Perseus-Link.
    # Das ID wird automatisch generiert
    def __init__(self, name, link):
        self.name = name
        self.link = link

    # Mit __repr__ definieren wir, wie ein Element der Tabelle präsentiert wird, wenn man sie abruft.
    def __repr__(self):
        return f"{self.name}"

#######################################################################################

# Tabelle für die Werke (ähnlich wie oben)
class Werken(db.Model):
    id_werk = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.Integer, db.ForeignKey('Autoren.id_autor'))
    titel = db.Column(db.Text, nullable=False)
    titel_link = db.Column(db.Text)
    wortliste_link = db.Column(db.Text)
    verfasser = db.relationship('Autoren', backref="autor", uselist=False)

    def __init__(self, autor, titel,titel_link,wortliste_link):
        self.autor = autor
        self.titel = titel
        self.titel_link = titel_link
        self.wortliste_link = wortliste_link

    def __repr__(self):
        return f"[{self.id_werk}] {self.titel} von {Autoren.query.get(self.autor).name}"

#######################################################################################

# Tabelle für die Wortliste (ähnlich wie oben)
class Wortlist(db.Model):

    id_wort = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.Text, db.ForeignKey("Autoren.name"),nullable=False)
    werk = db.Column(db.Text)
    wortform = db.Column(db.Text)
    lemma = db.Column(db.Text)
    uebersetzung = db.Column(db.Text)
    morphobestimmung = db.Column(db.Text)

    def __init__(self,wortform, lemma, übersetzung,morphobestimmung,autor,werk):
        self.autor = autor
        self.werk = werk
        self.wortform = wortform
        self.lemma = lemma
        self.uebersetzung = übersetzung
        self.morphobestimmung = morphobestimmung 

    def __repr__(self):
        return f"Wort: {self.wortform}\n Lexikoneintrag: {self.lemma}\n Übersetzung: {self.translation} \n Mögliche morphologische Bestimmungen: {self.morphobestimmung}"

#######################################################################################