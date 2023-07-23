import requests


def MakeAPIRequest(URL, API_KEY):

    headers = {
            'Authorization': f'Bearer {FACEIT_API_KEY}'
    }

    try:
        response = requests.get(HUB_INFO_URL, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occured: {e}")


if __name__ == "__main__":
    FACEIT_API_KEY = "5f6ab6e6-9e7c-4457-b377-7dbb9b05f16e"
    HUB_INFO_URL = 'https://open.faceit.com/data/v4/hubs/4531cb6b-7dd5-4492-aef5-f092648c072f/matches?offset=0&limit=20'

    apiResponse = MakeAPIRequest(HUB_INFO_URL, FACEIT_API_KEY)

    matchList = apiResponse["items"]

    for match in matchList:
        print(match["match_id"])