import openpyxl
from dotenv import load_dotenv
from mysql.connector import connect, Error
import os
import requests
import csv

def MatchInfoExtractor(path, file, cursor, connection):
    matchInfo = {}
    fullFilePath = os.path.join(path, file)
    endMatchID = file.find('.')
    matchID = file[0:endMatchID]
    if (matchID.find("export") != -1):
        matchID = matchID[0: matchID.find("export")-1]

    query = f"""
        SELECT MatchID
        FROM Matches m
        WHERE m.MatchID = '{matchID}'
    """
    cursor.execute(query)

    queryResult = cursor.fetchall()

    if (len(queryResult) == 0):
        matchInfo = getMatchInfo(fullFilePath)
        team1Score = 0
        team2Score = 0
        map = ""

        for key, value in matchInfo.items():
            if key == "Score team 1":
                team1Score = int(value)
            
            if key == "Score team 2":
                team2Score = int(value)

            if key == "Map":
                map = value

        insertMatchQuery = f"""
            INSERT INTO Matches(MatchID, Team_1_Score, Team_2_Score, Map, MatchTime)
            VALUES
            ('{matchID}', {team1Score}, {team2Score}, '{map}', {0})
        """

        cursor.execute(insertMatchQuery)

        connection.commit()
        print(f"Match - {matchID} - SUCCESSFUL")
    else:
        print(f"Match - {matchID} - ALREADY IN DB")



def getMatchInfo(fileList, path):
    matchInfo = {}
    errors = 0 
    for file in fileList:
        try:
            fullFilePath = os.path.join(path, file)
            wb_obj = openpyxl.load_workbook(fullFilePath)

            worksheet = wb_obj['General']
        except Exception as e:
            print(e)
            errors += 1
            print(errors)

    # for col in worksheet.iter_cols():
    #     key = col[0].value
    #     value = col[1].value
    #     matchInfo[key] = value

    return errors

def getTeamDictionary(file):
    wb_obj = openpyxl.load_workbook(file)
    teamDict = {}
    sheet = wb_obj["General"]
    team1Alias = sheet.cell(row = 2, column = 13)
    team2Alias = sheet.cell(row= 2, column=14)

    teamDict[1] = team1Alias.value
    teamDict[2] = team2Alias.value

    return teamDict

if __name__ == "__main__":
    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB = os.getenv("CSGO_DB")
    DB_PW = os.getenv("DB_USER_PASSWORD")

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

    ProcessedDemosPath = os.path.join(os.getcwd(), "PorcessedDemos")

    ProcessedDemos = os.listdir(ProcessedDemosPath)

    errors = getMatchInfo(ProcessedDemos, ProcessedDemosPath)

    print(errors)
