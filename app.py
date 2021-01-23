# -*- coding: utf-8 -*-

__author__ = 'Antonio Masotti'
__version__ = '1.0'
__date__ = '01.04.2019'

'''
DOC: Hauptdatei des Programms.
-------------------------------
In dieser Datei werden alle benötigten Module (sowohl meine als auch diejenigen aus Flask und SQLAlchemy) importiert.
Wenn diese Datei direkt ausgeführt wird, entweder über Python (python app.py) oder über Flask (flask run), sorgt sie dafür,
dass die richtigen HTML-Seiten geladen werden und befüllt diese mit dem mittels Python generierten Inhalt.

'''

################ Importe ###############################################
# Python und Flask Pakete, inklusiv SQLAlchemy für die Steuerung der SQLite-Datenbank
from common.grund_einstellungen import app, db
from flask import url_for,render_template,request,redirect
import csv # zur Erzeugung von csv Listen der Ergebnisse
import os
from urllib.parse import urlencode
from pathlib import Path

###### Meine Module ######
from common.mischmasch import * # wie der Name schon sagt, enthält dieses Modul alle meine Funktionen, die nicht deutlicher zu klassifizieren waren.
from models.db_klassen import Werken, Autoren, Wortlist # Die SQLAlchemy-Klassen, die den 3 Tabellen der Datenbank entsprechen.
from common.formulare import * # Python Klassen, mit denen die Formulare auf den HTML-Seiten generiert werden.
import common.Autoren.autoren_zeilen as vorbereitung_autoren # Befehle und Inhalte für die Erzeugung der Tabelle "Autoren".
from models.tables import * # Python-Klassen, mit denen die HTML-Tabellen zur Visualisierung der heruntergeladenen Daten generiert werden.

########################################################################

# Die DB wurde initialisiert (mit dem Import aus common.grundeinstellung.py).
# Jetzt müssen wir nur die vorbereitete Tabelle mit den Autoren bilden und befüllen

# die Tabellen werden erzeugt
db.create_all()
# die Tabelle "Autoren" wird befüllt
vorbereitung_autoren.add_neue_autoren()

################################################################
################################################################
#########################                 ######################
#########################  HAUPTPROGRAMM  ######################
#########################                 ######################
################################################################
################################################################

# Routing zu den einzelnen Seiten #
# der Rest dieser Datei sammelt die Infos und Inhalte aus den verschiedenen Pythonfunktionen und bildet die URLs, die im Browser abgerufen werden.
# Das eigentliche Routing geschieht mithilfe von den Python-Dekoratoren (Funktionen, die als Argumenten Funktionen nehmen, siehe Dokumentation.)

# Ich habe hier zwei Adressen für die Homepage definiert: ohne Prefix und mit /home.html als Prefix
# die Funktion homepage macht nichts anderes als die entsprechenden HTML-Datei abzurufen.
# Das Abrufen an sich erfolgt mittels der Funktion render_template(). Diese verlangt mindestens ein Argument:  die HTML-template, die visualisiert werden muss.
# Andere mögliche Argumente sind die Python Variabeln (Strings, Liste, Dictionaries usw...), die für spezifische Seiten benötigt werden könnten.
@app.route('/')
@app.route("/home", methods=[ "GET", "POST" ])
def startseite():
	return render_template('startseite.html')

#############################################################################################
#############################################################################################
#############################################################################################


