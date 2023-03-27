class Vertex :
    def __init__(self, key) :
        """
        :type key: depends on your mood UwU
        """
        self.key = key
        self.neighbours = {}

    def oriented_add_neighbour(self, neighbour, weight = None) :
        self.neighbours[neighbour] = weight

    def unoriented_add_neighbour(self, neighbour, weight = None) :
        """
        :param neighbour: Another vertex that is connected to this one in the graph.
        :type neighbour: Vertex
        :param weight : Weight of the edge to neighbour. Default is None for a non weighted graph.
        :type weight: Technically anything that can be compared
        """
        self.oriented_add_neighbour(neighbour, weight)
        neighbour.oriented_add_neighbour(self, weight)

    def get_connections(self) :
        return self.neighbours.keys()

    def degree(self) :
        return len(self.neighbours.keys())

    def get_weight(self, neighbour) :
        """
        :type neighbour: Vertex
        """
        return self.neighbours.get(neighbour, None)

    def oriented_modify_weight(self, neighbour, new_weight) :
        self.neighbours[neighbour] = new_weight

    def unoriented_modify_weight(self, neighbour, new_weight) :
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

    def oriented_add_edge(self, from_key, to_key, weight = None) :
        if not self.__contains__(from_key) :
            self.add_vertex(Vertex(from_key))
        if not self.__contains__(to_key) :
            self.add_vertex(Vertex(to_key))
        self.vertices[from_key].oriented_add_neighbour(self.vertices[to_key], weight)

    def unoriented_add_edge(self, from_key, to_key, weight = None) :
        if not self.__contains__(from_key) :
            self.add_vertex(Vertex(from_key))
        if not self.__contains__(to_key) :
            self.add_vertex(Vertex(to_key))
        self.vertices[from_key].unoriented_add_neighbour(self.vertices[to_key], weight)

    def get_edge(self, from_key, to_key) :
        return self.vertices.get(from_key, None).get_weight(self.vertices.get(to_key, None))

    def oriented_modify_edge(self, from_key, to_key, new_weight) :
        return self.vertices.get(from_key, None).oriented_modify_weight(self.vertices.get(to_key, None), new_weight)

    def unoriented_modify_edge(self, from_key, to_key, new_weight) :
        return self.vertices.get(from_key, None).unoriented_modify_weight(self.vertices.get(to_key, None), new_weight)

    def get_vertices(self) :
        return [self.vertices[k] for k in self.vertices.keys()]

    def __iter__(self) :
        return iter(self.vertices.values())

    def __str__(self) :
        for u in self :
            for v in u.get_connections() :
                print("{} -> {} : {}".format(u.key, v.key, self.get_edge(u.key, v.key)))


class Tree :
    def __init__(self, data) :
        self.Tag = data
        self.Children = []

    def add_child(self, obj) :
        self.Children.append(obj)


def natural_distribution(candidates) :
    candidates.sort()
    return candidates


def exact_posterior_distribution(candidates) :
    word_posteriors = {}
    for grid in candidates :
        for w in grid.Words :
            word_posteriors[w] = grid.Weight + word_posteriors.get(w, 0)

    for grid in candidates :
        for w in grid.Words :
            grid.QWeight += word_posteriors[w]

    return candidates


def constraint_network(grid) :
    N = Graph()
    for clue in grid.AClues :
        N.add_vertex(Vertex((clue.Length, grid.AClues[clue])))
    return N


def dfs_tree(G: Graph, depth: int, x, prev_vertex = None) :
    if G.get_vertex(x) is None :
        return "x is not in graph G"

    res_tree = Tree(x)
    cur_vertex = x
    if depth > 0 :
        for v in G.vertices[cur_vertex].neighbours :
            if not v == prev_vertex :
                res_tree.add_child(dfs_tree(G, depth - 1, v, prev_vertex = x))
    return res_tree


def match(tile1, d1, w1, tile2, d2, w2) :
    """
    :param tile1:
    :type tile1:
    :param d1:
    :type d1:
    :param w1:
    :type w1:
    :param tile2:
    :type tile2:
    :param d2:
    :type d2:
    :param w2:
    :type w2:
    :return True if words w1 and w2 placed in directions d1 and d2 starting from tile1 and tile 2 do not violate any constraint
    """
    res = True
    if d1 == d2 :
        if d1 == "a" :
            temp = tile1[0] != tile2[0]
            temp = temp or tile1[1] + len(w1) < tile2[1]
            temp = temp or tile2[1] + len(w2) < tile1[1]
            return temp
        if d1 == "d" :
            temp = tile1[1] != tile2[1]
            temp = temp or tile1[0] + len(w1) < tile2[0]
            temp = temp or tile2[0] + len(w2) < tile1[0]
            return temp
    else :
        if d1 == "a" :
            temp =
