class GameState:
    __slots__ = ("player_pos", "wolf_pos", "score")

    def __init__(self, player_pos, wolf_pos, score):
        self.player_pos = player_pos
        self.wolf_pos = wolf_pos
        self.score = score

    def clone(self):
        return GameState(self.player_pos, self.wolf_pos, self.score)