# Seite zur Visualisierung der heruntergeladenen Texte
@app.route('/zeig_text')
def zeige_text():
	# Klein Alert
	flash_extern(message="Aktuell habe ich geschafft, nur die Visualisierung für die Ilias von Homer zu optimieren. Ich bitte um Verständnis.")

	# Diese Visualisierungsseite verlangt einen Link zu dem Text, der heruntergeladen werden soll.
	# Diese Info kommt aus einer anderen Seite und wird mit der nächsten Zeile abgelesen.
	gewaehlter_text = request.args.get('gewaehlter_text')
	if request.args.get('link_zum_werk'): # Wenn ein Link zur Verfügung steht, kann der Text heruntergeladen werden
		link = request.args.get('link_zum_werk')
	else: # Ansonsten wird dem Benutzer eine Liste der vorhandenen Werke gezeigt.
		flash_extern(message="Der gesuchten Text wurde noch nicht heruntergeladen...")
		render_template(url_for('allewerke'))
	# Zunächst wird kontrolliert, ob eine lokale Version des Textes vorhanden ist.
	# Wenn der Text schon heruntergeladen wurde, dann wird er nur angezeigt. Ansonsten muss er erstmal heruntergeladen und lokal gespeichert werden.
	# Path ist eine Klasse aus der Library pathlib, die uns erlaubt, sehr schnell mit lokalen, relativen und absoluten Dateipfaden umzugehen.
	path = Path(('common/static/assets/'+gewaehlter_text+'/'+gewaehlter_text+'_vollständig.txt'))

	# Fall 1: Es gibt keine lokale Version des Textes
	if not path.exists():
		# get_texte (aus der Datei mischmasch.py) ist die Funktion, die Texte aus dem Internet herunterlädt.
		# Die Funktion verlangt zwei Parameter: einen Link, aus dem der Text heruntergeladen werden muss und einen bool-Wert, mit dem wir entscheiden,
		# ob der Text im Browser (=False) oder in einem separaten Text Editor (=True) geöffnet werden muss
		get_texte(link,aufmachen=False)
	# Fall 2: die lokale Version ist schon vorhanden oder der Text wurde im letzten Schritt heruntergeladen.
	# text_formatter (auch aus mischmasch.py) ist eine Funktion, die den Text aus der Datei liest und ihn für die Visualisierung im Browser optimiert.
	text_name = text_formatter(gewaehlter_text)[0]
	inhalt = text_formatter(gewaehlter_text)[1]
	# die HTML-Seite "zeige_text.html" wird geladen. Dieser Seite werden 2 Variabeln überführt: text_name und inhalt:
	# inhalt enthält den zu zeigenden Text und text_name bildet den Titel der Seite.
	return render_template('zeige_text.html', text_name = text_name, inhalt = inhalt)

#############################################################################################
#############################################################################################
#############################################################################################

# Kleine Funktion zur Auflistung der verfügbaren Autoren
@app.route("/autorenList")
def autorenList():
	lista = [ "Aeschines", "Aeschylus", "Andocides", "Anna Komnene", "Antiphon", "Apollodorus",
			  "Apollonius Rhodius", "Appian", "Aretaeus", "Aristophanes", "Aristotle", "Bacchylides",
			  "Callimachus", "Demades", "Demosthenes", "Dinarchus", "Diodorus Siculus", "Diogenes Laertius",
			  "Epictetus", "Euclid", "Euripides", "Flavius Josephus", "Galen", "Gorgias", "Herodotus", "Hesiod",
			  "Hippocrates", "Homer", "Hyperides", "Isaeus", "Isocrates", "Lycurgus", "Lysias", "NA", "Old Oligarch",
			  "Pausanias", "Pindar", "Plato", "Plutarch", "Polybius", "Sophocles", "Strabo",
			  "Theocritus", "Theophrastus", "Thucydides", "Xenophon" ]
	links = [ ]
	# Einfache Schleife zur Halbierung der Autorenliste
	for x in lista:
		links.append((
			"http://artflsrv02.uchicago.edu/cgi-bin/perseus/search3torth?dbname=GreekApr19&word=&OUTPUT=conc&ORTHMODE=ORG&CONJUNCT=PHRASE&DISTANCE=3&author=" + x + "&title=&POLESPAN=5&THMPRTLIMIT=1&KWSS=1&KWSSPRLIM=500&trsortorder=author%2C+title&editor=&pubdate=&language=&shrtcite=&genre=&sortorder=author%2C+title&dgdivhead=&dgdivtype=&dgsubdivwho=&dgsubdivn=&dgsubdivtag=&dgsubdivtype=",
			x))
	half = len(links) // 2
	links1 = links[ 0:half ]
	links2 = links[ half: ]
	# Die HTML-Datei 'autorenList.html' wird geladen
	return render_template('autorenList.html', autors=links1, autors2=links2)

