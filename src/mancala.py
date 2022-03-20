from copy import deepcopy
from typing import Literal


PITS = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
INITIAL_BOARD = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]


class Mancala:
    """
    Model of the game
    """

    def __init__(self, board: list = INITIAL_BOARD, board_size=6) -> None:
        assert len(board) == 14
        assert sum(board) == 48

        self.board = board
        self.board_sz = board_size

        self.player_houses = {0: [0, 1, 2, 3, 4, 5], 1: [7, 8, 9, 10, 11, 12]}

        self.player_pits = {0: 6, 1: 13}

        self.player = 0

        # print(f"Initialized the board{board}")

    def get_legal_moves(self, board, player: Literal[0, 1]) -> list:
        moves = {
            0: [
                i
                for i, e in enumerate(board)
                if e != 0
                and i
                not in self.player_houses[1] + [v for k, v in self.player_pits.items()]
            ],
            1: [
                i
                for i, e in enumerate(board)
                if e != 0
                and i
                not in self.player_houses[0] + [v for k, v in self.player_pits.items()]
            ],
        }[player]
        return moves

    def is_plyr_house(self, pit: Literal[PITS], player: Literal[0, 1]) -> bool:
        return pit in self.player_houses[player]

    def has_move(self, player: Literal[0, 1]) -> bool:
        legal_moves = self.get_legal_moves(player)
        return len(legal_moves) > 0

    def is_end_match(self, board):
        pit_indices = [int(v) for k, v in self.player_pits.items()]
        return sum(board[i] for i in pit_indices) == 48

    def is_win(self, board):
        assert self.is_end_match(board), "The game has not ended."
        pit_indices = [int(v) for k, v in self.player_pits.items()]
        outcome = [board[i] for i in pit_indices]
        if outcome[0] == outcome[1]:
            return None
        return outcome.index(max(outcome,))

    def opposite_player(self, player: Literal[0, 1]):
        if player == 1:
            return 0
        return 1

    def switch_player(self):
        self.player = self.opposite_player(self.player)

    def distr_pebbles(self, board, house: Literal[PITS], player: int) -> tuple:
        board = deepcopy(board)
        assert house in self.get_legal_moves(
            board, player
        ), f"The chosen house {house} is not in the set of legal moves for player {player}"

        pebbles = board[house]
        board[house] = 0

        while pebbles > 0:

            house = 0 if house == 13 else house + 1

            if not house == self.player_pits[self.opposite_player(player)]:
                board[house] += 1
                pebbles -= 1

        board = self.capture_opposite_house(board, player, house)
        board = self.early_win(board, player)
        board = self.early_gameover(board)

        extra_turn = ((player == 0) and (house == 6)) or (
            (player == 1) and (house == 13)
        )

        return board, extra_turn

    def capture_opposite_house(self, board, player, house) -> list:

        if not self.is_plyr_house(house, player):
            return board
        player_houses = self.player_houses[player]
        opposite_houses = self.player_houses[self.opposite_player(player)][::-1]
        steal = False
        player_house_index = player_houses.index(house)

        steal = board[house] == 1 and board[opposite_houses[player_house_index]] > 0

        if steal:
            player_pit = self.player_pits[player]
            board[player_pit] += board[opposite_houses[player_house_index]]
            board[opposite_houses[player_house_index]] = 0
            board[player_pit] += 1
            board[house] = 0

        return board

    def early_win(self, board, player) -> list:
        for player in [0, 1]:
            moves_left = self.get_legal_moves(board, player)
            if len(moves_left) == 0:
                take_over_pebbles = sum(
                    [board[i] for i in self.player_houses[self.opposite_player(player)]]
                )
                board[self.player_pits[player]] += take_over_pebbles

                for index, element in enumerate(self.board):
                    if index in self.player_houses[self.opposite_player(player)]:
                        board[index] = 0

        return board

    def early_gameover(self, board)->list:
        pit_indices = [int(v) for k, v in self.player_pits.items()]
        outcome = [board[i] for i in pit_indices]
        if any([outcome[0] >24, outcome[1] >24]):
            player_won = outcome.index(max(outcome))
            pebbles_left = 48 - outcome[0] - outcome[1]

            board[self.player_pits[player_won]] += pebbles_left

            for house in list(self.player_houses[0]+self.player_houses[1]):
                board[house] = 0
        return board            

    def update_game_board(self, board):
        self.board = board


if __name__ == "__main__":
    test_game = Mancala(board=[4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
    new_board = test_game.distr_pebbles(test_game.board, 0, 0)
    test_game.update_game_board(new_board)
    print(new_board)
