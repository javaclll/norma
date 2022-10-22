from abc import abstractmethod
import math
from tabnanny import verbose
from .helpers import movestoAction
import numpy as np
import tensorflow as tf 
from tensorflow import keras
from functools import reduce
import os
import random
from .constants import DISCOUNTFACTOR, OBSERVATIONSPACE, ACTIONSPACE

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.compat.v1.disable_eager_execution()


class Model:

    def __init__(self, savedModel = None):

        if savedModel:
            self.model = savedModel
        else:

            optimizer = keras.optimizers.Adam(learning_rate=0.001)
            initializer = keras.initializers.HeUniform()


            self.model = keras.Sequential()

            # self.model.add(keras.layers.Conv2D(32, (5, 5), padding='same', input_shape=(5,5,4)))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Conv2D(32, (4, 4), padding='same'))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Conv2D(32, (4, 4), padding='same'))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))

            # self.model.add(keras.layers.Flatten(input_shape=(5,5,4)))

            # self.model.add(keras.layers.Dense(74, kernel_initializer = keras.initializers.HeUniform()))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Dense(10, kernel_initializer = keras.initializers.HeUniform()))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Dense(10, kernel_initializer = keras.initializers.HeUniform()))
            # self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            # self.model.add(keras.layers.Dense(ACTIONSPACE, activation='linear'))
            # self.model.compile(optimizer= self.optimizer, loss=keras.losses.Huber(), metrics=['mae'])
            
            self.model.add(keras.layers.Dense(70, input_shape = (OBSERVATIONSPACE,), kernel_initializer = initializer))
            self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            self.model.add(keras.layers.Dense(30, kernel_initializer = initializer))
            self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            self.model.add(keras.layers.Dense((ACTIONSPACE, activation='linear', kernel_initializer = initializer))
            self.model.compile(optimizer= optimizer, loss=keras.losses.Huber(), metrics=['accuracy'])
    
            self.model.summary()

    def predict(self, game):

            flattenBoard = np.array(reduce(lambda z, y :z + y, game.board))
            goatBoard = (flattenBoard == 1) * 1
            tigerBoard = (flattenBoard == -1) * 1
            
            goatCaptured = np.zeros(5)
            
            goatCaptured[game.goat_captured - 1] = 1

            goatCounter = np.zeros(20)
            goatCounter[game.goat_counter - 1] = 1

            tigerTrap = np.zeros(4)
            tigerTrap[game.trapped_tiger - 1] = 1

            gameTurn = np.zeros(2)
            gameTurn[game.turn - 1] = 1

            predictTensor = np.concatenate((goatBoard, tigerBoard, tigerTrap, goatCaptured, goatCounter, gameTurn), axis=None)

            predictedValue = self.model.predict(predictTensor.reshape(1,-1))
            return predictedValue

    @abstractmethod
    def training(replayMemory, mainModel, targetModel, done):

        noOfData = len(replayMemory)

        affectFactor = 0.7
        batchSize = 1000
        if noOfData < batchSize:
            return

        
        batchSize = 1000

        miniBatch = random.sample(replayMemory, batchSize)
        miniBatchPossibleMoves = []
        miniBatchMemory = []

        for data in miniBatch:
            miniBatchPossibleMoves.append(data[0])
            miniBatchMemory.append(data[1])
        
        currentState = np.array([data[0][0:OBSERVATIONSPACE] for data in miniBatchMemory])
        currentActionList = mainModel.model.predict(currentState)

        newStates = np.array([data[0][OBSERVATIONSPACE + 1:OBSERVATIONSPACE + OBSERVATIONSPACE + 1] for data in miniBatchMemory])
        futureActionList = mainModel.model.predict(newStates)

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
                
                predictedTargetFuture = targetModel.model.predict(data[0][OBSERVATIONSPACE + 1: (OBSERVATIONSPACE * 2) + 1].reshape(1, -1))[0][action]
                maxFutureReward = data[0][-2] - DISCOUNTFACTOR * predictedTargetFuture
            
            else:
                maxFutureReward = data[0][-2]
            

            currentReward = currentActionList[index]


            currentReward[int(data[0][OBSERVATIONSPACE])] = (1 - affectFactor) * currentReward[int(data[0][OBSERVATIONSPACE])] + affectFactor * maxFutureReward

            trainX[index, :] = data[0][0:OBSERVATIONSPACE]
            trainY[index, :] = currentReward
        
        mainModel.model.fit(trainX, trainY, batch_size = batchSize, verbose = 2, shuffle = True)



        
