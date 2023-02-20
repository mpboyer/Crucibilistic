import numpy as np
import re
import setup
from collections import Counter


def exactmatch(length, clue):
    """
    :param int length: length of the wanted word
    :param knownClue clue: actual clue we want to solve
    :return: weighted list of words that have clue for their clue in the CWDB
    :rtype: tuple(knownClue, float) list
    """
    clue = clue.lower()
    clue = re.sub("[^\w\s:À-ÿ]", "", clue)
    candidates = []
    for c in setup.CWDB:
        c_clue = re.sub("[^\w\s:À-ÿ]", "", c.Clue)
        if c_clue == clue:
            c_word = re.sub("[^\w\s:À-ÿ]", "", c.Word)
            candidates.append(c_word)

    results: list[tuple[str, float]] = []
    co = 0
    for c in candidates:
        co += len(c) == length

    if co != 0:
        alpha = 1 - pow(-np.tanh((len(candidates) / co) - 1), 11)
        # Generates a confidence factor based on the number of answers
        # to the clue over the numbers of right length. The factor is such that it tends to one when the clue mainly
        # has solutions of the right length.
        d = dict(Counter(candidates))
        for c in d:
            results.append((c, alpha / (len(candidates) + 1 - d[c])))  # Generates a confidence distribution based on
            # the number of occurrences of a certain answer.

    def sorting_function(t) :
        return t[1]

    results.sort(key = sorting_function, reverse = True)
    return results


# print(exactmatch(5, "Express indirectly"))

