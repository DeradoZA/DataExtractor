import tensorflow as tf
import numpy as np
import os

if __name__ == "__main__":
    modelSaveFolder = os.path.join(os.getcwd(), "models")

    model = tf.keras.models.load_model(modelSaveFolder)

    test_prediction_data = "25,2,8,3,64.0,9,0.64,1.75,0,1,0,32,5,17,4,41.0,9,1.0,1.29,1,0,0,41,5,14,5,54.0,13,1.09,1.71,3,1,0,17,4,13,2,71.0,12,0.77,1.31,1,0,0,17,5,13,2,35.0,6,0.77,1.31,1,1,0,9,1,28,1,44.0,4,0.41,0.45,0,0,0,17,2,17,2,59.0,10,0.77,1.0,1,0,0,33,2,18,0,50.0,6,0.55,0.67,0,0,0,16,3,20,1,62.0,10,0.73,0.8,0,0,0,11,4,19,2,18.0,2,0.5,0.58,1,0,0"

    example_array = np.fromstring(test_prediction_data, sep=',')

    number_of_features = 110
    example_array = example_array.reshape(1, number_of_features)

    example_array = example_array.astype(np.float32)

    # Make a prediction using the trained model
    prediction = model.predict(example_array)

    print("Prediction:", prediction)