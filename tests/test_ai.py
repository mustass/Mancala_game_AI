import pytest

from src.mancala import Mancala
from src.alphabeta import AlphaBetaPlayer
from src.minimax import MiniMaxPlayer
from src.heuristics import *

from .test_mancala import INITIAL_BOARD, STEALER_BOARD


@pytest.mark.parametrize("board", [INITIAL_BOARD, STEALER_BOARD])
def test(board):

    test_game = Mancala(board)

    MiniMax = MiniMaxPlayer(test_game, 2, H3)
    AlphaBeta = AlphaBetaPlayer(test_game, 2, H3)

    mini_max_move = MiniMax.think(test_game.board, 0)
    alpha_beta_move = AlphaBeta.think(test_game.board, 0)

    assert mini_max_move == alpha_beta_move
