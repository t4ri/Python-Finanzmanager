# version
# t4ri.de, 03/2024 v1.1.0 see changelog
# t4ri.de, 02/2024 v1.0.2 see changelog
# t4ri.de, 02/2024 v1.0.1 see changelog
# t4ri.de, 02/2023 v1.0.0

# download
# https://github.com/t4ri/Python-Finanzmanager

# import
import pdfplumber
# https://github.com/jsvine/pdfplumber
import re
import os

# start
dir = ""
year = ""
booking_classes = {}
booking_dict = {}

def readini():
    global dir, year, booking_classes
    pre = re.compile(r'([0-9a-zA-ZäüöÄÜÖ_/]*) : (.*){1}(,(.*)){0,}')
    ini = open("com_fm.ini", 'r')
    line = ini.readline()
    while len(line) > 0:
        res = line.split(" : ")
        if len(res) == 2:
            item = res[0].rstrip()
            if item[0] != "#":
                if item == "pfad":
                    dir = res[1].lstrip(" ").rstrip()
                elif item == "jahr":
                    year = res[1].lstrip(" ").rstrip()
                else:
                    name = res[0]
                    values = res[1].lstrip(" ").rstrip().lower()
                    values = values.replace(",,",",")
                    if values[-1] == ",":
                        values = values[:-1]
                    res = values.split(",")                 
                    booking_classes[name]=res
        line = ini.readline()    
    ini.close()
    # Sammler Einnahmen 
    booking_classes["Einnahmen div."]="+"
    # Sammler Ausgaben     
    booking_classes["Ausgaben div."]="-"

# string in float Konvertierung
def str2float(val):
    s = val.replace(".","")
    s = s.replace("+","")
    s = s.replace(",",".")
    return float(s)
  
# Zuordnung der Buchungsgruppe  
def findclass(name, val):
    for key in booking_classes:
        cl = booking_classes[key]
        if isinstance(cl, str):
            # Sammler +/-
            v = str2float(val)
            if (cl == "+") and (v >= 0):
                return key
            elif (cl == "-") and (v < 0):
                return key
        else:               
            for attribute in cl:
                if name.find(attribute) >= 0:
                    # Schlüsselwort gefunden
                    return key
    return None
    
def appendBookingItem(bi):
    overview_name = findclass(bi["typ"] + ' / ' + bi["name"],bi["value"])
    if  overview_name == None:
        overview_name = "unbekannt"                  
    olist = []
    if overview_name in booking_dict:
        olist = booking_dict[overview_name]
    olist.append(bi)
    booking_dict[overview_name] = olist   

    
