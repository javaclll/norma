import math
import numpy
import tensorflow
import os
import random

from abc import abstractmethod
from functools import reduce
# from .actionmapper import movestoAction

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tensorflow.compat.v1.disable_eager_execution()

def model():
    print("Inside Model")
    optimizer = tensorflow.keras.optimizers.Adam(learning_rate = 0.001)
    
    inputData = tensorflow.keras.Input(shape = (109,))

    inputBoard = tensorflow.keras.layers.Reshape((5,5,3))(inputData[:,0:75])
    inputMisc = tensorflow.keras.layers.Reshape((34,))(inputData[:,75:]) # 2 Turn, 21 Goats Place, 5 Tiger Locked, 6 Goats Captured

    convBoard = tensorflow.keras.layers.Conv2D(16, (2,2), activation = "relu")(inputBoard)
    poolBoard = tensorflow.keras.layers.AveragePooling2D(pool_size = (2, 2), strides = (1, 1))(convBoard)
    flattenBoard = tensorflow.keras.layers.Flatten()(poolBoard)

    concatenatedNodes = tensorflow.keras.layers.Concatenate()([flattenBoard, inputMisc])

    layerOne = tensorflow.keras.layers.Dense(256, activation = "relu")(concatenatedNodes)
    layerTwo = tensorflow.keras.layers.Dense(256, activation = "relu")(layerOne)
    outputLayer = tensorflow.keras.layers.Dense(217, activation = "softmax")(layerTwo)

    model = tensorflow.keras.Model(inputs = inputData, outputs = outputLayer)
    model.compile(optimizer = optimizer, loss = tensorflow.keras.losses.Huber(), metrics = ['accuracy'])
    model.summary()
    print(model)
    return model

def predict(game):

    flattenBoard = numpy.array(reduce(lambda z, y : z + y, game.board))
    
    emptyBoard = numpy.zeros(25)

    goatBoard = (flattenBoard == 1) * 1
    tigerBoard = (flattenBoard == -1) * 1
    goatCaptured = numpy.zeros(6)
    goatCaptured[game.goat_captured] = 1

    goatCounter = numpy.zeros(21)
    goatCounter[game.goat_counter] = 1

    tigerTrap = numpy.zeros(5)
    tigerTrap[game.trapped_tiger] = 1

    turn = numpy.zeros(2)
    if game.turn == 1:
        turn[0] = 1 
    elif game.turn == -1:
        turn[1] = 1
    
    predictTensor = numpy.concatenate((emptyBoard, goatBoard, tigerBoard, tigerTrap, goatCaptured, goatCounter, turn), axis = None)

    predictionModel = model(predictTensor.reshape(1,-1))


def training(replayMemory, mainModel, opponentTargetModel, done):

    noOfData = len(replayMemory)

    affectFactor = 0.7
    batchSize = 512
    if noOfData < batchSize:
        return
    
    miniBatch = random.sample(replayMemory, batchSize)
    miniBatchPossibleMoves = []
    miniBatchMemory = []

    for data in miniBatch:
        miniBatchPossibleMoves.append(data[0])
        miniBatchMemory.append(data[1])
    print(miniBatch[0][1][0][0:OBSERVATIONSPACE])
    print(miniBatch[0][1][0][OBSERVATIONSPACE + 1:(OBSERVATIONSPACE * 2) + 1])

    currentState = np.array([data[0][0:OBSERVATIONSPACE] for data in miniBatchMemory])
    currentActionList = mainModel.model.predict(currentState)

    newStates = np.array([data[0][OBSERVATIONSPACE + 1 : OBSERVATIONSPACE + OBSERVATIONSPACE + 1] for data in miniBatchMemory])
    futureActionList = opponentTargetModel.model.predict(newStates)

    trainX = np.zeros((batchSize, OBSERVATIONSPACE))
    trainY = np.zeros((batchSize, ACTIONSPACE))

    for index, data in enumerate(miniBatchMemory):
        if not data[0][-1]:
            actions = []
            action = np.argmax(futureActionList[index])

            for move in miniBatchPossibleMoves[index]:

                actions.append(movestoAction(move["move"][0], move["move"][1]))

            while action not in actions:
                futureActionList[index][action] = - math.inf
                action = np.argmax(futureActionList[index])
            
            predictedTargetFuture = futureActionList[index][action]
            maxFutureReward = data[0][-2] - DISCOUNTFACTOR * predictedTargetFuture
        
        else:
            maxFutureReward = data[0][-2]
        
        currentReward = currentActionList[index]

        currentReward[int(data[0][OBSERVATIONSPACE])] = (1 - affectFactor) * currentReward[int(data[0][OBSERVATIONSPACE])] + affectFactor * maxFutureReward

        trainX[index, :] = data[0][0:OBSERVATIONSPACE]
        trainY[index, :] = currentReward
    
    mainModel.model.fit(trainX, trainY, batch_size = batchSize, verbose = 2, shuffle = True)

    