#############################################################################################
#############################################################################################
#############################################################################################


# Die Funktion "alleautoren" zeigt alle Autoren, die in der Datenbank gespeichert wurden.
@app.route('/alleautoren')
def alleautoren():
	# Der folgende Befehl entspricht der SQL-Query: SELECT * FROM Autoren;
	autoren = Autoren.query.all()
	# Die Ergebnisse werden später in einer Liste vorläufig gespeichert; die Liste wird hier initialisiert
	items_list = [ ]

	# Die folgende Schleife bildet die Zeile der HTML-Tabelle zur Visualisierung der Ergebnisse der Suche.
	for autor in autoren:
		item = Item_Autor(id=autor.id_autor, name=autor.name, link=autor.link)
		items_list.append(item)

	# Mit den Zeilen, die wir mit der Schleife erzeugt haben, wird jetzt eine HTML-Tabelle gebildet.
	tabelle = Autoren_Tabelle(items_list)

	# Die Seite 'alleautoren.html' wird geladen. Die Tabelle, die gezeigt werden muss, wird als Variabel überführt.
	return render_template('alleautoren.html', table=tabelle)


#############################################################################################
#############################################################################################
#############################################################################################


# Die folgende Seite/Funktion erzeugt eine Liste aller in der Datenbank gespeicherten Werke
@app.route('/allewerke')
def allewerke():

	# Der folgende Befehl illustriert die typische Syntax von SQLAlchemy. Das ist eine Query für die Klasse (d.h. SQL-Tabelle) der Werke.
	# Ohne SQLAlchemy, hätten wir eine SQL Query (Select * from Werken) und die Kursor und Execute Befehle benötigt.
	# Mit SQLAlchemy reduziert sich das ganze auf eine kurze Zeile.
	# Darüber hinaus funktioniert dieser Befehl mit beliebigen Datenbanken (PostGresSQL, MySQL, SQLite, MongoDB ecc..)
	werke = Werken.query.all()

	# Der folgende Code generiert die HTML-Tabelle
	items_list = [ ]
	for work in werke:
		# Der Parameter "download_link" wird einen Link erzeugen, der uns erlaubt den gewünschten Text herunterzuladen
		download_link = url_for('herunterladen', link_zum_werk = work.titel_link)
		# Der Parameter "aufmachen_link" wird einen Link erzeugen, der uns erlaubt, den gewünschten Text in einem Editor auf dem Rechner zu öffnen.
		aufmachen_link = url_for('zeige_text', gewaehlter_text = work.titel, link_zum_werk = work.titel_link, autor=Autoren.query.get(work.autor))
		link_unsere_wortliste = url_for('wortliste', autor=Autoren.query.get(work.autor), wl=work.wortliste_link, werk=work.titel)
		# Jedes item ist eine Instanz der Klasse "Item_Werk". Diese stellt wiederum eine Zeile der HTML-Tabelle dar.
		item = Item_Werk(id=work.id_werk,
						 titel=work.titel,
						 autor=Autoren.query.get(work.autor),
						 autor_id=Autoren.query.get(work.autor).id_autor,
						 download = download_link,
						 aufmachen = aufmachen_link,
						 verbesserte_wortliste = link_unsere_wortliste
						 )
		items_list.append(item)
	# Alle Instanzen der Klasse Item_Werk (spricht alle Zeilen der Tabelle) wurden in einer Liste gespeichert (mit der Methode .append).
	# Jetzt können wir die Tabelle befüllen und den entsprechenden HTML-Code generieren.
	tabelle = Werk_Tabelle(items_list,table_id='werke')
	# Klein Alert
	flash_extern(message="Die Funktionen zum Herunterladen und zur Visualisierung der Texte können etwas Zeit brauchen (je nachdem wie groß das Werk ist).")
	# Die HTML-Seite wird geladen
	return render_template('allenwerke_table.html', table=tabelle)

