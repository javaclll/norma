from bagchal import GameState, Bagchal
from .model import Model
from .constants import GOATMODELPATH, MODELPATH, NUMSIMS, TIGERMODELPATH, TARGETMODELPATH
from random import random, randint
from functools import reduce
import numpy as np
from collections import deque

#Length for DeQue
MAXLEN = 50000
# For Tiger
T_GOAT_CAPTURED = 2
T_GOT_TRAPPED = -2
T_TRAP_ESCAPE = 2

# For Goat
G_GOAT_CAPTURED = -2
G_TIGER_TRAP = 2
G_TIGER_ESCAPE = -2

#Common 
G_WIN = 6
T_WIN = 4
T_LOSE = -4
G_LOSE = -6


class Simulator:
    def __init__(self, targetModel = Model(), mainModel = Model()):
        self.game = Bagchal.new()
        self.replayMemory = deque(maxlen= MAXLEN)
        self.epsilon = 1
        self.mainModel = mainModel
        self.targetModel = targetModel

    def rewardCalculator(self):

        indivReward = 0

        turn = self.game.turn 
        prevTrapTiger = self.game.trapped_tiger
        prevGoatCapture = self.game.goat_captured

        move = self.move()
        
        currentTrapTiger = self.game.trapped_tiger
        currentGoatCapture = self.game.goat_captured
                
        if prevGoatCapture != currentGoatCapture:
            if turn == 1:
                indivReward += G_GOAT_CAPTURED
            else:
                indivReward += T_GOAT_CAPTURED

        if prevTrapTiger < currentTrapTiger:
            if turn == 1:
                indivReward += G_TIGER_TRAP
            else:
                indivReward += T_GOT_TRAPPED

        elif prevTrapTiger > currentTrapTiger:
            if turn == 1:
                indivReward += G_TIGER_ESCAPE
            else:
                indivReward += T_TRAP_ESCAPE

        if self.game.game_state == GameState.GOAT_WON.value:
            if turn == 1:
                indivReward += G_WIN
            else:
                indivReward += T_LOSE
        
        elif self.game.game_state == GameState.TIGER_WON.value:
            if turn == 1:
                indivReward += G_LOSE
            else:
                indivReward += T_WIN


        return move, indivReward

    def simulate(self, noOfSims = NUMSIMS):

        maxEpsilon = 1
        minEpsilon = 0.01
        decay = 0.01

        self.targetModel.model.set_weights(self.mainModel.model.get_weights())

        targetUpdate = 0
        
        for simNo in range(noOfSims):
            totalTrainingReward = 0
            self.game = Bagchal.new()

            done = False

            while not done:
                print(f"No of Sims: {simNo}")
                print(f"Target Update: {targetUpdate}")
                print()

                targetUpdate += 1

                flattenBoard = np.array(reduce(lambda z, y :z + y, self.game.board))
                goatBoard = (flattenBoard == 1) * 1
                tigerBoard = (flattenBoard == -1) * 1

                turn = self.game.turn 
                placedGoat = self.game.goat_counter
                prevTrapTiger = self.game.trapped_tiger
                prevGoatCapture = self.game.goat_captured

                move, indivReward = self.rewardCalculator()
                
                if self.game.game_status_check()["decided"] or len(self.game.game_history) > 100:
                    done = True

                sourceX = np.zeros(5)
                sourceY = np.zeros(5)

                targetX = np.zeros(5)
                targetY = np.zeros(5)
                
                targetX[move["move"][1][0]] = 1
                targetY[move["move"][1][1]] = 1

                if move["move"][0] is not None:
                    sourceX[move["move"][0][0]] = 1
                    sourceY[move["move"][0][1]] = 1

                futureBoard = np.array(reduce(lambda z, y :z + y, self.game.board))
                futureGoatBoard = (futureBoard == 1) * 1
                futureTigerBoard = (futureBoard == -1) * 1

                futureTurn = self.game.turn 
                futureplacedGoat = self.game.goat_counter
                futureTrapTiger = self.game.trapped_tiger
                futureGoatCapture = self.game.goat_captured
                
                futureMove = self.predictMove()
                
                futureSourceX = np.zeros(5)
                futureSourceY = np.zeros(5)

                futureTargetX = np.zeros(5)
                futureTargetY = np.zeros(5)

                if futureMove != None:
                    futureTargetX[futureMove["move"][1][0]] = 1
                    futureTargetY[futureMove["move"][1][1]] = 1

                    if futureMove["move"][0] is not None:
                        futureSourceX[futureMove["move"][0][0]] = 1
                        futureSourceY[futureMove["move"][0][1]] = 1

                flattenBoard = np.concatenate(
                    (goatBoard, tigerBoard, sourceX, sourceY, targetX, targetY, 
                    prevTrapTiger, prevGoatCapture, placedGoat, turn, 
                    futureGoatBoard, futureTigerBoard, futureSourceX, futureSourceY, futureTargetX, futureTargetY, 
                    futureTrapTiger, futureGoatCapture, futureplacedGoat, futureTurn, 
                    indivReward, done), axis=None).reshape((1,-1))
                
                
                self.replayMemory.append(flattenBoard)
                
                if targetUpdate % 4 == 0 or done:
                    Model.training(replayMemory = self.replayMemory, mainModel = self.mainModel, targetModel= self.targetModel, done = done)

                totalTrainingReward += indivReward
                print(f"Total Training Rewards: {totalTrainingReward} after {simNo} steps.")

                if done:
                    totalTrainingReward += 1

                    if targetUpdate >= 100:
                        self.targetModel.model.set_weights(self.mainModel.model.get_weights())
                        
                        self.targetModel.model.save(TARGETMODELPATH)
                        print(f"Target Model Saved at {targetUpdate} targets and {simNo} sims")

                        targetUpdate = 0
                    break
            
            self.epsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-decay * simNo)
        


    def moveState(self):
           
        possibleMoves = self.game.get_possible_moves()

        if random() < self.epsilon:

            maxMoves = len(possibleMoves) - 1

            move = possibleMoves[randint(0, maxMoves)]

        else:
            moves = []
            for move in possibleMoves:

                sourceX = np.zeros(5)
                sourceY = np.zeros(5)

                targetX = np.zeros(5)
                targetY = np.zeros(5)

                targetX[move["move"][1][0]] = 1
                targetY[move["move"][1][1]] = 1
                

                if move["move"][0] is not None:
                    sourceX[move["move"][0][0]] = 1
                    sourceY[move["move"][0][1]] = 1
                        

                source = {"x": sourceX, "y": sourceY}
                target = {"x": targetX, "y": targetY}
                # model.predict(state, action) => get reward
                moves.append({"game": self.game,"source": source, "target": target})
                # find the max reward and use that move in the game
            
            prediction = self.mainModel.predict(moves)
            print(prediction)
            maxIndex = np.argmax(prediction)
            
            move = possibleMoves[maxIndex]
        
        return move

        #find the predicted values for the moves ....
        #get the next board state from the current board state
        #use policy network to find the next move
    
    def predictMove(self):
   
        possibleMoves = self.game.get_possible_moves()

        moves = []

        if len(possibleMoves) != 0:
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
                moves.append({"game": self.game, "source": source, "target": target})
                # find the max reward and use that move in the game
            
            prediction = self.mainModel.predict(moves)
            print(prediction)

            maxIndex = np.argmax(prediction)
            
            move = possibleMoves[maxIndex]
        else:
            move = None

        return move

        #find the predicted values for the moves ....
        #get the next board state from the current board state
        #use policy network to find the next move

    def move(self):

        move = self.moveState()
        self.game.move(move["move"][0], move["move"][1])
        
        return move