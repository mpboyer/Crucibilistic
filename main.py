class Tile:
    def __init__(self, i, j, aclue = None, dclue = None):
        self.value = (i, j) # Position of the tile in the grid
        self.isBlank = True # Initialise as empty
        self.isBlock = False # Is not a black tile at first
        self.char = '' # Is empty
        self.AClue = aclue # Number of the clue going right from this tile : Is None if not the beginning of a
        # word across
        self.DClue = dclue # Same with Down

    def modify(self, blank = False, char = '', block = False):
        self.isBlank = blank
        self.char = char
        self.isBlock = block

class Clue :
    def __init__(self, clue, direction, answer, number, tile):
        self.Clue = clue # Real Clue
        self.Direction = direction # Down or Across
        self.Word = answer # Solution Word
        self.Number = number # Number of the clue
        self.Tile = tile.value() # Position of the beginning of the answer in the grid
        self.Solved = False


a = "across"
d = "down"


class Grid:  # Représentation des Grilles en python par des classes.
    def __init__(self, p, q, aclues, dclues):
        self.Size = (p, q)  # Dimensions of the grid
        self.Grid = [[Tile(i, j) for j in range(p)] for i in range(q)]  # Initialises as empty
        self.AClues = aclues  # List of the across clues
        self.Dclues = dclues  # List of the down clues
        self.Solved = False

    def try_word(self, word, i, j, dir): # Tries to put a word in the grid, starting in [i, j] and going dir.
        if dir == "across": # We assume the grid is solvable
            A = self.Grid[i][j].AClue
            if A.Word == word :
                A.Solved = True
                for c in range(len(word)):
                    self.Grid[i+c][j].modify(char = word[c])

        if dir == "down":
            D = self.Grid[i][j].DClue
            if D.Word == word :
                D.Solved = True
                for c in range(len(word)) :
                    self.Grid[i][j+c].modify(char = word[c])

        self.Solved = True

        for clue in self.AClues :
            self.Solved = self.Solved and clue.Solved
        for clue in self.Dclues :
            self.Solved = self.Solved and clue.Solved


    def copy(self):
        p, q = self.Size
        aclues = self.AClues
        dclues = self.Dclues


        return Grid.__init__(self, p, q, aclues, dclues)
