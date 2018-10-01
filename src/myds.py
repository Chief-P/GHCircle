import networkx as nx
import matplotlib.pyplot as plt
from glob import glob


# Maintain layer of node
# Double space cost
class LayerQueue:
	def __init__(self):
		self.lq = []

	def is_empty(self):
		return self.lq == []

	def enqueue(self, x, l):
		self.lq.insert(0, (x, l))

	def dequeue(self):
		return self.lq.pop()

	def get_size(self):
		return len(self.lq)

	def get_layer(self):
		if self.is_empty():
			return -1
		return self.lq[0][1]


# Store information of directed graph
class DirectedGraph(object):
	def __init__(self):
		self.__dg = nx.DiGraph() # Digraph
		self.__vl = [] # Visited list

	def is_visited(self, n):
		return n in self.__vl

	def append_visited_list(self, n):
		self.__vl.append(n)

	def count_layer(self, src):
		bt = nx.bfs_tree(self.__dg, src)
		return nx.dag_longest_path_length(bt)

	def remove_redundance(self):
		delete_list = []
		for n in self.__dg.nodes:
			if (self.__dg.in_degree(n), self.__dg.out_degree(n)) in ((1, 0), (0, 1)):
				delete_list.append(n)
		for n in delete_list:
			self.__dg.remove_node(n)

	def add_node(self, n):
		self.__dg.add_node(n)

	def add_edge(self, src, dst):
		self.__dg.add_edge(src, dst)

	"""
	def read_data(self, path):
		stored_users, stored_adjlists = [], []
		suffix = '*.adjlist'
		fns = glob(path + suffix)
		for fn in fns:
			stored_adjlists.append(nx.read_adjlist(fn))
			stored_users.append(fn[len(path):-len(suffix)])
		return stored_users, stored_adjlists

	def write_data(self, path, stored_users=None):
		if (stored_users == None):
			stored_users = []
		for line in nx.generate_adjlist(self.__dg):
			username = line[0]
			if username not in stored_users:
				with open(path + str(username) + '.adjlist', 'w', encoding='utf-8') as f:
					f.write(line)
	"""
	def read_data(self, path):
		stored_users, stored_adjlists = [], []
		with open(path, 'r', encoding='utf-8') as f:
			for line in f:
				nodes = line.split()
				DG = nx.DiGraph()
				start, ends = nodes[0], nodes[1:]
				for n in ends:
					DG.add_edge(start, n)
				stored_users.append(start)
				stored_adjlists.append(DG)

	def write_data(self, path, stored_users=None):
		if (stored_users == None):
			stored_users = []
		with open(path, 'w', encoding='utf-8') as f:
			for line in nx.generate_adjlist(self.__dg):
				username = line[0]
				if username not in stored_users:
					f.write(line + '\n')

	def display(self, username, path):
		plt.subplot(111)
		nx.draw_kamada_kawai(self.__dg, with_labels=True) # Forced-directed
		plt.savefig(path + username + '.png') # Implicit storage
		plt.show()

	def get_visited_list(self):
		return self.__vl


# Ignore the following
class Graph:
	def __init__(self):
		self.g = {}

	def is_empty(self):
		return self.g == {}

	def has_node(self, node):
		return node in self.g

	def add_node(self, node):
		self.g[node] = []

	def add_edge(self, src, dst):
		if src not in self.g:
			self.add_node(src)
		self.g[src].append(dst)

	def del_edge(self, src, dst):
		if src in self.g and dst in self.g[src]:
			self.g[src].remove(dst) # Assume simple graph

	def del_node(self, node):
		del self.g[node]

	def display(self):
		print(self.g)


class Stack:
	 def __init__(self):
		 self.items = []

	 def is_empty(self):
		 return self.items == []

	 def push(self, item):
		 self.items.append(item)

	 def pop(self):
		 return self.items.pop()

	 def peek(self):
		 return self.items[len(self.items)-1]

	 def size(self):
		 return len(self.items)


class Queue:
	def __init__(self):
		self.items = []

	def is_empty(self):
		return self.items == []

	def enqueue(self, item):
		self.items.insert(0, item)

	def dequeue(self):
		return self.items.pop()

	def size(self):
		return len(self.items)