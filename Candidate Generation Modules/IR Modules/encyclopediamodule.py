# Expert Module which searches an online encyclopedia to compute a distribution of terms close to the query term.

import re
import requests
from bs4 import BeautifulSoup

"""alphabet = "abcdefghijklmnopqrstuvwxyz"

def encyclopedia_disco(query : str):
    Prend en argument une recherche et calcule la distribution de termes proches sur la page Wikipédia de la
    recherche

    page = requests.get(r"https://en.wikipedia.org/wiki/" + query)
    soup = BeautifulSoup(page.content, "html.parser")

    text = (soup.find()).text
    t = re.split('\n', text)
    #print(text)
    para = []
    for i in t :
        if i == '' or i == ' ' or i[0].islower() :
            i = ''
        else :
            para.append(i)

    print(t)
    for i in para :
        print(i)


encyclopedia_disco("Thelma_%26_Louise")"""




