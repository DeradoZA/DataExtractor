from dotenv import load_dotenv
from mysql.connector import connect, Error
import os
import requests
import csv

def GameFetcher(match_id, API_KEY):
    load_dotenv()

    headers = {
            'Authorization': f'Bearer {API_KEY}'
    }

    URL = f'https://open.faceit.com/data/v4/matches/{match_id}/stats'
    try:
        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with response code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occured: {e}")
        return None

def JSONGameParser(match, matchTime, cursor, connection):
    
    validationResult, validationResultInfo = GameValidator(match)
    finalResult = True

    if (validationResult == False):
        finalResult = False
        return finalResult, validationResultInfo
    
    matchID = match['rounds'][0]['match_id']
    map = match['rounds'][0]['round_stats']['Map']
    teamOnePlayers = match['rounds'][0]['teams'][0]['players']
    teamTwoPlayers = match['rounds'][0]['teams'][1]['players']
    TeamOneScore = int(match['rounds'][0]['teams'][0]['team_stats']['Final Score'])
    TeamTwoScore = int(match['rounds'][0]['teams'][1]['team_stats']['Final Score'])


    #Match Queries
    matchesQuery = f"SELECT * FROM Matches WHERE MatchID = '{matchID}'"

    cursor.execute(matchesQuery)

    matchesResult = cursor.fetchall()

    if (len(matchesResult) == 0):
        insertMatchQuery = f"""INSERT INTO Matches(MatchID, Team_1_Score, Team_2_Score, Map, MatchTime)
          VALUES
            ('{matchID}', {TeamOneScore}, {TeamTwoScore}, '{map}', {matchTime})
        """
        cursor.execute(insertMatchQuery)
        connection.commit()
    else:
        finalResult = False
        return finalResult, f"Match ('{matchID}') already inserted."
    
    #--------

    #Player Queries
    
    for player in teamOnePlayers:
        playerID = player['player_id']

        playerSearchQuery = f"SELECT PlayerID FROM Players WHERE PlayerID = '{playerID}'"

        cursor.execute(playerSearchQuery)
        result = cursor.fetchall()

        if (len(result) == 0 ):
            playerInsertQuery = f"""INSERT INTO Players(PlayerID)
            VALUES
                ('{playerID}')
            """
            cursor.execute(playerInsertQuery)
            connection.commit()

    for player in teamTwoPlayers:
        playerID = player['player_id']

        playerSearchQuery = f"SELECT PlayerID FROM Players WHERE PlayerID = '{playerID}'"

        cursor.execute(playerSearchQuery)
        result = cursor.fetchall()

        if (len(result) == 0 ):
            playerInsertQuery = f"""INSERT INTO Players(PlayerID)
            VALUES
                ('{playerID}')
            """
            cursor.execute(playerInsertQuery)
            connection.commit()

    #----

    #PlayerStats Queries

    for player in teamOnePlayers:
        teamValue = 1
        playerID = player['player_id']
        playerStats = PlayerStatsCollector(player)

        playerStatsInsertQuery = f"""INSERT INTO
          PlayerStats(PlayerID, MatchID, Team, Kills, Assists, Deaths, Headshots, HeadshotsPerc, KR_Ratio, KD_Ratio, TripleKills, QuadroKills, PentaKills, MVPs)
          VALUES
            ('{playerID}', '{matchID}', {teamValue}, {playerStats[0]}, {playerStats[1]}, {playerStats[2]}, {playerStats[3]}, {playerStats[4]}, {playerStats[5]},
              {playerStats[6]}, {playerStats[7]}, {playerStats[8]}, {playerStats[9]}, {playerStats[10]})"""
        
        cursor.execute(playerStatsInsertQuery)
        connection.commit()

    for player in teamTwoPlayers:
        teamValue = 2
        playerID = player['player_id']
        playerStats = PlayerStatsCollector(player)

        playerStatsInsertQuery = f"""INSERT INTO
          PlayerStats(PlayerID, MatchID, Team, Kills, Assists, Deaths, Headshots, HeadshotsPerc, KR_Ratio, KD_Ratio, TripleKills, QuadroKills, PentaKills, MVPs)
          VALUES
            ('{playerID}', '{matchID}', {teamValue}, {playerStats[0]}, {playerStats[1]}, {playerStats[2]}, {playerStats[3]}, {playerStats[4]}, {playerStats[5]},
              {playerStats[6]}, {playerStats[7]}, {playerStats[8]}, {playerStats[9]}, {playerStats[10]})"""
        
        cursor.execute(playerStatsInsertQuery)
        connection.commit()
    
    #----

    return finalResult, f"Match inserted successfully for matchID - {matchID}"

def PlayerStatsCollector(player):
    playerStatsList = []

    playerStats = player['player_stats']

    playerStatsList.append(int(playerStats['Kills']))
    playerStatsList.append(int(playerStats['Assists']))
    playerStatsList.append(int(playerStats['Deaths']))
    playerStatsList.append(int(playerStats['Headshots']))
    playerStatsList.append(float(playerStats['Headshots %']))
    playerStatsList.append(float(playerStats['K/R Ratio']))
    playerStatsList.append(float(playerStats['K/D Ratio']))
    playerStatsList.append(int(playerStats['Triple Kills']))
    playerStatsList.append(int(playerStats['Quadro Kills']))
    playerStatsList.append(int(playerStats['Penta Kills']))
    playerStatsList.append(int(playerStats['MVPs']))

    return playerStatsList


def GameValidator(match):
    validationResult = None
    validationResultInfo = ''

    if (len(match['rounds'][0]['teams']) != 2):
        validationResultInfo = "Insufficient amount of teams"
        validationResult = False
        return validationResult, validationResultInfo
    else:
        validationResult = True

    teamOne = match['rounds'][0]['teams'][0]['players']
    teamTwo = match['rounds'][0]['teams'][1]['players']
    
    if (len(teamOne) != 5 or len(teamTwo) != 5):
        validationResultInfo =  "Insufficient amount of players."
        validationResult = False
    else:
        validationResult = True

    return validationResult, validationResultInfo

def WriteToCSV(formattedStats):
    formattedStatsFile = os.path.join(os.getcwd(), "FormattedStats", "FormattedCSGOStats.csv")

    with open(formattedStatsFile, mode='a', newline='')  as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(formattedStats)

if __name__ == "__main__":
    load_dotenv()
    gameCounter = 0
    matchesFile = os.path.join(os.getcwd(), "Matches", "MatchIDList.txt")
    matchInfoList = []
    FACEIT_API_KEY =  os.getenv('FACEIT_API_KEY')

    with open(matchesFile, 'r') as file:
        matchInfoList = file.readlines()

    try:
        connection = connect(
            host = "localhost",
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_USER_PASSWORD"),
            database = os.getenv("CSGO_DB")
        )
        cursor = connection.cursor()

        for matchInfo in matchInfoList:
            gameCounter += 1
            matchDetails = matchInfo.split(',')
            matchID = matchDetails[0]
            matchTime = int(matchDetails[1])
            matchStats = GameFetcher(matchID, FACEIT_API_KEY)
            print(f"PROCESSING MATCH - {gameCounter} out of {len(matchInfoList)}")

            if matchStats:
                parseResult, parseMessage = JSONGameParser(matchStats, matchTime, cursor, connection)
                if parseResult:
                    print(f"{matchID}")
                else:
                    print(f"PROCESSING ERROR --> {parseMessage}")

        print("FINISHED")
        cursor.close()
        connection.close()

    except Error as e:
        print(e)


