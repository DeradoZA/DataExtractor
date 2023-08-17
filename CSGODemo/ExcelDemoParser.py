import openpyxl
from dotenv import load_dotenv
from mysql.connector import connect, Error
import os
import requests
import csv




def getTeamDictionary(file):
    wb_obj = openpyxl.load_workbook(file)
    teamDict = {}
    sheet = wb_obj["General"]
    team1Alias = sheet.cell(row = 2, column = 13)
    team2Alias = sheet.cell(row= 2, column=14)

    teamDict[team1Alias.value] = 1
    teamDict[team2Alias.value] = 2

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

    file = "1-4b47e64b-7068-4f53-a3ed-67a3200b4d81-1-1.dem.xlsx"

    teamDict = getTeamDictionary(file)

    print(teamDict)
