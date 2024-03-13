
# Python Finanzmanager

[![Support Python versions](https://img.shields.io/pypi/pyversions/pdfplumber.svg)](https://pypi.python.org/pypi/pdfplumber)

**Python Finanzmanager zur Finanzübersicht von comdirect Finanzreports**<br>
Mittels eines Python-Skripts werden die auf dem PC abgelegten PDF Finanzreports eines Jahres eingelesen und die 
enthaltenen Eingaben und Ausgaben über Schlüsselwörter Buchungsgruppen zugeordnet.
Ergebnis sind CSV Dateien mit Salden und Umsätzen pro Gruppenname, diese können dann z.B. in Excel weiter ausgewertet 
werden.


## Disclaimer

**Es handelt sich um ein reines Hobby-Projekt.**
**Es wird keine Garantie für Fehlerfreiheit, Support oder zeitnahe Unterstützung gegeben!**
**Die genannten Produkt- und Markennamen sind Eigentum der jeweiligen Inhaber.**


## Anforderung

- Python 3.7+

Download und Support der Python Ablaufumgebung siehe [support page](https://www.python.org/).
Zum Lesen der PDF Finanzreports wird die Python Bibliothek [pdfplumber](https://github.com/jsvine/pdfplumber) benötigt.

## Installation

### Windows

1. Download [Python 3.11+](https://www.python.org/)
2. Unter Windows: Kommandozeilenfenster öffnen („Windows-Taste“ + „R“ starten. Dort den Befehl „cmd.exe“ eingeben und 
   mit „Enter“ bestätigen), alle weiteren Schritte sind im Kommandozeilenfenster auszuführen.
3. Python version prüfen mit dem Aufruf: python --version
4. Python Aktualisierung mit dem Aufruf: pip install update
5. pdfplumber installieren: pip install pdfplumber
6. [com_fm.py](com_fm.py) und [com_fm.ini](com_fm.ini) herunterladen
7. Parameteranpassung von com_fm.ini, siehe nachfolgend

### macOS

1. Terminal öffnen
2. Homebrew installieren:
   ```shell
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Python 3 und poetry installieren: 
   ```shell
   brew install python@3.11 poetry
   ```
4. Dieses Repository klonen:
   ```shell
   git clone https://github.com/t4ri/Python-Finanzmanager && cd Python-Finanzmanager
   ```
5. Poetry install im Projekt-Ordner ausführen:
   ```shell
   poetry install
   ```
6. com_fm.ini erstellen und ggf. Parameter anpassen:
   ```shell
   cp com_fm.ini.example com_fm.ini
   ```
7. Skript ausführen:
   ```shell
   poetry run python com_fm.py
   ```


## Parametrierung

Die Datei [com_fm.ini.example](com_fm.ini.example) enthält alle zur individuellen Anpassung notwendigen Parameter:

| Parameter                                                                                                | Beschreibung                                                                                                                         |
|----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| pfad : D:\\comdirect\\Kto1234567                                                                         | Pfad zum Ablageort der comdirect Finanzreports.                                                                                      |
| jahr : 2022                                                                                              | Auswertungsjahr                                                                                                                      |
| Gruppenname : Schlüsselwort1,Schlüsselwort2,... z.B.:<br>Online Ausgaben : paypal,amazon,internet,online | Unter dem Gruppenname werden alle Einnahmen und Ausgaben zusammengefasst deren Text eines der nachfolgenden Schlüsselwörter enthält. |                                                                          |

com_fm.ini enthält bereits Beispiel-Gruppennamen und Schlüsselwörter, die individuell erweitert oder angepasst werden
können.

Hierbei ist zu beachten:
* Die Trennung zwischen pfad, jahr und Gruppennamen ist ` : ` (ein Leerzeichen vor und nach dem Doppelpunkt).
* Die Schlüsselwörter (kleingeschrieben) ohne Leerzeichen mit Komma getrennt.
* com_fm.ini wird in der Reihenfolge der Eintragung durchsucht. Beachte, dass sehr kurze Schlüsselwörter spätere längere 
Schlüsselwörter unterdrücken können. So verhindert das Schlüsselwort "markt" z.B. das Auffinden von "kaufmarkt".


## Aufbau der Finanzreports

Die für die Auswertung relevanten Zahlungsvorgänge beginnen auf Seite 2 des Finanzreports und startet mit dem Einlesen
des alten Saldos. Die weiteren Einnahmen und Ausgaben werden bis zum Erreichen des neuen Saldos zeilenweise eingelesen.
Hierbei werden die Buchungstext-Zeilen berücksichtigt, z.B.:

`02.06.2022 Lastschrift/ STADTWERKE KD.-NR.345,00-ABSCHLAG0 -91,00`

Der Text wird mit den in com_fm.ini hinterlegten Schlüsselwörtern verglichen und der Buchungsbetrag dem Gruppensaldo
zugeordnet. Der Text wird beim Vergleich in Kleinbuchstaben umgewandelt, sodass Klein-/Grossschreibung keine Relevanz
hat. Kann keine Zuordnung gefunden werden, so werden Einnahmen der Gruppe "Einnahmen div." und Ausgaben der Gruppe
"Einnahmen div." zugeordnet.

Zur Überprüfung und ggf. Ergänzung von Schlüsselwörtern in com_fm.ini werden alle Buchungen der Gruppen "Einnahmen div."
und "Einnahmen div." am Ende ausgegeben. Enthält com_fm.ini keine Gruppennamen, so werden alle Einnahmen "Einnahmen 
div." und Ausgaben "Ausgaben div." zugeordnet.


## Aufruf

com_fm.py und com_fm.ini müssen sich im gleichen Verzeichnis befinden.<br>

```shell
python com_fm.py
```

Laufzeit Ausgaben:
```shell
Finanzreport_Nr._01_per_03.02.2020.pdf saldo delta 0.0
Finanzreport_Nr._02_per_02.03.2020.pdf saldo delta 0.0
...
```

Während der Bearbeitung werden die eingelesenen Finanzreport-Dateinamen angezeigt. Eine Saldenabweichung wird bei einem
Auswertungsfehler als delta angezeigt.

## Ergebnisdateien

Es werden zwei CSV Dateien erzeugt *jahr*_finmnanager.csv und *jahr*_finmnanager_bookings.csv. 

*jahr*_finmnanager.csv enthält die Gruppenübersicht und Gruppensalden mit den Spalten: 

| Jahr | Gruppenname | Anzahl Buchungen in der Gruppe | Saldo |
|------|-------------|--------------------------------|-------|

*jahr*_finmnanager_bookings.csv enthält

| Buchungsdatum | Gruppenname | Vorgang | Buchungstext | Betrag |
|---------------|-------------|---------|--------------|--------|


## Lizenz

**Creative Commons BY-NC-SA**

Give Credit, NonCommercial, ShareAlike

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.


[comment]: # (:large_blue_circle:)
