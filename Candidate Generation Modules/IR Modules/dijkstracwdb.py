import main
import dijkstramainmodule as dmm


cwdb = [c.Clue for c in main.CWDB]
print(dmm.graph_creator(cwdb))
