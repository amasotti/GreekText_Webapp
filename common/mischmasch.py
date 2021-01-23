# -*- coding: utf-8 -*-
__autor__ = "Antonio Masotti"
'''
DOC: kleine Funktionen um repetitive Aufgaben zu vermeiden.
Hier befinden sich alle Funktionen, die nicht direkt mit den HTML-Seiten interagieren, aber deren Visualisierung und Inhaltbefüllung unterstützen.

'''
# IMPORTE #
import requests
from flask import flash
from bs4 import BeautifulSoup
import lxml
import re
import os
from pathlib import Path
import csv


######################################################################################

# Klein Alert für die externen Links
def flash_extern(message='Die externen Links werden auf separaten Tabs geöffnet!'):
    flash(message)

######################################################################################

# Funktion, die alle Werke eines bestimmten Autors auflistet
def get_works(autor):
    # Link auf Perseus. Hier befindet sich die Liste der Werke
    link = "http://artflsrv02.uchicago.edu/cgi-bin/perseus/search3torth?dbname=GreekApr19&word=&OUTPUT=conc&ORTHMODE=ORG&CONJUNCT=PHRASE&DISTANCE=3&author="+autor+"&title=&POLESPAN=5&THMPRTLIMIT=1&KWSS=1&KWSSPRLIM=500&trsortorder=author%2C+title&editor=&pubdate=&language=&shrtcite=&genre=&sortorder=author%2C+title&dgdivhead=&dgdivtype=&dgsubdivwho=&dgsubdivn=&dgsubdivtag=&dgsubdivtype="

    # Der HTML-Code der Seite wird gelesen
    source = requests.get(link)
    # Der HTML-Code wird in ein für Python verständliches Format umgewandelt
    parsed = BeautifulSoup(source.content, 'lxml')
    # Alle Links (HTML-Tag <a></a>) werden aufgelistet
    werk_link = parsed.find_all("a")

    # Perseus bietet für jedes Werk zwei Links (Originaltext, Englische Übersetzung)
    # Die Links zu den Übersetzungen werden ausgefiltert
    regex = r"<a name=\"(.*)Gr\">"
    ergebnisse = []
    # Für jedes Werk werden die Links zum Text, Wortzählung und Wortliste zusammen mit dem Titel des Werks extrahiert
    for a in range(0,len(werk_link)):
        current_link = werk_link[a]
        gefunden = re.finditer(regex, str(current_link), re.MULTILINE)
        if gefunden is not None:
            for einzelwerk in gefunden:
                titel = werk_link[a+1].text
                link_gr_text = "http://artflsrv02.uchicago.edu/"+str(werk_link[a+1]['href'])
                link_wortzahlung = "http://artflsrv02.uchicago.edu/"+str(werk_link[a+3]['href'])
                ergebnisse.append((titel, link_gr_text, link_wortzahlung))
    return ergebnisse

######################################################################################


def text_formatter(gewaehlter_text):
    '''
    Funktion zur Formatierung der Texte und deren Visualisierung in Browser
    '''
    if gewaehlter_text == "Iliad":
        # Für die Ilias wurden hier spezielle RegExp programmiert, die das spezielle Layout dieses Textes berücksichtigen
        path = Path(('common/static/assets/Iliad/Iliad_vollständig.txt'))
        with open(path,"r",encoding="utf-8") as f:
            inhalt = f.read()
        regex_el = r"(\n)"
        subst_el = "</p >\\0<p class='testi_greci'>"
        inhalt = re.sub(regex_el, subst_el, str(inhalt), 0, re.MULTILINE)
        inhalt = "<p class='testi_greci'> <strong> 1.1 </strong> " + inhalt

        regex_il = r"(\d+\.?(\d+))"
        subst_il = "<strong> \\1 </strong> "
        inhalt = re.sub(regex_il, subst_il, inhalt, 0, re.MULTILINE)
    else:
        # Alle andere Texte werden im Moment nicht für die Visualisierung optimiert. Der grobe Text wird dann gezeigt
        path = Path.cwd() / "common" / "static" / "assets" / gewaehlter_text / str(gewaehlter_text.replace(" ","_") + "_vollständig.txt")
        with open(str(path.resolve()),"r",encoding="utf-8") as f:
            inhalt = f.read()
        inhalt = "<p class='testi_greci'>" + inhalt + "</p >"
    # Return sendet eine Tupel mit zwei Elementen: Titel des Werks und Inhalt.
    return (gewaehlter_text,inhalt)

######################################################################################

