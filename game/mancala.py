import random


class Game:
    def main(self):
        # Setup game
        board = self.new_board()
        # Determine whether AI should play. Currently AI plays both turns.
        AI = True

        # Init player
        # The south player plays first
        player = 0
        self.playerrepeat = False
        
        # start game
        print('Mancala Game!',"\n\n")
        game_over = False
        while not game_over:
            print('Board:')
            print('Player1 | houses: ', self.get_player_pits(board, 1)[::-1], ' | store: ', self.get_player_store(board, 1))
            print('Player0 | houses: ', self.get_player_pits(board, 0), ' | store: ', self.get_player_store(board, 0))
            print('===================================================',"\n")

            # player makes a move
            board = self.run_turn(board, player, AI)

            # check if player distributed the last pebble
            if self.is_end_match(board):
                # terminate game
                game_over = True
                #self.steal_all_opponent_pebbles(board, player)
            
            # switch players
            player = self.switch_players(player)

        # Discover winner. Disabled for now.
        #print('Game over! ', self.is_win(board))
        print('Final Board:')
        #print('Player1 | houses: ', self.get_player_pits(board, 1)[::-1], ' | store: ', self.get_player_store(board, 1))
        #print('Player0 | houses: ', self.get_player_pits(board, 0), ' | store: ', self.get_player_store(board, 0))
        print('Player1 |', self.get_player_store(board, 1) + sum(self.get_player_pits(board, 1)))
        print('Player0 |', self.get_player_store(board, 0) + sum(self.get_player_pits(board, 0)))
        
    def new_board(self):
        # reset/initialise board
        board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        #board = [0, 0, 0, 0, 1, 0, 10, 4, 0, 0, 0, 0, 0, 0] # For testing
        return board

    def get_player_stats(self, board, player):
        # Boards split at 7
        split = 7
        if player == 0:
            player_stats = board[:split]
        else:
            player_stats = board[split:]

        return player_stats

    def get_player_store(self, board, player):
        stats = self.get_player_stats(board, player)
        # Return store
        return stats[-1]

    def get_player_pits(self, board, player):
        stats = self.get_player_stats(board, player)
        # Return pits
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
        return ((total == 48) | (sum(self.get_player_pits(board, 0))==0) | (sum(self.get_player_pits(board, 1))==0))

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
            opponent = 1 if player == 0 else 0
            opponentPits = self.get_player_pits(board, opponent)
            steal = 0
            for index, pit in enumerate(opponentPits):
                steal += pit
                #board[index] = 0 # Changed to if/else below because index doesn't match both players
            
            # Set all opponent's pits to zero after stealing pebbles
            if player == 0:
                for i in range(7,13):
                    board[i]=0
            else:
                for i in range(0,6):
                    board[i]=0

            index = 6 if player == 0 else 13
            board[index] += steal
            
        return board

    def steal_opponent_adjacent_house(self, board, player, pit):
        # Some redundant code here
        adjacent_pits=dict(list(enumerate(range(7,13)[::-1],0)))
        if player == 0:
            adjacent_pit = adjacent_pits[pit]
        else:
            reversed = dict((v, k) for k, v in adjacent_pits.items())
            adjacent_pit = reversed[pit]
            
        steal = board[adjacent_pit]+board[pit]
        board[adjacent_pit] = 0
        board[pit]=0
        index = 6 if player == 0 else 13
        board[index] += steal

    def distr_pebbles(self, board, pit, player):
        # distribute pebbles for house in index pit
        self.playerrepeat=False
        if not self.is_plyr_house(player, pit):
            # pit not in player houses
            return board

        # pick pit pebbles
        pickedPebbles = board[pit]
        board[pit] = 0

        # start distr of pebbles
        nextPit = pit
        print('a')
        while pickedPebbles > 0:
            # move to the next pit or circle from the beginning
            nextPit = 0 if nextPit >= 13 else nextPit + 1

            # skip opponent store
            if (player == 0 and nextPit == 13) or (player == 1 and nextPit == 6):
                continue

            # drop a pebble in the pit
            board[nextPit] += 1
            pickedPebbles -= 1
            
        # check for single house steal
        adjacent_dict=dict(list(enumerate(range(7,13)[::-1],0)))
        # First check if final pit is in players row
        if (self.is_plyr_house(player, nextPit)):
            # Next compute adjacent pits
            if player == 0:
                    adjacent_pit = adjacent_dict[nextPit]
            else:
                    reversed = dict((v, k) for k, v in adjacent_dict.items())
                    adjacent_pit = reversed[nextPit]
            
            # Check if there is only 1 pebble in the final pit and adjacent pit is non-empty
            if (board[nextPit] == 1 and board[adjacent_pit]!=0):
                print('single steal')
                # Steal pebbles from adjacent pit
                self.steal_opponent_adjacent_house(board, player, nextPit)
            
        # check if final pebble is in own pit
        self.playerrepeat=(((player==0) & (nextPit==6)) | ((player==1) & (nextPit==13)))

        return board

    def switch_players(self, player):
        if self.playerrepeat:
            return player
        else:
            return 0 if player != 0 else 1

    def pick_pit(self, board, player, AI):
        availableMoves = self.get_available_moves(board, player)
        print("It is player {}'s turn".format(player))
        print('Select the position of the house you wish to distribute: ')
        print('House values:')
        if player == 1:
            print(self.get_player_pits(board, player)[::-1])
        else:
            print(self.get_player_pits(board, player))
        print('------------------')
        print('The available houses are:')
        
        if player == 1:
            # If player is 1, reverse list to match natural counter-clockwise nature of game
            availableMoves=availableMoves[::-1]
            print(availableMoves)
        else:
            print(availableMoves)
        
        ask = True
        while ask:
            print('>>>')
            # Let AI decide if AI is true
            if AI == True:
                pit = int(random.choice(availableMoves))
                print("The AI chose pit:{}".format(pit))
            else:
            # Else ask player
                try:
                    pit = int(input())

                except:
                    print("Input must be an integer")
                    continue

            # check selected pit is valid
            if pit in availableMoves:
                return pit
            print('Please select an available house, your available houses are: ', availableMoves)

    def run_turn(self, board, player, AI):
        # check player has available moves
        availableMoves = self.get_available_moves(board, player)
        # Disabled currently
        #if len(availableMoves) <= 0:
        #    winner = self.is_win(board)
        #    return 'Player' + str(player) + 'has no more available moves. ' + winner

        # prompt player to select pit
        pit = self.pick_pit(board, player, AI) - 1
        print('Player', player, 'picked house', pit)

        # distribute pebbles of selected pit and check if player
        board = self.distr_pebbles(board, pit, player)

        # check if player empties all houses and steal all opponents available pebbles
        self.steal_all_opponent_pebbles(board, player)

        return board

if __name__ == "__main__":
    game = Game()
    game.main()
