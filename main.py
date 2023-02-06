import setup
import candidate_generation_package.dijkstramodule as dijkstra
from candidate_generation_package.exactmatchmodule import exactmatch
from candidate_generation_package.partialmatchmodule import partial_match
from candidate_generation_package.wordlistmodule import wordlist

# Candidate Generation Part :

clue, length = setup.test_clue.Clue, len(setup.test_clue.Clue)

cwdb_wo_words = [c.Clue.lower() for c in setup.CWDB]
cwdb_with_words = [c.Clue.lower() + " " + c.Word.lower() for c in setup.CWDB]
dijkstra_results = dijkstra.dijkstra_gen(cwdb_with_words, clue)
exactmatch_results = exactmatch(length, clue)
partialmatch_results = partial_match(cwdb_wo_words, clue)
wordlist_results = wordlist(length)

full_results = [("dijkstra", dijkstra_results[:10]),
                ("exact_match", exactmatch_results[:10]),
                ("partial_match", partialmatch_results[:10]),
                ("word_list", wordlist_results[:10])]

print(full_results)

