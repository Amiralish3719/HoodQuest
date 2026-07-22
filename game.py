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
    
    def valid_moves(self):
        return [n for n, _w in self.graph.neighbors(self.player_pos)]

    def begin_turn_snapshot(self):
        return GameState(self.player_pos, self.wolf_pos, self.score)

    def is_valid_move(self, target_node):
        return self.graph.has_edge(self.wolf_pos, target_node)

    def apply_player_move(self, target_node, suggested_next):

        if not self.is_valid_move(target_node):
            return False, "Invalid move: that node is not directly connected to your current position."

        if target_node == suggested_next:
            self.score += self.MATCH_SUGGESTED_REWARD
            move_msg = f"Moved along the Dijkstra-suggested path (+{self.MATCH_SUGGESTED_REWARD} points)"
        else:
            self.score += self.ALT_VALID_MOVE_REWARD
            move_msg = f"Moved along a valid alternative path (+{self.ALT_VALID_MOVE_REWARD} point)"

        self.player_pos = target_node

        if self.player_pos == self.goal:
            self.score += self.REACH_GOAL_BONUS
            move_msg += f" | Reached Grandma's house (+{self.REACH_GOAL_BONUS} bonus points)"
            self.game_over = True
            self.result = "win"
            return True, move_msg

        if self.player_pos == self.wolf_pos:
            self.game_over = True
            self.result = "lose"
            return True, move_msg + " | You ran straight into the wolf! You lost."

        return True, move_msg

    def apply_undo(self):
        if self.undo_stack.is_empty():
            return False, "There is no previous turn to undo."
        prev_state = self.undo_stack.pop()
        self.player_pos = prev_state.player_pos
        self.wolf_pos = prev_state.wolf_pos
        self.score = prev_state.score
        return True, f"Previous turn restored ({self.UNDO_PENALTY} point penalty)."