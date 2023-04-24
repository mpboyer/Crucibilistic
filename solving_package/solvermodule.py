import os

import dill

import candidate_generation_package.dijkstramodule as dijkstra
import candidate_merging_package.simple_mergers as cmp_sm
import initializermodule
import setup
from candidate_generation_package.exactmatchmodule import exactmatch
from candidate_generation_package.partialmatchmodule import partial_match
from candidate_generation_package.wordlistmodule import wordlist

grid = initializermodule.grid
directions = {'a' : 'across', 'd' : 'down'}
clue_dir = os.path.join(initializermodule.directory, "clue_solver_results")
grid_dir = os.path.join(initializermodule.directory, "solved_candidate_grids")


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


def all_clue_solver(Grid) :
	print(initializermodule.directory)
	try :
		os.mkdir(initializermodule.directory)
		print("General Directory Created")
	except OSError :
		pass

	try :
		os.mkdir(clue_dir)
		print("Clue Directory Created")
	except OSError :
		pass

	p, q = Grid.Size
	for row in range(p) :
		for column in range(q) :
			if Grid.Grid[row][column].AClue :
				if not os.path.isfile(f"{clue_dir}" + r"\all" + f"_results_{row}_{column}_{'a'}.txt") :
					print(f"Solving for Clue : {row} {column} a")
					clue_solver(Grid, row, column, clue_dir, "a")
				else :
					print(f"Clue {row} {column} a already solved")

			if Grid.Grid[row][column].DClue :
				if not os.path.isfile(f"{clue_dir}" + r"\all" + f"_results_{row}_{column}_{'d'}.txt") :
					print(f"Solving for Clue : {row} {column} d")
					clue_solver(Grid, row, column, clue_dir, "d")
				else :
					print(f"Clue {row} {column} d already solved")


def grid_solver(Grid) :
	all_clue_solver(Grid)
	# The previous all_clue_solver is created for debug (and splitting runtime)
	# purposes only, in reality it will not be run apart from this call this function

	candidate_grids = []
	cur_grids = [Grid]
	p, q = Grid.Size
	try :
		os.mkdir(grid_dir)
		print("Directory Created \n")
	except OSError :
		pass

	for row in range(p) :
		for column in range(q) :
			for wae in directions.keys() :
				boolean = False
				save_string_clues = f"{clue_dir}" + r"\all" + f"_results_{row}_{column}_{wae}.txt"
				save_string_grids = f"{grid_dir}" + r"\candidate" + f"_grids_{row}_{column}_{wae}.txt"
				if os.path.isfile(save_string_grids) :
					with open(save_string_grids, "rb") as f :
						next_grids = dill.load(f)
					print(f"Grids Loaded for {row} {column} {directions[wae]}")
				else :

					next_grids = []
					print(f"{row} {column} {directions[wae]}\nCurrent Number of Candidate Grids : {len(cur_grids)}")
					boolean = (not Grid.Grid[row][column].AClue is None) if wae == 'a' else (
						not Grid.Grid[row][column].DClue is None)
					print("No Clue To Be Solved" if not boolean else "Beginning Solving")

					if boolean :
						with open(save_string_clues, "rb") as f :
							clue_results = dill.load(f)
							print("Loaded Candidate Words")
						sorting_method = clue_results[0]
						print(f"{len(sorting_method)} answers to study")
						for g in cur_grids :
							# for sorting_method in clue_results :

							for candidate_word in range(min(len(sorting_method), k)) :
								word, weight = sorting_method[candidate_word]
								r = g.fill_word(word, weight, directions[wae], row, column)
								if type(r) != bool :
									if r.isSolved() :
										candidate_grids.append(r)
									elif not r.Weight == 0 :
										next_grids.append(r)

					next_grids.sort()
					next_grids = next_grids

					if boolean :
						with open(save_string_grids, "wb") as f :
							if next_grids :
								dill.dump(next_grids, f)
								print("Dumped new Grids")
							else :
								dill.dump(next_grids, f)
								print("No Solutions")
					else :
						print("Dumped No Changes")

				cur_grids = next_grids if next_grids else cur_grids
				cur_grids.sort(reverse = True)
				print("Done and Sorted \n")

	candidate_grids.sort(reverse = True)

	with open(f"{grid_dir}" + r"\solved_candidate_grids.txt", "wb") as f :
		dill.dump(candidate_grids, f)

	return candidate_grids


with open(f"{clue_dir}" + r"\all_results_0_0_a.txt", "rb") as f :
	c_results = (dill.load(f))[0]

# print(c_results[:100])

grid_solver(grid)  # with open(f"{grid_dir}" + r"\solved_candidate_grids.txt", "rb") as f :
#    candidate_grids = dill.load(f)

# print(len(candidate_grids))
