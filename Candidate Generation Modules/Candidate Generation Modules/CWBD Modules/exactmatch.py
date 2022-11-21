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
        co += len(c.Word) == length

    if co != 0:
        alpha = 1 - np.tanh((len(candidates) / co) - 1)  # Generates a confidence factor based on the number of answers
        # to the clue over the numbers of right length. The factor is such that it tends to one when the clue mainly
        # has solutions of the right length.
        d = dict(Counter(candidates))
        for c in d:
            results.append((c.key,
                            alpha / c.value))  # Generates a confidence distribution based on the number of
            # occurrences of a certain answer.
    return results
