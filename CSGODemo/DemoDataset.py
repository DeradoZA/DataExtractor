from mysql.connector import Error, connect
import os
from dotenv import load_dotenv
import csv
import matplotlib.pyplot as plt

def analyzeValues(stat, match, cursor):
    query = f"""
        SELECT SUM({stat}), Team
        FROM playerstats ps
        where ps.MatchID = '{match}'
        GROUP BY ps.team
    """
    cursor.execute(query)

    queryResult = cursor.fetchall()

    team1Kills = queryResult[0][0]
    team2Kills = queryResult[1][0]

    return team1Kills, team2Kills


def calculate_team_averages(match_info, match, cursor):
    team1_stats = match_info[:70]  # Assuming the first 70 elements are for Team 1 stats
    team2_stats = match_info[70:140]  # Assuming elements 71 to 140 are for Team 2 stats

    # Calculate averages for Team 1 stats
    team1_averages = [sum([x for x in team1_stats[i::14] if x is not None]) / len([x for x in team1_stats[i::14] if x is not None]) for i in range(14)]

    # Calculate averages for Team 2 stats
    team2_averages = [sum([x for x in team2_stats[i::14] if x is not None]) / len([x for x in team2_stats[i::14] if x is not None]) for i in range(14)]

    matchOutcome, scoreDifference, closeMatch = getMatchResult(match, cursor)

    fullStats = team1_averages + team2_averages
    fullStats.append(matchOutcome)
    fullStats.append(scoreDifference)
    fullStats.append(closeMatch)
    return fullStats

def MatchProcessor(match, cursor):
    team1Players = GetAllPlayersForMatch(match, 1, cursor)
    team2Players = GetAllPlayersForMatch(match, 2, cursor)

    team1Stats = GetTeamStats(team1Players, match, cursor)
    team2Stats = GetTeamStats(team2Players, match, cursor)
    matchOutcome, scoreDifference, closeMatch = getMatchResult(match, cursor)

    fullMatchStats = team1Stats + team2Stats
    fullMatchStats.append(matchOutcome)
    fullMatchStats.append(scoreDifference)
    fullMatchStats.append(closeMatch)

    return fullMatchStats


def getMatchResult(match, cursor):
    team1Winner = 1
    scoreDifference = 0
    closeMatch = 0

    matchScoresQuery = f"""
        SELECT Team_1_Score, Team_2_Score
        FROM Matches
        WHERE MatchID = '{match}'
    """
    cursor.execute(matchScoresQuery)
    queryResult = cursor.fetchone()

    team1Score = queryResult[0]
    team2Score = queryResult[1]
    scoreDifference = abs(team1Score - team2Score)

    if scoreDifference <= 3:
        closeMatch = 1

    if (team1Score > team2Score):
        return team1Winner, scoreDifference, closeMatch #Team 1 won the match
    elif (team1Score == team2Score):
        team1Winner = 2 #Team 1, draw or faulty statistic
        return team1Winner, scoreDifference, closeMatch
    else:
        team1Winner = 0 #Team 1 lost the match
        return team1Winner, scoreDifference, closeMatch


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
    CLASSIFICATION_HEADER.append("ScoreDifference")
    CLASSIFICATION_HEADER.append("closeMatch?")

    CSVCreator(CLASSIFICATION_HEADER, "CSGODataset.csv")

    AVERAGE_CLASSIFICATION_HEADER = []

    # Generate column names for Team 1 average stats
    for stat in CLASSIFICATION_HEADER[:14]:  # Assuming the first 14 columns are for Team 1 players
        team1_stat = f"Team1_Avg_{stat.split('_')[2]}"  # Extracting the stat name after the second underscore
        AVERAGE_CLASSIFICATION_HEADER.append(team1_stat)

    # Generate column names for Team 2 average stats
    for stat in CLASSIFICATION_HEADER[14:28]:  # Assuming columns 15 to 28 are for Team 2 players
        team2_stat = f"Team2_Avg_{stat.split('_')[2]}"  # Extracting the stat name after the second underscore
        AVERAGE_CLASSIFICATION_HEADER.append(team2_stat)

    # Add the target columns
    AVERAGE_CLASSIFICATION_HEADER.extend(["Team_1_Win?", "ScoreDifference", "closeMatch?"])

    CSVCreator(AVERAGE_CLASSIFICATION_HEADER, 'AveragedDataset.csv')
    choice = input("Create(c)/Analyze(a)")
    matchList = GetAllMatches(cursor)

    if(choice == 'c'):
        progress = 0
        for match in matchList:
            progress += 1

            print(f"UPDATING MATCH - {progress} OUT OF {len(matchList)} [{match}]")
            matchInfo = MatchProcessor(match, cursor)
            teamAverages = calculate_team_averages(matchInfo, match, cursor)
            print(teamAverages)
            CSVCreator(matchInfo, "CSGODataset.csv")
            CSVCreator(teamAverages, 'AveragedDataset.csv')

    statDiffs = []
    scoreDiffs = []
    stat = 'RWS'

    for match in matchList:
        team1Kills, team2Kills = analyzeValues(stat, match, cursor)

        statDiff = abs(team2Kills - team1Kills)

        team1Winner, scoreDifference, closeMatch = getMatchResult(match, cursor)

        statDiffs.append(float(statDiff))
        scoreDiffs.append(scoreDifference)

    plt.figure(figsize=(10, 6))
    plt.scatter(statDiffs, scoreDiffs, color='blue aa', alpha=0.7)
    plt.title('statDiffs vs scoreDiffs')
    plt.xlabel('Score Differences')
    plt.ylabel(f'{stat} Differences')
    plt.grid(True)
    plt.show()
    