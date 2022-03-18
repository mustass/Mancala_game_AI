import curses
from argparse import ArgumentParser
from mancala import Mancala, INITIAL_BOARD
from human_player import UIPlayer
from minimax import MiniMaxPlayer
from alphabeta import AlphaBetaPlayer
from mcts import MonteCarloPlayer
from naive_maximizer import NaiveMaximizerPlayer
from heuristics import *

GAME_MODES = ["HvsH", "HvsMM", "HvsAB", "HvsMCTS", "MMvsH", "ABvsH", "MCTSvsH", "NvsH", "HvsN"]

PLAYER_CHOICES = {
    "human": UIPlayer,
    "minimax": MiniMaxPlayer,
    "alphabeta": AlphaBetaPlayer,
    "mcts": MonteCarloPlayer,
    "naive_max": NaiveMaximizerPlayer,
}

HEURISTIC_CHOICES = {"h1": H1, "h2": H2, "h3": H3, "h4": H4, "composite": Composite}


def get_args():
    parser = ArgumentParser(description="Evaluation argument parser")

    parser.add_argument(
        "--heuristic",
        type=str,
        help="Heuristic to use for AI player when applicable.",
        default="h1",
    )

    parser.add_argument(
        "-md",
        "--max_depth",
        type=int,
        help="Max depth for AI player when applicable.",
        default=2,
    )

    parser.add_argument(
        "-numit",
        "--mcts_number_of_iterations",
        type=int,
        help="Number of iterations for AI with MCTS.",
        default=10,
    )

    return parser.parse_args()


