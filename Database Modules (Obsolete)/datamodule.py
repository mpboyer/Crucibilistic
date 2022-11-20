import re
import requests
from bs4 import BeautifulSoup

URL = 'https://xwordinfo.com/Crossword?date=4/1/1994'


def disco(url):
    """Prend en argument l'URL d'une des pages du site xwordinfo contenant une grille de mots croisés.
    Renvoie la liste de toutes les listes [Mot, Indice]."""

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    aclues = (soup.find(id = "ACluesPan")).text[7:]
    dclues = (soup.find(id = "DCluesPan")).text[5:]

    print(aclues)
    print(dclues)
    aclues1 = (re.split("[0-9]+(?=[a-zA-Z,_,-,1])", aclues))[1:]
    for i in range(len(aclues1)):
        clue = re.split(' : ', aclues1[i])
        aclues1[i] = ["'" + clue[1].replace("'", " ") + "'", str(len(clue[1])), "'" + clue[0].replace("'", " ") + "'"]


    dclues1 = (re.split('[0-9]+(?=[a-zA-Z,_,0-9])', dclues))[1:]
    for i in range(len(dclues1)):
        clue = re.split(' : ', dclues1[i])
        dclues1[i] = ["'" + clue[1].replace("'", " ") + "'", str(len(clue[1])), "'" + clue[0].replace("'", " ") + "'"]


    Clues = aclues1 + dclues1
    print(Clues)
    return Clues

# A fixer, explose en cas de présence de nombres dans les définitions : Dates, renvoi vers d'autres définitions...

