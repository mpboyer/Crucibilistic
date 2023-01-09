import re
import numpy as np


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


def graph_creator1(db) :
    """
    :param db: Database containing all documents
    :type db: list[str]
    :return: Graph represented by an adjacency dict
    with all the words in db as vertices and weighted edges based on the inverse term frequency distribution
    :rtype: Graph
    """
    n_db = len(db)
    w = words(db)
    n_w = len(w)
    graph = Graph.__init__()
    i = n_w
    for t in w :  # Checks all words t in the db
        graph.add_vertex(Vertex(t))
        d_t = w[t][0]
        for j in w[t][1] :  # For each document containing the word t
            for u in j :  # Checks all words u in those documents
                u = u.lower()
                if graph :
                    if u in graph and t in graph[u] :
                        graph[u][t] - np.log(d_t / w[u][0])
                    else :
                        d_ut = 0
                        for j_ in w[u][1] :
                            if j_ in w[t][1] :  # Computes all the documents containing both u and t
                                d_ut += 1
                        # Adds an edge with weight -log(#docs containing u and t/#docs containing t) to the graph
                        graph[t][u] = -np.log(d_ut / d_t)
        i -= 1
        print(i)
    return graph, n_db, n_w


def graph_creator(db: list[str]) :
    """
    :type db: list[str]
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
    return Final

# En théorie ça fonctionne, après j'ai pas de preuves, et je sais pas combien de temps ça va prendre...
# CA MARCHE BORDEL. EN GENRE 1 ou 2 MINUTES


def dijkstra(G : Graph):
    return


