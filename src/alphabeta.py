from mancala import Mancala
from heuristics import GameScore, Heuristic


class AlphaBetaPlayer:
    def __init__(self, game: Mancala, max_depth, heuristic: Heuristic) -> None:
        self.game = game
        self.max_depth = max_depth

        self.beta = 1000000
        self.alpha = -1000000

        self.GameScore = GameScore(self.game)
        self.Heuristic = heuristic(self.game)

    def think(self, board, player):

        _, move = self.alpha_beta_algorithm(board, self.max_depth, player)

        return move

    def alpha_beta_algorithm(self, board, depth, player, maximizing=True):

        # Change turns every repetition
        if depth != self.max_depth:
            player = self.game.opposite_player(player)

        print(f"Depth is: {depth}, player {player}\n")
        print(board)
        print(f"\nAvailable moves are: {self.game.get_legal_moves(board, player)}\n")

        # Has max depth been reached
        if self.game.is_end_match(board):
            score = self.GameScore.score(board, player)
            print(score)
            print("-" * 88)
            return score, None

        elif depth == 0:
            score = self.Heuristic.score(board, player)
            print(score)
            print("-" * 88)
            return score, None

        # Is it max or mins turn
        if maximizing:
            stored_value = -99999
            # Generate nodes
            for move in self.game.get_legal_moves(board, player):
                print(f"Maximizing - pick: {move}")

                child_board, extra_turn = self.game.distr_pebbles(
                    board, move, player, AI="eval"
                )

                # Max of the max vs max of the min
                if extra_turn:
                    print("Getting an extra turn")
                    value, _ = self.alpha_beta_algorithm(
                        child_board, depth - 1, player, True
                    )
                else:
                    value, _ = self.alpha_beta_algorithm(
                        child_board, depth - 1, player, False
                    )

                if value > stored_value:
                    print(
                        f"The stored value {stored_value} was updated with {value} at move {move}"
                    )
                    stored_value = value
                    best_move = move

                if value >= self.beta:
                    break
                self.alpha = max(self.alpha, stored_value)

                print(f"stored value vs value for MAX is: {stored_value} vs {value}")
                print(f"stored best move vs i for MAX is: {best_move} vs {move}")

            return stored_value, move
        else:
            stored_value = 99999

            for move in self.game.get_legal_moves(board, player):
                print(f"Minimizing - pick: {move}")

                child_board, extra_turn = self.game.distr_pebbles(
                    board, move, player, AI="eval"
                )

                # Min of the min vs min of the max
                if extra_turn:
                    value = self.alpha_beta_algorithm(
                        child_board, depth - 1, player, False
                    )[0]
                else:
                    value = self.alpha_beta_algorithm(
                        child_board, depth - 1, player, True
                    )[0]
                if value < stored_value:
                    print(
                        f"The stored value {stored_value} was updated with {value} at move {move}"
                    )
                    stored_value = value
                    best_move = move

                if value <= self.alpha:
                    break
                self.beta = min(self.beta, stored_value)

                print(f"Stored value vs value for MIN is: {stored_value} vs {value}")
                print(f"Stored best move vs i for MIN is: {best_move} vs {move}")

            return stored_value, move
