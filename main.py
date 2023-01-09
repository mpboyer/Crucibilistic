import re
import random


class Clue:  # Representation of a clue
    def __init__(self, clue: str, answer: str):
        self.Clue = clue  # Real Clue
        self.Word = answer  # Solution Word


def ramette(c: Clue) -> tuple[int, str]:
    return len(c.Word), c.Word


def list_creator():
    """
    :return: lists containing all the clues in the CWDB and all the words in the CWDB and a dictionary as well as a
    list of 10 test clues
    :rtype: tuple[list[Clue], dict[str, int]]
    """
    # Generation of a list of all clues with their answers in CWDB
    database: list[Clue] = []

    with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\cwdb.txt', encoding = "utf-8") as f:
        lines = f.readlines()

    clues: list[tuple[str, str]] = []
    for line in lines:
        l_ = line.split("\t")
        clues.append((l_[2], l_[3]))

    for clue in clues:
        if "crosswordgiant" not in clue[0] and "crosswordgiant" not in clue[1]:
            database.append(Clue(clue[0], clue[1]))
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

    test_set: list[Clue] = []
    for i in range(10):
        n = len(database)
        test_set.append(database.pop(random.randint(0, n-1)))

    return database, allwords, test_set


CWDB, words, test_clues = list_creator()

a = "across"
d = "down"


class Tile:
    def __init__(self, i, j, aclue = None, dclue = None, block = False):
        """
        :rtype: Tile
        :type block: bool
        :type dclue: Clue
        :type aclue: Clue
        :type j: int
        :type i: int
        """
        self.value = (i, j)  # Position of the tile in the grid
        self.isBlank = True  # Initialise as empty
        self.isBlock = block  # Is not a black tile at first
        self.char = ''  # Initialises as empty
        self.AClue = aclue  # Clue going right from this tile : Is None if not the beginning of a
        # word across
        self.DClue = dclue  # Same as with across but with down instead

    def modify(self, char = '', block = False):
        """
        :param char: optional : specifies the letter that is placed in the tile. Default is ''. If block is True
        should be false.
        :type char: str
        :param block: optional : specifies if a letter can be placed in the tile. Default is False.
        :type block:
        """
        self.isBlock = self.isBlock or block
        if not self.isBlock:
            self.char = char


class Grid:  # Representation of a grid
    def __init__(self, p, q, aclues, dclues):
        """
        :param p: height of the grid
        :type p: int
        :param q: width of the grid
        :type q: int
        :param aclues: list of the across clues of the grid and the tile they start from, starting with the clue
        :type aclues: list[tuple[Clue, int]]
        :param dclues: list of the down clues of the grid
        :type dclues: list[tuple[Clue, int]]
        """
        self.Size = (p, q)
        self.Grid = [[Tile(i, j) for j in range(q)] for i in range(p)]  # Initialises as empty
        self.AClues = aclues
        self.DClues = dclues

        for clue in self.AClues:
            (i, j) = clue[1]
            self.Grid[i][j].AClue = clue[0]

        for clue in self.DClues:
            (i, j) = clue[1]
            self.Grid[i][j].DClue = clue[0]

    def copy(self):
        p, q = self.Size
        aclues = self.AClues
        dclues = self.DClues

        return Grid.__init__(self, p, q, aclues, dclues)
