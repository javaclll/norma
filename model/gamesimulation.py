from model.bagchal import Bagchal
from model.enum import AgentType, GameState
from model.agent import Agent
from model.model import Model

from functools import reduce
import numpy as np


class Simulator:

    def __init__(self, agentGoat: Agent, agentTiger: Agent, game: Bagchal):
        self.agentGoat = agentGoat
        self.agentTiger = agentTiger
        self.game = Bagchal.new()
        self.stateMemory = np.zeros((0, 5, 5, 4))

    def play(self, noOfPlays):

        previousGameNo = 0
        
        for _ in range(noOfPlays):
            # agentGoat.getState()
            # agentTiger.moveState()

            while not self.game.game_status_check()["decided"]:
                
                indivReward = 0
                
                flattenBoard = np.array(reduce(lambda z, y :z + y, self.game.board))
                goatBoard = (flattenBoard == 1) * 1
                tigerBoard = (flattenBoard == -1) * 1

                if self.game.turn == 1:
                    prevTrapGoat, prevTrapTiger = self.game.check_trap()
                    move, self.game = self.agentGoat.move(self.game)
                    currentTrapGoat, currentTrapTiger = self.game.check_trap()
                    

                    if currentTrapGoat - prevTrapGoat > 0:
                        indivReward = indivReward - (currentTrapGoat - prevTrapGoat)
                    elif currentTrapGoat - prevTrapGoat < 0:
                        indivReward = indivReward + (currentTrapGoat - prevTrapGoat)
                    
                    if currentTrapTiger - prevTrapTiger > 0:
                        indivReward = indivReward + (currentTrapTiger - prevTrapTiger)
                    elif currentTrapTiger - prevTrapTiger < 0:
                        indivReward = indivReward - (currentTrapTiger - prevTrapTiger)


                elif self.game.turn == -1:

                    prevGoatCapture = self.game.game_history[-1]["goat_captured"]
                    prevTrapGoat, prevTrapTiger = self.game.check_trap()
                    move, self.game = self.agentTiger.move(self.game)
                    currentTrapGoat, currentTrapTiger = self.game.check_trap()
                    currentGoatCapture = self.self.game.game_history[-1]["goat_captured"]

                    indivReward = indivReward + (currentGoatCapture - prevGoatCapture)

                    if currentTrapGoat - prevTrapGoat > 0:
                        indivReward = indivReward + (currentTrapGoat - prevTrapGoat)
                    elif currentTrapGoat - prevTrapGoat < 0:
                        indivReward = indivReward - (currentTrapGoat - prevTrapGoat)
                    
                    if currentTrapTiger - prevTrapTiger > 0:
                        indivReward = indivReward - (currentTrapTiger - prevTrapTiger)
                    elif currentTrapTiger - prevTrapTiger < 0:
                        indivReward = indivReward + (currentTrapTiger - prevTrapTiger)
                
                count += 1

                source = np.zeros((5,5))

                target = np.zeros((5,5))

                target[move["target"][0]][move["target"][1]] = 1
                

                if move["source"] is not None:
                    source[move["source"][0]][move["source"][1]] = 1
                
                
                source = source.flatten()
                target = target.flatten()
                
                flattenBoard = np.concatenate((goatBoard, tigerBoard, source, target, indivReward), axis=None)
                self.stateMemory = np.concatenate((self.stateMemory, flattenBoard), axis = 0)
                # print(playingGame.game_history)
                if count > 100:
                    break
            

            # reward distribution => total reward / (noOfPlays - i)
            

            noOfStates = len(self.game.game_history) - 1
            
            previousGameNo = previousGameNo + noOfStates
            

            totalReward = noOfStates * 2
            
            if self.game.game_state == GameState.TIGER_WON.value:
                totalReward = -1 * totalReward 
            
            elif self.game.game_state == GameState.NOT_DECIDED.value:
                totalReward = 0

            if totalReward != 0:
                for k in range(noOfStates):
                    if k % 2 == 0:
                        self.stateMemory[previousGameNo + k][71] = self.stateMemory[previousGameNo + k][71] + (totalReward / (noOfStates - k))
                    else:
                        self.stateMemory[previousGameNo + k][71] = self.stateMemory[previousGameNo + k][71] - (totalReward / (noOfStates - k))
                
            #Generate the Data for Training:
            #[playerGoat, plaerTiger] [state for Tiger], [state for Goat] [1  or 0]
        return {"Simulation End": True}


if __name__=="main":

    noOfSims = 3

    prevModel = None
    currentModel = None

    for _ in noOfSims:
        agentGoat = Agent(type = AgentType.GOAT.value, model = prevModel)
        agentTiger = Agent(type = AgentType.TIGER.value, model = currentModel)
        gameSimulation = Simulator(agentGoat = agentGoat, agentTiger = agentTiger)

        simulationResult = gameSimulation.play()

        if simulationResult["Simulation End"]:
            prevModel = currentModel 
            currentModel = Model()

            currentModel.training(flattendData = gameSimulation.stateMemory)
            
        
