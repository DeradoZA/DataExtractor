import os
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    dataCSV = os.path.join(os.getcwd(), "..", "DataExtractor", "FormattedStats", "FormattedCSGOStats.csv")
    modelSaveFolder = os.path.join(os.getcwd(), "models")

    df = pd.read_csv(dataCSV)

    train_size = int(0.8 * len(df))
    val_size = int(0.1 * len(df))

    train_data = df[:train_size]
    val_data = df[train_size:train_size + val_size]
    test_data = df[train_size + val_size:]

    train_features, train_labels = train_data.drop("ScoreDifference", axis=1), train_data['ScoreDifference']
    validation_features, validation_labels = val_data.drop("ScoreDifference", axis=1), val_data['ScoreDifference']
    test_features, test_labels = test_data.drop("ScoreDifference", axis=1), test_data['ScoreDifference']

    batch_size = 32

    train_dataset = tf.data.Dataset.from_tensor_slices((train_features, train_labels)).batch(batch_size)
    validation_dataset = tf.data.Dataset.from_tensor_slices((validation_features, validation_labels)).batch(batch_size)
    test_dataset = tf.data.Dataset.from_tensor_slices((test_features, test_labels)).batch(batch_size)

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(110, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ]
    )

    model.compile(optimizer='adam', loss='mean_squared_error')

    EPOCHS = 100

    model.fit(train_dataset, validation_data=validation_dataset, epochs=EPOCHS, verbose=1)

    model.save(modelSaveFolder)

    predictionLoss = model.evaluate(test_dataset)

    print(f"Test Loss: {predictionLoss}")

    predictions = model.predict(test_features)

    plt.scatter(test_labels, predictions, alpha=0.5)
    plt.xlabel('Actual Score Difference')
    plt.ylabel('Predicted Score Difference')
    plt.title('Actual vs. Predicted Score Difference')
    plt.show()

    test_prediction_data = "21,4,20,2,29.0,6,0.72,1.05,0,1,0,21,3,19,2,29.0,6,0.72,1.11,0,0,0,9,3,25,2,56.0,5,0.31,0.36,0,0,0,22,5,23,2,41.0,9,0.76,0.96,1,0,0,30,6,22,5,43.0,13,1.03,1.36,3,0,1,15,6,23,1,73.0,11,0.52,0.65,1,0,0,32,0,20,5,31.0,10,1.1,1.6,3,0,0,14,6,23,1,57.0,8,0.48,0.61,0,0,0,14,4,21,1,64.0,9,0.48,0.67,0,0,0,34,3,16,8,41.0,14,1.17,2.12,5,1,0"

# Convert the comma-separated string to a NumPy array
    example_array = np.fromstring(test_prediction_data, sep=',')

    # Reshape the example_array to a 2D array with shape (1, number_of_features)
    number_of_features = len(test_features.columns)
    example_array = example_array.reshape(1, number_of_features)

    example_array = example_array.astype(np.float32)

    # Make a prediction using the trained model
    prediction = model.predict(example_array)

    print("Prediction:", prediction)