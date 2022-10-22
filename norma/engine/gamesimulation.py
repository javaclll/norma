from bagchal import GameState, Bagchal
from .model import Model
from .constants import GOATMODELPATH, MODELPATH, NUMSIMS, TIGERMODELPATH, TARGETMODELPATH
from random import random, randint
from functools import reduce
import numpy as np
from collections import deque
from .helpers import movestoAction, actionToDoableMove
import math

#Length for DeQue
MAXLEN = 50000
# For Tiger
T_GOAT_CAPTURED = 4
T_GOT_TRAPPED = -2
T_TRAP_ESCAPE = 2

# For Goat
G_GOAT_CAPTURED = -4
G_TIGER_TRAP = 5
G_TIGER_ESCAPE = -1

#Common 
G_WIN = 10
T_WIN = 5
T_LOSE = -5
G_LOSE = -10


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

        move, action, possibleActions = self.move()
        
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


        return action, indivReward, possibleActions

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

                turn = np.zeros(2)
                if self.game.turn == 1:
                    turn[0] = 1
                elif self.game.turn == -1:
                    turn[1] = 1

                placedGoat = np.zeros(20)
                placedGoat[self.game.goat_counter - 1] = 1

                prevTrapTiger = np.zeros(4)
                prevTrapTiger[self.game.trapped_tiger - 1] = 1

                prevGoatCapture = np.zeros(5)
                prevGoatCapture[self.game.goat_captured - 1] = 1

                action, indivReward, possibleActions = self.rewardCalculator()
                
                if self.game.game_status_check()["decided"] or len(self.game.game_history) > 100:
                    done = True

                futureBoard = np.array(reduce(lambda z, y :z + y, self.game.board))
                futureGoatBoard = (futureBoard == 1) * 1
                futureTigerBoard = (futureBoard == -1) * 1

                futureTurn = np.zeros(2)
                if self.game.turn == 1:
                    turn[0] = 1
                elif self.game.turn == -1:
                    turn[1] = 1

                futureplacedGoat = np.zeros(20)
                futureplacedGoat[self.game.goat_counter - 1] = 1

                futureTrapTiger = np.zeros(4)
                futureTrapTiger[self.game.trapped_tiger - 1] = 1
                
                futureGoatCapture = np.zeros(5)
                futureGoatCapture[self.game.goat_captured - 1] = 1
                
                possibleMoves = self.game.get_possible_moves()

                flattenBoard = np.concatenate(
                    (goatBoard, tigerBoard, prevTrapTiger, prevGoatCapture, placedGoat, turn, action, futureGoatBoard, futureTigerBoard, futureTrapTiger, futureGoatCapture, futureplacedGoat, futureTurn, 
                    indivReward, done), axis=None).reshape((1,-1))
                
                self.replayMemory.append([possibleMoves, flattenBoard, possibleActions])
                
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
            print(move["move"])

            action = movestoAction(move["move"][0], move["move"][1])
            
        else:
            actions = []
            prediction = self.mainModel.predict(self.game)[0]
            
            action = np.argmax(prediction)

            for move in possibleMoves:
                print(move["move"])

                actions.append(movestoAction(move["move"][0], move["move"][1]))
            
            while action not in actions:

                prediction[action] = - math.inf
                action = np.argmax(prediction)

            moveIndex = actions.index(action)
            
            move = possibleMoves[moveIndex]
        
        return move, action, actions

        #find the predicted values for the moves ....
        #get the next board state from the current board state
        #use policy network to find the next move
    
    def predictMove(self):
   
        possibleMoves = self.game.get_possible_moves()

        if len(possibleMoves) != 0:

            actions = []
            prediction = self.mainModel.predict(self.game)[0]
            
            action = np.argmax(prediction)

            for move in possibleMoves:
                actions.append(movestoAction(move["move"][0], move["move"][1]))
            
            while action not in actions:

                prediction[action] = - math.inf
                action = np.argmax(prediction)

            moveIndex = actions.index(action)
            
            move = possibleMoves[moveIndex]
        
        else:
            move = None
            action = None

        return move, action

        #find the predicted values for the moves ....
        #get the next board state from the current board state
        #use policy network to find the next move

    def move(self):

        move, action, possibleActions = self.moveState()
        self.game.move(move["move"][0], move["move"][1])
        
        return move, action, possibleActions