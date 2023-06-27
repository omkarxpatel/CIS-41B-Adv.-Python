import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import os

class Database:
    def __init__(self, dbName):
        self.dbName = dbName
        self.connect()

    def connect(self):
        global sqliteConnection
        try:
            sqliteConnection = sqlite3.connect(self.dbName)
            cursor = sqliteConnection.cursor()
            select_Query = "select sqlite_version();"
            cursor.execute(select_Query)
            record = cursor.fetchall()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)


    def table(self, query):
        try:
            cursor = sqliteConnection.cursor()
            cursor.execute(query)
            sqliteConnection.commit()

        except sqlite3.Error as error:
            print("Table exists: ", error)


    def insert(self, query, df):
        try:
            cursor = sqliteConnection.cursor()

            for row in df.itertuples():
                cursor.execute(query.format(row[0], row[1]))
                
            sqliteConnection.commit()

        except sqlite3.Error as error:
            print("Failed to insert: ", error)


    def search(self, query, value):
        cursor = sqliteConnection.cursor()

        cursor.execute(query.format(value))
        result = cursor.fetchall()
        return result[0][0]
    

    def delete(self, query, id):
        try:
            cursor = sqliteConnection.cursor()
            delete_query = query + str(id)
            cursor.execute(delete_query)
            sqliteConnection.commit()

        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)


    def query_builder(self, Data_Base, Query_Type, colandType, dataType=[]):
        col = list(colandType)
        types = list(colandType.values())
        if Query_Type == ("TABLE"):
            query = f"CREATE TABLE IF NOT EXISTS {Data_Base} "

            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += f"{col[i]} {types[i]})"
                else:
                    query += f"({col[i]} {types[i]}, "

        elif Query_Type == ("INSERT"):
            query = f"INSERT INTO {Data_Base} "
            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += f"{col[i]}) VALUES "
                else:
                    query += f"({col[i]}, "

            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += "{})"
                else:
                    query += "({}, "

        elif Query_Type == ("SELECT"):
            query = f"SELECT {dataType[1]} FROM {Data_Base} WHERE {dataType[0]} == " + "'{}'"

        elif Query_Type == ("DELETE"):
            query = f"DELETE from {Data_Base} WHERE {dataType} = "

        return query

# path to my files is Files/... (in a files folder)   
    
html_data = pd.read_html("Files/Co2.html", header=2)
htmlDf = html_data[0].groupby('year')['average'].mean().round(2)
htmlDf = pd.DataFrame(htmlDf)

csvDF = pd.read_csv("Files/SeaLevel.csv", skiprows=3)
csvDF['year'] = csvDF['year'].astype(int)

csvDf = csvDF.groupby("year")['TOPEX/Poseidon'].mean().round(2)
csvDf = pd.DataFrame(csvDf)

database = "Lab1_.db"
db = Database(database)
colandType = {'year': 'INTEGER', 'average': "REAL"}

db.table(db.query_builder("SeaLevel", "TABLE", colandType))
db.insert(db.query_builder("SeaLevel", "INSERT", colandType), csvDf)
cursor = sqliteConnection.cursor()

cursor.execute("SELECT * FROM SeaLevel")
lod = cursor.fetchall()

print("NOAA Mean Sea Level Rise:\nYear:   Average:")
for item in lod:
    print(f"{item[0]}:   {item[1]}")

db.table(db.query_builder("CO2", "TABLE", colandType))
insertQ = db.query_builder("CO2", "INSERT", colandType)
db.insert(insertQ, htmlDf)

cursor.execute("SELECT * FROM CO2")
lod = cursor.fetchall()
print("Total Carbon Emissions:\nYear:   Average:")

for item in lod:
    print(f"{item[0]}:   {item[1]}")

sqliteConnection.close()
os.remove(database)