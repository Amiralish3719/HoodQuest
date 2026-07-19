from data_structures import Stack

from graph import build_game_map

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