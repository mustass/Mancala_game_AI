from typing import Literal

PITS = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


class Game:
    """
    Model of the game
    """

    def __init__(
        self, board: list = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0], board_size = 6
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


    def distr_pebbles(self, pit: Literal[PITS], player: int):
        assert pit in self.get_legal_moves(
            player
        ), f"The chosen {pit} is not in the set of legal moves for player {player}"

        pebbles = self.board[pit]

        self.board[pit] = 0

        while pebbles > 0:

            pit = 0 if pit == 13 else pit + 1

            if not pit == self.player_pits[self.opposite_player(player)]:
                self.board[pit] += 1
                pebbles -= 1
                self.steal_opposite_houses(player, pit)

        extra_turn = ((player == 0) and (pit == 6)) or ((player == 1) and (pit == 13))

        return extra_turn

    def steal_opposite_houses(self, player, pit):

        if not self.is_plyr_house(pit,player):
            return

        player_houses = self.player_houses[player]
        opposite_houses = self.player_houses[self.opposite_player(player)].reverse()
        steal = False

        player_house_index = player_houses.index(pit)

        steal = (
            self.board[pit] == 0 and self.board[opposite_houses[player_house_index]] > 0
        )

        if steal:
            player_pit = self.player_pits[player]
            self.board[player_pit] += self.board[opposite_houses[player_house_index]]
            self.board[opposite_houses[player_house_index]] = 0


if __name__ == "__main__":
    test = Game()
    moves1 = test.get_legal_moves(0)
    moves2 = test.get_legal_moves(1)

    print(
        test.is_plyr_house(5, 0),
        test.is_plyr_house(1, 0),
        test.is_plyr_house(12, 0),
        test.is_plyr_house(6, 0),
    )
    print(
        test.is_plyr_house(5, 1),
        test.is_plyr_house(1, 1),
        test.is_plyr_house(12, 1),
        test.is_plyr_house(6, 1),
    )

    print(
        test.is_end_match(), test.has_move(1), test.has_move(0),
    )

    test1 = Game([0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 24])
    print(test1.is_end_match(), test1.has_move(1), test1.has_move(0), test1.is_win())
