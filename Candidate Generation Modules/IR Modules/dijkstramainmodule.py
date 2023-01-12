import re
import numpy as np
from collections import deque


class Vertex :
    def __init__(self, key) :
        """
        :type key: depends on your mood UwU
        """
        self.key = key
        self.neighbors = {}

    def or_add_neighbor(self, neighbor, weight = None):
        self.neighbors[neighbor] = weight

    def un_add_neighbor(self, neighbor, weight = None) :
        """
        :param neighbor: Another vertex that is connected to this one in the graph.
        :type neighbor: Vertex
        :type weight: Technically anything that can be compared
        """
        self.or_add_neighbor(neighbor, weight)
        neighbor.or_add_neighbor(self, weight)

    def get_connections(self) :
        return self.neighbors.keys()

    def degree(self):
        return len(self.neighbors.keys())

    def get_weight(self, neighbor) :
        """
        :type neighbor: Vertex
        """
        return self.neighbors.get(neighbor, None)

    def or_modify_weight(self, neighbor, new_weight):
        self.neighbors[neighbor] = new_weight

    def un_modify_weight(self, neighbor, new_weight) :
        self.neighbors[neighbor] = new_weight
        neighbor.neighbors[self] = new_weight

    def __str__(self) :
        return '{} neighbors : {}'.format(self.key, [x.key for x in self.neighbors])


class Graph :
    def __init__(self) :
        self.vertices = {}

    def add_vertex(self, vertex) :
        if vertex.key in self.vertices :
            return
        self.vertices[vertex.key] = vertex

    def get_vertex(self, vertex) :
        return self.vertices.get(vertex.key, None)

    def __contains__(self, key) :
        return key in self.vertices

    def or_add_edge(self, from_key, to_key, weight = None):
        if not self.__contains__(from_key) :
            self.add_vertex(Vertex(from_key))
        if not self.__contains__(to_key) :
            self.add_vertex(Vertex(to_key))
        self.vertices[from_key].or_add_neighbor(self.vertices[to_key], weight)

    def un_add_edge(self, from_key, to_key, weight = None) :
        if not self.__contains__(from_key) :
            self.add_vertex(Vertex(from_key))
        if not self.__contains__(to_key) :
            self.add_vertex(Vertex(to_key))
        self.vertices[from_key].un_add_neighbor(self.vertices[to_key], weight)

    def get_edge(self, from_key, to_key) :
        return self.vertices.get(from_key, None).get_weight(self.vertices.get(to_key, None))

    def or_modify_edge(self, from_key, to_key, new_weight) :
        return self.vertices.get(from_key, None).or_modify_weight(self.vertices.get(to_key, None), new_weight)

    def un_modify_edge(self, from_key, to_key, new_weight) :
        return self.vertices.get(from_key, None).un_modify_weight(self.vertices.get(to_key, None), new_weight)

    def get_vertices(self) :
        return [self.vertices[k] for k in self.vertices.keys()]

    def __iter__(self) :
        return iter(self.vertices.values())

    def __str__(self) :
        for u in self :
            for v in u.get_connections() :
                print("{} -> {} : {}".format(u.key, v.key, self.get_edge(u.key, v.key)))


"""
G = Graph()
G.un_add_edge(0, 1, 2.3)
G.un_add_edge(0, 2, 1.75)
G.un_add_edge(1, 2, 2.9)
G.or_add_edge(0, 3, 2.2)
G.or_add_edge(3, 1, 2.6)
G.__str__()"""


def words(db) :
    """
    :param db: Database containing documents
    :type db: list[str]
    :return: Dictionary containing the number of occurences of a word and the documents it appears in.
    :rtype: dict[tuple[int, list[list[str]]]
    """
    w = {}
    for i in db :
        c = i.split(" ")
        c[-1] = re.sub(r"\n", "", c[-1])  # If the string still has its newline operator, deletes it.
        for j in c :
            j_ = j.lower()
            if j_ in w :
                w[j_][0] += 1
                w[j_][1].append(c)
            else :
                w[j_] = [1, [c]]
    return w


def graph_creator(db: list[str]) :
    """
    :param db: Database containing all documents
    :type db: list[str]
    :return: Graph represented by an adjacency dict (type Graph)
    with all the words in db as vertices and weighted edges based on the inverse term frequency distribution as well
    as a graph linking all documents d in the db to all the words w with weight |number of occurences of w in d|
    :rtype: Graph, Graph
    """
    Omega = Graph()
    # Creation of a not oriented graph linking a document d in db to all the words w in it with
    # weight |occurences of w in d|
    Words = Graph()
    # Creation of a not oriented graph linking two words u and v with weight |documents containing both u and v|
    for i in db :
        Omega.add_vertex(Vertex(i))
        w_i = i.split(" ")
        w_i[-1] = re.sub(r"\n", "", w_i[-1])
        for w in w_i :
            x_w = Omega.get_edge(i, w)
            if x_w is None :
                Omega.un_add_edge(i, w, 1)
            else :
                Omega.un_modify_edge(i, w, x_w + 1)
            Words.add_vertex(Vertex(w))
            for j in w_i :
                if j != w :
                    x_w_j = Words.get_edge(w, j)
                    if x_w_j is None :
                        Words.un_add_edge(w, j, 1)
                    else:
                        Words.un_modify_edge(w, j, x_w_j + 1)
    Final = Graph()
    # Creation of an oriented graph creating the edge (u,v)
    # with weight log(|documents containing u|)-log(|documents in d containing u and v|)
    for u in Words.get_vertices():
        for t in u.neighbors:
            u1, t1 = u.key, t.key
            d_t_u = Words.get_edge(u1, t1)
            d_u = len(Omega.get_vertex(u).get_connections())
            w_u_t = -np.log(d_t_u / d_u)
            Final.or_add_edge(u1, t1, w_u_t)
    # |documents containing u| is the degree of u in Omega, which is not oriented
    # |documents containing t and u| is the weight of (t,u) in Words, which is not oriented
    return Omega, Final

# Shit it works


def dijkstra(G : Graph, v):
    if G.get_vertex(v) is None :
        return "v is not in G"

    queue = deque([v])
    distance = {v : 0}
    while queue :
        t = queue.popleft()
        for n in G.get_vertex(t).neighbors:
            queue.append(n.key)
            n_dist = distance[t] + G.get_edge(t, n.key)
            if n not in distance or n_dist < distance[n]:
                distance[n] = n_dist
    return sorted(distance.items(), key = lambda k : k[1])


def weight(db : list[str], c : str, w : str):
    Omega, DB = graph_creator(db)
    terms = c.split(" ")
    r = 0
    for i in terms :
        distance = dijkstra(DB, i)
        r += -np.log(Omega.get_vertex(i).degree) - distance[w]
    return r


def dijkstra_gen(db : list[str], c : str):
    Omega, DB = graph_creator(db)
    terms = c.split(" ")
    nearest_neighbors = {}
    for i in terms :
        nearest_neighbors[i] = dijkstra(DB, i)

    distances = {}
    for w in DB.get_vertices():
        distances[w] = sum([nearest_neighbors[i][w.key] for i in terms])

    res = sorted(distances.items(), key = lambda k : k[1])
    return res

