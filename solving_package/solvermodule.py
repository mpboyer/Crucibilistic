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
directions = {'a' : 'across', 'd' : 'down'}


def clue_solver(Grid, i: int, j: int, save_path: str, direction = "a") :
    """
    :param save_path:
    :type save_path: str
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

    save_string = f"{save_path}" + r"\all" + f"_results_{i}_{j}_{direction}.txt"
    with open(save_string, "wb") as f :
        dill.dump(all_results, file = f)


def all_clue_solver(Grid, save_directory) :
    directory = os.path.join(f"{save_directory}")
    print(directory)
    created = False
    i = 0
    path_ = directory
    while not created :
        path_ = directory + f"({i})" if i != 0 else directory
        try :
            os.mkdir(path_)
            created = True
        except OSError :
            created = True
            pass
            """i += 1"""

    global directory
    directory = path_

    p, q = Grid.Size
    for row in range(p) :
        for column in range(q) :
            if Grid.Grid[row][column].AClue and not os.path.isfile(
                    f"{directory}" + r"\all" + f"_results_{row}_{column}_{'a'}.txt") :
                print(row, column, "a")
                clue_solver(Grid, row, column, directory, "a")
            if Grid.Grid[row][column].DClue and not os.path.isfile(
                    f"{directory}" + r"\all" + f"_results_{row}_{column}_{'d'}.txt") :
                print(row, column, "d")
                clue_solver(Grid, row, column, directory, "d")


def grid_solver(Grid, save_directory, k) :
    all_clue_solver(Grid, save_directory)
    # The previous all_clue_solver is created for debug (and spltting runtime)
    # purposes only, in reality it will not be run apart from this call this function

    candidate_grids = set()
    cur_grids = set(Grid)
    p, q = Grid.Size
    range_size = k
    for row in range(p) :
        for column in range(q) :
            for wae in directions.keys() :
                save_string = f"{directory}" + r"\all" + f"_results_{row}_{column}_{wae}.txt"
                next_grids = set()
                boolean = Grid.Grid[row][column].AClue if wae == 'a' else Grid.Grid[row][column].DClue
                if boolean :
                    with open(save_string, "rb") as f :
                        results = dill.load(f)

                    for g in cur_grids :
                        for method in results :
                            for essai in range(range_size) :
                                r = g.fill_word(method[essai], directions[wae], row, column)
                                if type(r) != bool and r not in next_grids :
                                    if not r.isSolved :
                                        next_grids.add(r)
                                    else :
                                        candidate_grids.add(r)
                    cur_grids = next_grids
    return candidate_grids
