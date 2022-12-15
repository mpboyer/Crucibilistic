import main
import dico


def wordlist_module(length: int) -> list[tuple[str, float]]:
    """
    :param length: length of the word we solve for
    :type length: int
    :return: uniformly weighted list of all the words in the databases of the right length
    :rtype: list[str, float]
    """
    candidates = []

    for c in main.CWDB:  # Adds candidates based on the cwdb
        if len(c.Word) == length:
            candidates.append(c.Word)

    for word in dico.words:  # Adds candidates based on the dictionary
        if len(word) == length:
            candidates.append(word)

    n = len(candidates)
    results = []
    if n != 0:
        for c in candidates:
            results.append((c, 1 / n))  # Gives each candidate a weight based on the number of candidates.

    # results = sorted(results, key = lambda t : t[1])
    # This line has been commented since it wouldn't do anything here.
    # It will remain in the code as it will be in each candidate generation module.

    return results


# print(wordlist_module(3)[:50])