#############################################################################################
#############################################################################################
#############################################################################################


# Die Funktion "herunterladen" steuert den Download von Texten aus Perseus. Sie bedient sich der Funktion get_texte aus mischmasch.py
@app.route('/herunterladen')
def herunterladen():
	# Link des gewählten Werkes
	link = request.args.get("link_zum_werk")
	# Abruf der Funktion "get_texte".
	# Achtung!: Die Funktion ist sehr langsam (bis 40-50 Minuten Laufzeit)
	get_texte(link)
	# Wenn der Download fertig ist, wird die Datei geöffnet. Die Webapp lädt die Seite "allewerke".
	return redirect(url_for('allewerke'))

#############################################################################################
#############################################################################################
#############################################################################################


# Eine einfache Funktion, um einen Werk aus der Datenbank zu löschen
@app.route('/loeschwerk', methods=[ "GET", "POST" ])
def loeschwerk():
	# Das Formular wird definiert. Damit wird es möglich, den ID der zu löschenden Werk einzutippen.
	# Bei diesem, wie bei allen anderen Formularen, handelt es sich um Klassen aus dem Paket flask_WTForms.
	# Die Logik der Python Klassen erlaubt es, sehr schnell und zuverlässig HTML-Formulare herzustellen
	form = LoeschWerk()

	# das If-Statement definiert, was geschehen soll, wenn das Formular ausgefüllt und der Button "Submit" gedrückt wird.
	# Wenn das Formular noch nicht gefüllt wurde, wird das leere Formular gezeigt, ansonsten kümmert sich das If-Statement um die Löschoperationen
	# und lädt am Ende die Seite 'allewerke'.
	if form.validate_on_submit():
		# Das Werk mit dem angegebenen ID wird gesucht
		id = form.id_werk.data
		werk = Werken.query.get(id)
		# das Werk wird gelöscht und die Änderung in der DB gespeichert.
		db.session.delete(werk)
		db.session.commit()
		# die Seite 'allewerke' wird geladen
		return redirect(url_for('allewerke'))

	# Beim ersten Laden der Seite, wird das Löschformular angezeigt. Dieses befindet sich auf der Seite 'loeschwerk.html'
	return render_template('loeschwerk.html', form=form)

#############################################################################################
#############################################################################################
#############################################################################################

