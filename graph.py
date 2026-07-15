import math
from data_structures import Queue


class Graph:

    def __init__(self):
        self._adj = {}          
        self._positions = {}    

    def add_node(self, node, position=None):
        if node not in self._adj:
            self._adj[node] = []
        if position is not None:
            self._positions[node] = position

    def add_edge(self, u, v, weight):
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append((v, weight))
        self._adj[v].append((u, weight))

    def neighbors(self, node):
        return list(self._adj.get(node, []))

    def nodes(self):
        return list(self._adj.keys())

    def has_edge(self, u, v):
        return any(n == v for n, _w in self._adj.get(u, []))

    def edge_weight(self, u, v):
        for n, w in self._adj.get(u, []):
            if n == v:
                return w
        return None

    def position(self, node):
        return self._positions.get(node, (0, 0))