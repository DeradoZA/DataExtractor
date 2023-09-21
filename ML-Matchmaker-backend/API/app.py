from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys
import numpy as np
import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), '../Services'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../Shared'))
from PlayerService import PlayerService
from DBConnectionCreator import DBConnectionCreator
from TeamService import TeamService
from PredictionService import PredictionService

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

@app.route('/api/randomMatch')
def getRandomMatch():
    modelPath = os.path.join(os.getcwd(), "..", "..", "CSGOML", "CSGOPredictor", "bestModel", "best_model.h5")
    JSONOutput = {}

    dbCreator = DBConnectionCreator('csgo', 'csgoDB', 'pwd')
    predictionService = PredictionService(modelPath)
    connection, cursor = dbCreator.dbConnection()
    playerService = PlayerService(cursor)
    teamService = TeamService()

    # Helper variables
    playerCount = 0
    playerList = []
    teamOne = []
    teamTwo = []
    teamOneELOs = []
    teamTwoELOs = []
    allPlayers = playerService.getAllPlayers()
    #-----------------------

    # Output variables
    playerTitles = ['steamID', 'avg_rws', 'avg_rating', 'avg_rating2', 
                    'avg_krRatio', 'avg_kdRatio', 'avg_kast', 'avg_adr']
    
    teamTitles = ['avg_rws', 'avg_rating', 'avg_rating2', 
                  'avg_krRatio', 'avg_kdRatio', 'avg_kast', 'avg_adr']
    #-----------------

    while playerCount < 10:
        playerID = playerService.getRandomPlayer(allPlayers)
        validPlayer = playerService.playerValidator(playerID)

        if validPlayer == True:
            playerCount += 1
            playerList.append(playerID)

    print(len(playerList))
    teamPlayerAvgValues = []

    print(playerList)

    for i in range(0, 5):
        player = playerList[i]

        playerValues = {}

        playerELO = playerService.getPlayerELO(player)
        teamOneELOs.append(playerELO)
        averagedPlayerStats = playerService.calculatePlayerStats(player)

        playerValues['avg_ELO'] = playerELO
        for i in range(len(averagedPlayerStats)):
            playerValues[playerTitles[i]] = averagedPlayerStats[i]
        
        teamPlayerAvgValues.append(playerValues)
        teamOne.append(averagedPlayerStats)

    JSONOutput['team1_player_stats'] = teamPlayerAvgValues

    teamPlayerAvgValues = []

    for i in range(5, 10):
        player = playerList[i]

        playerValues = {}

        playerELO = playerService.getPlayerELO(player)
        teamTwoELOs.append(playerELO)
        averagedPlayerStats = playerService.calculatePlayerStats(player)

        playerValues['avg_ELO'] = playerELO
        for i in range(len(averagedPlayerStats)):
            playerValues[playerTitles[i]] = averagedPlayerStats[i]

        teamPlayerAvgValues.append(playerValues)
        teamTwo.append(averagedPlayerStats)

    JSONOutput['team2_player_stats'] = teamPlayerAvgValues

    teamOneAveragedELO = teamService.calculateELOAverages(teamOneELOs)
    teamTwoAveragedELO = teamService.calculateELOAverages(teamTwoELOs)
    teamOneAveragedStats = teamService.calculateTeamAverages(teamOne)
    teamTwoAveragedStats = teamService.calculateTeamAverages(teamTwo)

    teamAvgValues = {}
    teamAvgValues['avg_ELO'] = teamOneAveragedELO
    for i in range(len(teamOneAveragedStats)):
        teamAvgValues[teamTitles[i]] = teamOneAveragedStats[i]

    JSONOutput['team1_avg_stats'] = teamAvgValues

    teamAvgValues = {}
    teamAvgValues['avg_ELO'] = teamTwoAveragedELO
    for i in range(len(teamTwoAveragedStats)):
        teamAvgValues[teamTitles[i]] = teamTwoAveragedStats[i]

    JSONOutput['team2_avg_stats'] = teamAvgValues

    fullMatchStats = teamOneAveragedELO + teamTwoAveragedStats + teamTwoAveragedELO + teamTwoAveragedStats
    fullMatchStats = np.array(fullMatchStats)
    fullMatchStats = np.reshape(fullMatchStats, (1, -1))

    print(fullMatchStats)

    matchPrediction = predictionService.PredictClassChances(fullMatchStats)

    print(f"classProbabilites --> {matchPrediction}")

    JSONOutput['match_prediction'] = float(matchPrediction[0][0])

    return jsonify(JSONOutput)

    

        
