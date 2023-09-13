import requests
import os
from dotenv import load_dotenv
import time


def FetchMatchList(API_KEY, HubIDList, MatchLimit):
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
                                matchInfo = f"{matchID},{matchTime}"
                                file.write(f"{matchInfo}\n")
                                gamesProcessedCounter += 1
                        requestSuccess = True
                    else:
                        print(f"Request failed with status code: {response.status_code}")
                        time.sleep(5)
                except requests.exceptions.RequestException as e:
                    print(f"Error occured: {e}")
            
            offset += LIMIT

    print("-------------PROCESSING COMPLETE--------------")
    print(f"Total number of matches fetched --> {len(matchIDList)}")
    return matchIDList, matchTimeList



if __name__ == "__main__":
    load_dotenv()

    FACEIT_API_KEY = os.getenv('FACEIT_API_KEY')
    HUB_ID_LIST_ENV = os.getenv('FACEIT_HUB_ID_LIST')

    HUB_ID_LIST = HUB_ID_LIST_ENV.split(',')

    matchIDList, matchTimeList = FetchMatchList(FACEIT_API_KEY, HUB_ID_LIST, 70000)