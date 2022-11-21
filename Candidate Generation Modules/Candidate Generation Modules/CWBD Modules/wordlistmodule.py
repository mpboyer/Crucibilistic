import main
import dico


def wordlist_module(length):
    """Given the length of a word, returns all possible words in the database of adequate length, without caring
    about the clues """
    candidates = []

    for c in main.CWDB:  # Adds candidates based on the cwdb
        if len(c.Word) == length:
            candidates.append((c.Word, 0))

    for word in dico.words:  # Adds candidates based on the dictionary
        if len(word) == length:
            candidates.append((word, 0))

    n = len(candidates)
    if n != 0:
        for c in candidates:
            c[1] = 1 / n  # Gives each candidate a weight based on the number of candidates.

    return candidates
