import candidate_generation_package.dijkstramodule as dmm
import setup
import solving_package.initializermodule as inim
from graph_classes import *
from graphing_package.main import *
import solving_package.weighingmodule as weim

def example_tree() :
	def binary_test_tree(depth, data, f) :

		def aux(k, e) :
			if k == 0 :
				return Tree(e), e
			else :
				t = Tree(e)
				if e % 2 == 0 :
					w = 1
				else :
					w = None
				t_, e = aux(k - 1, f(e))
				t.add_child(t_, w)
				t_, e = aux(k - 1, f(e))
				t.add_child(t_, w)
				return t, e

		return aux(depth, data)

	t, e = binary_test_tree(4, 0, lambda key : key + 1)
	tree_show(t)


def partial_dijkstra_db_graph1() :
	Omega, DB = dmm.graph_creator([c.Clue.lower() + " " + c.Word.lower() for c in setup.CWDB])
	distances_ = dmm.dijkstra(DB, 'absurd', 5)
	distances = sorted(distances_.items(), key = lambda t : t[1])[:20]
	G = nx.DiGraph()
	for vertex in distances :
		u = vertex[0]
		G.add_node(u)
	for vertex in distances :
		u, d = vertex
		vertex = DB.get_vertex(u)
		edges = [(u, v, w) for v, w in vertex.neighbours.items()]
		for e in edges :
			u, v, w = e
			if v not in G :
				pass
			G.add_edge(u, v, weight = w)

	graph_show(G, own_structure = False, save_string = "dijkstra_graph_example.png",
			   title = "Part of the Graph used for Dijkstra around 'Absurd'")


def constraint_network_graph() :
	G = inim.grid.constraint_network()
	node_partition = [[nodes for nodes in G if nodes[-1] == "A"], [nodes for nodes in G if nodes[-1] == "D"]]
	# In most cases, G is not a tree, since it is definitely not acyclic. It is however always connex.
	graph_show(G, vertice_partition = node_partition, own_structure = False,
			   save_string = "constraint_network_graph_example.png", title = "Constraint Network Graph Example")


def constraint_tree_graph() :
	G = weim.constraint_network(inim.grid)
	T = weim.dfs_tree(G, 3, "1A")
	tree_show(T, save_string = "constraint_tree_example.png", title = "Constraint Tree Around 1A, Depth = 3")


constraint_tree_graph()
