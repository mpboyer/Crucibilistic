import matplotlib.pyplot as plt
import networkx as nx

from graph_classes import *


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


def binary_test_tree(depth, data, f) :
	def aux(k, e) :
		if k == 0 :
			return Tree(e), e
		else :
			t = Tree(e)
			t_, e = aux(k - 1, f(e))
			t.add_child(t_)
			t_, e = aux(k - 1, f(e))
			t.add_child(t_)
			return t, e

	return aux(depth, data)


t, e = binary_test_tree(2, 0, lambda key : key + 1)


def tree_show(te) :
	T = tree_to_networkx(te)
	pos = nx.spring_layout(T)
	nodes = nx.draw_networkx_nodes(T, pos)
	edges = nx.draw_networkx_edges(T, pos)
	labels = nx.draw_networkx_labels(T, pos)
	edge_labels = nx.get_edge_attributes(T, "weight")
	nx.draw_networkx_edge_labels(T, pos, edge_labels)

	plt.show()


T = tree_to_networkx(t)
