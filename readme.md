# Python Finanzmanager 

[![Support Python versions](https://img.shields.io/pypi/pyversions/pdfplumber.svg)](https://pypi.python.org/pypi/pdfplumber)

**Python Finanzmanager zur Finanzübersicht von comdirect Finanzreports**<br>
Mittels eines Python-Skripts werden die auf dem PC abgelegten PDF Finanzreports eines Jahres eingelesen und die enthaltenen Eingaben und Ausgaben über Schlüsselwörter Buchungsgruppen zugeordnet. 
Ergbnis sind CSV Dateien mit Salden und Umsätzen pro Gruppenname, diese können dann z.B. in Excel weiter ausgewertet werden.


## Disclaimer

**Es handelt sich um ein reines Hobby-Projekte.**|
**Es wird keine Garantie für Fehlerfreiheit, (umfangreichen) Support, Realisierung von individuellen Wünschen oder zeitnahe Unterstützung geben!**|
**Die genannten Produkt- und Markennamen sind Eigentum der jeweilingen Inhaber**

<br>

## Anforderung

- Python 3.7+

Download und Support der Python Ablaufumgebung siehe [support page](https://www.python.org/).
Zum Lesen der PDF Finanzreports wird die Python Bibliothek [pdfplumber](https://github.com/jsvine/pdfplumber) benötigt.

## Installation

1. Download [Python 3.11+](https://www.python.org/)
2. Unter Windows: Kommandozeilenfenster öffnen („Windows-Taste“ + „R“ starten. Dort den Befehl „cmd.exe“ eingeben und mit „Enter“ bestätigen)
   Alle weiteren Schritte sind im Kommandozeilenfenster auszuführen.
3. Python version prüfen mit dem Aufruf: python --version
4. Python Aktualisierung mit dem Aufruf: pip install update
5. pdfplumber installieren: pip install pdfplumber
6. [com_fm.py](com_fm.py) und [com_fm.ini](com_fm.ini) herunter laden
7. Parameteranpassung von com_fm.ini, siehe nachfolgend

## Parametrierung

Die Datei [com_fm.ini](com_fm.ini) enthält alle zur individuellen Anpassung notwendigen Parameter:

| Parameter | Beschreibung |
|-------------------------------------------------------|------------------------------------------------------------------|
| pfad : D:\\comdirect\\Kto1234567 | Pfad zum Ablageort der comdirect Finanzreports, "\\" als Verzeichnistrenner beachten! |
| jahr : 2022 | Auswertungsjahr |
| Gruppenname :  Schlüsselwort1 , Schlüsselwort2, ... z.B.:<br>Online Ausgaben : paypal,amazon,internet,online | Unter dem Gruppenname werden alle Einnahmen und Ausgaben zusammengefasst 
deren Text eines der nachfolgenden Schlüsselwörter enthält. |

## Aufbau der Finanzreports

Die für Auswertung relevanten Zahlungsvorgänge beginnen auf Seite 2 des Finanzreports und startet mit dem Einlesen des Alten Saldos. Die weiteren Einnahmen und Ausgaben werden bis zum Erreichen des Neuen Saldos zeilenweise eingelesen. Hierbei werden die Buchungstext Zeilen berücksichtigt, z.B.<br>
02.06.2022 Lastschrift/ STADTWERKE KD.-NR.345,00-ABSCHLAG0 -91,00<br>
Der Text wird mit den in com_fm.ini hinterlegten Schlüsselwörtern verglichen und der Buchungsbetrag dem Gruppensaldo zugeordnet. Der Text wird beim Vergleich in Kleinbuchstaben umgewandelt, so dass Klein-/Grossschreibung keine Relevanz hat. Kann keine Zuordnung gefunden werden, so werden Einnahmen der Gruppe "Einnahmen div." und Ausgaben der Gruppe "Einnahmen div." zugeordnet. Zur Überprüfung und ggf. Ergänzung von Schlüsselwörtern in com_fm.ini werden alle Buchungen der Gruppen "Einnahmen div." und "Einnahmen div." ausgegeben. Enthält com_fm.ini keine Gruppennamen, so werden alle Einnahmen "Einnahmen div." und Ausgaben "Ausgaben div." zugeordnet.

## Aufruf

com_fm.py und com_fm.ini müssen sich im gleichen Verzeichnis befinden.<br>

```sh
python com_fm.py

Finanzreport_Nr._01_per_03.02.2020.pdf saldo delta 0.0
Finanzreport_Nr._02_per_02.03.2020.pdf saldo delta 0.0
...
```

## Ergebnisdateien
Es werden zwei CSV Dateien erzeugt *jahr*_finmnanager.csv und *jahr*_finmnanager_bookings.csv. *jahr*_finmnanager.csv enthält die Gruppenübersicht und Gruppensalden mit den Spalten Jahr; Gruppenname; Anzahl Buchungen in der Gruppe; Saldo.
*jahr*_finmnanager_bookings.csv enthält Buchungsdatum; Gruppenname; Vorgang; Buchungstext; Betrag.

## Lizenz

**Creative Commons BY-NC-SA**<br>
Give Credit, NonCommercial, ShareAlike

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.


[comment]: # (:large_blue_circle:)
