import re
import main
import numpy as np
import math


vsb = [w for w in main.words]  # Creation of a basis for the Vector Space Module, for illustration purpose only
allwords = {}
for w in vsb:
    allwords[w] = 0

freq = {}  # Representation of the vector space with a dictionary of dictionaries of the coordinates of the clue in vsb
for c in main.CWDB:
    d = c.Clue.split(" ")  # Separation of all words in the clue in elements in vsb
    n = len(d)
    f = {}
    for i in d:  # Computing a dictionary of frequencies of words in the clue
        if i not in f:
            f[i] = [1, i]
        else:
            f[i][0] += 1
    freq[c.Clue] = f
    for i in f:
        allwords[f[i][1]] += 1



def partial_match(clue: str):
    coords = {}
    clue1 = clue.split(" ")  # Separation of all words in the clue in elements in vsb
    leng = len(clue1)
    fre = {}
    for w in clue1:  # Computing a dictionary of frequencies of words in the clue
        if w not in fre:
            fre[w] = [1, w]
        else:
            fre[w][0] += 1
    for w in fre:
        # Creation of the dictionary containing the coordinates of the clue in vsb
        coords[fre[w][1]] = round(-np.log(fre[w][0] / leng), 3)

    def dot(co1, co2): # Given dictionaries representing the coordinates of two vectors in vsb :
        n1 = math.sqrt(sum([pow(co1[_], 2) for _ in co1]))
        n2 = math.sqrt(sum([pow(co2[_], 2) for _ in co2]))
        s = 0
        for co in co1:
            if co in co2:
                s += co1[co] * co2[co]
        if (n1*n2) == 0:
            print(co1, n1, co2, n2)
        return s/(n1*n2)

    results = []
    for c in main.CWDB:
        k = dot(freq[c.Clue], coords)
        if k != 0:
            results.append((c.Clue, k))

    return results


print(partial_match("Infamous Georgian"))
