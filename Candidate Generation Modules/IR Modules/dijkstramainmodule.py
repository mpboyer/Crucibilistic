import re
import numpy as np
import heapq


class Vertex :
    def __init__(self, key) :
        """
        :type key: depends on your mood UwU
        """
        self.key = key
        self.neighbours = {}

    def or_add_neighbour(self, neighbour, weight = None):
        self.neighbours[neighbour] = weight

    def un_add_neighbour(self, neighbour, weight = None) :
        """
        :param neighbour: Another vertex that is connected to this one in the graph.
        :type neighbour: Vertex
        :type weight: Technically anything that can be compared
        """
        self.or_add_neighbour(neighbour, weight)
        neighbour.or_add_neighbour(self, weight)

    def get_connections(self) :
        return self.neighbours.keys()

    def degree(self):
        return len(self.neighbours.keys())

    def get_weight(self, neighbour) :
        """
        :type neighbour: Vertex
        """
        return self.neighbours.get(neighbour, None)

    def or_modify_weight(self, neighbour, new_weight):
        self.neighbours[neighbour] = new_weight

    def un_modify_weight(self, neighbour, new_weight) :
        self.neighbours[neighbour] = new_weight
        neighbour.neighbours[self] = new_weight

    def __str__(self) :
        return '{} neighbours : {}'.format(self.key, [x.key for x in self.neighbours])


class Graph :
    def __init__(self) :
        self.vertices = {}

    def add_vertex(self, vertex) :
        if vertex.key in self.vertices :
            return
        self.vertices[vertex.key] = vertex

    def get_vertex(self, key) :
        return self.vertices.get(key, None)

    def __contains__(self, key) :
        return key in self.vertices

    def or_add_edge(self, from_key, to_key, weight = None):
        if not self.__contains__(from_key) :
            self.add_vertex(Vertex(from_key))
        if not self.__contains__(to_key) :
            self.add_vertex(Vertex(to_key))
        self.vertices[from_key].or_add_neighbour(self.vertices[to_key], weight)

    def un_add_edge(self, from_key, to_key, weight = None) :
        if not self.__contains__(from_key) :
            self.add_vertex(Vertex(from_key))
        if not self.__contains__(to_key) :
            self.add_vertex(Vertex(to_key))
        self.vertices[from_key].un_add_neighbour(self.vertices[to_key], weight)

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
    # weight |{occurrences of w in d}|
    Words = Graph()
    # Creation of a not oriented graph linking two words u and v with weight |documents containing both u and v|
    for i in db :
        i = i.lower()
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
    # Words.__str__()
    Final = Graph()
    # Creation of an oriented graph creating the edge (u,v)
    # with weight log(|documents containing u|)-log(|documents in d containing u and v|)
    for u in Words.get_vertices():
        for t in u.neighbours:
            u1, t1 = u.key, t.key
            d_t_u = Words.get_edge(u1, t1)/2
            d_u = len(Omega.get_vertex(u.key).get_connections())
            w_u_t = -np.log(d_t_u / d_u)
            Final.or_add_edge(u1, t1, w_u_t)
    # |documents containing u| is the degree of u in Omega, which is not oriented
    # |documents containing t and u| is the weight of (t,u) in Words, which is not oriented

    """Clues = Graph()
    for u in db:
        u = u.lower()
        Clues.add_vertex(Vertex(u))
        w_u = u.split(" ")[:-1]
               """
    return Omega, Final


def dijkstra(graph : Graph, vertex):
    if graph.get_vertex(vertex) is None :
        return f"{vertex} is not in G"

    priority_queue = []
    distance = {}
    for v in graph.vertices.keys():
        distance[v] = float("inf")

    heapq.heappush(priority_queue, (0, vertex))

    while priority_queue :
        dist, current_vertex = heapq.heappop(priority_queue)
        if distance[current_vertex] == float("inf"):
            distance[current_vertex] = dist
            for neighbour in graph.get_vertex(current_vertex).neighbors :
                next_vertex = neighbour.key
                heapq.heappush(priority_queue, (dist + graph.get_edge(current_vertex, next_vertex), next_vertex))

    return distance


def weight(db : list[str], clue : str, word : str):
    Omega, DB = graph_creator(db)
    terms = clue.split(" ")
    r = 0
    for i in terms :
        distance = dijkstra(DB, i)
        r += -np.log(Omega.get_vertex(i).degree) - distance[word]
    return r


def dijkstra_gen(database : list[str], clue : str):
    Omega, DB = graph_creator(database)
    clue_terms = clue.split(" ")
    nearest_neighbors = {}
    for term in clue_terms :
        term = term.lower()
        nearest_neighbors[term] = dijkstra(DB, term)

    distances = {}
    for w in DB.get_vertices():
        d = 0
        for term in clue_terms :
            term = term.lower()
            d += nearest_neighbors[term][w.key]
        distances[w.key] = d

    res = sorted([(u, distances[u]) for u in distances.keys() if distances[u] != float("inf")], key = lambda t : t[1])
    return res


Go = Graph()
Go.un_add_edge(0, 1, 2.3)
Go.un_add_edge(0, 2, 1.75)
Go.un_add_edge(1, 2, 2.9)
Go.or_add_edge(0, 3, 2.2)
Go.or_add_edge(3, 1, 2.6)


# print(dijkstra(Go, 0))

# base = ["La logique", "Logique", "La France", "France Logique", "France", "La logique France", "France la"]
# u, v = graph_creator(base)
# u.__str__()
# v.__str__()
# print(dijkstra_gen(base, "La logique"))

# Change the way distances between documents are calculated so that two similar documents produce the same
# list of candidates ? Calculate the distance between two documents answers included and calculate the distance
# between the clue without answer and the rest ? Calculate the distance between two clues ?

# Nothing worrying tho, results to be expected according to Keim, Littman, Shazeer

