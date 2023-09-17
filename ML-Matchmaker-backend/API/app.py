from flask import Flask
import os
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../Services'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../Shared'))
from PlayerService import PlayerService
from DBConnectionCreator import DBConnectionCreator
from TeamService import TeamService
from PredictionService import PredictionService



app = Flask(__name__)

@app.route('/randomMatch')
def getRandomMatch():
    modelPath = os.path.join(os.getcwd(), "..", "..", "CSGOML", "CSGOPredictor", "bestModel", "best_model.h5")


    dbCreator = DBConnectionCreator('csgo', 'csgoDB', 'pwd')
    predictionService = PredictionService(modelPath)
    connection, cursor = dbCreator.dbConnection()
    playerService = PlayerService(cursor)
    teamService = TeamService()

    playerCount = 0
    playerList = []
    teamOne = []
    teamTwo = []
    teamOneELOs = []
    teamTwoELOs = []

    while playerCount < 10:
        playerID = playerService.getRandomPlayer()
        validPlayer = playerService.playerValidator(playerID)

        if validPlayer == True:
            playerCount += 1
            playerList.append(playerID)

    for i in range(0, 5):
        player = playerList[i]

        playerELO = playerService.getPlayerELO(player)
        teamOneELOs.append(playerELO)
        averagedPlayerStats = playerService.calculatePlayerStats(player)
        teamOne.append(averagedPlayerStats)

    for i in range(6, 10):
        player = playerList[i]

        playerELO = playerService.getPlayerELO(player)
        teamTwoELOs.append(playerELO)
        averagedPlayerStats = playerService.calculatePlayerStats(player)
        teamTwo.append(averagedPlayerStats)

    teamOneAveragedELO = teamService.calculateELOAverages(teamOneELOs)
    teamTwoAveragedELO = teamService.calculateELOAverages(teamTwoELOs)
    teamOneAveragedStats = teamService.calculateTeamAverages(teamOne)
    teamTwoAveragedStats = teamService.calculateTeamAverages(teamTwo)

    fullMatchStats = np.array(teamOneAveragedELO + teamTwoAveragedStats + teamTwoAveragedELO + teamTwoAveragedStats)
    fullMatchStats = fullMatchStats.reshape(-1, 1)

    print(fullMatchStats)

    matchPrediction = predictionService.PredictClassChances(fullMatchStats)

    return "Hello"

    

        
