from mancala import Mancala


class Heuristic:
    def __init__(self, game: Mancala) -> None:
        self.game = game

    def score(self, board, player):
        pass


class GameScore(Heuristic):
    # Just game score
    def __init__(self, game: Mancala) -> None:
        super().__init__(game)

    def score(self, board, player):

        if self.game.is_end_match(board):
            score = board[self.game.player_pits[player]]
            if score > 24:
                score = 999
            elif score < 24:
                score = -999
            else:
                score = 0

        return score


class H1(Heuristic):
    # Keep as many houses empty as possible

    def __init__(self, game: Mancala) -> None:
        super().__init__(game)

    def score(self, board, player):
        pits = self.game.player_houses[player]
        print(pits)
        return sum([1 for pit in pits if board[pit] == 0])


class H2(Heuristic):
    # Have as many moves as possible (opposite of H1 essentially)

    def __init__(self, game: Mancala) -> None:
        super().__init__(game)

    def score(self, board, player):
        pits = self.game.player_houses[player]
        return sum([1 for pit in pits if board[pit] > 0])


class H3(Heuristic):
    # Maximize the difference in pepples in store
    def __init__(self, game: Mancala) -> None:
        super().__init__(game)

    def score(self, board, player):
        store_player = board[self.game.player_pits[player]]
        store_opposite_player = board[
            self.game.player_pits[self.game.opposite_player(player)]
        ]
        return store_player - store_opposite_player


class H4(Heuristic):
    # Maximize the number of pebbles next to player's own pit
    def __init__(self, game: Mancala) -> None:
        super().__init__(game)

    def score(self, board, player):
        return board[self.game.player_pits[player] - 1]


class Composite(Heuristic):
    # When we want a composite one
    def __init__(self, game: Mancala) -> None:
        super().__init__(game)

        self.one = H1()
        self.two = H2()
        self.three = H3()
        self.four = H4()

    def score(self, board, player):
        return (
            self.one.score(board, player)
            + self.two.score(board, player)
            + self.three.score(board, player)
            + 0.1 * self.four.score(board, player)
        )
