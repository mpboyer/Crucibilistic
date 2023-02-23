import re

a = "across"
d = "down"


class findClue:
    def __init__(self, Clue : str, word_length : int):
        self.Clue = Clue
        self.Length = word_length

    def __str__(self):
        print(self.Clue, self.Length)


class Tile :
    def __init__(self, row, column, aclue = None, dclue = None, block = False) :
        """
        :rtype: Tile
        :type block: bool
        :type dclue: knownClue
        :type aclue: knownClue
        :type column: int
        :type row: int
        """
        self.value = (row, column)  # Position of the tile in the grid
        self.isBlank = True  # Initialise as empty
        self.isBlock = block  # Is not a black tile at first
        self.char = ' '  # Initialises as empty
        self.AClue = aclue  # Clue going right from this tile : Is None if not the beginning of a
        # word across
        self.DClue = dclue  # Same as with across but with down instead

    def modify(self, char = ' ', block = False, aclue = None, dclue = None) :
        """
        :param char: optional : specifies the letter that is placed in the tile. Default is ''. If block is True
        should be false.
        :type char: str
        :param block: optional : specifies if a letter can be placed in the tile. Default is False.
        :type block:
        """
        self.isBlock = self.isBlock or block
        if not self.isBlock :
            self.char = char
            if aclue is not None :
                self.AClue = aclue
            if dclue is not None :
                self.DClue = dclue

    def __str__(self):
        if self.isBlock:
            print("#", end = "")
        else :
            print(self.char, end = "")


class Grid :  # Representation of a grid
    def __init__(self, p, q, aclues_list, dclues_list) :
        """
        :param p: height of the grid
        :type p: int
        :param q: width of the grid
        :type q: int
        :param aclues_list: list of the across clues of the grid and the tile they start from, starting with the clue
        :type aclues_list: list[tuple[findClue, tuple[int, int]]]
        :param dclues_list: list of the down clues of the grid
        :type dclues_list: list[tuple[findClue, tuple[int, int]]]
        """
        self.Size = (p, q)
        self.Grid = [[Tile(i, j) for j in range(q)] for i in range(p)]  # Initialises as empty
        self.AClues = {}
        self.DClues = {}

        for c in aclues_list:
            self.AClues[c[0]] = c[1]

        for c in dclues_list:
            self.DClues[c[0]] = c[1]

        for c in self.AClues :
            (i, j) = self.AClues[c]
            self.Grid[i][j].modify(aclue = c)

        for c in self.DClues :
            (i, j) = self.DClues[c]
            self.Grid[i][j].modify(dclue = c)

    def copy(self) :
        p, q = self.Size
        aclues_list = [(c, self.AClues[c]) for c in self.AClues]
        dclues_list = [(c, self.DClues[c]) for c in self.DClues]

        return Grid.__init__(self, p, q, aclues_list, dclues_list)

    def __str__(self, clues = True) :
        print(self.Size)
        if clues :
            print("Across Clues :")
            for c in self.AClues:
                c.__str__()

            print("Down Clues :")
            for c in self.DClues:
                c.__str__()

        p,q = self.Size
        for i in range(p):
            print("|", end = "")
            for j in range(q):
                tile = self.Grid[i][j]
                tile.__str__()
                if j != q - 1:
                    print("|", end = "")
                else :
                    print("|", end = "\n")


with open("grid.txt", "r") as f :
    auqlue = f.readlines()
    l1 = auqlue[0]
    l1 = re.sub("\n", "", l1)
    l1 = l1.split("  ")
    alen = int(l1[0])
    dlen = int(l1[1])
    raw_aclues = auqlue[1 : 1 + alen]
    raw_dclues = auqlue[1 + alen : 1 + alen + dlen]

    aclues = []
    for a_clue in raw_aclues :
        a_clue = a_clue.split("  ")
        a_clue[-1] = re.sub("\n", "", a_clue[-1])
        clue, length = a_clue[0], int(a_clue[1])
        coords = (int(a_clue[2]), int(a_clue[3]))
        aclues.append((findClue(clue, length), coords))

    dclues = []
    for d_clue in raw_dclues :
        d_clue = d_clue.split("  ")
        d_clue[-1] = re.sub("\n", "", d_clue[-1])
        clue, length = d_clue[0], int(d_clue[1])
        coords = (int(a_clue[2]), int(a_clue[3]))
        dclues.append((findClue(clue, length), coords))

    lines = auqlue[1 + alen + dlen :]
    lines = [re.sub("\n", "", line) for line in lines]
    grid = Grid(len(lines), len(lines[0]), aclues_list = aclues, dclues_list = dclues)

    for i in range(len(lines)) :
        for j in range(len(lines[0])) :
            if lines[i][j] == '#' :
                grid.Grid[i][j].modify(block = True)

