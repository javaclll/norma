from random import randint, random
from bagchal import Bagchal

import numpy as np

#agent is the player that plays games and then, stores the data for training.

#use this to generate the training data, so generate the self play data, and the montecarlo search tree data. 

class Agent:
    
    def __init__(self, type, model = None):
        self.noGames = 0
        self.epsilon = 10
        self.model = model
        self.type = type

    def moveState(self, game: Bagchal):
   
        possibleMoves = []
        
        possibleMoves = game.get_possible_moves()
        
        if self.model is None or random() < 0.15:
            print(self.model)
            print("Random")
            maxMoves = len(possibleMoves) - 1

            move = possibleMoves[randint(0, maxMoves)]["move"]

        else: 
            predictions = []
            for move in possibleMoves:

                source = np.zeros((5,5))

                target = np.zeros((5,5))

                target[move["move"][1][0]][move["move"][1][1]] = 1
                

                if move["move"][0] is not None:
                    source[move["move"][0][0]][move["move"][0][1]] = 1
                        
                # model.predict(state, action) => get reward
                predictions.append(self.model.predict(game.board, source, target))
                # find the max reward and use that move in the game

            maxIndex = np.argmax(predictions)
            
            move = possibleMoves[maxIndex]["move"]

            #find the predicted values for the moves ....
        #get the next board state from the current board state
        return move
        #use policy network to find the next move
    

    def move(self, game: Bagchal, pgn = None):

        move = self.moveState(game)

        game.move(move[0], move[1])
            
        return move, game