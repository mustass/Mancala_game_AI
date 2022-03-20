from copy import deepcopy
from mancala import Mancala
from heuristics import GameScore, Heuristic


class AlphaBetaPlayer:
    def __init__(self, game: Mancala, max_depth, heuristic: Heuristic) -> None:
        self.game = game
        self.max_depth = max_depth

        self.GameScore = GameScore(self.game)
        self.Heuristic = heuristic(self.game)

        self.alpha = -1000000
        self.beta = 1000000

    def think(self, board, player):

        _, move = self.alpha_beta_algorithm(
            board, self.max_depth, player, self.alpha, self.beta
        )

        return move

    def alpha_beta_algorithm(
        self, board, depth, player, alpha, beta, extra_turn=False, verbose=False
    ):

        board = deepcopy(board)
        alpha = deepcopy(alpha)
        beta = deepcopy(beta)
        # Change turns every repetition except in the beginning or if the player has an extra turn
        if depth != self.max_depth and not extra_turn:
            player = self.game.opposite_player(player)

        maximizing = {0: True, 1: False}[player]

        # Has max depth been reached
        if self.game.is_end_match(board):
            score = self.GameScore.score(board, player)
            if verbose:
                print("-" * 88)
                print(f"The game is over with the score {score}")
                print("-" * 88)
            return score, None

        elif depth == 0:
            score = self.Heuristic.score(board, player)
            if verbose:
                print("-" * 88)
                print(f"Reached max_depth with the score {score}")
                print("-" * 88)
            return score, None

        # Is it max or mins turn
        if maximizing:
            stored_value = -99999
            # Generate nodes
            for move in self.game.get_legal_moves(board, player):
                if verbose:
                    print("-" * 88)
                    print(
                        f"Maximizing for player {player} - looking at move: {move} out of {self.game.get_legal_moves(board, player)}\n"
                    )
                    print(board)

                child_board, extra_turn = self.game.distr_pebbles(board, move, player)
                # Max of the max vs max of the min
                value, _ = self.alpha_beta_algorithm(
                    child_board, depth - 1, player, alpha, beta, extra_turn
                )

                if value > stored_value:
                    if verbose:
                        print(
                            f"The stored value {stored_value} was updated with {value} after move {move} "
                        )
                    stored_value = value
                    best_move = move

                alpha = max(alpha, stored_value)

                if beta <= alpha:
                    break
                if verbose:
                    print(f"Stored value for MAX is: {stored_value}")
                    print(f"Stored best move for MAX is: {best_move}")
                    print("-" * 88)
            return stored_value, best_move
        else:
            stored_value = 99999

            for move in self.game.get_legal_moves(board, player):
                if verbose:
                    print("-" * 88)
                    print(
                        f"Minimizing for player {player} - looking at move: {move} out of {self.game.get_legal_moves(board, player)}"
                    )
                    print(board)

                child_board, extra_turn = self.game.distr_pebbles(board, move, player)

                # Min of the min vs min of the max
                value, _ = self.alpha_beta_algorithm(
                    child_board, depth - 1, player, alpha, beta, extra_turn
                )

                if value < stored_value:
                    if verbose:
                        print(
                            f"The stored value {stored_value} was updated with {value} at move {move}"
                        )
                    stored_value = value
                    best_move = move

                beta = min(beta, stored_value)

                if beta <= alpha:
                    break

                if verbose:
                    print(f"Stored value for MIN is: {stored_value}")
                    print(f"Stored best move for MIN is: {best_move}")
                    print("-" * 88)
            return stored_value, best_move
