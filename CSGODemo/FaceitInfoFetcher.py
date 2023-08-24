import requests
from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

def UpdateIDs(steamIDList, API_KEY, cursor, connection):
    progress = 0

    for steamID in steamIDList:
        progress += 1
        print(f"UPDATING PLAYER {progress} OUT OF {len(steamIDList)}")
        checkAlreadyInsertedQuery = f"""
            SELECT playerID
            FROM Players p
            WHERE SteamID = '{steamID}'
        """

        cursor.execute(checkAlreadyInsertedQuery)
        queryResult = cursor.fetchone()
        faceitID = queryResult[0]

        if faceitID != "0":
            print(f"Player - {steamID} - ALREADY UPDATED")
        else:
            faceitID = FaceitIDFetcher(API_KEY, steamID)

            if (faceitID == None):
                print(f"Player - {steamID} - FACEIT ID NOT FOUND")
            else:
                updateQuery = f"""
                    UPDATE Players p
                    SET p.playerID = '{faceitID}'
                    WHERE p.steamID = '{steamID}'
                """
                cursor.execute(updateQuery)
                connection.commit()
                print(f"Player - {steamID} - UPDATED")

def UpdateMatchTimes(matchList, API_KEY, cursor, connection):
    progress = 0

    for match in matchList:
        progress += 1
        print(f"UPDATING MATCH - {progress} OUT OF {len(matchList)} [{match}]")

        matchTime = matchTimeFetcher(API_KEY, match)

        updateQuery = f"""
            UPDATE matches m
            SET m.MatchTIme = {matchTime}
            WHERE m.matchID = '{match}'
        """
        cursor.execute(updateQuery)
        connection.commit()

        print(f"UPDATED MATCH --> {match}")


def matchTimeFetcher(API_KEY, matchID):
    URL=f"https://open.faceit.com/data/v4/matches/{matchID}"

    headers = {
            'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            data = response.json()
            matchTime = data.get('configured_at', 0)
            return matchTime
    except Error as e:
        print(e)
        return None

def GetAllMatches(cursor):
    matchList = []

    matchesQuery = f"""
        SELECT MatchID
        from matches
        WHERE MatchTime = {0}
    """
    cursor.execute(matchesQuery)
    queryResult = cursor.fetchall()

    for result in queryResult:
        matchList.append(result[0])

    return matchList

def FaceitIDFetcher(API_KEY, steamID):
    URL = f"https://open.faceit.com/data/v4/players?game=csgo&game_player_id={steamID}"

    headers = {
            'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            data = response.json()
            faceitID = data['player_id']
            return faceitID
        else:
            return None
    except Error as e:
        print(e)
        return None

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

    steamIDList = GetSteamIDs(cursor)

    UpdateIDs(steamIDList, FACEIT_API_KEY, cursor, connection)

    matchList = GetAllMatches(cursor)

    UpdateMatchTimes(matchList, FACEIT_API_KEY, cursor, connection)