# Die nächste Funktion listet die Werke in der Datenbanktabelle "Werke" auf und bietet die Links zu den Wortlisten und Originaltexten
@app.route('/zeigWerken', methods=["GET", "POST"])
def zeigWerken():

	# Die nötigen Variabeln werden initialisiert. Wir brauchen:
	# ein Formular, um den Autor zu wählen, dessen Werken aufgelistet werden sollen,
	form = WaehleAutor()
	# eine Liste zum vorläufigen Speichern der Query-Ergebnisse,
	werk_tabelle = [ ]
	# und eine Kontrollvariabel, die entweder das Formular "WaehlAutor" oder die Liste auf der HTML-Seite zeigt.
	zeig_tabelle = False

	# Die Tabelle muss nur dann gezeigt werden, wenn der Benutzer einen Autor gewählt hat.
	# Solange das nicht der Fall ist, muss die Seite nach einem Autor fragen.
	while zeig_tabelle == False:

		# Fall 1 : Wir haben keine Info über den gewünschten Autor. Das Suchformular wird gezeigt
		if request.args.get('autor') is None:

			# Fall 2: Das Formular is ausgefüllt. Wir beenden die Visualisierung des Formulars und bilden die Tabelle
			if form.validate_on_submit():
				# Tabelle wird gezeigt, das Formular verschwindet
				zeig_tabelle = True
				# Aus dem Formular wird den Name des Autors extrahiert. Danach wird das Formularfeld gelöscht, um später eine neue Suche zu erlauben
				autor_name = form.autor_name.data
				form.autor_name.data = ' '
			else:
				# Fall 2.1 : Das Formular ist nicht gefüllt und wir haben keine Info über einen gewünschten Autor. Das Formular wird geladen.
				flash_extern(message="das Aufladen der 'Verbesserte Wortliste' kann sehr lange dauern (bis 40 min). Jedes Wort wird im Internet gesucht, die nötige Infos werden extrapoliert und das ganze wird auf SQL-DB gespeichert (das ganze ist eine Schleife mit bis auf 50.000 Durchläufe!")
				zeig_tabelle = False
				# Lade die HTML-Seite mit dem Formular
				return render_template('zeigWerke.html',form = form, werke_tabelle = werk_tabelle,zeig_tabelle=zeig_tabelle)

	    # Fall 3: Wir haben Infos über den Autor. Die Tabelle kann direkt gebildet werden und die Schleife mit dem Formular beendet werden.
		if request.args.get('autor') is not None:
			autor_name = request.args.get('autor')
			zeig_tabelle = True

	# Der folgende Code baut sukzessiv die Tabelle mit den Werken auf
	# die Funktion get_works (aus mischmasch.py) sucht alle Werke eines Autors.
	werke_list = get_works(autor_name)
	werk_items = []
	# Für jedes gefundene Werk wird kontrolliert, ob dieses schon in unserer SQLite Datenbank vorhanden ist. Wenn nicht, wird eine neue Zeile dort geschrieben
	for werk in werke_list:
		check = Werken.query.filter_by(titel_link = werk[1]).first()
		if check:
			print("Werk schon vorhanden in der Datenbank")
		else:
			autor_id = Autoren.query.filter_by(name = autor_name).first().id_autor
			item = Werken(autor = autor_id, titel = werk[0],titel_link=werk[1],wortliste_link=werk[2])
			db.session.add(item)
			db.session.commit()
		# die gesammelten Daten werden jetzt in der Tabelle zur Visualisierung gespeichert
		link_unsere_wortliste = url_for('wortliste', autor = autor_name, wl = werk[2], werk = werk[0])
		# Wie bei anderen Funktionen, die die Klasse Table (aus flask_table) benutzten, müssen zunächst die einzelnen Zeile als Klasseninstanzen gebildet werden
		# Danach übergeben wir einfach die Liste mit den Tabellenzeilen der übergeordneten Klasse "Werke_aus_Perseus".
		# diese Klasse wird dann alle einzelnen Zeilen in einer Tabelle zusammenfügen und den HTML-Code dafür generieren.
		item = Item_PerseusWerk(titel=werk[0],
								autor = autor_name,
								link_text=werk[1],
								link_wortliste=werk[2],
								link_unsere_wortliste=link_unsere_wortliste
								)
		werk_items.append(item)
	# Alle einzelnen Zeilen der Tabelle, jetzt gespeichert in der Liste "werk_items", werden in einer Tabelle zusammengefügt.
	werk_tabelle = Werke_aus_Perseus(werk_items,table_id='werkePerseus')
	# Die HTML-Seite mit der Tabelle wird nun geladen.
	return render_template('zeigWerke.html',form = form, werke_tabelle = werk_tabelle,zeig_tabelle=zeig_tabelle)

#############################################################################################
#############################################################################################
#############################################################################################

