import pytest

from src.mancala import Mancala
from src.alphabeta import AlphaBetaPlayer
from src.minimax import MiniMaxPlayer
from src.heuristics import *

from .test_mancala import INITIAL_BOARD, STEALER_BOARD


@pytest.mark.parametrize("board", [INITIAL_BOARD, STEALER_BOARD])
@pytest.mark.parametrize("heuristic", [H1, H2, H3, H4])
@pytest.mark.parametrize("max_depth", [1, 2, 3, 4])

def test_MiniMax_and_AlphaBeta(board, heuristic, max_depth):

    test_game = Mancala(board)

    MiniMax = MiniMaxPlayer(test_game, max_depth, heuristic)
    AlphaBeta = AlphaBetaPlayer(test_game, max_depth, heuristic)

    mini_max_move = MiniMax.think(test_game.board, 0)
    alpha_beta_move = AlphaBeta.think(test_game.board, 0)

    assert mini_max_move == alpha_beta_move

    mini_max_move = MiniMax.think(test_game.board, 1)
    alpha_beta_move = AlphaBeta.think(test_game.board, 1)
    
    assert mini_max_move == alpha_beta_move
