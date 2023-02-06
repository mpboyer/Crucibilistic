import setup
import dijkstramodule as dmm


cwdb = [c.Clue.lower() + " " + c.Word.lower() for c in setup.CWDB]
print(setup.test_clue.Clue)
res = dmm.dijkstra_gen(cwdb, setup.test_clue.Clue)
print(len(res))
print(setup.test_clue.Word in [i[0] for i in res])

# Works but is a bit off when the clue is not common : exemple : Fan mag graphics. Especially when the answer is not
# in any other clue. Need to rework the weighing and dijkstra functions.

# Results match previously obtained ones, with a bit less efficiency.