# Die folgende Funktion zeigt eine Tabelle mit allen gespeicherten bzw. gesuchten Wortformen.
@app.route('/wortliste', methods=[ "GET", "POST" ])
def wortliste():
	# Die nötigen Paramater werden über die HTML Methode POST und GET gelesen:
	# Wortliste (= Link zur Perseus Wortlist)
	wl = request.args.get('wl')
	# Name des Autors
	autor = request.args.get('autor')
	# Name des untersuchten Werkes
	werk = request.args.get('werk')

	# Jedes Wort in der Wortliste wird untersucht. Das Ergebnis ist eine komplexe Liste von Listen. Jede Unterliste enthält folgende Infos:
	# (Wortform, Lemma, Übersetzung, morphologische_Bestimmungen)
	worter = search_infos(link=wl)

	# Analyse der einzelnen Wortformen
	for x in worter:
		# Zunächst wird kontrolliert, ob die Wortform schon vorhanden ist.
		zeile = Wortlist.query.filter_by(wortform= x[0],werk=x[3]).first()
		if zeile:
			# Wenn die Wortform schon vorhanden ist, wird sie übersprungen
			print(f"{x[0]} already thereeee!")
		else:
			# Ansonsten werden alle Spalten der Tabelle "Wortlist" befüllt
			zeile = Wortlist(autor = autor, wortform = x[0], lemma = x[1], übersetzung = x[2], morphobestimmung = x[3],werk = werk)
			# Die Infos werden in der Datenbank gespeichert
			db.session.add(zeile)
			db.session.commit()
	# Jetzt können die Wortformen visualisiert werden. Das funktioniert genau so wie bei der vorangehenden Funktion.
	tabelle_items = []
	for wortform in worter:
		tabelle_zeile = Wortlist_Item(wortform=wortform[0], lemma=wortform[1], übersetzung=wortform[2],morphobestimmung=wortform[3],autor=autor, werk=werk)
		tabelle_items.append(tabelle_zeile)
	wort_tabelle = WortlisteTabelle(tabelle_items,table_id="wortliste")
	return render_template('wortliste.html',tabelle=wort_tabelle, werk = werk, autore = autor)


#############################################################################################
#############################################################################################
#############################################################################################


# Die folgende Funktion lädt eine Suchseite, über die es möglich ist, gezielt nach morphologischen Kategorien zu suchen.
# die Suche nutzt die Spalte "morphologische Bestimmungen" in der Tabelle "Wortformen" in der Datenbank
@app.route('/sqlForm', methods=[ "GET", "POST" ])
def sqlForm():
	# das Formular für die Suche wird geladen.
	form = SQLQuery()
	# Wenn das Formular ausgefüllt und der Submit-Button gedruckt wurde, können wir die Informationen ablesen und eine Tabelle generieren.
	if form.validate_on_submit():
		morpho = form.morpho.data
		return redirect(url_for('gesuchteforme', query = morpho))
	# Wenn wir über keine Infos über die gesuchten morphologischen Kategorien verfügen, wird das Formular gezeigt
	return render_template('sqlForm.html', form=form)

#############################################################################################
#############################################################################################
#############################################################################################


# Die folgende Funktion findet und visualisiert alle Wortformen in der Datenbank, die der Query entsprechen
# oder alle Wortformen in der DB, wenn keine Query vorliegt.
@app.route('/gesuchteforme', methods=[ "GET", "POST" ])
def gesuchteforme():
	# Fall 1: Es liegt keine Query vor: die Seite zeigt alle gespeicherten Wortformen
	if request.args.get('query') is None:
		wortformen = Wortlist.query.all()
		query = " "
	else:
		# Es liegt eine Query vor. Die entsprechenden Wortformen werden gezeigt
		query = request.args.get('query')
		wortformen = Wortlist.query.filter(Wortlist.morphobestimmung.contains(query)).all()

	# Es wird eine Tabelle, wie bei ähnlichen Funktionen weiter oben, gebildet.
	tabelle_items = []
	for wortform in wortformen:
		tabelle_zeile = Wortlist_Item(wortform=wortform.wortform,
									  lemma=wortform.lemma,
									  übersetzung = wortform.uebersetzung,
									  morphobestimmung=wortform.morphobestimmung,
									  autor=wortform.autor,
									  werk=wortform.werk)

		tabelle_items.append(tabelle_zeile)

	wort_tabelle = WortlisteTabelle(tabelle_items,table_id="wortliste")
	return render_template('gesuchteforme.html', wort_tabelle = wort_tabelle,query=query)

