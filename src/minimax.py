from mancala import Mancala


def minimax(self, game: Mancala, depth, player):  # , maximizing=True):

    """
    MiniMax algorithm
    """

    if depth != self.init_depth:
        player_mm = game.switch_players(player)
    else:
        player_mm = player
    # evalboard = board
    print("Depth is: {}, player {}".format(depth, player_mm))
    print(evalboard)
    print(game.get_available_moves(evalboard, player_mm))

    # Has max depth been reached
    if (depth == 0) | (game.is_end_match(evalboard)):
        score = game.get_score(evalboard, player_mm)
        print(score)
        print("-------------------------------------------------")
        return score, None

    # Is it max or mins turn
    if maximizing:
        stored_value = -99999
        # Generate nodes
        for i in game.get_available_moves(evalboard, player_mm):
            print("maximizing - pick: {}".format(i))
            child = game.explore_moves(deepcopy(evalboard), player_mm, i, AI="eval")
            print(game.playerrepeat)

            # Generer, backpropagate, select best score/value
            # Max of the max vs max of the min
            if game.playerrepeat == True:
                value = self.minimax(child, depth - 1, player_mm, True)[0]
            else:
                value = self.minimax(child, depth - 1, player_mm, False)[0]
            if value > stored_value:
                print("Value was updated {} {}".format(value, i))
                stored_value = value
                move = i

            print(
                "stored value vs value for max is: {} vs {}".format(stored_value, value)
            )
            print("stored move vs i for max is: {} vs {}".format(move, i))

        return stored_value, move
    else:
        stored_value = 99999
        for i in game.get_available_moves(evalboard, player_mm):
            child = game.explore_moves(deepcopy(evalboard), player_mm, i, AI="eval")
            print("minimizing - pick: {}".format(i))
            # Min of the min vs min of the max
            if game.playerrepeat == True:
                value = self.minimax(child, depth - 1, player_mm, False)[0]
            else:
                value = self.minimax(child, depth - 1, player_mm, True)[0]
            if value < stored_value:
                print("Value was updated {} {}".format(value, i))
                stored_value = value
                move = i

            print("stored value for min is: {}".format(stored_value))

        return stored_value, move
    # Hvis depth = 0
    # Udregn score

    # Ellers reducer depth med 1 og anvend max/min på næste depth
