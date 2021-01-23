# -*- coding: utf-8 -*-
__author__ = 'Antonio Masotti'

'''
DOC: Die HTML Formulare verwenden das Paket flask_wtf. Ähnlich wie für die HTML-Tabellen und die SQLite-Tabellen sind die Formulare als Python-Klassen definiert.
Die Attribute der Klasse stellen die Felder des Formulars dar. Die Methoden zur Bildung des Formulars werden vererbt (Metaclasse "FlaskForm"). 

Dies erlaubt eine einheitliche Definition der Formulare und eine sehr schnelle Implementierung derselben in dem HTML-Code.
Sobald die Klassen definiert sind, wird es reichen in der HTML-Datei den Befehl {{wtf.quick_form(NAME_DES_FORMULARS)}} einzutippen.
Das Formular wird dann von Flask automatisch generiert.

'''

# IMPORTE #
# Klasse der Formulare in Python
from flask_wtf import FlaskForm
# Datentypen für Formulare (diese können Strings, Radiobutton, DateTimePicker, Dropdown Liste sein und vielmehr)
from wtforms import (StringField, SelectField, SubmitField, IntegerField, TextField, validators)
# Dieses Paket verfügt über eine große Klasse von "validators". Sie werden verwendet, um zu kontrollieren, dass der Benutzer die gewünschten Infos angibt.
# Diese Klassen führen vielen Kontrolle aus. Für unsere Zwecke reicht, dass der Benutzer das Feld ausfüllt. "DataRequired" wird ein Fehler Nachricht aufzeigen
# wenn die nötige Infos fehlen. SelectField stellt eine Dropdown-Liste dar, Stringfield ein Text-Input, RadioField ein Radiobutton usw...
from wtforms.validators import DataRequired

# 1. Formular: dieses wird auf der Startseite verwendet und erlaubt dem Benutzer eine Wortform in der Perseus Datenbank zu kontrollieren.
# Der folgende Code bildet das Formular aus einer Mischung von vererbten Parameter und Funktionen (aus FlaskForm) und unseren spezifischen Felder
class PerseusAbfrage(FlaskForm):
    wortform = StringField('Geben Sie eine griechische Wortform ein: ')
    submit = SubmitField('Los!')


# Formular, um ein Werk zu wählen und dieses aus der Datenbank zu löschen
class LoeschWerk(FlaskForm):
    id_werk = IntegerField('ID des Werks')
    submit = SubmitField('Lösch Werk')

# Formular zur Wahl eines zu untersuchenden Autors
class WaehleAutor(FlaskForm):
    autor_name = SelectField(u'Autoren', choices=[("Aeschines","Aeschines"), ("Aeschylus","Aeschylus"), ("Andocides","Andocides"), ("Anna Komnene","Anna Komnene"), ("Antiphon","Antiphon"), ("Apollodorus","Apollodorus"),
              ("Apollonius Rhodius","Apollonius Rhodius"), ("Appian","Appian"), ("Aretaeus","Aretaeus"), ("Aristophanes","Aristophanes"), ("Aristotle","Aristotle"), ("Bacchylides","Bacchylides"),
              ("Callimachus","Callimachus"), ("Demades","Demades"), ("Demosthenes","Demosthenes"), ("Dinarchus","Dinarchus"), ("Diodorus Siculus","Diodorus Siculus"), ("Diogenes Laertius","Diogenes Laertius"),
              ("Epictetus","Epictetus"), ("Euclid","Euclid"), ("Euripides","Euripides"), ("Flavius Josephus","Flavius Josephus"), ("Galen","Galen"), ("Gorgias","Gorgias"), ("Herodotus","Herodotus"), ("Hesiod","Hesiod"),
              ("Hippocrates","Hippocrates"), ("Homer","Homer"), ("Hyperides","Hyperides"), ("Isaeus","Isaeus"), ("Isocrates","Isocrates"), ("Lycurgus","Lycurgus"), ("Lysias","Lysias"), ("NA","NA"), ("Old Oligarch","Old Oligarch"),
              ("Pausanias","Pausanias"), ("Pindar","Pindar"), ("Plato","Plato"), ("Plutarch","Plutarch"), ("Polybius","Polybius"), ("Sophocles","Sophocles"), ("Strabo","Strabo"),
              ("Theocritus","Theocritus"), ("Theophrastus","Theophrastus"), ("Thucydides","Thucydides"), ("Xenophon","Xenophon")])

    submit = SubmitField('Entdecke seine Werke!')

# Formular für die SQL-Queries
class SQLQuery(FlaskForm):
    morpho = StringField('Suchen Sie nach einem speziellen Form', render_kw={"placeholder": "verb"})
    submit = SubmitField('Suche')
    