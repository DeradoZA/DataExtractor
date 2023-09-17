from flask import Flask
from Services.PlayerService import PlayerService
from Shared.DBConnectionCreator import DBConnectionCreator

app = Flask(__name__)

@app.route('/randomMatch')
def getRandomMatch():

    dbCreator = DBConnectionCreator('csgo', 'MLCSGO_DB', 'pwd')
    connection, cursor = dbCreator.dbConnection()
    playerService = PlayerService()

    playerCount = 0
    playerList = []

    while playerCount < 10:
        playerID = playerService.getRandomPlayer()
        validPlayer = playerService.playerValidator(playerID)

        if validPlayer == True:
            playerCount += 1
            playerList.append(playerID)

        
