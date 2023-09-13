import keras_tuner as kt
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import numpy as np

if __name__ == "__main__":
    modelDirectory = os.path.join(os.getcwd(), "..", "..", "CSGOML", "CSGOPredictor", "bestModel", "best_model.h5")

    gameEntry = [1.1542220048096954,0.7976232896948982,67.83687733715416,10.861241660158857,1.0815058563012854,1.1670215152407812,89.70973128123161,947.0,0.995756992779526,0.7209374739856538,64.07759760919527,9.793139903243638,0.9429070518446053,1.0277490510999387,81.00531728333118,1007.8]
    gameEntry = np.array(gameEntry)
    gameEntry = np.reshape(gameEntry, (1, -1))

    loaded_model = load_model(modelDirectory)

    loaded_model.summary()

    predictions = loaded_model.predict(gameEntry)

    print(predictions)

