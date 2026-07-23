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


def a_star(graph, start, goal, heuristic_scale=2.2):

    nodes = graph.nodes()
    g_score = {n: math.inf for n in nodes}
    f_score = {n: math.inf for n in nodes}
    prev = {n: None for n in nodes}
    g_score[start] = 0

    def h(n):
        return _euclidean(graph.position(n), graph.position(start)) * heuristic_scale

    f_score[start] = h(start)
    open_set = {start}
    closed_set = set()

    while open_set:
        current = min(open_set, key=lambda n: f_score[n])
        if current == goal:
            path = reconstruct_path(prev, start, goal)
            return path, g_score[goal]

        open_set.remove(current)
        closed_set.add(current)

        for neighbor, weight in graph.neighbors(current):
            if neighbor in closed_set:
                continue
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                prev[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h(neighbor)
                open_set.add(neighbor)

    return None, math.inf


def build_game_map():

    g = Graph()

    positions = {
        "A": (0, 1), "B": (1, 0), "C": (3, 0), "D": (5, 0), "E": (6, 1),
        "F": (2, 1), "G": (4, 1),
        "W": (4, 2), "M": (5, 2), "J": (2, 2), "K": (3, 2),
        "O": (0, 3), "P": (1, 3), "R": (3, 3), "S": (5, 3),
        "Q": (1, 4), "T": (3, 4), "U": (5, 4),
        "V": (3, 5),
    }
    for node, pos in positions.items():
        g.add_node(node, pos)

    edges = [
        ("A", "B", 3), ("A", "F", 6),
        ("B", "C", 2),
        ("C", "D", 5),
        ("D", "E", 1),
        ("F", "G", 4), ("F", "J", 6),
        ("G", "E", 3), ("G", "W", 5), ("G", "M", 4),
        ("W", "M", 3), ("W", "K", 2),
        ("J", "K", 3), ("J", "P", 5),
        ("K", "R", 2),
        ("M", "S", 1),
        ("O", "P", 3), ("O", "Q", 2),
        ("P", "R", 1),
        ("R", "S", 2), ("R", "T", 4),
        ("S", "U", 6),
        ("Q", "T", 5), ("Q", "V", 5),
        ("T", "U", 2),
        ("U", "V", 3),
    ]