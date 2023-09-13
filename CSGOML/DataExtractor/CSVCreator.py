import os
import csv
from dotenv import load_dotenv
from mysql.connector import connect, Error

def gameParser(cursor, matchID, playerList):
    formattedMatch = []

    team1, team2 = playerSplitter(matchID, cursor)

    validationResult, validationInfo = matchValidator(cursor, matchID, playerList)

    if (validationResult == False):
        return None, validationInfo

    for player in team1:
        queryStats = f"""
            SELECT AVG(Kills), AVG(Assists), AVG(Deaths), AVG(Headshots), AVG(HeadshotsPerc), AVG(KR_Ratio), AVG(KD_Ratio),
            AVG(TripleKills), AVG(QuadroKills), AVG(PentaKills), AVG(MVPs)
            FROM PlayerStats ps
            JOIN Matches m ON ps.MatchID = m.MatchID 
            WHERE m.MatchTime > (SELECT MatchTime FROM Matches WHERE MatchID = '{matchID}') - (60 * 60 * 24 * 60)
            AND m.MatchTime < (SELECT MatchTime FROM Matches WHERE MatchID = '{matchID}')
            AND ps.PlayerID = '{player}'
            AND ps.MatchID != '{matchID}'
            ORDER BY m.MatchTime DESC
            LIMIT 5
            """
        cursor.execute(queryStats)

        queryResult = cursor.fetchone()

        formattedMatch.append(float(queryResult[0]))
        formattedMatch.append(float(queryResult[1]))
        formattedMatch.append(float(queryResult[2]))
        formattedMatch.append(float(queryResult[3]))
        formattedMatch.append(float(queryResult[4]))
        formattedMatch.append(float(queryResult[5]))
        formattedMatch.append(float(queryResult[6]))
        formattedMatch.append(float(queryResult[7]))
        formattedMatch.append(float(queryResult[8]))
        formattedMatch.append(float(queryResult[9]))
        formattedMatch.append(float(queryResult[10]))

    for player in team2:
        queryStats = f"""
            SELECT AVG(Kills), AVG(Assists), AVG(Deaths), AVG(Headshots), AVG(HeadshotsPerc), AVG(KR_Ratio), AVG(KD_Ratio),
            AVG(TripleKills), AVG(QuadroKills), AVG(PentaKills), AVG(MVPs)
            FROM PlayerStats ps
            JOIN Matches m ON ps.MatchID = m.MatchID 
            WHERE m.MatchTime > (SELECT MatchTime FROM Matches WHERE MatchID = '{matchID}') - (60 * 60 * 24 * 60)
            AND m.MatchTime < (SELECT MatchTime FROM Matches WHERE MatchID = '{matchID}')
            AND ps.PlayerID = '{player}'
            AND ps.MatchID != '{matchID}'
            ORDER BY m.MatchTime DESC
            LIMIT 5
            """
        cursor.execute(queryStats)

        queryResult = cursor.fetchone()

        formattedMatch.append(float(queryResult[0]))
        formattedMatch.append(float(queryResult[1]))
        formattedMatch.append(float(queryResult[2]))
        formattedMatch.append(float(queryResult[3]))
        formattedMatch.append(float(queryResult[4]))
        formattedMatch.append(float(queryResult[5]))
        formattedMatch.append(float(queryResult[6]))
        formattedMatch.append(float(queryResult[7]))
        formattedMatch.append(float(queryResult[8]))
        formattedMatch.append(float(queryResult[9]))
        formattedMatch.append(float(queryResult[10]))

    queryScoreDiff = f"""
    SELECT Team_1_Score, Team_2_Score FROM Matches m
    WHERE m.MatchID = '{matchID}'
    """

    cursor.execute(queryScoreDiff)
    queryResult = cursor.fetchone()

    scoreDiff = abs(queryResult[0] - queryResult[1])
    formattedMatch.append(scoreDiff)

    return formattedMatch, "Parsing successful"

        
        
