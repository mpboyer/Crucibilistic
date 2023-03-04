import os

import dill

import candidate_generation_package.dijkstramodule as dijkstra
import candidate_merging_package.simple_mergers as cmp_sm
import initializermodule
import setup
from candidate_generation_package.exactmatchmodule import exactmatch
from candidate_generation_package.partialmatchmodule import partial_match
from candidate_generation_package.wordlistmodule import wordlist

grid_18_02_2023_Guardian = initializermodule.grid
gridname = "grid_18_02_2023_Guardian"


def clue_solver(Grid, i: int, j: int, path: str, direction = "a") :
    """
    :param path:
    :type path: str
    :param Grid: the grid in which the clue solved for is
    :type Grid: Grid
    :param i: Row Number
    :type i: int
    :param j: Column Number
    :type j: int
    :param direction: Direction of the clue, "a" for across, "d" for down
    :type direction: str
    """
    if direction == "a" :
        Clue = Grid.Grid[i][j].AClue
    else :
        Clue = Grid.Grid[i][j].DClue

    clue, length = Clue.Clue, Clue.Length
    cwdb_wo_words = [c.Clue.lower() for c in setup.CWDB]
    cwdb_with_words = [c.Clue.lower() + " " + c.Word.lower() for c in setup.CWDB]
    dijkstra_cwdb_results = dijkstra.dijkstra_gen(cwdb_with_words, clue, length)
    exactmatch_results = exactmatch(length, clue)
    partialmatch_results = partial_match(cwdb_wo_words, clue, length)
    wordlist_results = wordlist(length)

    raw_results = [dijkstra_cwdb_results, exactmatch_results, partialmatch_results, wordlist_results]
    all_results = [f(raw_results) for f in cmp_sm.all_simple_mergers]

    save_string = f"{path}" + r"\all" + f"_results_{i}_{j}_{direction}.txt"
    with open(save_string, "wb") as f :
        dill.dump(all_results, file = f)


def all_clue_solver(Grid, save_directory) :
    path = os.path.join(f"{save_directory}")
    print(path)
    created = False
    i = 0
    path_ = path
    while not created :
        path_ = path + f"({i})" if i != 0 else path
        try :
            os.mkdir(path_)
            created = True
        except OSError :
            created = True
            pass
            """i += 1"""

    path = path_

    p, q = Grid.Size
    for row in range(p) :
        for column in range(q) :
            if Grid.Grid[row][column].AClue and not os.path.isfile(
                    f"{path}" + r"\all" + f"_results_{row}_{column}_{'a'}.txt"):
                print(row, column, "a")
                clue_solver(Grid, row, column, path, "a")
            if Grid.Grid[row][column].DClue and not os.path.isfile(
                    f"{path}" + r"\all" + f"_results_{row}_{column}_{'d'}.txt") :
                print(row, column, "d")
                clue_solver(Grid, row, column, path, "d")


all_clue_solver(grid_18_02_2023_Guardian, gridname)


def grid_solver(Grid, save_directory) :
    all_clue_solver(Grid, save_directory)  # The previous all_clue_solver is created for debug (and spltting runtime)
    # purposes only, in reality it will not be run apart from this call this function

    # anyways, I started blasting. This won't be pretty : SAY HELLO TO MY LITTLE FRIEND
    candidate_grids = []
    p, q = Grid.Size
