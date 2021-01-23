# -*- coding: utf-8 -*-
__author__ = 'Antonio Masotti'

'''
Diese Datei enthält die Definitionen der Klassen, die über Python den HTML-Code für Tabelle generieren.
Dafür benötigen wir zwei Arten von Klassen:
# Eine Klasse, die die Metaclasse "Table" vererbt und als Container funktioniert. Diese generiert den HTML-Code für die gesamte Tabelle.
# Eine Klasse, deren einzelne Instanzen die Tabellenzeile darstellen.

'''
from flask import url_for
from flask_table import Table, Col
from flask_table.html import element


#################################################################################################

# Diese Klasse hat eine Nebenfunktion: sie definiert wie Weblinks als Inhalt der Tabellenzellen behandelt werden sollen.
# Die Dokumentation für diese Klasse kann hier gelesen werden: https://flask-table.readthedocs.io/en/stable/

class ExternalURLCol(Col):
    def __init__(self, name, url_attr, **kwargs):
        ''' 
        die Klasse wird initialisiert. Dafür brauchen, außer der Standardvariabel "self", auch eine für die Name der WebSeite und eine für die Adresse
        '''
        self.url_attr = url_attr
        super(ExternalURLCol, self).__init__(name, **kwargs)

    def td_contents(self, item, attr_list):
        '''
        Wird unsere Link in einer HTML-a tag übersetzen

        '''
        text = self.from_attr_list(item, attr_list)
        link = self.from_attr_list(item, [ self.url_attr ])
        return element('a', {'href': link, 'onclick' : "loading();"}, content=text)

#################################################################################################

# TABELLE FÜR DIE WERKE DER GRIECHISCHEN AUTOREN
### Klasse "Werk_Tabelle" : definiert die Spalten und die allgemeine Eigenschaften der Tabelle (was für Daten enthält, ob sie sortierbar ist...)
class Werk_Tabelle(Table):
    id = Col('ID') # ID ist die erste Spalte der Tabelle
    titel = Col('Titel') # wie oben
    autor = Col('Autor') # wie oben
    autor_id = Col('Autor_id') # wie oben
    classes = [ 'table table-striped' ] # HTML-Classe der Tabelle. "table-striped" ist eine Bootstrap-Klasse, die das Layout der Tabelle beinflusst.

    # download ist eine Spalte, die einen Weblink enthalten wird.
    # Der erste Parameter ist der Name der Spalte,
    # url_attr bezieht sich auf der Klasse der Zeilen (Item_Werk) und
    # attr ist das Label mit dem den Link visualisiert wird.
    download = ExternalURLCol('Text herunterladen', url_attr='download', attr='label_download')

    aufmachen = ExternalURLCol('Text zeigen', url_attr='aufmachen', attr='label_aufmachen') # wie oben

    verbesserte_wortliste = ExternalURLCol('Link zur verbesserten Wortliste', url_attr='verbesserte_wortliste',attr="label_verbesserte_wortliste") # wie oben
    

###############

## Klasse "Item_Werk": Klasse der einzelnen Zeilen der Tabelle.

# Alle andere Klasse hier unten folgen dem Modell von "Werk_Tabelle" und "Item_Werk"
class Item_Werk(object):
    # Die Methode __init__ ist der Konstruktor der Klasse. Sie wird alle benötigten Daten einlesen und eine vollständige Zeile für die Tabelle generieren.
    def __init__(self, id, titel, autor, autor_id, download,aufmachen,verbesserte_wortliste):
        self.id = id
        self.autor_id = autor_id
        self.titel = titel
        self.autor = autor
        self.download = download
        self.aufmachen = aufmachen
        self.label_download = f"Lade {self.titel} als Textdatei herunter"
        self.label_aufmachen = f"Lesen Sie {self.titel} im Browser"
        self.verbesserte_wortliste = verbesserte_wortliste
        self.label_verbesserte_wortliste = "Verbesserte Wortliste"

#################################################################################################

# HTML Tabelle für die Visualisierung der Autoren, die in der Datenbank gespeicher sind

## Klasse für die Tabelle an sich
class Autoren_Tabelle(Table):
    id = Col('Autor_id')
    name = Col('Name')
    link = ExternalURLCol('Link auf Perseus', url_attr='link', attr='text_link')
    werke_link = ExternalURLCol('Werke', url_attr='werke_link',attr="label_werke")
    classes = [ 'table table-striped' ]

#############

## Klasse "Item_Autor" : Klasse der einzelnen Zeilen der Tabelle "Autoren_Tabelle" 
class Item_Autor(object):
    def __init__(self, id, name, link):
        self.id = id
        self.name = name
        self.link = link
        self.text_link = "Texte von " + str(self.name) + " auf Perseus"
        self.werke_link = url_for('zeigWerken', autor=self.name,zeig_tabelle=False)
        self.label_werke = "Entdecke seine Werke"

#################################################################################################

# HTML-Tabelle, die die Werke eines bestimmten Autors auflistet (Quelle der Daten: Perseus Online Datenbank)
class Werke_aus_Perseus(Table):
    titel = Col('Titel')
    autor = Col('Autor')
    link_text = ExternalURLCol('Link zum Originaltext (Perseus)', url_attr='link_text', attr='label_text')
    link_wortliste = ExternalURLCol('Link zur Wortliste', url_attr='link_wortliste', attr='label_wl')
    link_unsere_wortliste = ExternalURLCol('Link zur verbesserten Wortliste', url_attr='link_unsere_wortliste',attr="label_uwl")
    classes = [ 'table table-striped' ]

###############
## Klasse "Item_PerseusWerk" : Klasse der einzelnen Zeilen der Tabelle "Werke_aus_Perseus"
class Item_PerseusWerk(object):
    def __init__(self, titel, autor, link_text, link_wortliste, link_unsere_wortliste):
        self.titel = titel
        self.autor = autor
        self.link_text = link_text
        self.link_wortliste = link_wortliste
        self.link_unsere_wortliste = link_unsere_wortliste
        self.label_text = f" {self.titel} auf Perseus Library"
        self.label_wl = "Wortliste"       
        self.label_uwl = "Verbesserte Wortliste"

#################################################################################################

# HTML-Tabelle der in der Datenbank gespeicherten Wortlisten
class WortlisteTabelle(Table):
    autor = Col("Autor")
    werk = Col("Werk")
    wortform = Col("Wortform")
    lemma = Col("Lemma")
    übersetzung = Col("Übersetzung")
    morphobestimmung = Col("Morphologische Bestimmung")
    classes = [ 'table table-striped' ]

#######################

# Klasse "Wortlist_Item" : Klasse der einzelnen Zeilen der Tabelle "WortlisteTabelle"
class Wortlist_Item(object):
    def __init__(self, wortform, lemma, übersetzung, morphobestimmung, autor, werk):
        self.autor = autor
        self.werk = werk
        self.wortform = wortform
        self.lemma = lemma
        self.übersetzung = übersetzung
        self.morphobestimmung = morphobestimmung


#################################################################################################