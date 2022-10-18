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

        randomNumber = random()
        if self.model is None or randomNumber< 0.25:
            print("Random")
            maxMoves = len(possibleMoves) - 1

            move = possibleMoves[randint(0, maxMoves)]["move"]

        else:
            print("Not Random")
            moves = []
            for move in possibleMoves:

                sourceX = np.zeros(5)
                sourceY = np.zeros(5)

                targetX = np.zeros(5)
                targetY = np.zeros(5)

                target = np.zeros((5,5))

                targetX[move["move"][1][0]] = 1
                targetY[move["move"][1][1]] = 1
                

                if move["move"][0] is not None:
                    sourceX[move["move"][0][0]] = 1
                    sourceY[move["move"][0][1]] = 1
                        

                source = {"x": sourceX, "y": sourceY}
                target = {"x": targetX, "y": targetY}
                # model.predict(state, action) => get reward
                moves.append({"game": game,"source": source, "target": target})
                # find the max reward and use that move in the game
            prediction = self.model.predict(moves)
            maxIndex = np.argmax(prediction)
            
            move = possibleMoves[maxIndex]["move"]

            #find the predicted values for the moves ....
        #get the next board state from the current board state
        return move
        #use policy network to find the next move
    

    def move(self, game: Bagchal, pgn = None):

        move = self.moveState(game)

        game.move(move[0], move[1])
            
        return move, game