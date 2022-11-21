# Expert Module which searches an online encyclopedia to compute a distribution of terms close to the query term.
# Later.

import re
import requests
from bs4 import BeautifulSoup

"""alphabet = "abcdefghijklmnopqrstuvwxyz"

def encyclopedia_disco(query : str):
    Given a query, computes a distribution of close words on the Wikipedia page of the query.

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




