from src.game import Game

INITIAL_BOARD = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
PLAYER_1_WINS_BOARD = [0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 25]
PLAYER_0_WINS_BOARD = [0, 0, 0, 0, 0, 0, 26, 0, 0, 0, 0, 0, 0, 22]
EARLY_WIN_BOARD = [0, 0, 0, 0, 0, 1, 10, 5, 5, 5, 5, 5, 5, 7]
STEALER_BOARD = [0, 5, 5, 0, 6, 5, 1, 5, 1, 5, 5, 5, 5, 0]

def test_init():
    test_game = Game()
    assert test_game.board == [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    assert test_game.board_sz == 6


def test_legal_moves():
    test_game = Game(board=INITIAL_BOARD)
    moves0 = test_game.get_legal_moves(0)
    moves1 = test_game.get_legal_moves(1)

    assert moves0 == [0, 1, 2, 3, 4, 5]
    assert moves1 == [7, 8, 9, 10, 11, 12]

    test_game = Game(board=PLAYER_1_WINS_BOARD)
    moves0 = test_game.get_legal_moves(0)
    moves1 = test_game.get_legal_moves(1)

    assert moves0 == []
    assert moves1 == []

    test_game = Game(board=PLAYER_0_WINS_BOARD)
    moves0 = test_game.get_legal_moves(0)
    moves1 = test_game.get_legal_moves(1)

    assert moves0 == []
    assert moves1 == []


def test_distribute_pebbles():

    test_game = Game(board=INITIAL_BOARD)

    test_game.distr_pebbles(0, 0)

    assert test_game.board == [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    # Illegal move for Player 1 will trigger a fail
    try:
        test_game.distr_pebbles(0, 1)
    except AssertionError:
        assert test_game.board == [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    test_game.distr_pebbles(8, 1)
    assert test_game.board == [0, 5, 5, 5, 5, 4, 0, 4, 0, 5, 5, 5, 5, 0]

    test_game.distr_pebbles(3, 0)
    assert test_game.board == [0, 5, 5, 0, 6, 5, 1, 5, 1, 5, 5, 5, 5, 0]

def test_stealing_opponent_house():
    test_game = Game(STEALER_BOARD)
    test_game.distr_pebbles(2, 0)
    assert test_game.board == [0, 5, 0, 1, 7, 6, 7, 6, 1, 0, 5, 5, 5, 0]


def test_early_win():
    test_game1 = Game(board=EARLY_WIN_BOARD)
    test_game1.distr_pebbles(5, 0)
    assert test_game1.board == [0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 7]
