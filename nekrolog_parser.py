print("N E K R O L O G  P A R S E R")
print("Lade os:", end=" ")
from os import system, name, getcwd
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
print(name, end="\n")

print("Lade HTML requests:", end=" ")
# URL INPUT
import requests as req
print(req.__version__, end="\n")

URL = str(input('Ganze URL des deutschen Wikipedia Nekrolog einfügen:'))
website = req.get(URL)

print("Lade Beautiful Soup 4:", end=" ")
#IMPORT BS4, FETCH TABLES FROM URL CONTENT
from bs4 import BeautifulSoup
print("fertig", end="\n")
results = BeautifulSoup(website.content, 'html.parser')
print("Wiki-Seite geladen.", end="\n")
t = results.find_all('table')

print("Lade Regex:", end=" ")
#IMPORT REGEX
import regex as re
print(re.__version__, end="\n")

#LISTE DER HTML-PERSONENEINTRÄGE
persons = []
for i in t:
    alla = i.find_all('a')
    for j in alla:
        f = BeautifulSoup(str(j), 'html.parser').a
        if len(f.attrs)==2 and 'href' in f.attrs and 'title' in f.attrs:
            persons.append(f)
print(len(persons), "Personeneinträge gefunden.")


#DEFINE DATE FORMATTER
def format(datum: str, lang: str = "de"):

    # Nominale Variablen
    monate = ["Januar ", "Februar ", "März ", "April ", "Mai ", "Juni ", "Juli ", "August ", "September ", "Oktober ", "November ", "Dezember "]
    indizes = ["01.", "02.", "03.", "04.", "05.", "06.", "07.", "08.", "09.", "10.", "11.", "12."]
    mon_ind_de = zip(monate, indizes)
    mon_dic_de = dict()
    
    for mon, ind in mon_ind_de:
        mon_dic_de[mon] = ind


    # Datum Formatieren

    for m in mon_dic_de:
        datum = re.sub(m, mon_dic_de[m], datum)    
    clear = re.sub(r"(\[\d\])|([^0-9.;])", "", datum)
    connect = re.sub("[;]", " - ", clear)
    
    return connect

print("Fetche Wikitexte der Einträge...")
#EXTRAHIERE PERSONENDATEN VON HTML
nekro = []

for i in persons:
    try:
        pURL = 'https://de.wikipedia.org/' + i['href']
        pwebsite = req.get(pURL)   
        presults = BeautifulSoup(pwebsite.content, 'html.parser')
        pwiki = presults.body.find('p').get_text()

        try:
            ptext = re.match(pattern=r"^.+?(\(.+?\))", string=pwiki).group(1)
        except Exception:
            ptext = ""
            pass

        date = format(ptext)
    except Exception:
        print(Exception)
    nekro.append((i['title'], date, pwiki[:250]))
    print(nekro[-1][0], nekro[-1][1], int(len(nekro)/len(persons)*100), "%")

try:
    with open("Nekrolog.txt", mode='w', encoding='utf8') as n:
        n.write('\n'.join('{}, {}, {}'.format(x[0],x[1],x[2]) for x in nekro))
except Exception:
    print(Exception)

input('Ergebnisse in Nekrolog.txt abgespeichtert. Pfad:{}\n'.format(getcwd()))
