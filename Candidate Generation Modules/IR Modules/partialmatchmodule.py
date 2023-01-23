from typing import Union, Any

import main
import numpy as np

db_size = len(main.CWDB)


def freq(name: str) :
    d = name.split(" ")
    n = len(d)
    frequencies = {}
    for i in d :
        frequencies[i] = frequencies.get(i, 0) + 1 / n
    return frequencies


def magnitude(coordinates : dict[str, float]):
    if coordinates == {}:
        return 0
    return np.sqrt(sum([pow(coordinates[_], 2) for _ in coordinates]))


class Vector :

    def __init__(self, name) :
        self.name = name
        self.frequencies = freq(name)
        self.coordinates = {}
        self.magnitude = magnitude(self.coordinates)

    def update(self, coords) :
        self.coordinates = coords
        self.magnitude = magnitude(self.coordinates)

    def dot__(self, v) :
        if self.coordinates == {} or v.coordinates == {} :
            return 0
        c1 = self.coordinates
        c2 = v.coordinates
        res = sum([c1[i] * c2.get(i, 0) for i in c1.keys()])
        return res/(self.magnitude * v.magnitude)


def base(db) :
    basis = {}
    for document in db :
        doc = document.split(" ")
        doc1 = {}
        for term in doc :
            basis[term] = basis.get(term, 0) + 1 - doc1.get(term, 0)
            doc1[term] = 1
    return basis


class Vector_Space :

    def __init__(self, db) :
        self.basis = base(db)
        self.dimension = len(self.basis)
        self.vectors = {}
        for document in db :
            self.vectors[document] = Vector(document)
        self.db_size = len(db)

        def update_coordinates() :
            for vector in self.vectors :
                frequencies = vector.frequencies
                coords = {}
                for term in frequencies.keys() :
                    coords[term] = frequencies[term] * np.log10(self.db_size / self.basis[term])
                vector.update(coords)

        update_coordinates()

    def add_vector(self, document):
        self.vectors[document] = (Vector(document))
        vector = self.vectors[-1]
        coords = {}
        frequencies = vector.frequencies
        for term in frequencies.keys() :
            coords[term] = frequencies[term] * np.log10(self.db_size / self.basis[term])
        vector.update(coords)


def initialize(db) :
    """
    :return: list of all_words in the databases, dictionary containing the coordinates dictionaries of all clues,
    number of all words in the database
    :rtype: tuple[dict[str, int], dict[str, dict[str, float]], int]
    """
    """vsb = [w for w in main.words]  # Creation of a basis for the Vector Space Module, for illustration purpose only
    all_words = main.words
    size_dict = len(vsb)

    freq = {}  # Representation of the vector space with a dictionary of dictionaries of the coordinates of the clue
    # in vsb
    for c in main.CWDB :
        d = c.Clue.split(" ")  # Separation of all words in the clue in elements in vsb
        tfd = {}
        for i in d :  # Computing a dictionary of frequencies of words in the clue
            if i not in tfd :
                tfd[i] = 1
            else :
                tfd[i] += 1
        freq[c.Clue] = tfd

    vs = {}
    for c in main.CWDB :
        coordinates = {}
        d = c.Clue.split(" ")  # Separation of all words in the clue in elements in vsb
        n = len(d)
        for i in freq[c.Clue] :
            coordinates[i] = freq[c.Clue][i] * np.log(size_dict / all_words[i]) / n  # tf-idf weight distribution
        vs[c.Clue] = coordinates"""

    VS = Vector_Space(db)  # Updated the module with classes. Fancier huh ?
    return VS


def dot(co1: dict[str, float], co2: dict[str, float]) :
    """
    :param dict[str, float] co1: dictionary containing the coordinates in the vsb model of the first clue
    :param dict[str, float] co2: dictionary containing the coordinates in the vsb model of the second clue
    :return: the usual dot product in R^n of the two vectors
    :rtype: int
    """
    # product of those vectors
    n1 = np.sqrt(sum([pow(co1[_], 2) for _ in co1]))
    n2 = np.sqrt(sum([pow(co2[_], 2) for _ in co2]))
    s = 0
    for co in co1 :
        if co in co2 :
            s += co1[co] * co2[co]
    if (n1 * n2) == 0 :
        print(co1, n1, co2, n2)
    return s / (n1 * n2)


def partial_match(clue: str) :
    """
    :param str clue: Clue that is solved for
    :return: weighted list of words that could match the clue
    :rtype: list[tuple[str, int]]
    """
    all_words, vs, size_dict = initialize()
    coordinates_c: dict[str, Union[float, Any]] = {}
    d_c = clue.split(" ")  # Separation of all words in the clue in elements in vsb
    length_c = len(d_c)
    tfd_c = {}
    for w in d_c :  # Computing a dictionary of frequencies of words in the clue
        if w not in tfd_c :
            tfd_c[w] = 1
        else :
            tfd_c[w] += 1
    for w in tfd_c :
        # Creation of the dictionary containing the coordinates of the clue in vsb
        # tf-idf weight distribution
        coordinates_c[w] = tfd_c[w] / length_c * np.log(size_dict / (all_words[w] + tfd_c[w]))

    results = []
    for clue in main.CWDB :
        k = dot(vs[clue.Clue], coordinates_c)  # Calculates the dot product between the clue and any clue in the CWBD
        if k != 0 :
            # TODO : Change the interpolation function so it does a fair interpolation.
            power = 7
            weight = 1 - pow((1 - k), power)  # Interpolates the weight between the dot product and the inverse of the
            # number of all known words
            results.append((clue.Word, weight))
    results.sort(key = lambda t : t[1], reverse = True)
    return results


print(partial_match("Infamous Georgian"))
