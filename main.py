import re


class Clue:  # Representation of a clue
    def __init__(self, clue, answer):
        self.Clue = clue  # Real Clue
        self.Word = answer  # Solution Word


def ramette(c):
    return len(c.Word), c.Word


# Generation of a list of all clues with their answers in CWDB
CWDB = []
with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\cwdb.txt', encoding = "utf-8") as f:
    lines = f.readlines()
clues = []
for line in lines:
    l = line.split("\t")
    clues.append((l[2], l[3]))
for clue in clues:
    if not "crosswordgiant" in clue[0] and not "crosswordgiant" in clue[1]:
        CWDB.append(Clue(clue[0], clue[1]))
CWDB.sort(key = ramette)
CWDB_ = [(CWDB[i].Clue, CWDB[i].Word) for i in range(len(CWDB))]


# Generation of a list of all words in the dictionary and/or CWBD clues and answers
with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\dictionnaire.txt', encoding = "utf-8") as f :
    lines_1 = f.readlines()

words = {}

for word in lines_1:
    word = re.sub(r"\n", '', word)
    words[word] = 1

with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\cwdb.txt', encoding = "utf-8") as f :
    lines_2 = f.readlines()

for line in lines_2:
    li = line.split("\t")
    words[li[3]] = 1
    li2 = li[2].split(" ")
    for w in li2:
        words[w] = 1


a = "across"
d = "down"


class Tile:
    def __init__(self, i, j, aclue = None, dclue = None, block = False):
        self.value = (i, j)  # Position of the tile in the grid
        self.isBlank = True  # Initialise as empty
        self.isBlock = block  # Is not a black tile at first
        self.char = ''  # Initialises as empty
        self.AClue = aclue  # Clue going right from this tile : Is None if not the beginning of a
        # word across
        self.DClue = dclue  # Same as with across but with down instead

    def modify(self, blank = False, char = '', block = False):
        self.isBlank = blank
        self.char = char
        self.isBlock = block


class Grid:  # Representation of a grid
    def __init__(self, p, q, aclues, dclues):
        self.Size = (p, q)  # Dimensions of the grid, usually p = q
        self.Grid = [[Tile(i, j) for j in range(p)] for i in range(q)]  # Initialises as empty
        self.AClues = aclues  # List of tuples of the across clues and the tile they start from. First one is the clue.
        self.DClues = dclues  # List of the down clues and the tile they start from

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
