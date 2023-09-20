from tensorflow.keras.models import load_model

class ModelCreator:
    def __init__(self, modelSavePath):
        self.modelPath = modelSavePath

    def LoadModel(self):
        model = load_model(self.modelPath)

        return model