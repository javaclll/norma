from bagchal import GameState, Bagchal
from bagchal.bagchal import G_LOSE
from .agent import Agent
from .model import Model
from .constants import MODELPATH, GOATMODELPATH, TIGERMODELPATH
from .constants import DECAYFACTOR, NUMSIMS, DISCOUNTFACTOR
from functools import reduce
import numpy as np
import math

# For Tiger
T_GOAT_CAPTURED = 1.5
T_GOT_TRAPPED = -1.5
T_TRAP_ESCAPE = 1

# For Goat
G_GOAT_CAPTURED = -1.5
G_TIGER_TRAP = 1.5
G_TIGER_ESCAPE = -1

#Common 
G_WIN = 4
T_WIN = 2
T_LOSE = -2
G_LOSE = -4

class Simulator:

    def __init__(self, agent: Agent, model: Model, goatWinPgn = []):
        self.model = model
        self.agent = agent
        self.game = Bagchal.new()
        self.stateMemory = np.zeros((0, 105))
        self.goatWinPgn = goatWinPgn

    def rewardPropagation(self):

        pgnUnit = ""
        goatWin = False
    
        while not self.game.game_status_check()["decided"]:
            
            indivReward = 0
            
            flattenBoard = np.array(reduce(lambda z, y :z + y, self.game.board))
            goatBoard = (flattenBoard == 1) * 1
            tigerBoard = (flattenBoard == -1) * 1

            turn = self.game.turn 
            placedGoat = self.game.goat_counter
            prevTrapTiger = self.game.trapped_tiger
            prevGoatCapture = self.game.goat_captured

            move, self.game = self.agent.move(self.game)

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
                goatWin = True
                if turn == 1:
                    indivReward += G_WIN
                else:
                    indivReward += T_LOSE
        
            elif self.game.game_state == GameState.TIGER_WON.value:
                if turn == 1:
                    indivReward += G_LOSE
                else:
                    indivReward += T_WIN
        
            elif self.game.game_state == GameState.NOT_DECIDED.value:
                _, futureReward = self.agent.predictMove(self.game)
                
                indivReward -= DISCOUNTFACTOR * futureReward
            


            source = np.zeros((5,5))

            target = np.zeros((5,5))

            target[move["move"][1][0]][move["move"][1][1]] = 1
            
            if move["move"][0] is not None:
                source[move["move"][0][0]][move["move"][0][1]] = 1

            source = source.flatten()
            target = target.flatten()

            flattenBoard = np.concatenate((goatBoard, tigerBoard, source, target, prevTrapTiger, prevGoatCapture, placedGoat, turn, indivReward), axis=None).reshape((1,-1))
            pgnUnit += Bagchal.coord_to_png_unit(*move["resulting_state"].prev_move) + "-"
            
            # self.model.training(flattenBoard, epochs = 1)
            self.stateMemory = np.concatenate((self.stateMemory, flattenBoard), axis = 0)
    
            if len(self.game.game_history) > 100:
                break
        
        self.model.training(self.stateMemory)
        
        self.stateMemory = np.zeros((0, 105))
        
        if goatWin == True:
            self.goatWinPgn.append(pgnUnit)
            goatWin = False
        
        print(pgnUnit[0:-1])
        pgnUnit = ""
        # previousGameNo = previousGameNo + noOfStates

        # noOfStates = len(self.game.game_history) - 1            
        
        # print("No Of States", noOfStates)
        
        # if self.game.game_state == GameState.GOAT_WON.value:
        #     for k in range(noOfStates):
        #         if k % 2 == 0:
        #             self.stateMemory[previousGameNo + k][104] = (self.stateMemory[previousGameNo + k][104]) + G_WIN
        #         else:
        #             self.stateMemory[previousGameNo + k][104] = self.stateMemory[previousGameNo + k][104] + T_LOSE
        
        # elif self.game.game_state == GameState.TIGER_WON.value:
        #     for k in range(noOfStates):
        #         if k % 2 == 0:
        #             self.stateMemory[previousGameNo + k][104] = self.stateMemory[previousGameNo + k][104] + G_LOSE
        #         else:
        #             self.stateMemory[previousGameNo + k][104] = self.stateMemory[previousGameNo + k][104] + T_WIN
        

        self.game = Bagchal.new()
    
        return self.model


def simulate(goatModel = None, tigerModel = None, model = None):
    if model == None:
        model = Model()
    EXPLORATION = 0.3

    goatPGN = []
    for noSims in range(NUMSIMS):

        EXPLORATION = EXPLORATION * DECAYFACTOR
            
        agent = Agent(model = model, epsilon = EXPLORATION)

        gameSimulation = Simulator(agent = agent, model = model, goatWinPgn = goatPGN)
        
        model = gameSimulation.rewardPropagation()
       
        # if simulationResult["Simulation End"]:
        goatPGN = gameSimulation.goatWinPgn
        #     model.training(flattendData = gameSimulation.stateMemory)
        print("Goat Win PGN:" , goatPGN)

        if goatModel != None:

            goatModel.model.save(GOATMODELPATH)   #save to a location

        if tigerModel != None:

            goatModel.model.save(TIGERMODELPATH)
        
        if model != None:
            print()
            print(f"MODEL SAVED at {noSims + 1}")
            print()
            
        

            # model.model.save(MODELPATH)

    return model.model