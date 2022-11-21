import cwdb


class Clue:  # Representation of a clue
    def __init__(self, clue, answer):
        self.Clue = clue  # Real Clue
        self.Word = answer  # Solution Word


CWDB = []
for clue in cwdb.clues:
    CWDB.append(Clue(clue[0], clue[1]))

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
        self.Dclues = dclues  # List of the down clues and the tile they start from
        for clue in self.AClues:
            (i, j) = clue[1]
            self.Grid[i][j].AClue = clue[0]

        for clue in self.DClues:
            (i, j) = clue[1]
            self.Grid[i][j].DClue = clue[0]

    def copy(self):
        p, q = self.Size
        aclues = self.AClues
        dclues = self.Dclues

        return Grid.__init__(self, p, q, aclues, dclues)
