from model import Model
from bagchal import GameState, Bagchal
from helpers import movestoAction
import csv
import os
import tensorflow
import numpy as np

import math
from constants import GOATMODELPATH, MODELPATH, TARGETMODELPATH, TIGERMODELPATH


def loadModels():
    goatModel = None
    tigerModel = None
    if os.path.exists(GOATMODELPATH):
        loadedModel = tensorflow.keras.models.load_model(GOATMODELPATH)
        goatModel = Model(savedModel=loadedModel)

    if os.path.exists(TIGERMODELPATH):
        loadedModel = tensorflow.keras.models.load_model(TIGERMODELPATH)
        tigerModel = Model(savedModel=loadedModel)

    print("Model Loaded")
    return goatModel, tigerModel


def generateAgentPlay():
    print("I am Here")
    goatModel, tigerModel = loadModels()
    print(goatModel)
    print(tigerModel)
    if goatModel and tigerModel:
        with open("agentplayrecord.csv", "w") as file:
            writer = csv.writer(file)
            field = [
                "Norma Agent",
                "Wins",
                "Loss",
                "Draw",
                "Game No",
                "Predicted Invalid Moves",
                "Turns",
            ]
            writer.writerow(field)

        goatDraw = 0
        goatWin = 0
        goatLoss = 0
        invalidMovesPredictedGoat = []
        gameGoatTurns = []

        tigerDraw = 0
        tigerWin = 0
        tigerLoss = 0
        invalidMovesPredictedTiger = []
        gameTigerTurns = []
        for i in range(0, 2000 + 1):
            game = Bagchal.new()

            done = False
            tigerTurn = 0
            goatTurn = 0
            while not done:
                possibleMoves = game.get_possible_moves()

                if game.turn == -1:
                    tigerTurn += 1

                    actions = []

                    for move in possibleMoves:
                        actions.append(movestoAction(move["move"][0], move["move"][1]))

                    prediction = tigerModel.predict(game)[0]

                    # Compute the probabilities using the softmax function
                    probabilities = np.exp(prediction / 0.5) / np.sum(
                        np.exp(prediction / 0.5), axis=0
                    )

                    # Choose an action based on the computed probabilities
                    action = np.random.choice(len(prediction), p=probabilities)

                    print(np.shape(prediction))
                    invalidMovePredictedTiger = 0
                    while action not in actions:
                        invalidMovePredictedTiger += 1
                        prediction[action] = -math.inf
                        probabilities = np.exp(prediction / 0.5) / np.sum(
                            np.exp(prediction / 0.5), axis=0
                        )
                        # Choose an action based on the computed probabilities
                        action = np.random.choice(len(prediction), p=probabilities)

                    moveIndex = actions.index(action)

                    invalidMovesPredictedTiger.append(invalidMovePredictedTiger)

                    move = possibleMoves[moveIndex]
                else:
                    goatTurn += 1

                    actions = []

                    for move in possibleMoves:
                        actions.append(movestoAction(move["move"][0], move["move"][1]))

                    prediction = goatModel.predict(game)[0]

                    # Compute the probabilities using the softmax function
                    probabilities = np.exp(prediction / 0.01) / np.sum(
                        np.exp(prediction / 0.01), axis=0
                    )

                    # Choose an action based on the computed probabilities
                    action = np.random.choice(len(prediction), p=probabilities)

                    print(np.shape(prediction))
                    invalidMovePredictedGoat = 0
                    while action not in actions:
                        invalidMovePredictedGoat += 1
                        prediction[action] = -math.inf
                        probabilities = np.exp(prediction / 0.01) / np.sum(
                            np.exp(prediction / 0.01), axis=0
                        )
                        # Choose an action based on the computed probabilities
                        action = np.random.choice(len(prediction), p=probabilities)

                    invalidMovesPredictedGoat.append(invalidMovePredictedGoat)

                    moveIndex = actions.index(action)

                    move = possibleMoves[moveIndex]

                game.move(move["move"][0], move["move"][1])

                if game.game_status_check()["decided"] or len(game.game_history) > 100:
                    if game.game_state == GameState.TIGER_WON.value:
                        tigerWin += 1
                        goatLoss += 1
                    elif game.game_state == GameState.GOAT_WON.value:
                        tigerLoss += 1
                        goatWin += 1
                    else:
                        tigerDraw += 1
                        goatDraw += 1

                    done = True

            gameTigerTurns.append(tigerTurn)
            gameGoatTurns.append(goatTurn)

            if i % 50 == 0:
                with open("agentplayrecord.csv", "a+") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [
                            -1,
                            tigerWin,
                            tigerLoss,
                            tigerDraw,
                            i + 1,
                            invalidMovesPredictedTiger,
                            gameTigerTurns,
                        ]
                    )
                    writer.writerow(
                        [
                            1,
                            goatWin,
                            goatLoss,
                            goatDraw,
                            i + 1,
                            invalidMovesPredictedGoat,
                            gameGoatTurns,
                        ]
                    )
