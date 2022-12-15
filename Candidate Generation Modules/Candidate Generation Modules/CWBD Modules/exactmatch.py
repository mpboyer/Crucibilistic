from typing import List, Tuple, Union, Any

import numpy as np

import main
from collections import Counter


def exactmatch(length, clue):
    """
    :param int length: length of the wanted word
    :param Clue clue: actual clue we want to solve
    :return: weighted list of words that have clue for their clue in the CWDB
    :rtype: tuple(Clue, float) list
    """
    candidates = []
    for c in main.CWDB:
        if c.Clue == clue:
            candidates.append(c.Word)

    results: list[tuple[str, Union[float, Any]]] = []
    co = 0
    for c in candidates:
        co += len(c) == length

    if co != 0:
        alpha = 1 - np.tanh((len(candidates) / co) - 1)  # Generates a confidence factor based on the number of answers
        # to the clue over the numbers of right length. The factor is such that it tends to one when the clue mainly
        # has solutions of the right length.
        d = dict(Counter(candidates))
        for c in d:
            results.append((c, alpha / (len(candidates) + 1 - d[c])))  # Generates a confidence distribution based on
            # the number of occurrences of a certain answer.
    return results
