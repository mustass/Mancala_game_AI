import json
from pathlib import Path
from argparse import ArgumentParser
from mancala import Mancala
from alphabeta import AlphaBetaPlayer
from minimax import MiniMaxPlayer
from mcts import MonteCarloPlayer
from naive_maximizer import NaiveMaximizerPlayer
from heuristics import *
from run_game import Match
from tqdm import tqdm


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
        required=False,
        help="Heuristic to use for AI player 0",
        default="h1",
    )

    parser.add_argument(
        "-h1",
        "--heuristic1",
        type=str,
        required=False,
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

    parser.add_argument(
        "-r",
        "--repeats",
        type=int,
        help="Number of repeats to run the experiment for.",
        default=100,
    )

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Name the experiment",
        default="blissful_elephant",
    )

    return parser.parse_args()


AI_CHOICES = {
    "minimax": MiniMaxPlayer,
    "alphabeta": AlphaBetaPlayer,
    "mcts": MonteCarloPlayer,
    "naive_max": NaiveMaximizerPlayer,
}

HEURISTIC_CHOICES = {"h1": H1, "h2": H2, "h3": H3, "h4": H4, "composite": Composite}


def main():
    args = get_args()
    print(args)

    result_sequence = []

    for i in tqdm(range(args.repeats)):
        game = Mancala()

        if AI_CHOICES[args.player0] is MonteCarloPlayer:
            player_0 = AI_CHOICES[args.player0](game, args.mcts_number_of_it_0)
        elif AI_CHOICES[args.player0] is NaiveMaximizerPlayer:
            player_0 = AI_CHOICES[args.player0](game)
        else:
            player_0 = AI_CHOICES[args.player0](
                game, args.max_depth_0, HEURISTIC_CHOICES[args.heuristic0]
            )

        if AI_CHOICES[args.player1] is MonteCarloPlayer:
            player_1 = AI_CHOICES[args.player1](game, args.mcts_number_of_it_1)
        elif AI_CHOICES[args.player1] is NaiveMaximizerPlayer:
            player_1 = AI_CHOICES[args.player1](game)
        else:
            player_1 = AI_CHOICES[args.player1](
                game, args.max_depth_1, HEURISTIC_CHOICES[args.heuristic1]
            )

        match = Match(game, player_0, player_1)
        result_sequence.append(match.run(verbose=False))
        match.run()

    experiment_name = f"{args.player0}_vs_{args.player1}_{args.repeats}_{args.name}"

    destination_path = Path("./experiments") / experiment_name

    destination_path.mkdir(exist_ok=True)

    with open(destination_path / "results.txt", "w") as f:
        for item in result_sequence:
            f.write("%s\n" % item)

    with open(destination_path / "args.txt", "w") as f:
        f.write(json.dumps(vars(args)))


if __name__ == "__main__":
    main()
