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
    



def dijkstra(graph, start, goal=None):

    dist = {node: math.inf for node in graph.nodes()}
    prev = {node: None for node in graph.nodes()}
    visited = {node: False for node in graph.nodes()}
    dist[start] = 0

    remaining = set(graph.nodes())
    while remaining:
        current = min(remaining, key=lambda n: dist[n])
        if dist[current] == math.inf:
            break
        remaining.remove(current)
        visited[current] = True

        if goal is not None and current == goal:
            break

        for neighbor, weight in graph.neighbors(current):
            if visited[neighbor]:
                continue
            new_dist = dist[current] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current

    return dist, prev


def reconstruct_path(prev, start, goal):
    if goal not in prev:
        return None
    path = []
    node = goal
    while node is not None:
        path.append(node)
        if node == start:
            break
        node = prev[node]
    path.reverse()
    if not path or path[0] != start:
        return None
    return path


def shortest_path_dijkstra(graph, start, goal):
    dist, prev = dijkstra(graph, start, goal)
    path = reconstruct_path(prev, start, goal)
    if path is None:
        return None, math.inf
    return path, dist[goal]


def bfs_shortest_path(graph, start, goal):

    if start == goal:
        return [start]

    visited = {start}
    prev = {start: None}
    q = Queue()
    q.enqueue(start)

    while not q.is_empty():
        current = q.dequeue()
        for neighbor, _weight in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                prev[neighbor] = current
                if neighbor == goal:
                    return reconstruct_path(prev, start, goal)
                q.enqueue(neighbor)

    return None

def _euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
