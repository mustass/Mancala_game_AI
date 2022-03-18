import random
from copy import deepcopy
from mancala import Mancala
from heuristics import GameScore, Heuristic

class ExactAgentPlayer:
    def __init__(self, game: Mancala, max_depth, heuristic: Heuristic) -> None:
        self.game = game
        self.max_depth = max_depth
        self.GameScore = GameScore(self.game)
        self.Heuristic = heuristic(self.game)
        
        
    def think(self, board, player):

        move = self.Exact_Agent_algorithm(board, self.max_depth, player)

        return move 
    
    def Exact_Agent_algorithm(self, board, depth, player, extra_turn=False):
        
        player_board = deepcopy(board)
        next_move_pit = None
        next_move_pits = []
        score = 0
        
        print("player ", player)
        print("player_board ", player_board)
        
        # Change turns?! 
        if extra_turn:
            player = self.game.opposite_player(player)
        print("player ", player)


        availableMoves = self.game.get_legal_moves(board, player)
        print("availableMoves ", availableMoves)
        
        if len(availableMoves)>0:
            for pit in availableMoves:
                s = abs(7 - (pit+player_board[pit]+1)) 
                if s == 7 or s == 0:
                   next_move_pits.append(pit)
                                      
            if len(next_move_pits) != 0:
                next_move_pit = max(next_move_pits)
            else:
                # Max Agent
                scores = []
                for pit in availableMoves:
                    board_temp, extra_turn = self.game.distr_pebbles(player_board, pit, player)
                    if player == 0:
                        store_temp = board_temp[6]
                    else:
                        store_temp = board_temp[13]
                    if store_temp>=score:
                        score = store_temp
                        scores.append(score)
                        next_move_pits.append(pit)
                print(" ")        
                print("next_move_pits ", next_move_pits) 
                print("scores ", scores)
                next_move_pits = [i for i,j in zip(next_move_pits,scores) if j==max(scores)]
                next_move_pit = random.choice(next_move_pits)
                
                    
                print("player_board ", player_board)
        print("next_move_pits ", next_move_pits) 
        print("next_move_pit ", next_move_pit) 
        
        return next_move_pit
        
        
        