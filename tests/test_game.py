from pyrsistent import v
import pytest
from src.game import Game

INITIAL_BOARD = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
PLAYER_1_WINS_BOARD = [0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 25]
PLAYER_0_WINS_BOARD = [0, 0, 0, 0, 0, 0, 26, 0, 0, 0, 0, 0, 0, 22]



def test_init():
    test_game = Game()
    assert test_game.board == [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    assert test_game.board_sz == 6

def test_legal_moves():
    test_game = Game(board= INITIAL_BOARD)
    moves1 = test_game.get_legal_moves(0)
    moves2 = test_game.get_legal_moves(1)

    

