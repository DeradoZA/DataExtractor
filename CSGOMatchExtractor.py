import requests
import os
from dotenv import load_dotenv
import time


def FetchMatchList(API_KEY, HubIDList, MatchLimit):
    matchIDList = []
    offset = 0
    LIMIT = 100
    iterationAmount = 0

    headers = {
            'Authorization': f'Bearer {FACEIT_API_KEY}'
    }

    for hub in HubIDList:
        print(f"Fetching match IDs: {hub}")

        while (offset < MatchLimit):
            requestSuccess = False
            URL = f"https://open.faceit.com/data/v4/hubs/{hub}/matches?offset={offset}&limit={LIMIT}"
            iterationAmount += 1
            print(f"Iteration number {iterationAmount}, matches processed {len(matchIDList)}")

            while (requestSuccess == False):
                try:
                    response = requests.get(URL, headers=headers)

                    if response.status_code == 200:
                        data = response.json()
                        matchList = data["items"]

                        for match in matchList:
                            matchID = match["match_id"]
                            matchIDList.append(matchID)
                        requestSuccess = True
                    else:
                        print(f"Request failed with status code: {response.status_code}")
                        time.sleep(5)
                except requests.exceptions.RequestException as e:
                    print(f"Error occured: {e}")
            
            offset += LIMIT

    print("-------------PROCESSING COMPLETE--------------")
    print(f"Total number of matches fetched --> {len(matchIDList)}")
    return matchIDList

def MatchIDListSaver(matchIDList):
    print("Writing match IDs to disk")
    with open("MatchIDList.txt", 'w') as file:
        for matchID in matchIDList:
            file.write(f"{matchID}\n")



if __name__ == "__main__":
    load_dotenv()

    FACEIT_API_KEY = os.getenv('FACEIT_API_KEY')
    HUB_ID_LIST_ENV = os.getenv('FACEIT_HUB_ID_LIST')

    HUB_ID_LIST = HUB_ID_LIST_ENV.split(',')

    matchIDList = FetchMatchList(FACEIT_API_KEY, HUB_ID_LIST, 50000)

    MatchIDListSaver(matchIDList)