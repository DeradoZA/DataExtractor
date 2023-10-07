import tensorflow as tf
from ModelCreator import ModelCreator
from sklearn.preprocessing import StandardScaler

class PredictionService:
    def __init__(self, modelSavePath) -> None:
        self.modelDirectory = modelSavePath
        self.modelCreator = ModelCreator(self.modelDirectory)

    def PredictClassChances(self, match):
        model = self.modelCreator.LoadModel()
        scaler = StandardScaler()

        scaled_features = scaler.fit_transform(match)

        prediction = model.predict(match)

        return prediction
        
    
