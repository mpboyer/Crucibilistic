import setup
import candidate_generation_package.dijkstramodule as dijkstra
from candidate_generation_package.exactmatchmodule import exactmatch
from candidate_generation_package.partialmatchmodule import partial_match
from candidate_generation_package.wordlistmodule import wordlist
import candidate_merging_package.simple_mergers as cmp_sm

# Candidate Generation Part :
clue, length = "Express indirectly", 5
# These values are part of a test on The Guardian's quick Crosswords No 16,470 from Sat 18/02
# https://www.theguardian.com/crosswords/quick/16470#19-across

cwdb_wo_words = [c.Clue.lower() for c in setup.CWDB]
cwdb_with_words = [c.Clue.lower() + " " + c.Word.lower() for c in setup.CWDB]
dijkstra_results = dijkstra.dijkstra_gen(cwdb_with_words, clue, length)
exactmatch_results = exactmatch(length, clue)
partialmatch_results = partial_match(cwdb_wo_words, clue, length)
wordlist_results = wordlist(length)

raw_results = [dijkstra_results, exactmatch_results, partialmatch_results, wordlist_results]

full_results = [("dijkstra", dijkstra_results[:10]), ("exact_match", exactmatch_results[:10]),
                ("partial_match", partialmatch_results[:10]), ("word_list", wordlist_results[:10])]

# Candidate Merging Part :
better_results = cmp_sm.better_coeff_merger(raw_results)
arithmetic_mean_results = cmp_sm.arithmetic_mean_coeff_merger(raw_results)
geometric_mean_results = cmp_sm.geometric_mean_coeff_merger(raw_results)
worse_results = cmp_sm.worse_coeff_merger(raw_results)


all_results = [better_results, arithmetic_mean_results, geometric_mean_results, worse_results]
"""presentable_results = {}
for res in all_results:
    for i in range(10):
        candidate_word, weight = res[i]
        prev = presentable_results.get(candidate_word, [])
        next = prev.append((f"{res}", weight))
        presentable_results[candidate_word] = next
"""

presentable_results = [method[:10] for method in all_results]
print(presentable_results)

