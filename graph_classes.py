import re


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
		self.is_oriented = False

	def add_vertex(self, vertex) :
		if vertex.key in self.vertices :
			return
		self.vertices[vertex.key] = vertex

	def get_vertex(self, key) :
		return self.vertices.get(key, None)

	def __contains__(self, key) :
		return key in self.vertices

	def oriented_add_edge(self, from_key, to_key, weight = None) :
		if from_key not in self :
			self.add_vertex(Vertex(from_key))
		if to_key not in self :
			self.add_vertex(Vertex(to_key))
		self.is_oriented = True
		self.vertices[from_key].oriented_add_neighbour(self.vertices[to_key], weight)

	def unoriented_add_edge(self, from_key, to_key, weight = None) :
		if from_key not in self :
			self.add_vertex(Vertex(from_key))
		if to_key not in self :
			self.add_vertex(Vertex(to_key))
		self.vertices[from_key].unoriented_add_neighbour(self.vertices[to_key], weight)

	def get_edge(self, from_key, to_key) :
		return self.vertices.get(from_key, None).get_weight(self.vertices.get(to_key, None))

	def oriented_modify_edge(self, from_key, to_key, new_weight) :
		self.is_oriented = True
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

	def add_child(self, obj, weight = None) :
		self.Children.append((obj, weight))

	def depth(self) :
		if not self.Children :
			return 0
		return 1 + max([t[0].depth for t in self.Children])

	def diameter(self) :
		if self.Children :
			child_diameter = max([t[0].diameter for t in self.Children])
			depths = sorted([t[0].depth for t in self.Children])
			return max(child_diameter, 1 + depths[0] + depths[1])
		return 0

	def per_depth_vertices(self) :
		p_d_v = [[self.Tag]]
		p_d_childs = []
		for t in self.Children :
			t = t[0]
			p_d_childs.append(t.per_depth_vertices())
		while p_d_childs :
			depth_vertices = []
			for i in range(len(p_d_childs)) :
				depth_vertices.append(p_d_childs[i].pop())
				if not p_d_childs[i] :
					p_d_childs.pop(i)
			p_d_v.append(depth_vertices)
		return p_d_v

	def n_ary(self) :
		return max(len(self.Children), max([t.n_ary() for t in self.Children]))

	def __str__(self, depth = 0) :
		tree_str = f"{self.Tag}"
		for child in self.Children :
			tree_str += f"\n\t"
			child_str = f"{child}"
			child_str = re.sub("\n", "\n\t", child_str)
			tree_str += child_str
		return tree_str

	def paths(self) :
		p = []
		if self.Children :
			for c in self.Children :
				c = c[0]
				follow_up = c.paths()
				p += [str(self.Tag) + f for f in follow_up]
			p += [str(self.Tag)]
			return p
		else :
			return [str(self.Tag)]
