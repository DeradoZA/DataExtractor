import requests
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
from mysql.connector import Error, connect

def FetchMatchList(API_KEY, HubIDList, MatchLimit, cursor):
    matchIDList = []
    matchTimeList = []
    offset = 0
    LIMIT = 100
    iterationAmount = 0
    file = open("MatchIDList.txt", 'w')
    gamesProcessedCounter = 0

    headers = {
            'Authorization': f'Bearer {FACEIT_API_KEY}'
    }

    for hub in HubIDList:
        offset = 0
        print(f"Fetching match IDs: {hub}")

        while (offset < MatchLimit):
            requestSuccess = False
            URL = f"https://open.faceit.com/data/v4/hubs/{hub}/matches?offset={offset}&limit={LIMIT}"
            iterationAmount += 1
            print(f"Iteration number {iterationAmount}, matches processed {gamesProcessedCounter}")

            while (requestSuccess == False):
                try:
                    response = requests.get(URL, headers=headers)

                    if response.status_code == 200:
                        data = response.json()
                        matchList = data["items"]

                        for match in matchList:
                            if match["status"] == "FINISHED":
                                matchID = match["match_id"]
                                matchTime = match["configured_at"]

                                # Convert Unix timestamp to datetime
                                matchDatetime = datetime.utcfromtimestamp(matchTime)

                                # Check if the match occurred within the last 4 months
                                if (datetime.utcnow() - matchDatetime) <= timedelta(days=120):
                                    demoLink = match["demo_url"][0]
                                    matchInfo = f"{matchID},{matchTime}-{demoLink}"

                                    query = f"""
                                        SELECT MatchID
                                        FROM Matches
                                        WHERE MatchID = '{matchID}'
                                    """

                                    cursor.execute(query)

                                    matchSearch = cursor.fetchall()

                                    if len(matchSearch) == 0:
                                        file.write(f"{matchInfo}\n")

                                    gamesProcessedCounter += 1
                                else:
                                    # Match time is older than 4 months, exit loops
                                    requestSuccess = True
                                    offset = MatchLimit  # Exit outer loop
                                    break

                        requestSuccess = True
                    else:
                        print(f"Request failed with status code: {response.status_code}")
                        time.sleep(5)
                except requests.exceptions.RequestException as e:
                    print(f"Error occurred: {e}")

            offset += LIMIT

    print("-------------PROCESSING COMPLETE--------------")
    print(f"Total number of matches fetched --> {gamesProcessedCounter}")
    return matchIDList, matchTimeList

if __name__ == "__main__":
    load_dotenv()

    FACEIT_API_KEY = os.getenv('FACEIT_API_KEY')
    HUB_ID_LIST_ENV = os.getenv('FACEIT_HUB_ID_LIST')

    HUB_ID_LIST = HUB_ID_LIST_ENV.split(',')

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

    matchIDList, matchTimeList = FetchMatchList(FACEIT_API_KEY, HUB_ID_LIST, 70000, cursor)