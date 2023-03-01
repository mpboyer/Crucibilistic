import re

a = "across"
d = "down"


class findClue:
    def __init__(self, Clue : str, word_length : int):
        self.Clue = Clue
        self.Length = word_length
        self.isSolved = False

    def __str__(self):
        return f"{self.Clue}, {self.Length}"


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
            if not self.char == ' ' :
                self.char = char
            if aclue is not None :
                self.AClue = aclue
            if dclue is not None :
                self.DClue = dclue
            self.isBlank = self.char == ' '

    def __str__(self):
        if self.isBlock:
            return "#"
        else :
            return self.char


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

    def isSolved(self):
        p, q = self.Size
        for i in range(p):
            for j in range(q):
                if self.Grid[i][j].isBlank :
                    return False
        return True

    def __str__(self, clues = True) :
        grid_string = f"{self.Size} \n"

        p, q = self.Size
        across_str = []
        down_str = []
        for i in range(p) :
            grid_string += "|"
            for j in range(q) :
                tile = self.Grid[i][j]
                grid_string += tile.__str__()
                if tile.AClue is not None:
                    across_str.append((tile.AClue, i, j))
                if tile.DClue is not None:
                    down_str.append((tile.DClue, i, j))
                if j != q - 1 :
                    grid_string += "|"
                else :
                    grid_string += "| \n"

        if clues :
            grid_string += f"Across Clues : \n"
            for c in across_str:
                grid_string += (c[0].__str__() + f", {c[1]}, {c[2]}\n")

            grid_string += f"Down Clues : \n"
            for c in down_str:
                grid_string += (c[0].__str__() + f", {c[1]}, {c[2]}\n")

        return grid_string[:-1]

    def fill_word(self, direction, row, column, word):
        wordLength = len(word)

        if direction == a:
            for k in range(wordLength):
                tile = self.Grid[row][column + k]
                if tile.isBlock:
                    return False
                if not tile.isBlank:
                    if tile.char != word[k]:
                        return False

            grid_copy = self.copy()
            for k in range(wordLength):
                tile = grid_copy.Grid[row][column + k]
                tile.modify(char = word[k])

        else :
            for k in range(wordLength) :
                tile = self.Grid[row + k][column]
                if tile.isBlock :
                    return False
                if not tile.isBlank :
                    if tile.char != word[k] :
                        return False

            grid_copy = self.copy()
            for k in range(wordLength) :
                tile = grid_copy.Grid[row + k][column]
                tile.modify(char = word[k])

        c = grid_copy.Grid[row][column].AClue if direction == "a" else grid_copy.Grid[row][column].DClue
        c.isSolved = True
        return grid_copy


with open(f"grid.txt", "r") as f :
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
        coords = (int(d_clue[2]), int(d_clue[3]))
        dclues.append((findClue(clue, length), coords))

    lines = auqlue[1 + alen + dlen :]
    lines = [re.sub("\n", "", line) for line in lines]
    grid = Grid(len(lines), len(lines[0]), aclues_list = aclues, dclues_list = dclues)

    for i in range(len(lines)) :
        for j in range(len(lines[0])) :
            if lines[i][j] == '#' :
                grid.Grid[i][j].modify(block = True)

print(grid)
