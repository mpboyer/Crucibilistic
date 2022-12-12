import re
import numpy as np


def words(db):
    w = {}
    for i in db:
        c = i.split(" ")
        c[-1] = re.sub("\n", "", c[-1])  # If the string still has its newline operator, deletes it.
        for j in c:
            if j in w:
                w[j][0] += 1
                w[j][1].append(c)
            else:
                w[j] = [1, [c]]
    return w


def graph_creator(db):
    n_db = len(db)
    w = words(db)
    n_w = len(w)
    graph = {}
    for t in w:  # Checks all words t in the db
        graph[t] = {}
        d_t = w[t][0]
        for j in w[t][1]:  # For each document containing the word t
            for u in j:  # Checks all words u in those documents
                d_ut = 0
                for j_ in w[u][1]:
                    if j_ in w[t][1]:  # Computes all the documents containing both u and t
                        d_ut += 1
                # Adds an edge with weight -log(#docs containing u and t/#docs containing t) to the graph
                graph[t][u] = -np.log(d_ut/d_t)
    return graph, n_db, n_w