def playerSplitter(matchID, cursor):
    teamOnePlayers = []
    teamTwoPlayers = []

    queryTeamOne = f"""
    SELECT ps.PlayerID FROM PlayerStats ps
    WHERE ps.MatchID = '{matchID}' AND ps.Team = 1
    """
    cursor.execute(queryTeamOne)
    queryResult = cursor.fetchall()

    for result in queryResult:
        teamOnePlayers.append(result[0])
    
    queryTeamTwo = f"""
    SELECT ps.PlayerID FROM PlayerStats ps
    WHERE ps.MatchID = '{matchID}' AND ps.Team = 2
    """
    cursor.execute(queryTeamTwo)
    queryResult = cursor.fetchall()

    for result in queryResult:
        teamTwoPlayers.append(result[0])

    return teamOnePlayers, teamTwoPlayers


def getAllMatches(cursor):
    matchesList = []
    gamesQuery = "SELECT MatchID FROM Matches"

    cursor.execute(gamesQuery)

    queryResult = cursor.fetchall()

    for result in queryResult:
        matchesList.append(result[0])

    return matchesList

def matchValidator(cursor, matchID, playerList):
    validationResultInfo = ""
    validationResult = True

    if (len(playerList) != 10):
        validationResultInfo = "Insufficient amount of players for match."
        validationResult = False
        return validationResult, validationResultInfo
    
    for player in playerList:
        query = f"""SELECT COUNT(ps.MatchID)
        FROM PlayerStats ps
        JOIN Matches m ON ps.MatchID = m.MatchID 
        WHERE m.MatchTime > (SELECT MatchTime FROM Matches WHERE MatchID = '{matchID}') - (60 * 60 * 24 * 60)
        AND m.MatchTime < (SELECT MatchTime FROM Matches WHERE MatchID = '{matchID}')
        AND ps.PlayerID = '{player}'
        AND ps.MatchID != '{matchID}'
        """

        cursor.execute(query)
        queryResult = cursor.fetchone()

        matchesPlayed = queryResult[0] if queryResult is not None else 0
        if (matchesPlayed < 5):
            validationResult = False
            validationResultInfo = "Player with too few games."
            return validationResult, validationResultInfo
    
    validationResultInfo = "Valid Game"
    return validationResult, validationResultInfo

def getAllPlayersForMatch(cursor, matchID):
    playerList = []
    playerQuery = f"SELECT PlayerID from playerstats where MatchID = '{matchID}'"

    cursor.execute(playerQuery)

    queryResult = cursor.fetchall()

    for result in queryResult:
        playerList.append(result[0])
    
    return playerList


def WriteToCSV(data, fileName):
    with open(fileName, mode = 'a', newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=',')
        csvWriter.writerow(data)

