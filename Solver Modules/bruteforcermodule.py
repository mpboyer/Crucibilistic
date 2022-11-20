import main
# Le code suivant n'est pas complet tant que les DICOS ne sont pas prêts
# Calculation of the perfect solution, knowing the answer

def bruteforcer(grid):
    # We only answer the across clues as they should (if the puzzle is well designed) cover the whole grid
    # This program doesn't take into account the clues, since it is technically possible to solve a crossword without.
    # You gotta be lucky tho.
    if grid.Solved:
        return "Solved", grid
    else:
        i = 0
        while i < len(grid.AClues) and grid.AClues[i].Solved:  # O(len(Aclues))
            i += 1
        Words = [
            """List of the words that can go in that spot"""]  # Words of the right length, and of a certain "shape"
        # Usage of SQL will ease this :
        # SELECT word FROM DICO
        # WHERE length = n
        # AND word LIKE "be__t___l"
        # -> beautiful etc...
        # O(1 ?)
        j = 0
        g = grid.copy()  # O(len(Aclues) + len(Dclues) + p * q)
        while not g.AClues[i].Solved:  # O(len(Words))
            g.try_word(Words[j], g.AClues[i].values[0], g.AClues[i].values[1], "across")
            j += 1
        bruteforcer(g)


# O(len(Aclues)*len(dictionnaire))
# len(dictionnaire) is ginormous.
# Thus, we have a new solution to ensure a best average time complexity :
# We will calculate the smallest Levenshtein Distance between known definitions of a possible word and the clue we are
# solving for.

def levenshtein(c1, c2):
    if min(len(c1), len(c2)) == 0:
        return max(len(c1), len(c2))
    elif c1[0] == c2[0]:
        return levenshtein(c1[1:], c2[1:])

    else:
        return 1+min(levenshtein(c1[1:], c2[1:]), levenshtein(c1, c2[1:]), levenshtein(c1[1:], c2))


def defsort(l, clue):
    W = []
    for w in l:
        lev_w = min([levenshtein(clue, w[i]) for i in range(1, len(w))])
        W.append((w[0], lev_w))

    W.sort(key = lambda tup: tup[1], reverse = True)

    return W


def knowledgeable_bruteforcer(grid):
    if grid.Solved:
        return "Solved", grid
    else:
        i = 0
        while i < len(grid.AClues) and grid.AClues[i].Solved:
            i += 1
        clue = grid.AClues[i]
        Words = [
            """List of the words that can go in that spot"""]  # Words of the right length, and of a certain "shape"
        # with their possible definitions
        # Usage of SQL will ease this :
        # SELECT word, def1, def2, ... FROM DICO
        # WHERE length = n
        # AND word LIKE "be__t___l"
        # -> (beautiful, as a butterfly, ...), etc...

        Words = defsort(Words, clue)  # On trie la liste par meilleure distance de Levenshtein d'une définition du mot
        # à l'indice.

        j = 0
        g = grid.copy()
        while not grid.AClues[i].Solved:
            g.try_word(Words[j], g.AClues[i].values[0], g.AClues[i].values[1], "across")
            j += 1
        bruteforcer(g)

# Both of these solutions have TERRIBLE time complexity, and are not even guaranteed to find an answer
# if the crossword contains a previously unmet word

# We will now try to find the 'best' solution using probabilistic methods