def readPDF(fname):
    # Öffne das PDF Dokument
    pdf = pdfplumber.open(fname)
    # Regulärer Filter
    #Zeile1 der Buchung, z.B. 02.06.2022 Lastschrift/ STADTWERKE KD.-NR.346,00-ABSCHLAG0 -91,00
    preval1 = re.compile(r'(?P<date>[0-9]{2}.[0-9]{2}.[0-9]{4}) (?P<type>[a-zA-ZäüöÄÜÖ]*)/{0,1} (?P<text>.*) (?P<value>[+,-]([0-9]{1,3}.{0,1})*,[0-9]{2})$')
    # Zeile2 der Buchung
    preval2 = re.compile(r'(?P<date>[0-9]{2}.[0-9]{2}.[0-9]{4}) (?P<type>[a-zA-ZäüöÄÜÖ]*) (?P<text>.*)$')
    # Zeile Saldo, z.B. AlterSaldo 01.06.2022 +1.704,05
    presaldo = re.compile(r'(?P<saldo>[a-zA-Z]*Saldo) (?P<date>[0-9]{2}.[0-9]{2}.[0-9]{4}) (?P<value>[+,-]([0-9]{1,3}.{0,1})*,[0-9]{2})$')
    p = 1
    stop = False
    saldo = 0;
    booking_item = None
    for page in pdf.pages:
        # start ab Seite 2
        if p>1:
            # Seitentext
            pagetext = page.extract_text()
            lines = pagetext.split("\n")
            for line in lines:
                # Textzeile
                info = ""
                if preval1.search(line):
                    # Regular expression Datenzeile
                    info = str(preval1.search(line).groupdict()) 
                    saldo += str2float(preval1.search(line).group("value"))
                    name = preval1.search(line).group("text")
                    typ = preval1.search(line).group("type")
                    # Wertbuchung und Zuordnung
                    if booking_item != None:
                        appendBookingItem(booking_item)
                    booking_item = {}
                    booking_item["date"] = preval1.search(line).group("date")
                    booking_item["name"] = name.lower()
                    booking_item["typ"] = typ.lower()
                    val = preval1.search(line).group("value")
                    booking_item["value"] = val
                elif preval2.search(line):
                    text = preval2.search(line).group("text")
                    typ = preval2.search(line).group("type")
                    booking_item["name"] = booking_item["name"] + ' ' + text.lower()
                    booking_item["typ"] = booking_item["typ"] + ' ' + typ.lower()                 
                elif presaldo.search(line):
                    # Regular expression Saldo
                    info = str(presaldo.search(line).groupdict())
                    saldotyp = presaldo.search(line).group("saldo")
                    if (saldotyp == "AlterSaldo"):
                        saldo = str2float(presaldo.search(line).group("value"))
                    if (saldotyp == "NeuerSaldo"):
                        neuersaldo = str2float(presaldo.search(line).group("value"))
                        saldo = round(saldo,2)
                        delta = neuersaldo - saldo
                        # Saldoabweichung
                        print(fname + " saldo delta "+str(delta))
                        stop = True
                else:
                    # sonstige Zeilen der Buchung
                    if booking_item != None:
                        booking_item["name"] = booking_item["name"] + ' ' + line.lower()
                if stop:
                    break
            if booking_item != None:
                appendBookingItem(booking_item)
                booking_item = None
            if stop:
                break
        p += 1
    pdf.close()

    

readini()
if len(dir) == 0:   
    print("ini Datei fehlerhaft")
    exit()
    
files = os.listdir(dir) 
if len(files) == 0:
    print("keine Finanzreports gefunden")
    exit()

# PDF auswerten
for file in files:
    if (file.find(year) >= 0) and (file.find("Finanzreport") >= 0):
        readPDF(os.path.join(dir, file))

# csv Datenexport
res = open(year + "_finmanger.csv", 'w')
bres = open(year + "_finmanger_bookings.csv", 'w')
saldo=0
res.write("Jahr;Gruppenname;Anzahl Buchungen in der Gruppe;Saldo\n")
bres.write("Buchungsdatum;Gruppenname;Vorgang;Buchungstext;Betrag\n")
for key in booking_dict.keys():
    l = 0
    sum = 0
    for booking in booking_dict[key]:
        sum += str2float(booking["value"])
        bres.write(booking["date"]+";"+key+";"+booking["typ"]+';'+booking["name"]+";"+booking["value"]+"\n")
        l += 1
    sum = round(sum,2)
    saldo += sum
    t = year + ";" + key + ";" + str(l) + ";" + str(sum)
    print (t)
    res.write(t+ "\n")
saldo = round(saldo,2)
t = year + ";Saldo;1;" + str(saldo)
print (t)
res.write(t+ "\n")
res.close()
bres.close()

s="Einnahmen div."
print("\n-----------------------------\n"+s+":")
for booking in booking_dict[s]:
    print (booking["date"]+"; "+booking["typ"]+'; '+booking["name"]+"; "+booking["value"])
    
s="Ausgaben div."
print("\n-----------------------------\n"+s+":")
for booking in booking_dict[s]:
    print (booking["date"]+"; "+booking["typ"]+'; '+booking["name"]+"; "+booking["value"])
    
