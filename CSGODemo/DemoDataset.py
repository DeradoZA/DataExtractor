from mysql.connector import Error, connect
import os
from dotenv import load_dotenv
import csv

def MatchProcessor(match, cursor):
    team1Players = GetAllPlayersForMatch(match, 1, cursor)
    team2Players = GetAllPlayersForMatch(match, 2, cursor)

    team1Stats = GetTeamStats(team1Players, match, cursor)
    team2Stats = GetTeamStats(team2Players, match, cursor)
    matchOutcome = getMatchResult(match, cursor)

    fullMatchStats = team1Stats + team2Stats
    fullMatchStats.append(matchOutcome)

    return fullMatchStats


def getMatchResult(match, cursor):
    team1Winner = 1

    matchScoresQuery = f"""
        SELECT Team_1_Score, Team_2_Score
        FROM Matches
        WHERE MatchID = '{match}'
    """
    cursor.execute(matchScoresQuery)
    queryResult = cursor.fetchone()

    team1Score = queryResult[0]
    team2Score = queryResult[1]

    if (team1Score > team2Score):
        return team1Winner #Team 1 won the match
    elif (team1Score == team2Score):
        team1Winner = 2 #Team 1, draw or faulty statistic
        return team1Winner
    else:
        team1Winner = 0 #Team 1 lost the match
        return team1Winner


def GetTeamStats(team, match, cursor):
    teamStats = []

    for player in team:
        playerStats = []
        playerELO = getPlayerELO(player, match, cursor)

        playerAveragedQuery = f"""
            SELECT AVG(Kills), AVG(Assists), AVG(Deaths), AVG(HeadshotsPerc),
            AVG(KR_Ratio), AVG(KD_Ratio), AVG(KAST), AVG(EntryKills),
            AVG(RWS), AVG(Rating), AVG(Rating2), AVG(ATD), AVG(ADR)
            FROM PlayerStats p
            WHERE p.SteamID = '{player}' AND matchID != '{match}'
        """
        cursor.execute(playerAveragedQuery)
        queryResult = cursor.fetchone()

        for stat in queryResult:
            if stat == None:
                stat = -1
            playerStats.append(float(stat))
        
        playerStats.append(playerELO)
        teamStats += playerStats

    return teamStats


def GetAllPlayersForMatch(match,team, cursor):
    playerList = []

    getAllPlayersQuery = f"""
        SELECT steamID
        FROM playerstats
        WHERE matchID = '{match}' AND team = {team}
    """
    cursor.execute(getAllPlayersQuery)
    queryResult = cursor.fetchall()

    for result in queryResult:
        playerList.append(result[0])

    return playerList

def getPlayerELO(player, match, cursor):
    matchExactELOQuery = f"""
        SELECT ELO
        FROM playerelos
        WHERE matchID = '{match}' AND steamID = '{player}' LIMIT 1
    """
    cursor.execute(matchExactELOQuery)
    queryResult = cursor.fetchone()

    if queryResult:
        ELO = queryResult[0]
        return ELO
    else:
        matchTime = GetMatchTime(match, cursor)

        matchELOEstimateQuery = f"""
            SELECT ELO
            from playerelos p
            WHERE p.steamID = '{player}'
            order by abs(p.MatchTime - {matchTime}) LIMIT 1
        """
        cursor.execute(matchELOEstimateQuery)
        queryResult = cursor.fetchone()

        if queryResult:
            ELO = queryResult[0]
            return ELO
        else:
            return None

def GetMatchTime(match, cursor):
    matchTimeQuery = f"""
        SELECT MatchTime
        FROM matches
        WHERE matchID = '{match}'
    """
    cursor.execute(matchTimeQuery)
    queryResult = cursor.fetchone()

    matchTime = queryResult[0]

    return matchTime

def GetAllMatches(cursor):
    matchList = []
    allMatchesQuery = f"""
        SELECT matchID from matches
    """

    cursor.execute(allMatchesQuery)
    queryResult = cursor.fetchall()

    for result in queryResult:
        matchList.append(result[0])

    return matchList

def CSVCreator(line, file):
    csvPath = os.path.join("Dataset", file)

    with open(csvPath, "a", newline="") as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(line)

if __name__ == "__main__":
    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB = os.getenv("CSGO_DB")
    DB_PW = os.getenv("DB_USER_PASSWORD")
    FACEIT_API_KEY = os.getenv("FACEIT_API_KEY")

    try:
        connection = connect(
            host = "localhost",
            user = DB_USER,
            password = DB_PW,
            database = DB
        )

        cursor = connection.cursor()
    except Error as e:
        print(e)

    CLASSIFICATION_HEADER = []
    for player in range(1, 6):
        player_prefix = f"Team1_Player{player}_"
        player_columns = [
            f"{player_prefix}Kills",
            f"{player_prefix}Assists",
            f"{player_prefix}Deaths",
            f"{player_prefix}HeadshotsPerc",
            f"{player_prefix}KR_Ratio",
            f"{player_prefix}KD_Ratio",
            f"{player_prefix}KAST",
            f"{player_prefix}EntryKills",
            f"{player_prefix}RWS",
            f"{player_prefix}Rating",
            f"{player_prefix}Rating2",
            f"{player_prefix}ATD",
            f"{player_prefix}ADR",
            f"{player_prefix}ELO"
        ]
        CLASSIFICATION_HEADER.extend(player_columns)

    # Generate column names for Team 2 players (Player 1 to 5)
    for player in range(1, 6):
        player_prefix = f"Team2_Player{player}_"
        player_columns = [
            f"{player_prefix}Kills",
            f"{player_prefix}Assists",
            f"{player_prefix}Deaths",
            f"{player_prefix}HeadshotsPerc",
            f"{player_prefix}KR_Ratio",
            f"{player_prefix}KD_Ratio",
            f"{player_prefix}KAST",
            f"{player_prefix}EntryKills",
            f"{player_prefix}RWS",
            f"{player_prefix}Rating",
            f"{player_prefix}Rating2",
            f"{player_prefix}ATD",
            f"{player_prefix}ADR",
            f"{player_prefix}ELO"
        ]
        CLASSIFICATION_HEADER.extend(player_columns)
    
    CLASSIFICATION_HEADER.append("Team_1_Win?")

    CSVCreator(CLASSIFICATION_HEADER, "CSGODataset.csv")

    matchList = GetAllMatches(cursor)
    progress = 0
    for match in matchList:
        progress += 1

        print(f"UPDATING MATCH - {progress} OUT OF {len(matchList)} [{match}]")
        matchInfo = MatchProcessor(match, cursor)
        CSVCreator(matchInfo, "CSGODataset.csv")
    