from typing import Literal


class Game:
    """
    Model of the game
    """

    def __init__(
        self, board: list = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    ) -> None:
        assert len(board) == 14
        assert sum(board) == 48

        self.board = board

        self.player_houses = {0: [0, 1, 2, 3, 4, 5], 1: [7, 8, 9, 10, 11, 12]}

        self.player_pits = {0: 6, 1: 13}

        print(f"Initialized the board{board}")

    def get_legal_moves(self, player: Literal = [0, 1]) -> list:
        moves = {
            0: [
                i for i, e in enumerate(self.board) if e != 0 and i not in self.player_houses[1] + [v for k,v in self.player_pits.items()]
            ],
            1: [i for i, e in enumerate(self.board) if e != 0 and i not in self.player_houses[0] + [v for k,v in self.player_pits.items()]
            ],
        }[player]
        return moves

    def is_plyr_house(
        self, pit: Literal = [range(0, 14)], player: Literal = [0, 1]
    ) -> bool:
        return pit in self.player_houses[player]

    def has_move(self, player: Literal = [0, 1]) -> bool:
        legal_moves = self.get_legal_moves(player)
        print(legal_moves)
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
    print(
        test1.is_end_match(), test1.has_move(1), test1.has_move(0),test1.is_win()
    )