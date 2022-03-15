from argparse import ArgumentParser

from mancala import Mancala
from alphabeta import AlphaBetaPlayer
from minimax import MiniMaxPlayer
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
                print(f"Board at iteration {iteration}:")
                print(
                    "Player0 | houses: ",
                    self.game.board[self.game.player_houses[0]],
                    " | pit: ",
                    self.game.board[self.game.player_pits[0]],
                )
                print(
                    "Player1 | houses: ",
                    self.game.board[self.game.player_houses[1]],
                    " | pit: ",
                    self.game.board[self.game.player_pits[1]],
                )
                print("\n", "=" * 88, "\n")

            move = {0: self.player_0, 1: self.player_1}[self.game.player].think(
                self.game.board, self.game.player
            )

            if verbose:
                print(f"Player {self.game.player} chose move {move}")
                print("\n", "=" * 88, "\n")

            next_board, extra_move = self.game.distr_pebbles(
                self.game.board, move, self.game.player
            )
            self.game.update_game_board(next_board)

            if not extra_move:
                self.game.switch_player()

            iteration += 1

            print(f"\nFinal board:")
            print(
                "Player0 | houses: ",
                self.game.board[self.game.player_houses[0]],
                " | pit: ",
                self.game.board[self.game.player_pits[0]],
            )
            print(
                "Player1 | houses: ",
                self.game.board[self.game.player_houses[1]],
                " | pit: ",
                self.game.board[self.game.player_pits[1]],
            )
            print("\n", "=" * 88, "\n")
            print(f"Player {self.game.is_win(self.game.board)} wins!")


AI_CHOICES = {"minimax": MiniMaxPlayer, "alphabeta": AlphaBetaPlayer}

HEURISTIC_CHOICES = {"h1": H1, "h2": H2, "h3": H3, "h4": H4, "composite": Composite}


def main():
    args = get_args()
    game = Mancala()

    player_0 = AI_CHOICES[args.player0](
        game, args.max_depth_0, HEURISTIC_CHOICES[args.heuristic0]
    )
    player_1 = AI_CHOICES[args.player1](
        game, args.max_depth_1, HEURISTIC_CHOICES[args.heuristic1]
    )

    match = Match(game, player_0, player_1)

    match.run()


if __name__ == "__main__":
    main()
