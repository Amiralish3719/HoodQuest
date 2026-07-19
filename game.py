from data_structures import Stack

from graph import build_game_map, dijkstra, reconstruct_path,a_star

import random

class GameState:
    __slots__ = ("player_pos", "wolf_pos", "score")

    def __init__(self, player_pos, wolf_pos, score):
        self.player_pos = player_pos
        self.wolf_pos = wolf_pos
        self.score = score

    def clone(self):
        return GameState(self.player_pos, self.wolf_pos, self.score)

class HoodQuestGame:
    UNDO_PENALTY = -2
    MATCH_SUGGESTED_REWARD = 3
    ALT_VALID_MOVE_REWARD = 1
    REACH_GOAL_BONUS = 5

    def __init__(self):
        self.graph, self.goal = build_game_map()
        self.player_pos = None
        self.wolf_pos = None
        self.score = 0
        self.undo_stack = Stack()
        self.turn_number = 1
        self.game_over = False
        self.result = None
        self._setup_initial_positions()

    def _setup_initial_positions(self):
        candidates = [n for n in self.graph.nodes() if n != self.goal]
        self.player_pos = random.choice(candidates)
        remaining = [n for n in candidates if n != self.player_pos]
        self.wolf_pos = random.choice(remaining)

    def suggested_path(self):
        dist, prev = dijkstra(self.graph, self.player_pos, self.goal)
        path = reconstruct_path(prev, self.player_pos, self.goal)
        cost = dist[self.player_pos] if path else None
        return path, cost

    def suggested_path_astar(self):
        path, cost = a_star(self.graph, self.player_pos, self.goal)
        return path, cost