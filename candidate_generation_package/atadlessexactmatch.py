import numpy as np
import setup
import time


def levenshtein(c1, c2, n = 0):
    """
    :param n: current distance in the recursive calculation. If more than 10, stops. Default : 0
    :type n: int
    :param c1: word 1
    :type c1: str
    :param c2: word 2
    :type c2: str
    :return: Exact Levenshtein distance between word 1 and word 2
    :rtype: int
    """
    # The presence of the parameter n blocks the maximum complexity to a certain value (~30 operations).
    if n > 10:
        return n
    elif c1 == '':
        return len(c2) + n
    elif c2 == '':
        return len(c1) + n
    elif c1[0] == c2[0]:
        return levenshtein(c1[1:], c2[1:], n)
    else:
        return min(levenshtein(c1[1:], c2, n+1), levenshtein(c1, c2[1:], n+1), levenshtein(c1[1:], c2[1:], n+1))


def a_tad_less_exactmatch(length: int, clue: str):
    """
    :param int length: length of the word we solve for
    :param str clue: clue we solve for
    :return: weighted list of words that could answer the clue
    :rtype: list[str, float]
    """
    results = []
    new_york_times = [time.time() / 3600]
    candidates = []
    i = len(setup.CWDB)
    for c in setup.CWDB:
        n = levenshtein(c.Clue, clue)
        i -= 1
        if i % 100 == 0:
            new_york_times.append(time.time() / 3600)
            los_angeles_times = [new_york_times[i+1] - new_york_times[i] for i in range(len(new_york_times) - 1)]
            print(f"{i} candidates left, ETA : {(sum(los_angeles_times)/len(los_angeles_times))* i} hours")
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
                1])))  # Generates a confidence distribution based on the number of occurrences of a certain answer.

    return results


print(a_tad_less_exactmatch(3, "Small Battery"))
