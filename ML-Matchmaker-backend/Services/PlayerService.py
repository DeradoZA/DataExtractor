import random

class PlayerService:
    def __init__(self, cursor) -> None:
        self.cursor = cursor

    def getAllPlayers (self):
        queryAllPlayers = f"""
            SELECT SteamID
            FROM players
        """
        self.cursor.execute(queryAllPlayers)
        playerList = self.cursor.fetchall()

        return playerList

    def getRandomPlayer (self):
        playerList = self.getAllPlayers()

        queryAllPlayers = f"""
            SELECT COUNT(*)
            FROM players
        """
        self.cursor.execute(queryAllPlayers)
        queryResult = self.cursor.fetchone()
        numPlayers = queryResult[0]

        randomPlayerValue = random.randint(0, len(playerList))

        return playerList[randomPlayerValue][0]
    
    def calculatePlayerStats (self):
        pass

    def searchForPlayerInList (self, playerListIDs, playerID):
        isPlayerInList = False

        for playerListID in playerListIDs:
            if playerListID == playerID:
                isPlayerInList = True
                break

        return isPlayerInList

    def playerValidator (self, playerID):
        playerHasEnoughGames = True

        gameAmountQuery = f"""
            SELECT COUNT(*)
            FROM PlayerStats
            WHERE SteamID = '{playerID}'
        """

        self.cursor.execute(gameAmountQuery)

        queryResult = self.cursor.fetchone()

        numberOfGamesPlayed = queryResult[0]

        if numberOfGamesPlayed < 5:
            playerHasEnoughGames = False

        return playerHasEnoughGames

    
