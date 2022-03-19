import math
import random
from typing import Literal
from mancala import Mancala
from copy import deepcopy

# random.seed(10)
class MCTSNode:
    def __init__(
        self, move: int, player: Literal[0, 1], parent=None
    ):  # move is from parent to node
        self.move, self.parent, self.player, self.children = move, parent, player, []
        self.wins, self.visits = 0, 0

    def expand_node(
        self, is_terminal_node: bool, func_get_legal_moves, board: list, player: int,
    ):
        if not is_terminal_node:
            for move in func_get_legal_moves(board, player):
                nc = MCTSNode(move, player, self)  # new child node
                self.children.append(nc)

    def update(self, player_won):
        self.visits += 1
        if player_won is not None and self.parent is not None and self.parent.player == player_won:
            self.wins += 1
        elif self.parent is None and self.player == player_won:
            self.wins += 1

    @property
    def is_leaf(self):
        return len(self.children) == 0

    @property
    def has_parent(self):
        return self.parent is not None

    @property
    def UCB(self):
        if self.visits == 0:
            return 1e5
        return self.wins / self.visits + math.sqrt(
            2 * math.log(self.parent.visits) / self.visits
        )


class MonteCarloPlayer:
    def __init__(self, game: Mancala, num_iterations: int) -> None:
        self.game = game
        self.num_iterations = num_iterations

    def think(self, board, player):

        _, move = self.mcts_algorithm(board, player)

        return move

    def mcts_algorithm(self, board, player):
        root_node = MCTSNode(None, player, None)
        for _ in range(self.num_iterations):
            n, _board, _player = root_node, deepcopy(board), deepcopy(player)
            moves_seq = []
            while not n.is_leaf:  # select leaf
                n = self.tree_policy_child(n)
                moves_seq.append((n.move, n.player))

            if len(moves_seq) > 0:
                _board, _player = self.play_game_sequence(_board, moves_seq)
            n.expand_node(
                self.game.is_end_match(_board),
                self.game.get_legal_moves,
                _board,
                _player,
            )  # expand
            if not self.game.is_end_match(_board):
                n = self.tree_policy_child(n)

            while not self.game.is_end_match(_board):  # simulate
                _board, _player = self.simulation_policy_child(_board, _player)
            player_won = self.game.is_win(_board)
            while n.has_parent:  # propagate
                n.update(player_won)
                n = n.parent
            # Root node has to be updated as well
            n.update(player_won)

        return self.select_action(root_node)

    def tree_policy_child(self, node: MCTSNode):
        assert not node.is_leaf, "The node must be expanded"

        if all([child.visits == 0 for child in node.children]):
            return node.children[0]
        else:
            selected_node = None
            ucb = -1
            for nd in node.children:
                if nd.UCB > ucb:
                    selected_node = nd
                    ucb = nd.UCB
            return selected_node

    def select_action(self, root_node: MCTSNode):
        selected_node = None
        ucb = 0
        for nd in root_node.children:
            if nd.UCB > ucb:
                selected_node = nd
                ucb = nd.UCB
        return ucb, selected_node.move

    def simulation_policy_child(self, board, player):
        available_moves = self.game.get_legal_moves(board, player)
        move = random.choice(available_moves)
        board, player = self.play_game_sequence(board, [(move, player)])
        return board, player

    def score_outcome(self, board, root_node: MCTSNode):
        if (
            self.game.is_win(board) is not None
            and self.game.is_win(board) == root_node.player
        ):
            return 1
        return 0

    def play_game_sequence(self, board: list, moves: list):

        for _, elmnt in enumerate(moves):
            board, extra_move = self.game.distr_pebbles(board, elmnt[0], elmnt[1])
        return board, elmnt[1] if extra_move else self.game.opposite_player(elmnt[1])
