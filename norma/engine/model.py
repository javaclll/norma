from abc import abstractmethod
from tabnanny import verbose
import numpy as np
import tensorflow as tf 
from tensorflow import keras
from functools import reduce
import os
import random
from .constants import DISCOUNTFACTOR

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.compat.v1.disable_eager_execution()


class Model:

    def __init__(self, savedModel = None):

        if savedModel:
            self.model = savedModel
        else:

            self.optimizer = keras.optimizers.Adam(learning_rate=0.001)

            self.model = keras.models.Sequential()

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

            self.model.add(keras.layers.InputLayer(input_shape = (74,)))
            self.model.add(keras.layers.Dense(74, kernel_initializer = keras.initializers.HeUniform()))
            self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            self.model.add(keras.layers.Dense(10, kernel_initializer = keras.initializers.HeUniform()))
            self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            self.model.add(keras.layers.Dense(10, kernel_initializer = keras.initializers.HeUniform()))
            self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            self.model.add(keras.layers.Dense(121, activation='linear'))
            self.model.compile(optimizer= self.optimizer, loss=keras.losses.Huber(), metrics=['mae'])

            self.model.summary()

    def predict(self, moves, batch = True):
        if batch:
            noOfMoves = len(moves)
            predictTensor = np.zeros((0, 74))

            for i in range(noOfMoves):

                flattenBoard = np.array(reduce(lambda z, y :z + y, moves[i]["game"].board))
                goatBoard = (flattenBoard == 1) * 1
                tigerBoard = (flattenBoard == -1) * 1
                sourceX = moves[i]["source"]["x"]
                sourceY = moves[i]["source"]["y"]

                targetX = moves[i]["target"]["x"]
                targetY = moves[i]["target"]["y"]

                goatCaptured = moves[i]["game"].goat_captured

                goatCounter = moves[i]["game"].goat_counter

                tigerTrap = moves[i]["game"].trapped_tiger

                gameTurn = moves[i]["game"].turn

                flattenBoard = np.concatenate((goatBoard, tigerBoard, sourceX, sourceY, targetX, targetY, goatCaptured, goatCounter, tigerTrap, gameTurn), axis=None)
                predictTensor = np.concatenate((predictTensor, flattenBoard.reshape((1,-1))), axis = 0)

            predictedValue = self.model.predict_on_batch(predictTensor)

            return predictedValue
        else:
            noOfMoves = len(moves)

            predictedValue = [] 

            for i in range(noOfMoves):
                flattenBoard = np.array(reduce(lambda z, y :z + y, moves[i]["game"].board))
                goatBoard = (flattenBoard == 1) * 1
                tigerBoard = (flattenBoard == -1) * 1
                sourceX = moves[i]["source"]["x"]
                sourceY = moves[i]["source"]["y"]

                targetX = moves[i]["target"]["x"]
                targetY = moves[i]["target"]["y"]

                goatCaptured = moves[i]["game"].goat_captured

                goatCounter = moves[i]["game"].goat_counter

                tigerTrap = moves[i]["game"].trapped_tiger

                gameTurn = moves[i]["game"].turn

                flattenBoard = np.concatenate((goatBoard, tigerBoard, sourceX, sourceY, targetX, targetY, goatCaptured, goatCounter, tigerTrap, gameTurn), axis=None)

                predictedValue.append(self.model.predict(flattenBoard))

            return predictedValue

    @abstractmethod
    def training(replayMemory, mainModel, targetModel, done):

        noOfData = len(replayMemory)

        affectFactor = 0.7
        MINREPLAYSIZE = 1500
        if noOfData < MINREPLAYSIZE:
            return

        
        batchSize = 1000

        miniBatch = random.sample(replayMemory, batchSize)

        for data in miniBatch:
            print("Current : ", data[0][0:74])
            print("Future :", data[0][74:148])
            print("Reward, Done : ", data[0][-2:])
        
        currentState = np.array([data[0][0:74] for data in miniBatch])
        currentRewardList = mainModel.model.predict(currentState)

        newStates = np.array([data[0][74:148] for data in miniBatch])
        futureRewardList = mainModel.model.predict(newStates)

        trainX = np.zeros((batchSize, 74))
        trainY = np.zeros((batchSize,1))

        for index, data in enumerate(miniBatch):
            if not data[0][-1]:
                maxFutureReward = data[0][-2] - DISCOUNTFACTOR * futureRewardList[index]
            else:
                maxFutureReward = data[0][-2]
            
            print("Max Future Reward: ", maxFutureReward)

            currentReward = (1 - affectFactor) * currentRewardList[index] + affectFactor * maxFutureReward
            print("Current Reward: ", currentReward)

            trainX[index, :] = data[0][0:74]
            trainY[index, :] = currentReward
        
        mainModel.model.fit(trainX, trainY, batch_size = batchSize, verbose = 2, shuffle = True)



        
