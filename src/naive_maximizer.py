import random
from copy import deepcopy
from mancala import Mancala

class NaiveMaximizerPlayer:
    def __init__(self, game: Mancala) -> None:
        self.game = game
        
    def think(self, board, player):

        move = self.naive_maximizer_algorithm(board, player)

        return move 
    
    def naive_maximizer_algorithm(self, board, player, verbose = False):
        
        player_board = deepcopy(board)
        best_move = None
        next_moves = []

        availableMoves = self.game.get_legal_moves(board, player)
        
        if len(availableMoves)>0:
            
            ## Find moves that will give you an extra move
            
            for move in availableMoves:
                s = abs(7 - (move+player_board[move]+1)) 
                if s == 7 or s == 0:
                   next_moves.append(move)
            
            ## If there are moves giving extra, choose the closest          
            
            if len(next_moves) != 0:
                return max(next_moves) 
            
            ## If no pebble can end up in player pit, choose the move that will maximize the score
            best_score = 0
            scores = []
            for move in availableMoves:
                board_temp, _ = self.game.distr_pebbles(player_board, move, player)
                store_temp = board_temp[self.game.player_pits[player]]
                
                if store_temp >= best_score:
                    best_score = store_temp
                    scores.append(best_score)
                    next_moves.append(move)
            
            next_moves = [i for i,j in zip(next_moves,scores) if j==max(scores)]
            best_move = random.choice(next_moves)
                
        if verbose:            
            print(f"Player_board: {player_board}")
            print(f"Available moves: {availableMoves}" )
            print(f"Candidate moves: {next_moves}") 
            print(f"Best move: {best_move}") 
        
        return best_move
        
        
        