#############################################################################################
#############################################################################################
#############################################################################################

# die Funktion bereinigt die Tabelle "Wortformen" in der Datenbank.
# Alle dort gespeicherten Informationen werden gelöscht
@app.route("/loeschFormen", methods=[ "GET", "POST" ])
def loeschFormen():
	db.session.query(Wortlist).delete()
	db.session.commit()
	flash_extern(message="Die Tabelle mit den Wortformen wurde erfolgreich gelöscht")
	return render_template('startseite.html')

#############################################################################################
#############################################################################################
#############################################################################################

# Funktion für den Download von Wortformen als csv Datei
@app.route('/csv_herunterladen', methods=[ "GET", "POST" ])
def csv_herunterladen():
	# Wenn eine Query vorliegt, werden nur die entsprechenden Wortformen heruntergeladen, ansonsten alle vorhandenen.
	if request.args.get('query') is None:
		wortformen = Wortlist.query.all()
	else:
		query = request.args.get('query')
		wortformen = Wortlist.query.filter(Wortlist.morphobestimmung.contains(query)).all()
		print(query)
	# das aktuelle Arbeitsverzeichnis wird gespeichert
	HAUPTVERZEICHNIS = Path.cwd()
	# in path_csv wird der Pfad der zukünftigen csv Datei gespeichert
	path_csv = HAUPTVERZEICHNIS / "common" / "static" / "assets" / "lista.csv"

	# die Datei wird geöffnet und geschrieben (mithilfe des Pakets csv)
	export =  open(str(path_csv.resolve()),"w",encoding="UTF-8")
	out = csv.writer(export)
	out.writerow(['id','autor','wortform','lemma','übersetzung','morpho'])

	for zeile in wortformen:
		out.writerow([zeile.id_wort, zeile.autor,zeile.wortform,zeile.lemma,zeile.uebersetzung,zeile.morphobestimmung])

	# Die Datei wird geschlossen
	export.close()

	# je nach Einstellung auf dem eigenen Rechner könnten die griechsiche Charakter nicht korrekt dargestellt werden
	verzeichnis_csv = str(path_csv.parents[0].resolve())
	os.chdir(verzeichnis_csv)
	os.system("lista.csv")
	# Verzeichniswechsel (zurück zum Hauptverzeichnis)
	os.chdir(str(HAUPTVERZEICHNIS))

	flash_extern("Die Liste wurde erfolgreich heruntergeladen")
	# Zum Schluss wird die Homepage geladen
	return render_template('startseite.html')

#############################################################################################
#############################################################################################
#############################################################################################