if __name__ == "__main__":
    load_dotenv()

    HOST = "localhost"
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_USER_PASSWORD")
    DB = os.getenv("CSGO_DB")

    try:
        connection = connect(
            host = HOST,
            user = DB_USER,
            password = DB_PASSWORD,
            database = DB
        )
        cursor = connection.cursor()
    except Error as e:
        print(e)
        
    CSV_HEADER = [
        "Team1_Player1_Kills", "Team1_Player1_Assists","Team1_Player1_Deaths", "Team1_Player1_MVPs","Team1_Player1_HeadshotPercentage", "Team1_Player1_Headshots","Team1_Player1_K/R-Ratio", "Team1_Player1_K/D-Ratio","Team1_Player1_TripleKills", "Team1_Player1_QuadroKills", "Team1_Player1_PentaKills",
        "Team1_Player2_Kills", "Team1_Player2_Assists","Team1_Player2_Deaths", "Team1_Player2_MVPs","Team1_Player2_HeadshotPercentage", "Team1_Player2_Headshots","Team1_Player2_K/R-Ratio", "Team1_Player2_K/D-Ratio","Team1_Player2_TripleKills", "Team1_Player2_QuadroKills", "Team1_Player2_PentaKills",
        "Team1_Player3_Kills", "Team1_Player3_Assists","Team1_Player3_Deaths", "Team1_Player3_MVPs","Team1_Player3_HeadshotPercentage", "Team1_Player3_Headshots","Team1_Player3_K/R-Ratio", "Team1_Player3_K/D-Ratio","Team1_Player3_TripleKills", "Team1_Player3_QuadroKills", "Team1_Player3_PentaKills",
        "Team1_Player4_Kills", "Team1_Player4_Assists","Team1_Player4_Deaths", "Team1_Player4_MVPs","Team1_Player4_HeadshotPercentage", "Team1_Player4_Headshots","Team1_Player4_K/R-Ratio", "Team1_Player4_K/D-Ratio","Team1_Player4_TripleKills", "Team1_Player4_QuadroKills", "Team1_Player4_PentaKills",
        "Team1_Player5_Kills", "Team1_Player5_Assists","Team1_Player5_Deaths", "Team1_Player5_MVPs","Team1_Player5_HeadshotPercentage", "Team1_Player5_Headshots","Team1_Player5_K/R-Ratio", "Team1_Player5_K/D-Ratio","Team1_Player5_TripleKills", "Team1_Player5_QuadroKills", "Team1_Player5_PentaKills",
        "Team2_Player1_Kills", "Team2_Player1_Assists","Team2_Player1_Deaths", "Team2_Player1_MVPs","Team2_Player1_HeadshotPercentage", "Team2_Player1_Headshots","Team2_Player1_K/R-Ratio", "Team2_Player1_K/D-Ratio","Team2_Player1_TripleKills", "Team2_Player1_QuadroKills", "Team2_Player1_PentaKills",
        "Team2_Player2_Kills", "Team2_Player2_Assists","Team2_Player2_Deaths", "Team2_Player2_MVPs","Team2_Player2_HeadshotPercentage", "Team2_Player2_Headshots","Team2_Player2_K/R-Ratio", "Team2_Player2_K/D-Ratio","Team2_Player2_TripleKills", "Team2_Player2_QuadroKills", "Team2_Player2_PentaKills",
        "Team2_Player3_Kills", "Team2_Player3_Assists","Team2_Player3_Deaths", "Team2_Player3_MVPs","Team2_Player3_HeadshotPercentage", "Team2_Player3_Headshots","Team2_Player3_K/R-Ratio", "Team2_Player3_K/D-Ratio","Team2_Player3_TripleKills", "Team2_Player3_QuadroKills", "Team2_Player3_PentaKills",
        "Team2_Player4_Kills", "Team2_Player4_Assists","Team2_Player4_Deaths", "Team2_Player4_MVPs","Team2_Player4_HeadshotPercentage", "Team2_Player4_Headshots","Team2_Player4_K/R-Ratio", "Team2_Player4_K/D-Ratio","Team2_Player4_TripleKills", "Team2_Player4_QuadroKills", "Team2_Player4_PentaKills",
        "Team2_Player5_Kills", "Team2_Player5_Assists","Team2_Player5_Deaths", "Team2_Player5_MVPs","Team2_Player5_HeadshotPercentage", "Team2_Player5_Headshots","Team2_Player5_K/R-Ratio", "Team2_Player5_K/D-Ratio","Team2_Player5_TripleKills", "Team2_Player5_QuadroKills", "Team2_Player5_PentaKills",
        "ScoreDifference"
    ]

    DatasetFile = os.path.join(os.getcwd(), "FormattedStats", "CSGODataset.csv")
    WriteToCSV(CSV_HEADER, DatasetFile)

    MatchIDs = getAllMatches(cursor)
    matchCounter = 0

    for matchID in MatchIDs:
        playerList = getAllPlayersForMatch(cursor, matchID)
        formattedMatch, resultInfo = gameParser(cursor, matchID, playerList)
        matchCounter += 1

        print(f"PROCESSING MATCH {matchCounter} OUT OF {len(MatchIDs)}")

        if(formattedMatch == None):
            print(f"Match processing for {matchID} failed --> {resultInfo}")
        else:
            WriteToCSV(formattedMatch, DatasetFile)
            print(f"{resultInfo} --> writing to CSV.")
        
        print("----------------------------------------------------------------------------")