import curses
from typing import Literal
from game import Game


class UIPlayer:
    def __init__(self, game, player_number: Literal[0, 1], AI=None):
        self.game = game
        self.player_number = player_number
        self.nxt_pos = 0
        self.is_ai = False
        if AI is not None:
            self.is_ai = True
            self.AI = AI

    @property
    def move(self):
        nxt_move = self.nxt_pos if self.player_number == 0 else self.nxt_pos + 7
        if nxt_move in self.game.get_legal_moves(self.player_number):
            return nxt_move
        else:
            return None

    def inc(self):
        self.nxt_pos = min(self.nxt_pos + 1, self.game.board_sz - 1)

    def dec(self):
        self.nxt_pos = max(self.nxt_pos - 1, 0)


class Window:
    def __init__(self, stdscr):
        self.screen = stdscr
        curses.curs_set(0)
        self.colors = self.setup_colors()
        self.body_state = "game"

        self.game, self.players = self.new_game()

        self.nrows, self.ncols = self.screen.getmaxyx()
        self.header = self.screen.subwin(1, self.ncols, 0, 0)
        self.body = self.screen.subwin(self.nrows - 2, self.ncols, 1, 0)
        self.footer = self.screen.subwin(1, self.ncols, self.nrows - 1, 0)

        self.draw_header()
        self.draw_body()
        self.draw_footer()

        curses.doupdate()
        self.main_loop()

    def new_game(self):
        game = Game()
        players = [UIPlayer(game, 0), UIPlayer(game, 1)]
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

            elif self.body_state == "game":
                curr_player = self.players[self.game.player]
                is_top_player = self.game.player == 0
                if c == ord("n"):
                    self.game.board, self.players = self.new_game()
                elif c == curses.KEY_LEFT:
                    curr_player.dec() if is_top_player else curr_player.inc()
                elif c == curses.KEY_RIGHT:
                    curr_player.inc() if is_top_player else curr_player.dec()
                elif c == curses.KEY_ENTER or c == 10 or c == 13:
                    if curr_player.move is not None:
                        extra_move = self.game.distr_pebbles(
                            curr_player.move, curr_player.player_number
                        )
                        if not extra_move:
                            self.game.switch_player()
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
        else:
            self.draw_help()

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

        if self.game.is_end_match():
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

            if curr_player.is_ai == True:
                curr_player.think()

            move_idx = self.game.player * (self.game.board_sz + 1) + curr_player.nxt_pos
            move_format = (
                self.colors["green"] if self.game.player else self.colors["red"]
            ) | (curses.A_UNDERLINE)
            pos_y = uly + self.game.player * (height + 1) + (height + 1) // 2
            if self.game.player == 0:
                pos_x = ulx + (curr_player.nxt_pos + 1) * (width + 1) + (width) // 2
            else:
                pos_x = lrx - (curr_player.nxt_pos + 1) * (width + 1) - (width) // 2 - 1
            self.body.addstr(
                pos_y, pos_x, "%2d" % self.game.board[move_idx], move_format
            )

        self.body.noutrefresh()


if __name__ == "__main__":
    curses.wrapper(Window)
