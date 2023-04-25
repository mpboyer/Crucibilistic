import random

import matplotlib.pyplot as plt
import networkx as nx


def graph_to_networkx(g) :
	if g.is_oriented :
		return "Unoriented Graphs Only"
	G = nx.Graph()
	G.add_nodes_from(g.vertices.keys())
	for u in g.vertices :
		for v in g[u].get_connections() :
			G.add_edge(u, v, weight = g.get_edge(u, v))
	return G


def digraph_to_networkx(g) :
	if not g.is_oriented :
		return "Oriented Graphs Only"
	DG = nx.Digraph()
	DG.add_nodes_from(g.vertices.keys())
	for u in g.vertices :
		for v in g[u].get_connections() :
			DG.add_edge(u, v, weight = g.get_edge(u, v))
	return DG


def tree_to_networkx(te) :
	T = nx.Graph()

	def aux(tree) :
		T.add_node(tree.Tag, label = tree.Tag)
		for c in tree.Children :
			lab, w = c
			aux(lab)
			T.add_edge(tree.Tag, lab.Tag, weight = w)

	aux(te)

	return T


def hierarchy_layout(G, root = None, width = 1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5) :
	"""
	If the graph is a tree this will return the positions to plot this in a
	hierarchical layout.

	G: the graph (must be a tree)

	root: the root node of current branch
	- if the tree is directed and this is not given, the root will be found and used
	- if the tree is directed and this is given, then the positions will be just for the descendants of this node.
	- if the tree is undirected and not given, then the node with minimum label will be used

	width: horizontal space allocated for this branch - avoids overlap with other branches

	vert_gap: gap between levels of hierarchy

	vert_loc: vertical location of root

	xcenter: horizontal location of root
	"""
	if not nx.is_tree(G) :
		raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

	if root is None :
		if isinstance(G, nx.DiGraph) :
			root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
		else :
			root = random.choice(list(G.nodes))

	def _hierarchy_pos(G, root, width = 1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None) :
		'''
		see hierarchy_pos docstring for most arguments

		pos: a dict saying where all nodes go if they have been assigned
		parent: parent of this branch. - only affects it if non-directed

		'''

		if pos is None :
			pos = {root : (xcenter, vert_loc)}
		else :
			pos[root] = (xcenter, vert_loc)
		children = list(G.neighbors(root))
		if not isinstance(G, nx.DiGraph) and parent is not None :
			children.remove(parent)
		if len(children) != 0 :
			dx = width / len(children)
			nextx = xcenter - width / 2 - dx / 2
			for child in children :
				nextx += dx
				pos = _hierarchy_pos(G, child, width = dx, vert_gap = vert_gap, vert_loc = vert_loc - vert_gap,
									 xcenter = nextx, pos = pos, parent = root)
		return pos

	return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def tree_show(te, scale_factor = 1, save_string = None) :
	T = tree_to_networkx(te)
	pos = hierarchy_layout(T, 0)
	pos = nx.rescale_layout_dict(pos, scale_factor)
	fig = plt.clf()
	fig.set_figwidth(15)
	fig.set_figheight(15)
	nx.draw_networkx_nodes(T, pos)
	nx.draw_networkx_edges(T, pos)
	nx.draw_networkx_labels(T, pos)
	edge_labels_ = nx.get_edge_attributes(T, "weight")
	edge_labels = {n : w for n, w in edge_labels_.items() if w is not None}
	nx.draw_networkx_edge_labels(T, pos, edge_labels)

	if save_string is not None :
		plt.savefig(save_string)
	else :
		plt.show()


def graph_show(g, vertice_partition = None, own_structure = True, save_string = None, title = "") :
	if own_structure :
		if g.is_oriented :
			G = digraph_to_networkx(g)
		else :
			G = graph_to_networkx(g)
	else :
		G = g

	fig = plt.figure()
	pos = nx.circular_layout(G)
	colours = ["#de0c62", "#a2cffe", "#a2cffe", "#ceb301", "#b790d4", "#ffa756", "#ce5dae"]
	# In order : Red, Blue, Green, Purple, Yellow, Orange, Pink
	if vertice_partition is None :
		nx.draw_networkx_nodes(G, pos, node_color = "White", node_shape = "s", linewidths = 1.0)
	else :
		for i in range(len(vertice_partition)) :
			j = i % len(colours)
			nx.draw_networkx_nodes(G, pos, node_color = colours[j], alpha = .8, node_shape = "s", linewidths = 1.0,
								   nodelist = vertice_partition[i])
			nx.draw_networkx_labels(G, pos, font_color = "Black", font_weight = 4, horizontalalignment = "center",
									labels = {n : n for n in G if n in vertice_partition[i]})

	nx.draw_networkx_edges(G, pos, style = "-", edge_color = "Black", alpha = .6)
	edge_labels_ = nx.get_edge_attributes(G, "weight")
	edge_labels = {n : w for n, w in edge_labels_.items() if w is not None}
	nx.draw_networkx_edge_labels(G, pos, edge_labels)
	if save_string is not None :
		plt.title(title)
		plt.savefig(save_string)
	else :
		plt.show()
