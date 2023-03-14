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
gridname = "grid_14_03_2023_MiniNYT"
directions = {'a' : 'across', 'd' : 'down'}


def sort_add(list, e) :
    if not list :
        return [e]
    else :
        i = 0
        while i < len(list) :
            if e < list[i] :
                i += 1
            else :
                return list[:i - 1] + [e] + list[i - 1 :]
        return list + [e]


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
    global directory
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

    candidate_grids = []
    cur_grids = [Grid]
    p, q = Grid.Size
    range_size = k
    global save_dir
    save_dir = os.path.join(directory, "solved_candidate_grids")
    try :
        os.mkdir(save_dir)
        print("Directory Created \n")
    except OSError :
        pass

    for row in range(p) :
        for column in range(q) :
            for wae in directions.keys() :
                save_string_clues = f"{directory}" + r"\all" + f"_results_{row}_{column}_{wae}.txt"
                save_string_grids = f"{save_dir}" + r"\candidate" + f"_grids_{row}_{column}_{wae}.txt"
                if os.path.isfile(save_string_grids) :
                    with open(save_string_grids, "rb") as f :
                        next_grids = dill.load(f)
                    print(f"Grids Loaded for {row} {column} {wae}")
                else :
                    next_grids = []
                    print(f"{row} {column} {wae} \t {len(cur_grids)}")
                    boolean = (not Grid.Grid[row][column].AClue is None) if wae == 'a' else (
                        not Grid.Grid[row][column].DClue is None)
                    print(boolean)
                    if boolean :
                        with open(save_string_clues, "rb") as f :
                            results = dill.load(f)
                            print("Loaded")
                        method = results[0]
                        print(len(method))
                        for g in cur_grids :
                            # for method in results :
                            for essai in range(range_size) :
                                word, weight = method[essai]

                                r = g.fill_word(word, weight, directions[wae], row, column)
                                if type(r) != bool :
                                    if r.isSolved() :
                                        candidate_grids.append(r)
                                    else :
                                        next_grids.append(r)

                    next_grids.sort()
                    next_grids = next_grids[:100]

                    with open(save_string_grids, "wb") as f :
                        if next_grids :
                            dill.dump(next_grids, f)
                            print("Dumped new Grids")
                        else :
                            dill.dump(cur_grids, f)
                            print("Dumped No Changes")

                cur_grids = next_grids if next_grids else cur_grids
                cur_grids.sort(reverse = True)
                print("Done \n")

    candidate_grids.sort(reverse = True)

    with open(f"{save_dir}" + r"\solved_candidate_grids.txt", "wb") as f :
        dill.dump(candidate_grids, f)

    return candidate_grids


print([c.Weight for c in grid_solver(grid_18_02_2023_Guardian, gridname, 1000)])

"""
with open(f"{save_dir}" + r"\solved_candidate_grids.txt", "rb") as f :
    candidate_grids = dill.load(f)
    for i in range(10):
        print(candidate_grids[i].__str__(clues = False))
"""
