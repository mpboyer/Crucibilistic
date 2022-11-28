import numpy as np
import main


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
        n = levenshtein(c.Clue, clue)
        print(n)
        if n <= 10:
            candidates.append((c.Word, n))

    sorted(candidates)
    print(candidates)
    d = {}
    for c in candidates:
        if c[0] not in d.keys():
            d[c[0]] = (c[1], 1)

        else:
            w, n = d[c[0]]
            d[c[0]] = ((n * w + c[1]) / (n + 1), n + 1)

    co = 0
    for c in d:
        co += len(c) == length

    if co != 0:
        alpha = 1 - np.tanh((len(candidates) / co) - 1)  # Generates a confidence factor based on the number of answers
        # to the clue over the numbers of right length. The factor is such that it tends to one when the clue mainly
        # has solutions of the right length.
        for c in d:
            results.append((c, alpha / (1 + d[c][
                1])))  # Generates a confidence distribution based on the number of  # occurrences of a certain answer.

    return results


print(a_tad_less_exactmatch(3, "Small Battery"))
