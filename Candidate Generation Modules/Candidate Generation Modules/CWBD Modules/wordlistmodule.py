import cwdb

def wordlist_module(length):
    candidates = []
    for c in cwdb.clues :
        if len(c[1]) == length :
            candidates.append((c[1], 0))

    n = len(candidates)
    if n != 0 :
        for c in candidates :
            c[1] = 1/n

    return candidates
