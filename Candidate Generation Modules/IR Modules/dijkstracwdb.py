import main
import dijkstramainmodule as dmm


cwdb = [c.Clue for c in main.CWDB]
dmm.graph_creator(cwdb).__str__()
