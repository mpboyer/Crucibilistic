from initializermodule import *


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
		graph_string = ""
		for u in self :
			for v in u.get_connections() :
				graph_string += "{} -> {} : {}".format(u.key, v.key, self.get_edge(u.key, v.key)) + "\n"
		return graph_string


class Tree :
	def __init__(self, data) :
		self.Tag = data
		self.Children = []

	def add_child(self, obj) :
		self.Children.append(obj)

	def __str__(self, depth = 0) :
		tree_str = f"{self.Tag}"
		for child in self.Children :
			tree_str += f"\n\t"
			child_str = f"{child}"
			child_str = re.sub("\n", "\n\t", child_str)
			tree_str += child_str
		return tree_str


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
	p, q = grid.Size
	clue_counter = 1
	N = Graph()
	prev_clue_dict = {}

	for row in range(p) :
		for column in range(q) :
			tile = grid.Grid[row][column]
			if tile.AClue is not None or tile.DClue is not None :
				if tile.AClue is not None :
					N.add_vertex(Vertex(f"{clue_counter}A"))
					tile_list = set([(row, column + k) for k in range(tile.AClue.Length)])
					k = len(tile_list)
					for node in [node for node in N.vertices.keys() if node != f"{clue_counter}A"] :
						node_tiles = prev_clue_dict[node]
						k2 = len(node_tiles)
						if len(tile_list.union(node_tiles)) < k + k2 :
							N.unoriented_add_edge(node, f"{clue_counter}A")
					prev_clue_dict[f"{clue_counter}A"] = tile_list
				if tile.DClue is not None :
					N.add_vertex(Vertex(f"{clue_counter}D"))
					tile_list = set([(row + k, column) for k in range(tile.DClue.Length)])
					k = len(tile_list)
					for node in [node for node in N.vertices.keys() if node != f"{clue_counter}D"] :
						node_tiles = prev_clue_dict[node]
						k2 = len(node_tiles)
						if len(tile_list.union(node_tiles)) < k + k2 :
							N.unoriented_add_edge(node, f"{clue_counter}D")
					prev_clue_dict[f"{clue_counter}D"] = tile_list
				clue_counter += 1
	return N


def dfs_tree(G: Graph, depth: int, x, prev_vertex = None) :
	if G.get_vertex(x) is None :
		return "x is not in graph G"

	res_tree = Tree(x)
	cur_vertex = x
	if depth > 0 :
		for v in G.vertices[cur_vertex].neighbours :
			if not v.key == prev_vertex :
				res_tree.add_child(dfs_tree(G, depth - 1, v.key, prev_vertex = x))
	return res_tree


N = constraint_network(grid)
print(N, end = "\n \n \n \n")
print(dfs_tree(N, depth = 3, x = "1A"))
