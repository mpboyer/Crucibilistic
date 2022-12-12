import main
import numpy as np


vsb = [w for w in main.words]  # Creation of a basis for the Vector Space Module, for illustration purpose only
all_words = {}
for w in vsb:
    all_words[w] = 0
size_dict = len(vsb)

freq = {}  # Representation of the vector space with a dictionary of dictionaries of the coordinates of the clue in vsb
for c in main.CWDB:
    d = c.Clue.split(" ")  # Separation of all words in the clue in elements in vsb
    n = len(d)
    tfd = {}
    for i in d:  # Computing a dictionary of frequencies of words in the clue
        if i not in tfd:
            tfd[i] = 1
        else:
            tfd[i] += 1
    freq[c.Clue] = tfd
    for i in tfd:
        all_words[i] += 1

vs = {}
for c in main.CWDB:
    coordinates = {}
    d = c.Clue.split(" ")  # Separation of all words in the clue in elements in vsb
    n = len(d)
    for i in freq[c.Clue]:
        coordinates[i] = freq[c.Clue][i] * np.log(size_dict / all_words[i]) / n  # tf-idf weight distribution
    vs[c.Clue] = coordinates


def partial_match(clue: str):
    coordinates_c = {}
    d_c = clue.split(" ")  # Separation of all words in the clue in elements in vsb
    length_c = len(d_c)
    tfd_c = {}
    for w in d_c:  # Computing a dictionary of frequencies of words in the clue
        if w not in tfd_c:
            tfd_c[w] = 1
        else:
            tfd_c[w] += 1
    for w in tfd_c:
        # Creation of the dictionary containing the coordinates of the clue in vsb
        # tf-idf weight distribution
        coordinates_c[w] = tfd_c[w] / length_c * np.log(size_dict / (all_words[w] + tfd_c[w]))

    def dot(co1, co2):  # Given dictionaries representing the coordinates of two vectors in vsb computes the dot
        # product of those vectors
        n1 = np.sqrt(sum([pow(co1[_], 2) for _ in co1]))
        n2 = np.sqrt(sum([pow(co2[_], 2) for _ in co2]))
        s = 0
        for co in co1:
            if co in co2:
                s += co1[co] * co2[co]
        if (n1*n2) == 0:
            print(co1, n1, co2, n2)
        return s/(n1*n2)

    results = []
    for clue in main.CWDB:
        k = dot(vs[clue.Clue], coordinates_c)  # Calculates the dot product between the clue and any clue in the CWBD
        if k != 0:
            # TODO : Change the interpolation function so it does a fair interpolation.
            power = 7
            weight = 1 - pow((1-k), power)  # Interpolates the weight between the dot product and the inverse of the
            # number of all known words
            results.append((clue.Clue, weight))
    results.sort(key = lambda t: t[1], reverse = True)
    return results


print(partial_match("Infamous Georgian"))
