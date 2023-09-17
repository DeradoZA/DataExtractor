import tensorflow as tf
from Shared.ModelCreator import ModelCreator

class PrecitionService:
    def __init__(self, modelSavePath) -> None:
        self.modelDirectory = modelSavePath
        self.modelCreator = ModelCreator(self.modelDirectory)

    def PredictClassChances(self, match):
        model = self.modelCreator.LoadModel()

        prediction = model.predict(match)

        return prediction
        
    
