import cwdb

def compatible(word, target):
    r = True
    i= 0
    while r == True and i < len(target):
        r = target[i] == word[i]
        i+=1
    return r


def exactmatch(length, clue):
    candidates = []
    for c in cwdb.clues :
        if c[0]== clue and len(c[1]) == length :
            candidates.append(c[1])

    def weight(c):
        # TODO : Add a weighing function to rate the candidates. Should be almost 1, geometric estimation ?
        return

    for i in range(len(candidates)):
        weight(candidates[i])