# Funktion für den Download der gesuchten bzw. gespeicherten Wortformen in einer pdf Datei
# Die Logik ist dieselbe wie bei der Funktion "csv_herunterladen";
@app.route('/TeX_herunterladen')
def TeX_herunterladen():
	AKTUELLE_VERZEICHNIS = Path.cwd()

	# Die verlangten Wortformen werden in der Datenbank gesucht
	if request.args.get('query') is None:
		wortformen = Wortlist.query.all()
	else:
		query = request.args.get('query')
		wortformen = Wortlist.query.filter(Wortlist.morphobestimmung.contains(query)).all()
	# Der Abschnittstitel für die LaTeX Datei wird festgelegt
	if query is None:
		query_tex = ''' {\Large Query: alle Wortformen in der Datenbank } '''
	else:
		query_tex = "{\Large Query: "+query+" }\n\n"

	# die Variabel inhalt_tex wird erzeugt. Sie wird den Inhalt der TeX-Datei enthalten
	inhalt_tex = ""
	for form in wortformen:
		wf = form.wortform.replace("_"," ")
		lemma = form.lemma.replace("_"," ")
		uebersetzung = form.uebersetzung.replace("_"," ")
		mb = form.morphobestimmung.replace("_"," ")
		# Jede Wortform und die entsprechenden Infos werden für die TeX-Datei formatiert
		inhalt_tex = inhalt_tex + " " + "\item \eintrag{"+wf+"}{"+lemma+"}{"+uebersetzung+"}{"+mb+"}\n"

	# Das Ganze wird von einer itemize-Umgebung umschlossen
	inhalt_tex = "\\begin{itemize}\n "+ inhalt_tex + " \\end{itemize}"

	# Die TeX-Datei wird geschrieben
	path_tex = Path.cwd() / "common" / "static" / "tex" / "Tex_formen.tex"
	with open(path_tex, "w", encoding="UTF-8") as tex_output:
		tex_output.write(query_tex)
		tex_output.write(inhalt_tex)

	# die TeX-Datei (Vorlage + neuer Inhalt) wird kompiliert
	os.chdir(str(path_tex.parents[0].resolve()))
	befehl = "xelatex Vorlage_wortformen.tex"
	os.system(befehl)
	# die PDF-Datei wird geöffnet
	os.system("Vorlage_wortformen.pdf")
	os.chdir(str(AKTUELLE_VERZEICHNIS.resolve()))
	flash_extern(message="Eine pdf wurde erzeugt!")
	# Zum Schluss wird man zur Homepage umadressiert
	return render_template("startseite.html")

#############################################################################################
#############################################################################################
#############################################################################################

# Kleine Suchmaske auf der Homepage. Diese Fnktion liest das angegebene Wort im Formular und öffnet einen Link zu dem Perseus Greek Word Study Tool.
@app.route('/redirecting')
def redirect_zu_perseus():
	'''
	Fast banale Funktion, die den Input des Benutzers aus dem Formular (siehe Startseite) automatisch über das request-Paket annimmt und
	die entsprechende Seite in dem Perseus Portal öffnet.
	'''
	wortform = request.args.get('wortform')
	link = "http://www.perseus.tufts.edu/hopper/morph?l=" + wortform + "&la=greek"
	return redirect(link)

#############################################################################################
#############################################################################################
#############################################################################################


# Technische Infos über diese WebApp
@app.route('/technisches')
def technisches():
	return render_template('technisches.html')


#############################################################################################
#############################################################################################
#############################################################################################


# Routing zu einer festgelegten Seite, die immer abgerufen werden soll, wenn der Benutzer eine nicht-vorhandene Seite besuchen möchte.
@app.errorhandler(500) # die Seite existiert, aber eine Python-Funktion enthält einen Fehler
@app.errorhandler(404) # die Seite existiert nicht.
def keine_seite(e):
	'''
	Standardseite für den 404-Fehler. Wird automatisch abgerufen, falls der Benutzer versucht, eine nicht-vorhanden Seite zu laden.
	Test: Wenn Sie die App lokal laufen (URL: localhost:500/home oder 127.0.0.1:5000/home) versuchen Sie die Adresse:
		localhost:5000/djaklsjdkas
	oder ähnlich zu besuchen.
	:param e: Standardvariabel für Fehler.
	:return: ein Template mit einer festgelegten Fehlerseite.
	'''
	return render_template('error_seite.html'), 404

#############################################################################################
#############################################################################################
#############################################################################################


#################################### STARTE DIE APP ##########################################
# Mit dem folgenden Befehl starten die App.
# Die Bedingung ist, dass die App nur startet, wenn man diese Datei mit Python ausführt.
if __name__ == "__main__":
	app.jinja_env.cache = {}
	# Setzen Sie debug auf "False", um die Debug-Statements auf der Konsole auszuschalten.
	app.run(debug=True)

################################### ENDE #####################################################
