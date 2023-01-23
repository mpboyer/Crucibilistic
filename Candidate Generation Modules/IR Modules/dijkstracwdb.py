import main
import dijkstramainmodule as dmm


cwdb = [c.Clue.lower() + " " + c.Word.lower() for c in main.CWDB]
print(main.test_clues[0].Clue)
res = dmm.dijkstra_gen(cwdb, main.test_clues[0].Clue)
print(len(res))
print(main.test_clues[0].Word in [i[0] for i in res])

# Works but is a bit off when the clue is not common : exemple : Fan mag graphics. Especially when the answer is not
# in any other clue. Need to rework the weighing and dijkstra functions.

# Results match previously obtained ones, with a bit less efficiency.

