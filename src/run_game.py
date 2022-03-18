from argparse import ArgumentParser
from copy import deepcopy
from mancala import Mancala
from alphabeta import AlphaBetaPlayer
from minimax import MiniMaxPlayer
from mcts import MonteCarloPlayer
from heuristics import *


def get_args():
    parser = ArgumentParser(description="Evaluation argument parser")

    parser.add_argument(
        "-p0",
        "--player0",
        type=str,
        required=True,
        help="Type of AI to play player 0",
        default="minimax",
    )

    parser.add_argument(
        "-p1",
        "--player1",
        type=str,
        required=True,
        help="Type of AI to play player 1",
        default="alphabeta",
    )

    parser.add_argument(
        "-h0",
        "--heuristic0",
        type=str,
        required=True,
        help="Heuristic to use for AI player 0",
        default="h1",
    )

    parser.add_argument(
        "-h1",
        "--heuristic1",
        type=str,
        required=True,
        help="Heuristic to use for AI player 1",
        default="h1",
    )

    parser.add_argument(
        "-md0", "--max_depth_0", type=int, help="Max depth for AI player 0", default=2
    )

    parser.add_argument(
        "-md1", "--max_depth_1", type=int, help="Max depth for AI player 1", default=2
    )

    parser.add_argument(
        "-mcts_n0",
        "--mcts_number_of_it_0",
        type=int,
        help="Number of iterations for MCTS if AI player 0",
        default=10,
    )

    parser.add_argument(
        "-mcts_n1",
        "--mcts_number_of_it_1",
        type=int,
        help="Number of iterations for MCTS if AI player 0",
        default=10,
    )

    return parser.parse_args()


class Match:
    def __init__(self, game: Mancala, player_0, player_1) -> None:
        self.game = game
        self.player_0 = player_0
        self.player_1 = player_1

    def run(self, verbose=True):
        print("Mancala Game match:", "\n\n")

        iteration = 0
        while not self.game.is_end_match(self.game.board):
            if verbose:
                print("\n", "=" * 88, "\n")
                print(f"Board at iteration {iteration}:")
                print(
                    "Player0 | houses: ",
                    [self.game.board[i] for i in self.game.player_houses[0]],
                    " | pit: ",
                    self.game.board[self.game.player_pits[0]],
                )
                print(
                    "Player1 | houses: ",
                    [self.game.board[i] for i in self.game.player_houses[1][::-1]],
                    " | pit: ",
                    self.game.board[self.game.player_pits[1]],
                )
                print("\n", "=" * 88, "\n")
            try:
                move = {0: self.player_0, 1: self.player_1}[self.game.player].think(
                    self.game.board, self.game.player
                )
            except AssertionError:
                print(self.game.board)
                print(self.game.player)
                raise (AssertionError)

            if verbose:
                print(f"Player {self.game.player} chose move {move}")
                print("\n", "=" * 88, "\n")

            try:
                next_board, extra_move = self.game.distr_pebbles(
                    self.game.board, move, self.game.player
                )
            except AssertionError:
                print(self.game.board)
                print(move, self.game.player)
                raise (AssertionError)
            self.game.update_game_board(next_board)

            if not extra_move:
                self.game.switch_player()

            iteration += 1

        print(f"\nFinal board:")
        print(
            "Player0 | houses: ",
            [self.game.board[i] for i in self.game.player_houses[0]],
            " | pit: ",
            self.game.board[self.game.player_pits[0]],
        )
        print(
            "Player1 | houses: ",
            [self.game.board[i] for i in self.game.player_houses[1]],
            " | pit: ",
            self.game.board[self.game.player_pits[1]],
        )
        print("\n", "=" * 88, "\n")
        print(f"Player {self.game.is_win(self.game.board)} wins!")


AI_CHOICES = {
    "minimax": MiniMaxPlayer,
    "alphabeta": AlphaBetaPlayer,
    "mcts": MonteCarloPlayer,
}

HEURISTIC_CHOICES = {"h1": H1, "h2": H2, "h3": H3, "h4": H4, "composite": Composite}


def main():
    args = get_args()
    game = Mancala()

    if AI_CHOICES[args.player0] is MonteCarloPlayer:
        player_0 = AI_CHOICES[args.player0](game, args.mcts_number_of_it_0)
    else:
        player_0 = AI_CHOICES[args.player0](
            game, args.max_depth_0, HEURISTIC_CHOICES[args.heuristic0]
        )

    if AI_CHOICES[args.player1] is MonteCarloPlayer:
        player_1 = AI_CHOICES[args.player1](game, args.mcts_number_of_it_1)
    else:
        player_1 = AI_CHOICES[args.player1](
            game, args.max_depth_1, HEURISTIC_CHOICES[args.heuristic1]
        )

    match = Match(game, player_0, player_1)

    match.run()


if __name__ == "__main__":
    main()