def get_worter(link):
    '''
    Diese Funktion akzeptiert den Link eines Textes und bildet daraus eine Wortlist aller Wörter in diesem Text.

    '''

    # Der Text wird heruntergeladen
    source = requests.get(link)
    parsed = BeautifulSoup(source.content, 'lxml')
    # die Wortliste in Perseus befindet sich innerhalb von den HTML tags <pre></pre>. Wir suchen gezielt danach:
    wort_list = parsed.find("pre").text

    # wort_list ist jetzt ein sehr langer String, der gereinigt werden muss

    # Wir löschen erstmal die Infos über die Frequenz der Wörter und die nicht-griechischen Wörter
    loesch_nicht_gr = r"([a-z]\s?\,?\.?\;?|[A-Z]\s?\,?\.?\;?|\d+)"
    wort_list = re.sub(loesch_nicht_gr, "", wort_list, 0, re.MULTILINE)
    # Anstelle der gelöschten Infos stehen jetzt leere Zeilen. Diese können auch gelöscht werden
    leere_zeile = r"^\s*$"
    wort_list = re.sub(leere_zeile, "", wort_list, 0, re.MULTILINE)
    # Nach jedem Wort stehen vor dem Zeilenumbruch noch leere Zeichen. Wir löschen sie auch, um am Ende eine reine Wortliste zu bekommen
    leere_zeichen = r"\s+$"
    wort_list = re.sub(leere_zeichen, "", wort_list, 0, re.MULTILINE)

    # Wir wandeln den langen String in eine Liste von Wörtern um
    new_list = wort_list.split("\n")
    # die erzeugte Liste wird  als Output gesendet
    return new_list

######################################################################################


def search_infos(link):
    '''
    Die Funktion sucht alle Infos, die wir brauchen, um die Tabellen zu füllen
    '''
    # die Funktion get_worter lädt eine Liste alle Wortformen herunter, die im Folgenden verarbeitet wird
    words = get_worter(link)
    # die nötigen leeren Variabeln werden initialisiert
    ergebnisse = []
    zaehler = 0
    # Für jede Wortform werden die benötigten Infos gesucht (Wortform, Lemma, Übersetzung, morphologische_Bestimmung)
    for x in words:
        # Die Liste der Ergebnisse wird initialisiert
        result = [ ]
        # Das erste Element jedes Elements in der Liste ist die Wortform selbst. Wenn diese leer ist, wird die Wortform übersprüngen
        if x == " " or x == "" or x == "." or x == ",":
            continue
        else:
            result.insert(0,x) # word
            # Ein Link zum Perseus Wörterbuch wird generiert
            link = "http://www.perseus.tufts.edu/hopper/morph?l="+x+"&la=greek#lexicon"

            # Die Seite des Worterbuchs wird eingelesen und untersucht
            get_source = requests.get(link)
            source = get_source.text
            parsed = BeautifulSoup(source, 'lxml')

            # der String des Lexikoneintrags wird gesucht und gespeichert
            lemma_raw = re.finditer(r"h4 class=\"greek\">(\w+)<\/h4>", str(parsed), re.MULTILINE)
            lemma = " "
            # Wenn ein Lemma gefunden wird, wird dieses mit einer RegExp gespeichert
            if lemma_raw is not None:
                for num, match in enumerate(lemma_raw,start=1):
                    lemma = lemma + str(match.group(1)) + " "
            # Das Lemma ist das zweite Element in der Ergebnisliste
            result.insert(1, lemma)  # 1: lemma

            # Wenn das Wörterbuch eine Übersetzung für das Lemma anbietet, wird diese gesucht

            # Fall 1: es wird keine Übersetzung angeboten. Als Übersetzung wird ein festgelegter String verwendet
            if parsed.select('span.lemma_definition') == [ ] or len(parsed.select('span.lemma_definition')) <= 0:
                translation = "keine Übersetzung gefunden"
            else:
                # Fall 2: Es gibt eine Übersetzung. Diese wird übernommen.
                translation = str(parsed.select('span.lemma_definition')[ 0 ].text.strip())
            if "unavailable" in translation:
                translation = "keine Übersetzung gefunden"
            # Die Übersetzung wird als drittes Element in der Liste gespeichert
            result.insert(2, translation)

            # Die möglichen morphologischen Bestimmungen werden gesucht
            morpho_raw = re.finditer(r"<td class=\"greek\">(.*)<\/td>\s?\n?<td>(.*)<\/td>\s?\n?<td style=\"font-size:", str(parsed), re.MULTILINE)
            morpho_poss = []
            # Wenn mophologische Informationen verfügbar sind, werden diese in einen String zusammengefügt (und mit "OR" verbunden)
            if morpho_raw is not None:
                for num, match in enumerate(morpho_raw,start=1):
                    morpho_poss.append(str(match.group(2)))

            if len(morpho_poss) > 1:
                morpho_parsing = " OR ".join(x for x in morpho_poss)
            # Fall 2: Perseus bietet keine morphologische Bestimmung: der String "Nichts gefunden" wird als Wert für die Variabel verwendet
            elif morpho_poss is None or morpho_poss == [ ]:
                morpho_parsing = "Nichts gefunden"
            # Wenn die morphologische Bestimmung eindeutig ist (nur eine vorhanden), kann der Wert direkt übernommen werden
            else:
                morpho_parsing = morpho_poss[0]

            # Die gewonnenen Informationen bilden das vierte Element der Ergebnisliste
            result.insert(3,morpho_parsing)
            # Der Zähler wird um eins erhöht
            zaehler += 1
            # Ein Print-Statement infomiert uns über den Fortschritt bei der Bildung der Liste
            print(f"Ich bearbeite item {zaehler} von {len(words)}")
            # Die Liste wird einer obergeordneten Liste zugefügt.
            ergebnisse.append(result)
    # Die Liste aller Ergebnisse wird als Output wiedergegeben.
    return ergebnisse

