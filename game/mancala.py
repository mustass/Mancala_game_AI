class Game:
    def main(self):
        # Setup game
        board = self.new_board()

        # Init player
        player = 0

        # start game
        print('Mancala Game!',"\n\n")
        game_over = False
        while not game_over:
            print('Board:')
            print('Player0 | houses: ', self.get_player_pits(board, 0), ' | store: ', self.get_player_store(board, 0))
            print('Player1 | houses: ', self.get_player_pits(board, 1), ' | store: ', self.get_player_store(board, 1))
            print('===================================================',"\n")

            # player makes a move
            board = self.run_turn(board, player)

            # check if player distributed the last pebble
            if self.is_end_match(board):
                # terminate game
                game_over = True

            # switch players
            player = self.switch_players(player)

        # Discover winner
        print('Game over! ', self.is_win(board))
        print('Final Board:')
        print('Player0 | houses: ', self.get_player_pits(board, 0), ' | store: ', self.get_player_store(board, 0))
        print('Player1 | houses: ', self.get_player_pits(board, 1), ' | store: ', self.get_player_store(board, 1))

    def new_board(self):
        # reset/initialise board
        board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        return board

    def get_player_stats(self, board, player):
        split = 7
        if player == 0:
            player_stats = board[:split]
        else:
            player_stats = board[split:]

        return player_stats

    def get_player_store(self, board, player):
        stats = self.get_player_stats(board, player)

        return stats.pop()

    def get_player_pits(self, board, player):
        stats = self.get_player_stats(board, player)

        return stats[:6]

    def get_available_moves(self, board, player):
        # get player pits
        player_pits = self.get_player_pits(board, player)

        # discover available houses
        available_moves = list()
        for index, pit in enumerate(player_pits):
            if pit > 0:
                player_pit_index = index + 1 if player == 0 else index + 8
                available_moves.append(player_pit_index)

        return available_moves

    def has_move(self, board, player):
        player_pits = self.get_player_pits(board, player)
        for index, pit in enumerate(player_pits):
            if pit > 0:
                # player has at least one pit with pebbles!
                return True

        # player does not have pebbles!
        return False

    def is_plyr_house(self, player, pit):
        # get player houses
        player_pits = [0, 1, 2, 3, 4, 5] if player == 0 else [7, 8, 9, 10, 11, 12]

        # check house belongs to player
        return pit in player_pits

    def is_end_match(self, board):
        total = self.get_player_store(board, 0) + self.get_player_store(board, 1)
        return total == 48

    def is_win(self, board):
        if self.get_player_store(board, 0) > self.get_player_store(board, 1):
            return "Player0 wins!"
        elif self.get_player_store(board, 0) < self.get_player_store(board, 1):
            return "Player1 wins!"
        else:
            return "It's a tie!"

    def steal_all_opponent_pebbles(self, board, player):
        # check if player empties all houses and steal opponents pebbles
        availableMoves = self.get_available_moves(board, player)
        if len(availableMoves) == 0:
            opponent = self.switch_players(player)
            opponentPits = self.get_player_pits(board, opponent)
            steal = 0
            for index, pit in enumerate(opponentPits):
                steal += pit
                board[index] = 0

            index = 6 if player == 0 else 13
            board[index] += steal

    def steal_opponent_adjacent_house(self, board, player, pit):
        adjacent_pit = pit + 7 if player == 0 else pit - 7
        steal = board[adjacent_pit]
        board[adjacent_pit] = 0
        index = 6 if player == 0 else 13
        board[index] += steal

    def distr_pebbles(self, board, pit, player):
        # distribute pebbles for house in index pit
        if not self.is_plyr_house(player, pit):
            # pit not in player houses
            return board

        # pick pit pebbles
        pickedPebbles = board[pit]
        board[pit] = 0

        # start distr of pebbles
        nextPit = pit
        while pickedPebbles > 0:
            # move to the next pit or circle from the beginning
            nextPit = 0 if nextPit >= 13 else nextPit + 1

            # skip opponent store
            if (player == 0 and nextPit == 13) or (player == 1 and nextPit == 6):
                continue

            # check for single house steal
            if pickedPebbles == 1 and board[nextPit] == 0 and self.is_plyr_house(player, nextPit):
                print('single steal')
                self.steal_opponent_adjacent_house(board, player, nextPit)

            # drop a pebble in the pit
            board[nextPit] += 1
            pickedPebbles -= 1

        return board

    def switch_players(self, player):
        return 0 if player != 0 else 1

    def pick_pit(self, board, player):
        availableMoves = self.get_available_moves(board, player)
        print('Select the position of the house you wish to distribute: ')
        print('House values:')
        print(self.get_player_pits(board, player))
        print('------------------')
        print('The available houses are:')
        print(availableMoves)

        ask = True
        while ask:
            print('>>>')
            pit = int(input())

            # check selected pit is valid
            if pit in availableMoves:
                return pit
            print('Please select an available house, your available houses are: ', availableMoves)

    def run_turn(self, board, player):
        # check player has available moves
        availableMoves = self.get_available_moves(board, player)
        if len(availableMoves) <= 0:
            winner = self.is_win(board)
            return 'Player' + str(player) + 'has no more available moves. ' + winner

        # prompt player to select pit
        pit = self.pick_pit(board, player) - 1
        print('Player', player, 'picked house', pit)

        # distribute pebbles of selected pit
        self.distr_pebbles(board, pit, player)

        # check if player empties all houses and steal all opponents available pebbles
        self.steal_all_opponent_pebbles(board, player)

        return board

if __name__ == "__main__":
    game = Game()
    game.main()
