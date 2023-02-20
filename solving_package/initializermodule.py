a = "across"
d = "down"


class findClue:
    def __init__(self, Clue : str, length : int):
        self.Clue = Clue
        self.Length = length


class Tile :
    def __init__(self, i, j, aclue = None, dclue = None, block = False) :
        """
        :rtype: Tile
        :type block: bool
        :type dclue: knownClue
        :type aclue: knownClue
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

    def modify(self, char = '', block = False) :
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


class Grid :  # Representation of a grid
    def __init__(self, p, q, aclues, dclues) :
        """
        :param p: height of the grid
        :type p: int
        :param q: width of the grid
        :type q: int
        :param aclues: list of the across clues of the grid and the tile they start from, starting with the clue
        :type aclues: list[tuple[knownClue, tuple[int, int]]]
        :param dclues: list of the down clues of the grid
        :type dclues: list[tuple[knownClue, tuple[int, int]]]
        """
        self.Size = (p, q)
        self.Grid = [[Tile(i, j) for j in range(q)] for i in range(p)]  # Initialises as empty
        self.AClues = aclues
        self.DClues = dclues

        for clue in self.AClues :
            (i, j) = clue[1]
            self.Grid[i][j].AClue = clue[0]

        for clue in self.DClues :
            (i, j) = clue[1]
            self.Grid[i][j].DClue = clue[0]

    def copy(self) :
        p, q = self.Size
        aclues = [c for c in self.AClues]
        dclues = [c for c in self.DClues]

        return Grid.__init__(self, p, q, aclues, dclues)


with open("grid.txt", "r") as f :
    AnswertotheUltimateQuestionofLifetheUniverseandEverything = f.readlines()
    alen, dlen = AnswertotheUltimateQuestionofLifetheUniverseandEverything[0].split("\t")[0], \
                 AnswertotheUltimateQuestionofLifetheUniverseandEverything[0].split("\t")[1]
    raw_aclues = AnswertotheUltimateQuestionofLifetheUniverseandEverything[1 : 1 + alen]
    raw_dclues = AnswertotheUltimateQuestionofLifetheUniverseandEverything[1 + alen : 1 + alen + dlen]

    aclues = []
    for a_clue in raw_aclues :
        a_clue = a_clue.split("\t")
        clue, length = a_clue[0], a_clue[1]
        coords = (int(a_clue[2]), int(a_clue[3]))
        aclues.append((clue, coords))

    dclues = []
    for d_clue in raw_dclues :
        d_clue = d_clue.split("\t")
        clue, length = d_clue[0], d_clue[1]
        coords = (int(a_clue[2]), int(a_clue[3]))
        dclues.append((findClue(clue, length), coords))

    lines = AnswertotheUltimateQuestionofLifetheUniverseandEverything[1 + alen + dlen :]
    grid = Grid(len(lines), len(lines[0]), aclues = aclues, dclues = dclues)

    for i in range(len(lines)) :
        for j in range(len(lines[0])) :
            if lines[i][j] == '#' :
                grid.Grid[i][j].modify(block = True)