######################################################################################

def get_texte(link_zum_werk,aufmachen=True):

    '''
    DOC:
    Funktion zum Download von Texten aus Perseus

    '''
    # Der Link zu einem Werk wird geöffnet und der HTML-Code durchgelesen (Web-Scraping mit BeautifulSoup 4)
    get_source = requests.get(link_zum_werk)
    # Der HTML-Code muss zunächst in ein für Python lesbares Format umgewandelt werden
    parsed = BeautifulSoup(get_source.text, 'lxml')
    # Der Titel des Werks wird gefunden und gespeichert
    italics = parsed.find('i')
    titel = italics.find('a').text

    # Die Variabeln für die Dateipfade werden initialisiert und festgelegt
    datei_name = str(titel) + "_vollständig.txt"
    HAUPTDIRECTORY = Path(os.getcwd())
    WERKADRESSE = Path(os.getcwd()) / "common" / "static" / "assets" / titel / datei_name
    ARBEITSVERZEICHNIS = WERKADRESSE.parents[0]


    # Zunächst kontrollieren wir, ob die Datei bzw. die Verzeichnisse schon vorhanden sind:
    # Fall 1: Die Datei ist schon vorhanden und wird einfach geöffnet (sie wurde bereits heruntergeladen)
    if ARBEITSVERZEICHNIS.resolve().exists():
        print("\nWerk schon vorhanden...wird gesprungen")

        if aufmachen:
            print(str(ARBEITSVERZEICHNIS.resolve()))
            os.chdir(ARBEITSVERZEICHNIS.resolve())
            os.system("notepad.exe "+str(datei_name.replace(" ","_")))
    # Fall 2: die Datei existiert noch nicht. Der Text muss heruntergeladen werden
    else:
        print(f"\n Neues Werk: {titel} wird heruntergeladen...")
        ARBEITSVERZEICHNIS.mkdir()
        os.chdir(ARBEITSVERZEICHNIS.resolve())

        # Einige Print-Statements informieren den Benutzer mittels der Konsole über die laufenden Schritte
        print(f"Die einzelnen Kapitel von {titel} werden gesucht")

        # Die einzelnen Kapitel werden gefunden und deren Titel und Links kopiert
        buecher_urls = re.finditer(r"<span class=\"navlevel1\"><a href=\"(.*)\">", str(parsed),re.MULTILINE)
        kapitel_titels = re.finditer(r"<span class=\"navlevel1\"><a href=\"(.*)\">(.*)<\/a>", str(parsed),re.MULTILINE)
        buecher_links = []

        # Eine Liste der Kapitel wird generiert
        for link in buecher_urls:
            buecher_links.append("http://artflsrv02.uchicago.edu/cgi-bin/perseus/"+link.group(1))

        titel_list = []
        for kapitel_titel in kapitel_titels:
            titel_list.append(kapitel_titel.group(2))

        zaehler = 0
        vollständiger_text = []

        # Die einzelnen Kapitel werden geöffnet und deren Inhalt kopiert
        for buch in buecher_links:
            print(f'Kapitel {zaehler} von {str(len(buecher_links))} heruntergeladen')


            get_book = requests.get(buch)
            parse_book = BeautifulSoup(get_book.text, 'lxml')
            # innerhalb von HTML-tags <div id="perseuscontent"></div> befindet sich der für uns interessante Inhalt.
            # Dieser wird gespeichert
            text = parse_book.find("div", {"id": "perseuscontent"}).text
            file_name = titel +"_"+ str(titel_list[zaehler])+".txt"

            # Der Text wird in eine Textdatei geschrieben
            with open(file_name, "w+", encoding="UTF-8") as testo:
                testo.write(text)
            vollständiger_text.append(text)
            zaehler += 1

        # Alle vollständige Texte werden mit nache einem Standardpattern gespeichert
        fname = titel.replace(" ","_") + "_vollständig.txt"

        # Alle einzelnen Kapitel werden in eine einzige Textdatei zusammengeführt.
        with open(fname, "w+",encoding="UTF-8") as testo:
            volltext = "\n\n".join(x for x in vollständiger_text)
            testo.write(volltext)

        # Es wird kontrolliert, ob die Datei geöffnet werden muss
        if aufmachen:
            os.system(fname)
    # Verzeichniswechsel (zurück zum Hauptverzeichnis)
    os.chdir(HAUPTDIRECTORY)

######################################################################################
