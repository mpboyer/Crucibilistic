import dijkstramodule as dmm
import setup

cwdb = [c.Clue.lower() + " " + c.Word.lower() for c in setup.CWDB]
print(setup.test_clue.Clue)
res = dmm.dijkstra_gen(cwdb, setup.test_clue.Clue)
input("reafy ?")
print(len(res))
print([i[0] for i in res][:10])

# Works but is a bit off when the clue is not common : exemple : Fan mag graphics. Especially when the answer is not
# in any other clue. Need to rework the weighing and dijkstra functions.

# Results match previously obtained ones, with a bit less efficiency.
