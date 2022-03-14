from typing import Literal

PITS = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


class Game:
    """
    Model of the game
    """

    def __init__(
        self, board: list = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0], board_size=6
    ) -> None:
        assert len(board) == 14
        assert sum(board) == 48

        self.board = board
        self.board_sz = board_size

        self.player_houses = {0: [0, 1, 2, 3, 4, 5], 1: [7, 8, 9, 10, 11, 12]}

        self.player_pits = {0: 6, 1: 13}

        self.player = 0

        print(f"Initialized the board{board}")

    def get_legal_moves(self, player: Literal[0, 1]) -> list:
        moves = {
            0: [
                i
                for i, e in enumerate(self.board)
                if e != 0
                and i
                not in self.player_houses[1] + [v for k, v in self.player_pits.items()]
            ],
            1: [
                i
                for i, e in enumerate(self.board)
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

    def is_end_match(self):
        pit_indices = [int(v) for k, v in self.player_pits.items()]
        return sum(self.board[i] for i in pit_indices) == 48

    def is_win(self):
        assert self.is_end_match(), "The game has not ended."
        pit_indices = [int(v) for k, v in self.player_pits.items()]
        outcome = [self.board[i] for i in pit_indices]
        if outcome[0] == outcome[1]:
            return None
        return outcome.index(max(outcome,))

    def opposite_player(self, player: Literal[0, 1]):
        if player == 1:
            return 0
        return 1

    def switch_player(self):
        self.player = self.opposite_player(self.player)

    def distr_pebbles(self, house: Literal[PITS], player: int):
        assert house in self.get_legal_moves(
            player
        ), f"The chosen house {house} is not in the set of legal moves for player {player}"

        pebbles = self.board[house]

        self.board[house] = 0

        while pebbles > 0:

            house = 0 if house == 13 else house + 1

            if not house == self.player_pits[self.opposite_player(player)]:
                self.board[house] += 1
                pebbles -= 1

        self.capture_opposite_house(player, house)
        self.early_win(player)

        extra_turn = ((player == 0) and (house == 6)) or (
            (player == 1) and (house == 13)
        )

        return extra_turn

    def capture_opposite_house(self, player, house):

        if not self.is_plyr_house(house, player):
            return
        player_houses = self.player_houses[player]
        opposite_houses = self.player_houses[self.opposite_player(player)][::-1]
        steal = False
        player_house_index = player_houses.index(house)

        steal = (
            self.board[house] == 1
            and self.board[opposite_houses[player_house_index]] > 0
        )

        if steal:
            player_pit = self.player_pits[player]
            self.board[player_pit] += self.board[opposite_houses[player_house_index]]
            self.board[opposite_houses[player_house_index]] = 0

    def early_win(self, player):
        moves_left = self.get_legal_moves(player)
        if len(moves_left) == 0:
            print(self.player_houses[self.opposite_player(player)])
            take_over_pebbles = sum(
                [
                    self.board[i]
                    for i in self.player_houses[self.opposite_player(player)]
                ]
            )
            self.board[self.player_pits[player]] += take_over_pebbles

            for index, element in enumerate(self.board):
                if index in self.player_houses[self.opposite_player(player)]:
                    self.board[index] = 0


if __name__ == "__main__":
    test_game = Game([0, 5, 1, 0, 6, 5, 1, 5, 1, 5, 4, 5, 5, 5])
    test_game.distr_pebbles(2, 0)
    print(test_game.board)
