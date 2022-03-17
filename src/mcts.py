import math
import random
from typing import Literal
from mancala import Mancala
from copy import deepcopy


class MCTSNode:
    def __init__(
        self, move: int, player: Literal[0, 1], parent=None
    ):  # move is from parent to node
        self.move, self.parent, self.player, self.children = move, parent, player, []
        self.wins, self.visits = 0, 0

    def expand_node(
        self,
        func_check_terminal: function,
        func_get_legal_moves: function,
        func_get_extra_move: function,
        board: list,
        player: int,
    ):
        if not func_check_terminal(board):
            for move in func_get_legal_moves(board, player):
                # This is to know if there is an extra move
                _, extra_move = func_get_extra_move(board, move, player)
                # Naive next player
                child_player = 0 if self.player == 1 else 1
                # Make sure to pass the correct next player
                nc = MCTSNode(
                    move, player if extra_move else child_player, self
                )  # new child node
                self.children.append(nc)

    def update(self, r):
        self.visits += 1
        self.wins += r

    @property
    def is_leaf(self):
        return len(self.children) == 0

    @property
    def has_parent(self):
        return self.parent is not None

    @property
    def UCB(self):
        return self.wins / self.visits + math.sqrt(
            2 * math.log(self.parent.visits) / self.visits
        )


class MonteCarloPlayer:
    def __init__(self, game: Mancala, num_iterations: int) -> None:
        self.game = game
        self.num_iterations = num_iterations

    def think(self, board, player):

        _, move = self.mcts_algorithm(board, player, self.num_iterations)

        return move

    def mcts_algorithm(self, board, player):
        root_node = MCTSNode(None, player, None)

        for _ in range(self.num_iterations):
            n, board = root_node, deepcopy(board)
            moves_seq = []
            while not n.is_leaf():  # select leaf
                n = self.tree_policy_child(n)
                moves_seq.append((n.move, n.player))

            board, player = self.play_game_sequence(board, moves_seq)

            n.expand_node(
                self.game.is_end_match, self.game.get_legal_moves, board, player
            )  # expand

            n = self.tree_policy_child(n)

            while not self.game.is_end_match(board):  # simulate
                board, player = self.simulation_policy_child(board, player)
            result = self.score_outcome(board, root_node)
            while n.has_parent():  # propagate
                n.update(result)
                n = n.parent

        return self.select_action(root_node)

    def tree_policy_child(self, node: MCTSNode):

        if not node.is_leaf:
            selected_node = None
            ucb = 0
            for nd in node.children:
                if nd.UCB > ucb:
                    selected_node = nd
                    ucb = nd.UCB
            return selected_node
        else:
            if node.visits == 0:
                return node
            else:
                return node.children[0]

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
        board, player = self.play_game_sequence(board, (move, player))
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
