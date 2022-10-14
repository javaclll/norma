import numpy as np
from tensorflow import keras
from functools import reduce
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

class Model:

    def __init__(self):
        self.optimizer = keras.optimizers.Adam(learning_rate=0.01)

        self.model = keras.models.Sequential()

        self.model.add(keras.layers.Conv2D(32, (5, 5), padding='same', input_shape=(5,5,4)))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))
        self.model.add(keras.layers.Conv2D(32, (4, 4), padding='same'))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))
        self.model.add(keras.layers.Conv2D(32, (4, 4), padding='same'))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))
        self.model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))
        self.model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))
        self.model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))
        self.model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))

        self.model.add(keras.layers.Flatten(input_shape=(5,5,4)))
        self.model.add(keras.layers.Dense(100))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))
        self.model.add(keras.layers.Dense(10))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))
        self.model.add(keras.layers.Dense(10))
        self.model.add(keras.layers.LeakyReLU(alpha=0.3))

        self.model.add(keras.layers.Dense(1, activation='linear'))
        self.model.compile(optimizer=self.optimizer, loss='mean_squared_error', metrics=['accuracy'])

        self.model.summary()

    def stateToTensor(self, flatStateMove, train = True):

        if train:
            print("FF", flatStateMove.shape)
            xTensor = flatStateMove[:,:-1]
            yTensor = flatStateMove[:,-1]
            print(xTensor)
            print(yTensor)
            print("xT",xTensor.shape)
            print("yT",yTensor.shape)
            
            yTensor = yTensor.reshape((1,1,1))
            xTensor = xTensor.reshape((1,5,5,-1))

            return xTensor, yTensor
        else:
            xTensor = flatStateMove.reshape((1,5,5,-1))
            return xTensor


    def training(self, flattendData, startLoss = 30):
        noOfData = flattendData.shape[0]

        print(noOfData)
        trainX = np.zeros((noOfData,5,5,4))
        trainY = np.zeros((noOfData,1,1))
        for index, data in enumerate(flattendData):
            xTensor, yTensor = self.stateToTensor(data.reshape((1,-1)))
            trainX[index, :, :, :] = xTensor
            trainY[index, :, :] = yTensor

        count = 0

        while startLoss > 0.02:
            self.model.fit(trainX, trainY, epochs = 10, batch_size = 256, verbose = 2)
            startLoss = self.model.evaluate(trainX, trainY, batch_size=256, verbose=2)[0]
            count += 1

            print("Counter: ", count, " Loss: ", startLoss)

            if count > 500:
                break

        newX = trainX[0,:,:,:]
        newX = newX[np.newaxis, :]

        print(newX.shape)
        print(self.model.predict(newX))

    def predict(self, state, source, target):

        flattenBoard = np.array(reduce(lambda z, y :z + y, state))
        goatBoard = (flattenBoard == 1) * 1
        tigerBoard = (flattenBoard == -1) * 1
        source = source.flatten()
        target = target.flatten()
        flattenBoard = np.concatenate((goatBoard, tigerBoard, source, target), axis=None)

        predictTensor = self.stateToTensor(flattenBoard.reshape((1,-1)), train = False)
        print(predictTensor.shape)

        predictedValue = self.model.predict(predictTensor, verbose = 2)
        print(predictedValue)
        return predictedValue

       
