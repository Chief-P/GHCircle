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