class Window:
    def __init__(self, stdscr, ai_args: dict):
        self.screen = stdscr
        curses.curs_set(0)
        self.colors = self.setup_colors()
        self.body_state = "game"

        self.ai_args = ai_args

        self.game, self.players = self.new_game("HvsH", self.ai_args)

        self.nrows, self.ncols = self.screen.getmaxyx()
        self.header = self.screen.subwin(1, self.ncols, 0, 0)
        self.body = self.screen.subwin(self.nrows - 2, self.ncols, 1, 0)
        self.footer = self.screen.subwin(1, self.ncols, self.nrows - 1, 0)

        self.draw_header()
        self.draw_body()
        self.draw_footer()

        curses.doupdate()
        self.main_loop()

    def new_game(self, mode: str, ai_args):

        game = Mancala(board=INITIAL_BOARD)

        if mode[0] == "H":
            player_0 = UIPlayer(game, 0)
        elif mode[0] == "A":
            player_0 = AlphaBetaPlayer(game, ai_args["max_depth"], ai_args["heuristic"])
        elif mode[0:1] == "MM":
            player_0 = MiniMaxPlayer(game, ai_args["max_depth"], ai_args["heuristic"])
        elif mode[0:1] == "MC":
            player_0 = MonteCarloPlayer(game, ai_args["mcts_numit"])
        elif mode[0] == "N":
            player_0 = NaiveMaximizerPlayer(game)
        else:
            raise ValueError

        if mode[-1] == "H":
            player_1 = UIPlayer(game, 1)
        elif mode[-2] == "A":
            player_1 = AlphaBetaPlayer(game, ai_args["max_depth"], ai_args["heuristic"])
        elif mode[len(mode) - 2 :] == "MM":
            player_1 = MiniMaxPlayer(game, ai_args["max_depth"], ai_args["heuristic"])
        elif mode[len(mode) - 2 :] == "TS":
            player_1 = MonteCarloPlayer(game, ai_args["mcts_numit"])
        elif mode[-1] == "N":
            player_1 = NaiveMaximizerPlayer(game)
        else:
            raise ValueError

        players = [player_0, player_1]

        return game, players

    def main_loop(self):
        while True:
            c = self.screen.getch()
            if c == ord("q"):
                exit()
            elif c == ord("h"):
                self.body_state = "help"
                self.draw_body()
            elif c == ord("g"):
                self.body_state = "game"
                self.draw_body()
            elif c == curses.KEY_RESIZE:
                self.nrows, self.ncols = self.screen.getmaxyx()
                self.header = self.screen.subwin(1, self.ncols, 0, 0)
                self.body = self.screen.subwin(self.nrows - 2, self.ncols, 1, 0)
                self.footer = self.screen.subwin(1, self.ncols, self.nrows - 1, 0)

                self.draw_header()
                self.draw_body()
                self.draw_footer()

            elif self.body_state == "choices":
                if c == ord("1"):
                    self.game, self.players = self.new_game(GAME_MODES[0], self.ai_args)
                    self.body_state = "game"
                elif c == ord("2"):
                    self.game, self.players = self.new_game(GAME_MODES[1], self.ai_args)
                    self.body_state = "game"
                elif c == ord("3"):
                    self.game, self.players = self.new_game(GAME_MODES[2], self.ai_args)
                    self.body_state = "game"
                elif c == ord("4"):
                    self.game, self.players = self.new_game(GAME_MODES[3], self.ai_args)
                    self.body_state = "game"
                elif c == ord("5"):
                    self.game, self.players = self.new_game(GAME_MODES[4], self.ai_args)
                    self.body_state = "game"
                elif c == ord("6"):
                    self.game, self.players = self.new_game(GAME_MODES[5], self.ai_args)
                    self.body_state = "game"
                elif c == ord("7"):
                    self.game, self.players = self.new_game(GAME_MODES[6], self.ai_args)
                    self.body_state = "game"
                elif c == ord("8"):
                    self.game, self.players = self.new_game(GAME_MODES[7], self.ai_args)
                    self.body_state = "game"
                elif c == ord("9"):
                    self.game, self.players = self.new_game(GAME_MODES[8], self.ai_args)
                    self.body_state = "game"
                self.draw_body()

            elif self.body_state == "game":
                curr_player = self.players[self.game.player]
                is_top_player = self.game.player == 0
                if c == ord("n"):
                    self.body_state = "choices"
                elif c == curses.KEY_LEFT:
                    if isinstance(curr_player, UIPlayer):
                        curr_player.dec() if is_top_player else curr_player.inc()
                elif c == curses.KEY_RIGHT:
                    if isinstance(curr_player, UIPlayer):
                        curr_player.inc() if is_top_player else curr_player.dec()
                elif c == curses.KEY_ENTER or c == 10 or c == 13:
                    if not isinstance(curr_player, UIPlayer):
                        next_move = curr_player.think(self.game.board, self.game.player)
                    else:
                        next_move = curr_player.move
                    if next_move is not None:
                        new_board, extra_move = self.game.distr_pebbles(
                            self.game.board, next_move, self.game.player
                        )
                        self.game.update_game_board(new_board)
                        if not extra_move:
                            self.game.switch_player()
                        if self.game.is_end_match(self.game.board):
                            self.body_state = "gameover"
                self.draw_body()

            elif self.body_state == "gameover":
                if c == ord("n"):
                    self.body_state = "choices"
                self.draw_body()
            curses.doupdate()

    def setup_colors(self):
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        return {
            color: curses.color_pair(idx + 1)
            for idx, color in enumerate(["black", "red", "green"])
        }

    def draw_header(self):
        self.header.clear()
        self.header.bkgd(curses.A_REVERSE)
        header_str = "Mancala v0.1"
        self.header.addstr(0, (self.ncols - len(header_str)) // 2, header_str)
        self.header.noutrefresh()

    def draw_footer(self):
        self.footer.clear()
        self.footer.bkgd(curses.A_REVERSE)
        footer_items = [["New Game: n", "Help: h", "Return to Game: g"], ["Quit: q"]]
        footer_str_parts = ["    ".join(item_list) for item_list in footer_items]
        footer_str = (
            " "
            + footer_str_parts[0]
            + " " * (self.ncols - 2 - sum([len(part) for part in footer_str_parts]))
            + footer_str_parts[1]
        )
        # footer_str = footer_str_parts[0] + " " + footer_str_parts[1]
        self.footer.addstr(footer_str)
        self.footer.noutrefresh()

    def draw_body(self):
        if self.body_state == "game":
            self.draw_game()
        elif self.body_state == "help":
            self.draw_help()
        elif self.body_state == "choices":
            self.draw_choices()
        elif self.body_state == "gameover":
            self.draw_gameover()

    def draw_gameover(self):
        self.body.clear()
        winner = self.game.is_win(self.game.board)
        if winner is not None:
            if isinstance(self.players[winner], UIPlayer) and isinstance(
                self.players[self.game.opposite_player(winner)], UIPlayer
            ):
                string = f"""
                    Well Done Player {winner}! 
                    You won with {self.game.board[self.game.player_pits[winner]]} points. 
                    """
            elif isinstance(self.players[winner], UIPlayer) and not isinstance(
                self.players[self.game.opposite_player(winner)], UIPlayer
            ):
                string = f"""
                    Well Done!
                    You defeated the AI with {self.game.board[self.game.player_pits[winner]]} points. 
                    """
            else:
                string = f"""
                    Close but no cigar!
                    You lost to AI with score {self.game.board[self.game.player_pits[winner]]} against  {self.game.board[self.game.player_pits[self.game.opposite_player(winner)]]}. 
                    
                    Try again. 
                    """
        else:
            string = "It's a draw!"

        for idx, line in enumerate(string.split("\n")):
            self.body.addstr(idx, 0, line)

        self.body.noutrefresh()

    def draw_help(self):
        self.body.clear()

        help_str = """
            Game Game:
                - Board Size: 2x6
                - Pebbles per pit: 4
                - Move ending on player's house results in free turn
                - Move ending on an empty pit "captures" all seeds from the opposite pit
                - Player never seeds opponent's house
            Controls:
                - Left and Right Arrow Key to select hole
                - Enter for simple move
        """

        for idx, line in enumerate(help_str.split("\n")):
            self.body.addstr(idx, 0, line)

        self.body.noutrefresh()

    def draw_choices(self):
        self.body.clear()

        help_str = """
            Choose Game Mode:
                - 1: Human vs. Human
                - 2: Human vs. MiniMax AI
                - 3: Human vs. AlfaBeta AI
                - 4: Human vs. Monte Carlo Tree Search AI
                - 5: MiniMax AI vs. Human 
                - 6: AlfaBeta AI vs. Human
                - 7: Monte Carlo Tree Search AI vs. Human 
                - 8: Naive Maximizer vs. Human
                - 9: Human vs. Naive Maximizer
        """

        for idx, line in enumerate(help_str.split("\n")):
            self.body.addstr(idx, 0, line)

        self.body.noutrefresh()

    def draw_game(self):
        self.body.clear()

        height, width = 1, 4
        cell_y, cell_x = (2, 14 // 2 + 1)
        total_height, total_width = cell_y * (height + 1) + 1, cell_x * (width + 1) + 1

        nrows, ncols = self.body.getmaxyx()
        uly, ulx = (nrows - total_height) // 2, (ncols - total_width) // 2
        lry, lrx = (uly + total_height - 1, ulx + total_width - 1)

        # Draw hlines
        for idx_y in range(cell_y + 1):
            pos_y = uly + idx_y * (height + 1)
            for idx_x in range(cell_x):
                pos_x = ulx + idx_x * (width + 1)
                if idx_y == 0:
                    if idx_x == 0:
                        self.body.addch(pos_y, pos_x, curses.ACS_ULCORNER)
                    else:
                        self.body.addch(pos_y, pos_x, curses.ACS_TTEE)
                    self.body.hline(pos_y, pos_x + 1, curses.ACS_HLINE, width)
                elif idx_y == 1:
                    if idx_x == 0:
                        self.body.addch(pos_y, pos_x, curses.ACS_VLINE)
                    elif idx_x == 1:
                        self.body.addch(pos_y, pos_x, curses.ACS_LTEE)
                    elif idx_x == cell_x - 1:
                        self.body.addch(pos_y, pos_x, curses.ACS_RTEE)
                    else:
                        self.body.addch(pos_y, pos_x, curses.ACS_PLUS)
                    if idx_x != 0 and idx_x != cell_x - 1:
                        self.body.hline(pos_y, pos_x + 1, curses.ACS_HLINE, width)
                else:
                    if idx_x == 0:
                        self.body.addch(pos_y, pos_x, curses.ACS_LLCORNER)
                    else:
                        self.body.addch(pos_y, pos_x, curses.ACS_BTEE)
                    self.body.hline(pos_y, pos_x + 1, curses.ACS_HLINE, width)
            if idx_y == 0:
                self.body.addch(pos_y, lrx, curses.ACS_URCORNER)
            elif idx_y == 1:
                self.body.addch(pos_y, lrx, curses.ACS_VLINE)
            else:
                self.body.addch(pos_y, lrx, curses.ACS_LRCORNER)

        # Draw vlines
        for idx_y in range(cell_y):
            pos_y = uly + idx_y * (height + 1) + 1
            for idx_x in range(cell_x + 1):
                pos_x = ulx + idx_x * (width + 1)
                self.body.vline(pos_y, pos_x, curses.ACS_VLINE, height)

        # Fill values
        pos_y = uly + (height + 1) // 2
        for idx_x in range(cell_x - 2):
            pos_x = ulx + (idx_x + 1) * (width + 1) + (width) // 2
            self.body.addstr(
                pos_y, pos_x, "%2d" % self.game.board[idx_x], self.colors["red"]
            )
            self.body.addstr(
                pos_y + (height + 1),
                pos_x,
                "%2d" % self.game.board[-idx_x - 2],
                self.colors["green"],
            )
        self.body.addstr(
            uly + height + 1,
            lrx - width // 2 - 1,
            "%2d" % self.game.board[6],
            self.colors["red"],
        )
        self.body.addstr(
            uly + height + 1,
            ulx + width // 2,
            "%2d" % self.game.board[13],
            self.colors["green"],
        )

        if self.game.is_end_match(self.game.board):
            # Final state
            if self.game.board[6] > self.game.board[13]:
                final_string = "Top player wins"
            elif self.game.board[6] < self.game.board[13]:
                final_string = "Bottom Player wins"
            else:
                final_string = "Draw"
            self.body.addstr(lry + 2, (ncols - len(final_string)) // 2, final_string)
        else:
            # Highlight next move
            curr_player = self.players[self.game.player]
            if isinstance(curr_player, UIPlayer):
                move_idx = (
                    self.game.player * (self.game.board_sz + 1) + curr_player.nxt_pos
                )
                move_format = (
                    self.colors["green"] if self.game.player else self.colors["red"]
                ) | (curses.A_UNDERLINE)
                pos_y = uly + self.game.player * (height + 1) + (height + 1) // 2
                if self.game.player == 0:
                    pos_x = ulx + (curr_player.nxt_pos + 1) * (width + 1) + (width) // 2
                else:
                    pos_x = (
                        lrx - (curr_player.nxt_pos + 1) * (width + 1) - (width) // 2 - 1
                    )
                self.body.addstr(
                    pos_y, pos_x, "%2d" % self.game.board[move_idx], move_format
                )

        self.body.noutrefresh()


if __name__ == "__main__":
    args = get_args()

    ai_args = {
        "heuristic": HEURISTIC_CHOICES[args.heuristic],
        "max_depth": args.max_depth,
        "mcts_numit": args.mcts_number_of_iterations,
    }

    curses.wrapper(Window, ai_args)
