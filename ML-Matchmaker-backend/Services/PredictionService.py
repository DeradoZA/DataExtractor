import tensorflow as tf
from ModelCreator import ModelCreator

class PredictionService:
    def __init__(self, modelSavePath) -> None:
        self.modelDirectory = modelSavePath
        self.modelCreator = ModelCreator(self.modelDirectory)

    def PredictClassChances(self, match):
        model = self.modelCreator.LoadModel()

        prediction = model.predict(match)

        return prediction
        
    
