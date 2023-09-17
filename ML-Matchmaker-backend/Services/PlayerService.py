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
    
    def calculatePlayerStats (self, playerID):
        playerAveragedQuery = f"""
            SELECT SteamID, AVG(RWS), AVG(Rating), AVG(Rating2), AVG(KR_Ratio),
            AVG(KD_Ratio), AVG(KAST), AVG(ADR)
            FROM (
            SELECT SteamID, RWS, Rating, Rating2, KR_Ratio, KD_Ratio, KAST, ADR
            FROM PlayerStats p
            JOIN Matches m on p.MatchID = m.MatchID
            WHERE SteamID = '{playerID}'
            ORDER BY m.MatchID DESC
            LIMIT 5
            ) as LastMatches
        """
        self.cursor.execute(playerAveragedQuery)
        averagedStats = self.cursor.fetchone()

        return averagedStats
    
    def getPlayerELO(self, playerID):
        queryPlayerELO = f"""
            SELECT p.ELO
            FROM playerelos p
            WHERE steamID = {playerID}
            ORDER BY p.MatchTime DESC
            LIMIT 1
        """

        self.cursor.execute(queryPlayerELO)
        queryResult = self.cursor.fetchone()
        playerELO = queryResult[0]

        return playerELO

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

    
