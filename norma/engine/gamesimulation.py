from bagchal import AgentType, GameState, Bagchal
from .agent import Agent
from .model import Model
from .constants import GOATMODELPATH, TIGERMODELPATH

from functools import reduce
import numpy as np
from random import random

# For Tiger
T_GOAT_CAPTURED = 2
T_GOT_TRAPPED = -1
T_TRAP_ESCAPE = 0.5

# For Goat
G_GOAT_CAPTURED = -2
G_TIGER_TRAP = 1
G_TIGER_ESCAPE = -0.5

#Common 
WIN_REWARD = 5


class Simulator:

    def __init__(self, agentGoat: Agent, agentTiger: Agent):
        self.agentGoat = agentGoat
        self.agentTiger = agentTiger
        self.game = Bagchal.new()
        self.stateGoatMemory = np.zeros((0, 105))
        self.stateTigerMemory = np.zeros((0,105))

    def rewardPropagation(self, noOfPlays):

        previousGameNo = 0
        noOfStates = 0
        
        for _ in range(noOfPlays):

            while not self.game.game_status_check()["decided"]:
                
                indivReward = 0
                
                flattenBoard = np.array(reduce(lambda z, y :z + y, self.game.board))
                goatBoard = (flattenBoard == 1) * 1
                tigerBoard = (flattenBoard == -1) * 1

                turn = self.game.turn 
                placedGoat = self.game.goat_counter
                prevTrapTiger = self.game.trapped_tiger
                prevGoatCapture = self.game.goat_captured
                move, self.game = self.agentGoat.move(self.game)
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

                source = np.zeros((5,5))

                target = np.zeros((5,5))

                target[move[1][0]][move[1][1]] = 1
                

                if move[0] is not None:
                    source[move[0][0]][move[0][1]] = 1
                
                
                source = source.flatten()
                target = target.flatten()
                
                flattenBoard = np.concatenate((goatBoard, tigerBoard, source, target, prevTrapTiger, prevGoatCapture, placedGoat, turn, indivReward), axis=None).reshape((1,-1))
                
                if turn == 1:
                    self.stateGoatMemory = np.concatenate((self.stateGoatMemory, flattenBoard), axis = 0)
                else:
                    self.stateTigerMemory = np.concatenate((self.stateTigerMemory, flattenBoard), axis = 0)
                
                if len(self.game.game_history) > 100:
                    break

            previousGameNo = previousGameNo + int(noOfStates/2)

            noOfStates = len(self.game.game_history) - 1            
            print("No Of States", noOfStates)
            totalReward = WIN_REWARD
            
            if self.game.game_state == GameState.TIGER_WON.value:
                totalReward = -1 * totalReward 
            
            if self.game.game_state == GameState.DRAW.value:
                totalReward = totalReward / 2
                for k in range(noOfStates):
                    if k % 2 == 0:
                        self.stateGoatMemory[previousGameNo + int(k/2)][104] = self.stateGoatMemory[previousGameNo + int(k/2)][104] - (totalReward / (noOfStates - k))
                    else:
                        self.stateTigerMemory[previousGameNo + int(k/2)][104] = self.stateTigerMemory[previousGameNo + int(k/2)][104] - (totalReward / (noOfStates - k))
            
            elif self.game.game_state == GameState.TIGER_WON.value or self.game.game_state == GameState.GOAT_WON.value:
                for k in range(noOfStates):
                    if k % 2 == 0:
                        self.stateGoatMemory[previousGameNo + int(k/2)][104] = self.stateGoatMemory[previousGameNo + int(k/2)][104] + (totalReward / (noOfStates - k))
                    else:
                        self.stateTigerMemory[previousGameNo + int(k/2)][104] = self.stateTigerMemory[previousGameNo + int(k/2)][104] - (totalReward / (noOfStates - k))


            self.game = Bagchal.new()

        return {"Simulation End": True}


def simulate(noOfSims = 50, goatModel = None, tigerModel = None):

    for simNo in range(noOfSims - 1):

        agentGoat = Agent(type = AgentType.GOAT.value, model = goatModel)
        agentTiger = Agent(type = AgentType.TIGER.value, model = tigerModel)
       
        gameSimulation = Simulator(agentGoat = agentGoat, agentTiger = agentTiger)
        
        simulationResult = gameSimulation.rewardPropagation(noOfPlays = 400)
        
        if simulationResult["Simulation End"]:
            goatModel = Model()
            tigerModel = Model()

            goatModel.training(flattendData = gameSimulation.stateGoatMemory, trainingfactor = min([(simNo + 1) * 100, 3000]))
            tigerModel.training(flattendData = gameSimulation.stateTigerMemory, trainingfactor = min([(simNo + 1) * 100, 3000]))

    agentGoat = Agent(type = AgentType.GOAT.value, model = goatModel)
    agentTiger = Agent(type = AgentType.TIGER.value, model = tigerModel)
       
    gameSimulation = Simulator(agentGoat = agentGoat, agentTiger = agentTiger)
        
    simulationResult = gameSimulation.rewardPropagation(noOfPlays = 1000)

    if simulationResult["Simulation End"]:
            goatModel = Model()
            tigerModel = Model()

            goatModel.training(flattendData = gameSimulation.stateGoatMemory, trainingfactor = min([(simNo + 1) * 100, 3000]))
            tigerModel.training(flattendData = gameSimulation.stateTigerMemory, trainingfactor = min([(simNo + 1) * 100, 3000]))
    if goatModel != None:

        goatModel.model.save(GOATMODELPATH)   #save to a location

    if tigerModel != None:

        goatModel.model.save(TIGERMODELPATH)
    
    return goatModel.model, tigerModel.model