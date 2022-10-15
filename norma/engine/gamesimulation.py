from bagchal import AgentType, GameState, Bagchal
from .agent import Agent
from .model import Model
from .constants import MODELPATH

from functools import reduce
import numpy as np


# For Tiger
T_GOAT_CAPTURED = 2
T_GOT_TRAPPED = -1
T_TRAP_ESCAPE = 0.5

# For Goat
G_GOAT_CAPTURED = -2
G_TIGER_TRAP = 1
G_TIGER_ESCAPE = -0.5


class Simulator:

    def __init__(self, agentGoat: Agent, agentTiger: Agent):
        self.agentGoat = agentGoat
        self.agentTiger = agentTiger
        self.game = Bagchal.new()
        self.stateMemory = np.zeros((0, 101))

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
                
                flattenBoard = np.concatenate((goatBoard, tigerBoard, source, target, indivReward), axis=None).reshape((1,-1))


                self.stateMemory = np.concatenate((self.stateMemory, flattenBoard), axis = 0)
                
                if len(self.game.game_history) > 100:
                    break

            previousGameNo = previousGameNo + noOfStates

            noOfStates = len(self.game.game_history) - 1            

            totalReward = (200 - noOfStates) * 2
            
            if self.game.game_state == GameState.TIGER_WON.value:
                totalReward = -1 * totalReward 
            
            if self.game.game_state == GameState.DRAW.value:
                totalReward = totalReward / 3
                for k in range(noOfStates):
                    if k % 2 == 0:
                        self.stateMemory[previousGameNo + k][71] = self.stateMemory[previousGameNo + k][71] - (totalReward / (noOfStates - k))
                    else:
                        self.stateMemory[previousGameNo + k][71] = self.stateMemory[previousGameNo + k][71] - (totalReward / (noOfStates - k))
            else:
                for k in range(noOfStates):
                    if k % 2 == 0:
                        self.stateMemory[previousGameNo + k][71] = self.stateMemory[previousGameNo + k][71] + (totalReward / (noOfStates - k))
                    else:
                        self.stateMemory[previousGameNo + k][71] = self.stateMemory[previousGameNo + k][71] - (totalReward / (noOfStates - k))


            self.game = Bagchal.new()

        return {"Simulation End": True}


def simulate(noOfSims = 5, prevModel = None, currentModel = None):

    for _ in range(noOfSims):

        agentGoat = Agent(type = AgentType.GOAT.value, model = prevModel)
        agentTiger = Agent(type = AgentType.TIGER.value, model = currentModel)
        gameSimulation = Simulator(agentGoat = agentGoat, agentTiger = agentTiger)

        simulationResult = gameSimulation.rewardPropagation(noOfPlays = 10)
        
        if simulationResult["Simulation End"]:
            prevModel = currentModel 
            currentModel = Model()

            currentModel.training(flattendData = gameSimulation.stateMemory)
            
    if currentModel != None:
        currentModel.model.save(MODELPATH) #save to a location

    return currentModel.model