import random
import re


class knownClue:  # Representation of a clue
    def __init__(self, clue: str, answer: str):
        self.Clue = clue  # Real Clue
        self.Word = answer  # Solution Word


def ramette(c: knownClue) -> tuple[int, str]:
    return len(c.Word), c.Word


def list_creator_obsolete():
    """
    :return: lists containing all the clues in the CWDB and all the words in the CWDB and a dictionary as well as a
    list of 10 test clues
    :rtype: tuple[list[knownClue], dict[str, int]]
    """
    # Generation of a list of all clues with their answers in CWDB
    database: list[knownClue] = []

    with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\cwdb.txt', encoding = "utf-8") as f:
        lines = f.readlines()

    clues: list[tuple[str, str]] = []
    for line in lines:
        l_ = line.split("\t")
        clues.append((l_[2], l_[3]))

    for clue in clues:
        if "crosswordgiant" not in clue[0] and "crosswordgiant" not in clue[1]:
            database.append(knownClue(clue[0], clue[1]))
    database.sort(key = ramette)
    # CWDB_ = [(CWDB[i].Clue, CWDB[i].Word) for i in range(len(CWDB))]  # For presentation purpose

    # Generation of a list of all words in the dictionary and/or CWBD clues and answers
    with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\dictionnaire.txt', encoding = "utf-8") as f:
        lines_1 = f.readlines()

    allwords: dict[str, int] = {}  # Dictionary containing words and their number of occurrences in the CWDB

    for word in lines_1:
        word = re.sub(r"\n", '', word)
        allwords[word] = allwords.get(word, 0) + 1

    with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\cwdb.txt', encoding = "utf-8") as f:
        lines_2 = f.readlines()

    for line in lines_2:
        li = line.split("\t")
        allwords[li[3]] = 1
        li2 = li[2].split(" ")
        for w in li2:
            allwords[w] = allwords.get(w, 0) + 1

    test_set: list[knownClue] = []
    for i in range(10):
        n = len(database)
        test_set.append(database.pop(random.randint(0, n-1)))

    return database, allwords, test_set


# CWDB, words, test_clues = list_creator_obsolete()


def setup_main():
    with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\cwdb.txt', encoding = "utf-8") as f :
        CWDB_raw = f.readlines()

    all_words = {}
    CWDB_dict = {}
    CWDB_clue_list = []
    for line in CWDB_raw :
        line_ = (line.lower())
        line_ = re.sub('[^\w\s:À-ÿ&"]', '', line_)
        line_ = line_.split()

        CWDB_dict[line_[2]] = line_[3]
        CWDB_clue_list.append(knownClue(line_[2], line_[3]))
        for word in line_[2].split(" ") :
            all_words[word] = all_words.get(word, 0) + 1
        all_words[line_[3]] = all_words.get(line_[3], 0) + 1

    with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\dictionnaire.txt', encoding = "utf-8") as f:
        dictionary_raw = f.readlines()

    for word in dictionary_raw :
        word = re.sub(r"\n", '', word)
        all_words[word] = all_words.get(word, 0) + 1

    return CWDB_dict, CWDB_clue_list, all_words


clue_table, CWDB, words = setup_main()

# print(clue_table.__str__())
# print('inits.' in clue_table)




