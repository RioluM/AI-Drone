import pickle
from pickle import UnpicklingError
import numpy as np
import tensorflow as tf


if __name__ == "__main__":
    xTrain = []
    yTrain = []
    file = open('X.pickle', 'rb')
    while True:
        try:
            xTrain.append(pickle.load(file))
        except (EOFError, UnpicklingError):
            break
    file.close()
    file = open('Y.pickle', 'rb')
    while True:
        try:
            yTrain.append(pickle.load(file))
        except (EOFError, UnpicklingError):
            break
    file.close()
    xTrain = np.array(xTrain)
    yTrain = np.array(yTrain)
    inputs = tf.keras.Input(shape=(9,))
    x = tf.keras.layers.Dense(32, activation='relu')(inputs)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    predictions = tf.keras.layers.Dense(2)(x)
    model = tf.keras.Model(inputs=inputs, outputs=predictions)
    model.compile(optimizer='adam',
                  loss='mse',
                  metrics=['accuracy'])
    model.fit(xTrain, yTrain, epochs=200)
    model.save('./my_model')