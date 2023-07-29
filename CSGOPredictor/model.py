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

    test_prediction_data = "16,2,18,1,62.0,10,0.7,0.89,0,0,0,18,4,13,5,39.0,7,0.78,1.38,1,0,0,14,6,15,2,43.0,6,0.61,0.93,0,0,0,25,6,11,5,56.0,14,1.09,2.27,1,0,0,19,2,17,3,53.0,10,0.83,1.12,1,0,0,9,3,18,0,33.0,3,0.39,0.5,0,0,0,6,2,18,0,33.0,2,0.26,0.33,0,0,0,20,2,17,3,35.0,7,0.87,1.18,1,0,0,18,1,20,1,61.0,11,0.78,0.9,2,1,0,21,2,19,3,71.0,15,0.91,1.11,1,0,0"

# Convert the comma-separated string to a NumPy array
    example_array = np.fromstring(test_prediction_data, sep=',')

    # Reshape the example_array to a 2D array with shape (1, number_of_features)
    number_of_features = len(test_features.columns)
    example_array = example_array.reshape(1, number_of_features)

    example_array = example_array.astype(np.float32)

    # Make a prediction using the trained model
    prediction = model.predict(example_array)

    print("Prediction:", prediction)