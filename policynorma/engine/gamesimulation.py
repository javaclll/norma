import re
from bagchal import GameState, Bagchal
from .model import Model
from .constants import GOATMODELPATH, MODELPATH, NUMSIMS, TIGERMODELPATH, TARGETMODELPATH
from random import random, randint
from functools import reduce
import numpy as np
from collections import deque
from .helpers import movestoAction
import math
import csv

#Length for DeQue
MAXLEN = 25000

# For Tiger
T_GOAT_CAPTURED = 5
T_GOT_TRAPPED = -5
T_TRAP_ESCAPE = 2

# For Goat
G_GOAT_CAPTURED = -5
G_TIGER_TRAP = 7
G_TIGER_ESCAPE = -2

#Common 
G_WIN = 10
T_WIN = 10
T_LOSE = -10
G_LOSE = -10

DRAW = -5

class Simulator:
    def __init__(self, targetGoatModel = Model(), mainGoatModel = Model(), targetTigerModel = Model(), mainTigerModel = Model()):
        self.game = Bagchal.new()
        self.replayGoatMemory = deque(maxlen = MAXLEN)
        self.replayTigerMemory = deque(maxlen = MAXLEN)
        self.goatEpsilon = 1
        self.tigerEpsilon = 1
        self.mainGoatModel = mainGoatModel
        self.targetGoatModel = targetGoatModel
        self.mainTigerModel = mainTigerModel
        self.targetTigerModel = targetTigerModel
        self.goatWins = 0
        self.draws = 0
        self.tigerWins = 0

    def rewardCalculator(self):

        indivReward = 0

        turn = self.game.turn 
        prevTrapTiger = self.game.trapped_tiger
        prevGoatCapture = self.game.goat_captured

        move, action = self.move()
        
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
            self.goatWins += 1
            if turn == 1:
                indivReward += G_WIN
            else:
                indivReward += T_LOSE
        
        elif self.game.game_state == GameState.TIGER_WON.value:
            self.tigerWins += 1
            if turn == 1:
                indivReward += G_LOSE
            else:
                indivReward += T_WIN

        elif self.game.game_state == GameState.DRAW.value:
            self.draws += 1
            indivReward += DRAW


        return action, indivReward

    def simulate(self, noOfSims = NUMSIMS, simStart = 0):
        with open('gameplayrecord.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["Norma Agent", "Wins", "Loss", "Draw", "Total Games Played", "Predicted Invalid Moves"]
            
            writer.writerow(field)
            file.close()

        maxEpsilon = 1
        minEpsilon = 0.01
        goatDecay = 0.01
        tigerDecay = 0.01

        self.targetGoatModel.model.set_weights(self.mainGoatModel.model.get_weights())
        self.targetTigerModel.model.set_weights(self.mainTigerModel.model.get_weights())

        self.goatEpsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-goatDecay * simStart)
        self.tigerEpsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-tigerDecay * simStart)

        targetUpdate = 0

        for simNo in range(simStart, noOfSims):
            totalTrainingReward = 0

            self.game = Bagchal.new()

            done = False

            while not done:

                print(f"No of Sims: {simNo + 1}")
                print(f"Target Update: {targetUpdate}")
                print()

                targetUpdate += 1
                
                flattenBoard = np.array(reduce(lambda z, y :z + y, self.game.board))

                goatBoard = (flattenBoard == 1) * 1
                tigerBoard = (flattenBoard == -1) * 1

                turn = self.game.turn

                placedGoat = np.zeros(21)
                placedGoat[self.game.goat_counter] = 1

                prevTrapTiger = np.zeros(5)
                prevTrapTiger[self.game.trapped_tiger] = 1

                prevGoatCapture = np.zeros(6)
                prevGoatCapture[self.game.goat_captured] = 1

                action, indivReward = self.rewardCalculator()
                
                if self.game.game_status_check()["decided"] or len(self.game.game_history) > 100:
                    done = True
                
                print(f"Total Goat Win, Tiger Wins, Draws: {self.goatWins, self.tigerWins, self.draws} in {simNo + 1} Simulations.")

                futureBoard = np.array(reduce(lambda z, y :z + y, self.game.board))
                futureGoatBoard = (futureBoard == 1) * 1
                futureTigerBoard = (futureBoard == -1) * 1

                futureplacedGoat = np.zeros(21)
                futureplacedGoat[self.game.goat_counter] = 1

                futureTrapTiger = np.zeros(5)
                futureTrapTiger[self.game.trapped_tiger] = 1
                
                futureGoatCapture = np.zeros(6)
                futureGoatCapture[self.game.goat_captured] = 1
                
                possibleMoves = self.game.get_possible_moves()

                flattenBoard = np.concatenate(
                    (goatBoard, tigerBoard, prevTrapTiger, prevGoatCapture, placedGoat, action, futureGoatBoard, futureTigerBoard, futureTrapTiger, futureGoatCapture, futureplacedGoat, 
                    indivReward, done), axis=None).reshape((1,-1))
                
                if turn == 1:
                    self.replayGoatMemory.append([possibleMoves, flattenBoard])

                elif turn == -1:
                    self.replayTigerMemory.append([possibleMoves,flattenBoard])
                
                if targetUpdate % 7 == 0 or done:

                    print("Tiger Training !")
                    Model.training(replayMemory= self.replayTigerMemory, mainModel= self.mainTigerModel, opponentTargetModel = self.targetGoatModel, done = done)

                    print("Goat Training !")
                    Model.training(replayMemory= self.replayGoatMemory, mainModel= self.mainGoatModel, opponentTargetModel = self.targetTigerModel, done = done)

                totalTrainingReward += indivReward
                print(f"Total Training Rewards: {totalTrainingReward} after {simNo + 1} steps.")

                if done:
                    totalTrainingReward += 1

                    if targetUpdate >= 200:
                        self.targetGoatModel.model.set_weights(self.mainGoatModel.model.get_weights())
                        self.targetTigerModel.model.set_weights(self.mainTigerModel.model.get_weights())
                        
                        self.targetGoatModel.model.save(GOATMODELPATH)
                        self.targetTigerModel.model.save(TIGERMODELPATH)
                        print(f"Target Models Saved at {targetUpdate} targets and {simNo + 1} sims")

                        targetUpdate = 0
                        ## Play a Game with Random Opponent and Save the Data:

                        goatDraw = 0
                        goatWin = 0
                        goatLoss = 0
                        invalidMovePredictedGoat = 0

                        tigerDraw = 0
                        tigerWin = 0
                        tigerLoss = 0
                        invalidMovePredictedTiger = 0

                        for _ in range(20):
                            randomGamePlay = Bagchal.new()

                            randomDone = False
                            while not randomDone:
                                possibleMoves = randomGamePlay.get_possible_moves()

                                if(randomGamePlay.turn == -1):
                                    actions = []

                                    for move in possibleMoves:
                                        actions.append(movestoAction(move["move"][0], move["move"][1]))

                                        prediction = self.mainTigerModel.predict(randomGamePlay)[0]
                                    
                                    action = np.argmax(prediction)
                                    
                                    while action not in actions:
                                        invalidMovePredictedTiger += 1
                                        prediction[action] = - math.inf
                                        action = np.argmax(prediction)

                                    moveIndex = actions.index(action)
                                    
                                    move = possibleMoves[moveIndex]
                                else:
                                    maxMoves = len(possibleMoves) - 1

                                    move = possibleMoves[randint(0, maxMoves)]

                                    action = movestoAction(move["move"][0], move["move"][1])

                                randomGamePlay.move(move["move"][0], move["move"][1])
                                
                                if randomGamePlay.game_status_check()["decided"] or len(randomGamePlay.game_history) > 100:
                                    
                                    if(randomGamePlay.game_state == GameState.TIGER_WON.value):
                                        tigerWin += 1
                                    elif(randomGamePlay.game_state == GameState.GOAT_WON.value):
                                        tigerLoss += 1
                                    else:
                                        tigerDraw += 1

                                    randomDone = True
                            

                            randomGamePlay = Bagchal.new()

                            randomDone = False
                            while not randomDone:
                                possibleMoves = randomGamePlay.get_possible_moves()

                                if(randomGamePlay.turn == 1):
                                    actions = []

                                    for move in possibleMoves:
                                        actions.append(movestoAction(move["move"][0], move["move"][1]))

                                        prediction = self.mainGoatModel.predict(randomGamePlay)[0]
                                    
                                    action = np.argmax(prediction)
                                    
                                    while action not in actions:
                                        invalidMovePredictedGoat += 1
                                        prediction[action] = - math.inf
                                        action = np.argmax(prediction)

                                    moveIndex = actions.index(action)
                                    
                                    move = possibleMoves[moveIndex]
                                else:
                                    maxMoves = len(possibleMoves) - 1

                                    move = possibleMoves[randint(0, maxMoves)]

                                    action = movestoAction(move["move"][0], move["move"][1])

                                randomGamePlay.move(move["move"][0], move["move"][1])
                                
                                if randomGamePlay.game_status_check()["decided"] or len(randomGamePlay.game_history) > 100:
                                    
                                    if(randomGamePlay.game_state == GameState.GOAT_WON.value):
                                        goatWin += 1
                                    elif(randomGamePlay.game_state == GameState.TIGER_WON.value):
                                        goatLoss += 1
                                    else:
                                        goatDraw += 1
                                    
                                    randomDone = True
                            
                            with open('gameplayrecord.csv', 'a', newline='') as file:
                                writer.writerow([-1, tigerWin, tigerLoss, tigerDraw, 20, invalidMovePredictedTiger])
                                writer.writerow([1, goatWin, goatLoss, goatDraw, 20, invalidMovePredictedGoat])
                                file.close()
                        break
            
            self.goatEpsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-goatDecay * (simNo + 1))
            self.tigerEpsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-tigerDecay * (simNo + 1))
        
    def moveState(self):
           
        possibleMoves = self.game.get_possible_moves()
    
        randNumber = random()

        if (randNumber < self.goatEpsilon and self.game.turn == 1) or (randNumber < self.tigerEpsilon and self.game.turn == -1):

            maxMoves = len(possibleMoves) - 1

            move = possibleMoves[randint(0, maxMoves)]

            action = movestoAction(move["move"][0], move["move"][1])
            
        else:
            actions = []
            for move in possibleMoves:
                actions.append(movestoAction(move["move"][0], move["move"][1]))

            if self.game.turn == 1:
                prediction = self.mainGoatModel.predict(self.game)[0]
            elif self.game.turn == -1:
                prediction = self.mainTigerModel.predict(self.game)[0]
            
            action = np.argmax(prediction)
            
            while action not in actions:

                prediction[action] = - math.inf
                action = np.argmax(prediction)

            moveIndex = actions.index(action)
            
            move = possibleMoves[moveIndex]
        
        return move, action
    

    #find the predicted values for the moves ....
        #get the next board state from the current board state
        #use policy network to find the next move
    
    def predictMove(self, predictModel = None):
        if not predictModel:
            if self.game.turn == 1:
                predictModel = self.mainGoatModel
            elif self.game.turn == -1:
                predictModel = self.mainTigerModel

        possibleMoves = self.game.get_possible_moves()

        if len(possibleMoves) != 0:

            actions = []
            prediction = predictModel.predict(self.game)[0]
            
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

        move, action = self.moveState()
        self.game.move(move["move"][0], move["move"][1])
        
        return move, action



    # def goatsimulate(self, noOfSims = NUMSIMS, targetGoatModel = None, startSimNo = 0):

    #     if not self.tigerModel:
    #         return 

    #     maxEpsilon = 1
    #     minEpsilon = 0.01
    #     goatDecay = 0.01
    #     tigerDecay = 0.01

    #     if targetGoatModel == None:
    #         self.targetGoatModel.model.set_weights(self.mainGoatModel.model.get_weights())
    #     else:
    #         self.targetGoatModel.model.set_weights(targetGoatModel.get_weights())
    #         self.mainGoatModel.model.set_weights(self.targetGoatModel.model.get_weights())

    #         self.goatEpsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-goatDecay * simNo)
    #         self.tigerEpsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-tigerDecay * simNo)  

    #     targetUpdate = 0
    #     noOfSims += startSimNo

    #     for simNo in range(startSimNo, noOfSims):
    #         totalTrainingReward = 0

    #         self.game = Bagchal.new()

    #         goatWon = False
    #         done = False

    #         prevSelfreplay = len(self.replayGoatMemory)

    #         while not done:

    #             print(f"No of Sims: {simNo + 1}")
    #             print(f"Target Update: {targetUpdate}")
    #             print()

    #             targetUpdate += 1
                
    #             flattenBoard = np.array(reduce(lambda z, y :z + y, self.game.board))

    #             goatBoard = (flattenBoard == 1) * 1
    #             tigerBoard = (flattenBoard == -1) * 1

    #             turn = np.zeros(2)
    #             if self.game.turn == 1:
    #                 turn[0] = 1
    #             elif self.game.turn == -1:
    #                 turn[1] = 1

    #             placedGoat = np.zeros(20)
    #             placedGoat[self.game.goat_counter - 1] = 1

    #             prevTrapTiger = np.zeros(4)
    #             prevTrapTiger[self.game.trapped_tiger - 1] = 1

    #             prevGoatCapture = np.zeros(5)
    #             prevGoatCapture[self.game.goat_captured - 1] = 1

    #             action, indivReward = self.rewardCalculator()
                
    #             if self.game.game_status_check()["decided"] or len(self.game.game_history) > 100:
    #                 done = True
                    
    #             else:
    #                 move, _= self.predictMove(predictModel= self.tigerModel) 
    #                 self.game.move(move["move"][0], move["move"][1])
    #                 indivReward += self.game.move_reward_goat[-1]
                    
    #                 if self.game.game_status_check()["decided"] or len(self.game.game_history) > 100:
    #                     done = True
    #                     if self.game.game_state == GameState.DRAW.value:
    #                         self.draws += 1
    #                     elif self.game.game_state == GameState.GOAT_WON.value:
    #                         self.goatWins += 1
    #                     elif self.game.game_state == GameState.TIGER_WON.value:
    #                         self.tigerWins += 1

    #             print(f"Total Goat Win, Tiger Wins, Draws: {self.goatWins, self.tigerWins, self.draws} in {simNo + 1} Simulations.")

    #             futureBoard = np.array(reduce(lambda z, y :z + y, self.game.board))
    #             futureGoatBoard = (futureBoard == 1) * 1
    #             futureTigerBoard = (futureBoard == -1) * 1

    #             futureTurn = np.zeros(2)
    #             if self.game.turn == 1:
    #                 turn[0] = 1
    #             elif self.game.turn == -1:
    #                 turn[1] = 1

    #             futureplacedGoat = np.zeros(20)
    #             futureplacedGoat[self.game.goat_counter - 1] = 1

    #             futureTrapTiger = np.zeros(4)
    #             futureTrapTiger[self.game.trapped_tiger - 1] = 1
                
    #             futureGoatCapture = np.zeros(5)
    #             futureGoatCapture[self.game.goat_captured - 1] = 1
                
    #             possibleMoves = self.game.get_possible_moves()

    #             flattenBoard = np.concatenate(
    #                 (goatBoard, tigerBoard, prevTrapTiger, prevGoatCapture, placedGoat, turn, action, futureGoatBoard, futureTigerBoard, futureTrapTiger, futureGoatCapture, futureplacedGoat, futureTurn, 
    #                 indivReward, done), axis=None).reshape((1,-1))
                
    #             self.replayGoatMemory.append([possibleMoves, flattenBoard])
                
    #             if targetUpdate % 4 == 0 or done:
    #                 Model.goatTraining(replayMemory = self.replayMemory, mainGoatModel = self.mainGoatModel, targetGoatModel= self.targetGoatModel, done = done)

    #             totalTrainingReward += indivReward
    #             print(f"Total Training Rewards: {totalTrainingReward} after {simNo + 1} steps.")

    #             if done:
    #                 totalTrainingReward += 1

    #                 if targetUpdate >= 100:
    #                     self.targetGoatModel.model.set_weights(self.mainGoatModel.model.get_weights())
                        
    #                     self.targetGoatModel.model.save(GOATMODELPATH)
    #                     print(f"Target Model Saved at {targetUpdate} targets and {simNo + 1} sims")

    #                     targetUpdate = 0
    #                 break
            
    #         self.goatEpsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-goatDecay * simNo)
    #         self.tigerEpsilon = minEpsilon + (maxEpsilon - minEpsilon) * np.exp(-tigerDecay * simNo)
