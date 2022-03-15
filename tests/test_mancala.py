from src.mancala import Mancala

INITIAL_BOARD = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
PLAYER_1_WINS_BOARD = [0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 25]
PLAYER_0_WINS_BOARD = [0, 0, 0, 0, 0, 0, 26, 0, 0, 0, 0, 0, 0, 22]
EARLY_WIN_BOARD = [0, 0, 0, 0, 0, 1, 10, 5, 5, 5, 5, 5, 5, 7]
STEALER_BOARD = [0, 5, 1, 0, 6, 5, 1, 5, 1, 5, 4, 5, 5, 5]


def test_init():
    test_game = Mancala()
    assert test_game.board == [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    assert test_game.board_sz == 6


def test_legal_moves():
    test_game = Mancala(board=INITIAL_BOARD)
    board = test_game.board
    moves0 = test_game.get_legal_moves(board, 0)
    moves1 = test_game.get_legal_moves(board, 1)

    assert moves0 == [0, 1, 2, 3, 4, 5]
    assert moves1 == [7, 8, 9, 10, 11, 12]

    test_game = Mancala(board=PLAYER_1_WINS_BOARD)
    board = test_game.board
    moves0 = test_game.get_legal_moves(board, 0)
    moves1 = test_game.get_legal_moves(board, 1)

    assert moves0 == []
    assert moves1 == []

    test_game = Mancala(board=PLAYER_0_WINS_BOARD)
    board = test_game.board
    moves0 = test_game.get_legal_moves(board, 0)
    moves1 = test_game.get_legal_moves(board, 1)

    assert moves0 == []
    assert moves1 == []


def test_distribute_pebbles():

    test_game = Mancala(board=INITIAL_BOARD)
    new_board, _ = test_game.distr_pebbles(test_game.board, 0, 0)
    test_game.update_game_board(new_board)

    assert new_board == [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    # Illegal move for Player 1 will trigger a fail
    try:
        new_board, _ = test_game.distr_pebbles(test_game.board, 0, 1)
        test_game.update_game_board(new_board)
    except AssertionError:
        assert test_game.board == [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    new_board, _ = test_game.distr_pebbles(test_game.board, 8, 1)
    test_game.update_game_board(new_board)
    assert new_board == [0, 5, 5, 5, 5, 4, 0, 4, 0, 5, 5, 5, 5, 0]

    new_board, _ = test_game.distr_pebbles(test_game.board, 3, 0)
    test_game.update_game_board(new_board)
    assert new_board == [0, 5, 5, 0, 6, 5, 1, 5, 1, 5, 5, 5, 5, 0]


def test_stealing_opponent_house():
    test_game = Mancala(STEALER_BOARD)
    new_board, _ = test_game.distr_pebbles(test_game.board, 2, 0)
    test_game.update_game_board(new_board)
    assert test_game.board == [0, 5, 0, 0, 6, 5, 7, 5, 1, 0, 4, 5, 5, 5]


def test_early_win():
    test_game1 = Mancala(board=EARLY_WIN_BOARD)
    new_board, _ = test_game1.distr_pebbles(test_game1.board, 5, 0)
    test_game1.update_game_board(new_board)
    assert test_game1.board == [0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 7]
