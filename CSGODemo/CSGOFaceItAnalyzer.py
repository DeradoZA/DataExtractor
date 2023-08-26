import requests
from mysql.connector import connect, Error, errorcode  # Keep only the necessary module imports
from mysql.connector.errors import IntegrityError
import os
from dotenv import load_dotenv
import time


def UpdateMatches(steamIDList, cursor, API_KEY, connection):
    progress = 0

    for steamID in steamIDList:
        progress += 1

        print(f"API UPDATING PLAYER {progress} OUT OF {len(steamIDList)} [{steamID}]")
        mustUpdate = checkPlayerUpdate(steamID, cursor)

        if mustUpdate == False:
            print(f"Player - {steamID} - ALREADY HAS ELO RECORDS")
        else:
            faceitID = getFaceitID(steamID)

            time.sleep(4)

            playerMatches = GetPlayerMatches(faceitID, API_KEY)

            if playerMatches != None:
                for match in playerMatches:
                    matchTime = match.get('created_at', 0)
                    playerELO = match.get('elo', 0)
                    matchID = match.get('matchId', 0)
                    matchType = match.get('gameMode', "Default")

                    insertELOQuery = f"""
                        INSERT INTO PlayerELOs (steamID, matchID, MatchTime, MatchType, ELO)
                        VALUES
                        ('{steamID}', '{matchID}', {int(matchTime)}, '{matchType}', {int(playerELO)})
                    """
                    try:
                        cursor.execute(insertELOQuery)
                        connection.commit()
                    except Error as e:
                        if isinstance(e, IntegrityError) and e.errno == errorcode.ER_DUP_ENTRY:
                            print(f"Duplicate entry skipped: {steamID} - {matchID}")
                        else:
                            raise e  # Reraise the exception if it's not a duplicate entry error

                print(f"Player - {steamID} - ELO RECORDS INSERTED")

def getFaceitID(steamID):
    faceitIDQuery = f"""
        SELECT playerID
        FROM players p
        WHERE p.steamID = '{steamID}'
    """
    cursor.execute(faceitIDQuery)
    queryResult = cursor.fetchone()
    faceitID = queryResult[0]

    return faceitID
            
def checkPlayerUpdate(steamID, cursor):
    mustUpdate = False

    checkForMatchesQuery = f"""
        SELECT steamID
        FROM PlayerELOs pe
        WHERE pe.SteamID = '{steamID}'
    """
    cursor.execute(checkForMatchesQuery)
    queryResult = cursor.fetchall()

    if (len(queryResult) == 0):
        mustUpdate = True

    return mustUpdate


def GetSteamIDs(cursor):
    playerIDsQuery = """
        SELECT SteamID
        FROM Players p
    """
    cursor.execute(playerIDsQuery)

    queryResult = cursor.fetchall()

    steamIDList = []

    for result in queryResult:
        steamIDList.append(result[0])

    return steamIDList

def GetPlayerMatches(playerID, API_KEY):
    URL = f"https://faceitanalyser.com/api/matches/{playerID}?key={API_KEY}&page_size=1000"
    
    try:
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            return data['segments']
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB = os.getenv("CSGO_DB")
    DB_PW = os.getenv("DB_USER_PASSWORD")
    FACEIT_ANALYZER_KEY = os.getenv("FACEIT_ANALYZER_API_KEY")

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

    steamIDList = GetSteamIDs(cursor)

    UpdateMatches(steamIDList, cursor, FACEIT_ANALYZER_KEY, connection)

