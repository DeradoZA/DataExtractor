from dotenv import load_dotenv
import os
import requests
import csv

def GameFetcher(API_KEY, match_id):
    headers = {
            'Authorization': f'Bearer {API_KEY}'
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

    formattedGame = formattedTeamOnePlayerStats + formattedTeamTwoPlayerStats
    formattedGame.append(ScoreDifference)

    return formattedGame

def TeamPlayerParser(team):
    playerStatsList = []

    for player in team:
        playerStats = player['player_stats']

        playerStatsList.append(playerStats['Kills'])
        playerStatsList.append(playerStats['Assists'])
        playerStatsList.append(playerStats['Deaths'])
        playerStatsList.append(playerStats['MVPs'])
        playerStatsList.append(playerStats['Headshots %'])
        playerStatsList.append(playerStats['Headshots'])
        playerStatsList.append(playerStats['K/R Ratio'])
        playerStatsList.append(playerStats['K/D Ratio'])
        playerStatsList.append(playerStats['Triple Kills'])
        playerStatsList.append(playerStats['Quadro Kills'])
        playerStatsList.append(playerStats['Penta Kills'])
    
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

    FACEIT_API_KEY = os.getenv('FACEIT_API_KEY')
    gameCounter = 0
    matchesFile = os.path.join(os.getcwd(), "Matches", "MatchIDList - 34285.txt")
    matchIdList = []
    CSV_HEADER = [
        "Team1_Player1_Kills", "Team1_Player1_Assists","Team1_Player1_Deaths", "Team1_Player1_MVPs","Team1_Player1_HeadshotPercentage", "Team1_Player1_Headshots","Team1_Player1_K/R-Ratio", "Team1_Player1_K/D-Ratio","Team1_Player1_TripleKills", "Team1_Player1_QuadroKills", "Team1_Player1_PentaKills",
        "Team1_Player2_Kills", "Team1_Player2_Assists","Team1_Player2_Deaths", "Team1_Player2_MVPs","Team1_Player2_HeadshotPercentage", "Team1_Player1_Headshots","Team1_Player1_K/R-Ratio", "Team1_Player1_K/D-Ratio","Team1_Player1_TripleKills", "Team1_Player1_QuadroKills", "Team1_Player1_PentaKills",
        "Team1_Player3_Kills", "Team1_Player3_Assists","Team1_Player3_Deaths", "Team1_Player3_MVPs","Team1_Player3_HeadshotPercentage", "Team1_Player1_Headshots","Team1_Player1_K/R-Ratio", "Team1_Player1_K/D-Ratio","Team1_Player1_TripleKills", "Team1_Player1_QuadroKills", "Team1_Player1_PentaKills",
        "Team1_Player4_Kills", "Team1_Player4_Assists","Team1_Player4_Deaths", "Team1_Player4_MVPs","Team1_Player4_HeadshotPercentage", "Team1_Player1_Headshots","Team1_Player1_K/R-Ratio", "Team1_Player1_K/D-Ratio","Team1_Player1_TripleKills", "Team1_Player1_QuadroKills", "Team1_Player1_PentaKills",
        "Team1_Player5_Kills", "Team1_Player5_Assists","Team1_Player5_Deaths", "Team1_Player5_MVPs","Team1_Player5_HeadshotPercentage", "Team1_Player1_Headshots","Team1_Player1_K/R-Ratio", "Team1_Player1_K/D-Ratio","Team1_Player1_TripleKills", "Team1_Player1_QuadroKills", "Team1_Player1_PentaKills",
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
        matchStats = GameFetcher(FACEIT_API_KEY, matchID)
        print(f"Amount of matches processed: {gameCounter}")

        if matchStats:
            formattedStats = JSONGameParser(matchStats)
            if formattedStats:
                WriteToCSV(formattedStats)

