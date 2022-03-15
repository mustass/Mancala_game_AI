from mancala import Mancala
from heuristics import GameScore, Heuristic


class MiniMaxPlayer:
    def __init__(self, game: Mancala, max_depth, heuristic: Heuristic) -> None:
        self.game = game
        self.max_depth = max_depth
        self.GameScore = GameScore(self.game)
        self.Heuristic = heuristic(self.game)

    def think(self, board, player):

        _, move = self.minimax_algorithm(board, self.max_depth, player)

        return move

    def minimax_algorithm(self, board, depth, player, extra_turn=False):

        # Change turns every repetition except in the beginning or if the player has an extra turn
        if depth != self.max_depth and not extra_turn:
            player = self.game.opposite_player(player)

        maximizing = {0: True, 1: False}[player]

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

                child_board, extra_turn = self.game.distr_pebbles(board, move, player)

                # Max of the max vs max of the min
                value, _ = self.minimax_algorithm(
                    child_board, depth - 1, player, extra_turn
                )

                if value > stored_value:
                    print(
                        f"The stored value {stored_value} was updated with {value} at move {move}"
                    )
                    stored_value = value
                    best_move = move

                print(f"stored value vs value for MAX is: {stored_value} vs {value}")
                print(f"stored best move vs i for MAX is: {best_move} vs {move}")

            return stored_value, move
        else:
            stored_value = 99999

            for move in self.game.get_legal_moves(board, player):
                print(f"Minimizing - pick: {move}")

                child_board, extra_turn = self.game.distr_pebbles(board, move, player)

                # Min of the min vs min of the max
                value, _ = self.minimax_algorithm(
                    child_board, depth - 1, player, extra_turn
                )

                if value < stored_value:
                    print(
                        f"The stored value {stored_value} was updated with {value} at move {move}"
                    )
                    stored_value = value
                    best_move = move

                print(f"Stored value vs value for MIN is: {stored_value} vs {value}")
                print(f"Stored best move vs i for MIN is: {best_move} vs {move}")

            return stored_value, move
