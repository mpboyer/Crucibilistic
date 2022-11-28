import numpy as np

import main
from collections import Counter


def exactmatch(length, clue):
    """Given"""
    candidates = []
    for c in main.CWDB:
        if c.Clue == clue:
            candidates.append(c.Word)

    results = []
    co = 0
    for c in candidates:
        co += len(c) == length

    if co != 0:
        alpha = 1 - np.tanh((len(candidates) / co) - 1)  # Generates a confidence factor based on the number of answers
        # to the clue over the numbers of right length. The factor is such that it tends to one when the clue mainly
        # has solutions of the right length.
        d = dict(Counter(candidates))
        for c in d:
            results.append((c, alpha / (len(candidates) + 1 - d[
                c])))  # Generates a confidence distribution based on the number of occurrences of a certain answer.
    return results



def a_tad_less_exactmatch(length: int, clue: str):
    results = []

    def levenshtein(c1, c2):
        if c1 == '':
            return len(c2)
        elif c2 == '':
            return len(c1)
        elif c1[0] == c2[0]:
            return levenshtein(c1[1:], c2[1:])
        else:
            return 1 + min(levenshtein(c1[1:], c2), levenshtein(c1, c2[1:]), levenshtein(c1[1:], c2[1:]))

    candidates = []
    for c in main.CWDB:
        r = False
        i = 0
        while i and not r :
            if levenshtein(c.Clue, clue) <= i:
                candidates.append((c.Word, i))
                r = True
            i += 1

    sorted(candidates)
    d = {}
    for c in candidates :
        if d[c[0]] == 0 :
            d[c[0]] = c[1]

        else :

