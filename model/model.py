import numpy as np
import keras
import keras.layers as kl
import keras.models as km
from keras import optimizers
from functools import reduce

class Model:

    def __init__(self):
        self.optimizer = optimizers.Adam(learning_rate=0.01)

        self.model = km.Sequential()

        self.model.add(kl.Conv2D(32, (5, 5), padding='same', input_shape=(5,5,4)))
        self.model.add(kl.LeakyReLU(alpha=0.3))
        self.model.add(kl.Conv2D(32, (4, 4), padding='same'))
        self.model.add(kl.LeakyReLU(alpha=0.3))
        self.model.add(kl.Conv2D(32, (4, 4), padding='same'))
        self.model.add(kl.LeakyReLU(alpha=0.3))
        self.model.add(kl.Conv2D(64, (3, 3), padding='same'))
        self.model.add(kl.LeakyReLU(alpha=0.3))
        self.model.add(kl.Conv2D(64, (3, 3), padding='same'))
        self.model.add(kl.LeakyReLU(alpha=0.3))
        self.model.add(kl.Conv2D(64, (3, 3), padding='same'))
        self.model.add(kl.LeakyReLU(alpha=0.3))
        self.model.add(kl.Conv2D(64, (3, 3), padding='same'))
        self.model.add(kl.LeakyReLU(alpha=0.3))

        self.model.add(kl.Flatten(input_shape=(5,5,4)))
        self.model.add(kl.Dense(100))
        self.model.add(kl.LeakyReLU(alpha=0.3))
        self.model.add(kl.Dense(10))
        self.model.add(kl.LeakyReLU(alpha=0.3))
        self.model.add(kl.Dense(10))
        self.model.add(kl.LeakyReLU(alpha=0.3))

        self.model.add(kl.Dense(1, activation='linear'))
        self.model.compile(optimizer=self.optimizer, loss='mean_squared_error', metrics=['accuracy'])

        self.model.summary()

    def stateToTensor(self, flatStateMove):
        xTensor = flatStateMove[:-2]
        yTensor = flatStateMove[-1]
        
        yTensor = yTensor.reshape((1,1,1))
        xTensor = xTensor.reshape((1,-1,5,5))

        return xTensor, yTensor



    def training(self, flattendData, startLoss = 30):
        noOfData = flattendData.shape[0]
        trainX = np.zeros((noOfData,4,5,5))
        trainY = np.zeros((noOfData,1,1))
        for index, data in enumerate(flattendData):
            xTensor, yTensor = self.stateToTensor(data)
            trainX[index, :, :, :] = xTensor
            trainY[index, :, :] = yTensor

        count = 0

        while startLoss > 0.02:
            self.model.fit(trainX, trainY, epochs = 10, batch_size = 256, verbose = 2)
            startLoss = self.model.evaluate(trainX, trainY, batch_size=256, verbose=2)
            count += 1

            print("Counter: ", count, " Loss: ", startLoss)

    def predict(self, state, source, target):

        flattenBoard = np.array(reduce(lambda z, y :z + y, state))
        goatBoard = (flattenBoard == 1) * 1
        tigerBoard = (flattenBoard == -1) * 1
        source = source.flatten()
        target = target.flatten()
        flattenBoard = np.concatenate((goatBoard, tigerBoard, source, target), axis=None)

        predictTensor = self.stateToTensor(flattenBoard)

        predictedValue = self.model.predict(predictTensor, verbose = 2)

        return predictedValue
        

    def NNModel():
        pass

       
