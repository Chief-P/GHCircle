from datafetch import *

def build_circle():
	data_path = '../data/data.adjlist'
	graph_path = '../graph/'
	digraph = DirectedGraph()
	# stored_users, stored_adjlists = digraph.read_data(data_path)

	username = input('Plz input username: ')
	max_layer = input('Plz input max relation layers: ')
	max_layer = regularize_max_layer(int(max_layer))

	# Trivial BFS
	q = LayerQueue()
	q.enqueue(username, 0)
	digraph.add_node(username)

	while not q.is_empty():
		user, cur_layer = q.dequeue()
		if cur_layer == max_layer: # Layer control
			break
		followers, followings = get_relation(user, digraph)
		for f in remove_duplicates(followers + followings, digraph):
			print(f)
			q.enqueue(f, cur_layer + 1)

	# digraph.write_data(data_path, stored_users)

	digraph.remove_redundance()
	if max_layer < 4:
		digraph.display(username, graph_path)
	# some fuckin analysis of dg here

build_circle()