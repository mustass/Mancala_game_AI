from typing import Literal
from mancala import Mancala


class UIPlayer:
    def __init__(self, game: Mancala, player_number: Literal[0, 1]):
        self.game = game
        self.player_number = player_number
        self.nxt_pos = 0

    @property
    def move(self):
        nxt_move = self.nxt_pos if self.player_number == 0 else self.nxt_pos + 7
        if nxt_move in self.game.get_legal_moves(self.game.board, self.player_number):
            return nxt_move
        else:
            return None

    def inc(self):
        self.nxt_pos = min(self.nxt_pos + 1, self.game.board_sz - 1)

    def dec(self):
        self.nxt_pos = max(self.nxt_pos - 1, 0)


class AIPlayer:
    pass
