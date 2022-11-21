import main


def exactmatch(length, clue):
    """Given"""
    candidates = []
    for c in main.CWDB :
        if c.Clue == clue and len(c.Word) == length :
            candidates.append(c.Word)

    def weight(c):
        # TODO : Add a weighing function to rate the candidates. Should be almost 1, geometric estimation ?
        return

    for i in range(len(candidates)):
        weight(candidates[i])


