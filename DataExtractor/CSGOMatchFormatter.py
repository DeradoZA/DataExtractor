from dotenv import load_dotenv
import os
import requests
import csv

def GameFetcher(match_id):
    load_dotenv()

    FACEIT_API_KEY = os.getenv('FACEIT_API_KEY')

    headers = {
            'Authorization': f'Bearer {FACEIT_API_KEY}'
    }

    URL = f'https://open.faceit.com/data/v4/matches/{match_id}/stats'
    try:
        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            print("Game Fetch Successful")
            data = response.json()
            return data
        else:
            print(f"Request failed with response code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occured: {e}")
        return None
    
def PlayerHistoryFetcher(player_id):
    FACEIT_API_KEY = os.getenv('FACEIT_API_KEY')
    print(FACEIT_API_KEY)
    
    headers = {
            'Authorization': f'Bearer {FACEIT_API_KEY}'
    }

    URL = f"https://open.faceit.com/data/v4/players/{player_id}/history?game=csgo&offset=0&limit=20"

    try:
        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            print("Game Fetch Successful")
            data = response.json()
            return data
        else:
            print(f"Request failed with response code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occured: {e}")
        return None


def JSONGameParser(match):
    
    validationResult, validationResultInfo = GameValidator(match)

    if (validationResult == False):
        print(f"Invalid match - {validationResultInfo}")
        return None
    
    formattedGame = []
    TeamOneScore = int(match['rounds'][0]['teams'][0]['team_stats']['Final Score'])
    TeamTwoScore = int(match['rounds'][0]['teams'][1]['team_stats']['Final Score'])

    teamOnePlayers = match['rounds'][0]['teams'][0]['players']
    teamTwoPlayers = match['rounds'][0]['teams'][1]['players']
    ScoreDifference = abs(TeamOneScore - TeamTwoScore)

    formattedTeamOnePlayerStats = TeamPlayerParser(teamOnePlayers)
    formattedTeamTwoPlayerStats = TeamPlayerParser(teamTwoPlayers)

    if (formattedTeamOnePlayerStats == None or formattedTeamTwoPlayerStats == None):
        print(f"Invalid match - history game not valid or too few games.")
        return None

    formattedGame = formattedTeamOnePlayerStats + formattedTeamTwoPlayerStats
    formattedGame.append(ScoreDifference)

    return formattedGame

def TeamPlayerParser(team):
    playerIDList = []
    teamStats = []

    for player in team:
        playerID = player['player_id']
        print(playerID)
        playerStats = PlayerStatsCalculator(playerID)

        teamStats += playerStats
    
    return teamStats

def PlayerStatsCalculator(playerID):
    playerHistory = PlayerHistoryFetcher(playerID)
    playerMatchHistoryList = []

    if len(playerHistory) < 5:
        return None
    
    Kills = 0
    Assists = 0
    Deaths = 0
    MVPs = 0
    HeadshotsPerc = 0
    Headshots = 0
    KR_Ratio = 0
    KD_Ratio = 0
    Triple_Kills = 0
    Quadro_Kills = 0
    Penta_Kills = 0
    numMatches = 0

    for match in playerHistory['items']:
        playerMatch = match['match_id']

        matchStats = GameFetcher(playerMatch)

        validationResult, validationResultInfo = GameValidator(matchStats)

        if (validationResult == False):
            return None
        else:
            numGames += 1
        
        team1Players = []
        team2Players = []

        team1 = matchStats['rounds'][0]['teams'][0]['players']
        team2 = matchStats['rounds'][0]['teams'][1]['players']

        for player in team1:
            team1Players.append(player['player_id'])
        
        for player in team2:
            team2Players.append(player['player_id'])
        
        if (playerID in team1):
            playerStats = matchStats['rounds'][0]['teams'][0]['players'][team1.index(playerID)]['player_stats']
        else:
            playerStats = matchStats['rounds'][0]['teams'][0]['players'][team2.index(playerID)]['player_stats']

        Kills += int(playerStats['Kills'])
        Assists += int(playerStats['Assists'])
        Deaths += int(playerStats['Deaths'])
        MVPs += int(playerStats['MVPs'])
        HeadshotsPerc += float(playerStats['Headshots %'])
        Headshots += playerStats['Headshots']
        KR_Ratio += float(playerStats['K/R Ratio'])
        KD_Ratio += float(playerStats['K/D Ratio'])
        Triple_Kills += int(playerStats['Triple Kills'])
        Quadro_Kills += int(playerStats['Quadro Kills'])
        Penta_Kills += int(playerStats['Penta Kills'])


    averagedKills = Kills/numMatches
    averagedAssists = Assists/numMatches
    averagedDeaths = Deaths/numMatches
    averagedMVPs = MVPs/numMatches
    averagedHeadshotsPerc = HeadshotsPerc/numMatches
    averagedHeadshots = Headshots/numMatches
    averagedKR_Ratio = KR_Ratio/numMatches
    averagedKD_Ratio = KD_Ratio/numMatches
    averagedTKills = Triple_Kills/numMatches
    averagedQKills = Quadro_Kills/numMatches
    averagedPKills = Penta_Kills/numMatches

    playerAveragedStats = []
    playerAveragedStats.append(averagedKills)
    playerAveragedStats.append(averagedAssists)
    playerAveragedStats.append(averagedDeaths)
    playerAveragedStats.append(averagedMVPs)
    playerAveragedStats.append(averagedHeadshotsPerc)
    playerAveragedStats.append(averagedHeadshots)
    playerAveragedStats.append(averagedKR_Ratio)
    playerAveragedStats.append(averagedKD_Ratio)
    playerAveragedStats.append(averagedTKills)
    playerAveragedStats.append(averagedQKills)
    playerAveragedStats.append(averagedPKills)

    return playerAveragedStats


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
    gameCounter = 0
    matchesFile = os.path.join(os.getcwd(), "Matches", "MatchIDList.txt")
    matchIdList = []
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

    WriteToCSV(CSV_HEADER)

    with open(matchesFile, 'r') as file:
        matchIdList = file.readlines()

    for matchID in matchIdList:
        gameCounter += 1
        matchStats = GameFetcher(matchID)
        print(f"Amount of matches processed: {gameCounter}")

        if matchStats:
            formattedStats = JSONGameParser(matchStats)
            if formattedStats:
                WriteToCSV(formattedStats)

