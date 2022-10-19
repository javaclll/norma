from re import S
import numpy as np
import tensorflow as tf 
from tensorflow import keras
from functools import reduce
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.compat.v1.disable_eager_execution()


class Model:

    def __init__(self, savedModel = None):

        if savedModel:
            self.model = savedModel
        else:

            self.optimizer = keras.optimizers.Adam(learning_rate=0.01)

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

            self.model.add(keras.layers.InputLayer(input_shape = (104,)))
            self.model.add(keras.layers.Dense(10, kernel_initializer = keras.initializers.HeUniform()))
            self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            self.model.add(keras.layers.Dense(7, kernel_initializer = keras.initializers.HeUniform()))
            self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            self.model.add(keras.layers.Dense(3,  kernel_initializer = keras.initializers.HeUniform()))
            self.model.add(keras.layers.LeakyReLU(alpha=0.3))
            
            self.model.add(keras.layers.Dense(1, activation='linear'))
            self.model.compile(optimizer= self.optimizer, loss=keras.losses.Huber(), metrics=['mae'])

            self.model.summary()

    def stateToTensor(self, flatStateMove):
        xTensor = flatStateMove[:,:-1]
        yTensor = flatStateMove[:,-1]

        return xTensor, yTensor


    def training(self, flattendData, startLoss = 30, epochs = 50):
        noOfData = flattendData.shape[0]
        print(noOfData)
        trainX = np.zeros((noOfData, 104))
        trainY = np.zeros((noOfData,1))
        for index, data in enumerate(flattendData):
            xTensor, yTensor = self.stateToTensor(data.reshape((1,-1)))
            trainX[index, :] = xTensor
            trainY[index, :] = yTensor


        self.model.fit(trainX, trainY, epochs = epochs, batch_size = noOfData, verbose = 2)
        startLoss = self.model.evaluate(trainX, trainY, batch_size=256, verbose=2)[0]

        print("Loss: ", startLoss)

    def predict(self, moves, batch = True):
        if batch:
            noOfMoves = len(moves)
            predictTensor = np.zeros((0, 104))

            for i in range(noOfMoves):

                flattenBoard = np.array(reduce(lambda z, y :z + y, moves[i]["game"].board))
                goatBoard = (flattenBoard == 1) * 1
                tigerBoard = (flattenBoard == -1) * 1
                sourceX = moves[i]["source"]["x"]
                sourceY = moves[i]["source"]["y"]

                targetX = moves[i]["target"]["x"]
                targetY = moves[i]["target"]["y"]

                goatCaptured = np.zeros(6)
                goatCaptured[moves[i]["game"].goat_captured] = 1

                goatCounter = np.zeros(21)
                goatCounter[moves[i]["game"].goat_counter] = 1

                tigerTrap = np.zeros(5)
                tigerTrap[moves[i]["game"].trapped_tiger] = 1

                gameTurn = np.zeros(2)

                if moves[i]["game"].turn == 1:
                    gameTurn[0] = 1
                elif moves[i]["game"].turn == -1:
                    gameTurn[1] = 1

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

                goatCaptured = np.zeros(6)
                goatCaptured[moves[i]["game"].goat_captured] = 1

                goatCounter = np.zeros(21)
                goatCounter[moves[i]["game"].goat_counter] = 1

                tigerTrap = np.zeros(5)
                tigerTrap[moves[i]["game"].trapped_tiger] = 1

                gameTurn = np.zeros(2)

                if moves[i]["game"].turn == 1:
                    gameTurn[0] = 1
                elif moves[i]["game"].turn == -1:
                    gameTurn[1] = 1

                flattenBoard = np.concatenate((goatBoard, tigerBoard, sourceX, sourceY, targetX, targetY, goatCaptured, goatCounter, tigerTrap, gameTurn), axis=None)

                predictedValue.append(self.model.predict(flattenBoard))

            
            return predictedValue
        
