from game.bagchal import Bagchal
from game.bagchal.enum import GameState
from .agent import Agent

from functools import reduce
import numpy as np


class Simulator:

    def __init__(self, agentGoat: Agent, agentTiger: Agent, game: Bagchal):
        self.agentGoat = agentGoat
        self.agentTiger = agentTiger
        self.game = Bagchal.new()
        self.stateMemory = np.zeros((0, 71))

    def play(self, noOfPlays):

        previousGameNo = 0
        
        for _ in range(noOfPlays):
            # agentGoat.getState()
            # agentTiger.moveState()

            while not self.game.game_status_check()["decided"]:
                
                indivReward = 0
                
                flattenBoard = np.array(reduce(lambda z, y :z + y, self.game.game_history[-1]["board"]))
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

                sourceOne = np.zeros(5)
                sourceTwo = np.zeros(5)

                targetOne = np.zeros(5)
                targetTwo = np.zeros(5)

                targetOne[move["target"][0]] = 1
                targetTwo[move["target"][1]] = 1

                if move["source"] is not None:
                    sourceOne[move["source"][0]] = 1
                    sourceTwo[move["source"][1]] = 1
                
                flattenBoard = np.concatenate((goatBoard, tigerBoard, sourceOne, sourceTwo, targetOne, targetTwo, indivReward), axis=None)
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

            if totalReward is not 0:
                for k in range(noOfStates):
                    if k % 2 == 0:
                        self.stateMemory[previousGameNo + k][71] = self.stateMemory[previousGameNo + k][71] + (totalReward / (noOfStates - k))
                    else:
                        self.stateMemory[previousGameNo + k][71] = self.stateMemory[previousGameNo + k][71] - (totalReward / (noOfStates - k))
                
            #Generate the Data for Training:
            #[playerGoat, plaerTiger] [state for Tiger], [state for Goat] [1  or 0]
        #[return data in the form [state, action pair] and reward]