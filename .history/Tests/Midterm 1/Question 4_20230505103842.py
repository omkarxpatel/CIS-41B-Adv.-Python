import requests
from bs4 import BeautifulSoup
from typing import NamedTuple
import sqlite3
import pandas as pd
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
    
    

class GreenhouseGasData(NamedTuple):
    Gas: str
    Pre_1750: float
    Recent: str
    Absolute_increase_since_1750: str
    Percentage_increase_since_1750: str

class GreenhouseGasCollection:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def sort_by(self, column):
        if column not in GreenhouseGasData._fields:
            raise ValueError(f"{column} not found in {GreenhouseGasData._fields}")
        
        self.data = sorted(self.data, key=lambda x: getattr(x, column))

    def search(self, gas):
        for gas_data in self.data:
            if gas_data.Gas == gas:
                return gas_data
        return None


def main():

    url = 'https://en.wikipedia.org/wiki/Greenhouse_gas'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table', {'class': 'wikitable'})
    rows = tables[2].find_all('tr')
    gas_list = []

    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip().replace("ppm", "").replace("ppb", "") for col in cols]
        cols = [col.split('[')[0].split('\xa0')[0] if '[' in col else col.split('\xa0')[0] for col in cols]

        gas_list.append(cols)

    gas_list = [[col[0]] + col[1::] for col in gas_list]

    data = [
        GreenhouseGasData(str(gas_list[0][0]), int(gas_list[0][1]), str(gas_list[0][2]), str(gas_list[0][3]), str(gas_list[0][4])),
        GreenhouseGasData(str(gas_list[1][0]), int(gas_list[1][1]), str(gas_list[1][2]), str(gas_list[1][3]), str(gas_list[1][4])),
        GreenhouseGasData(str(gas_list[2][0]), int(gas_list[2][1]), str(gas_list[2][2]), str(gas_list[2][3]), str(gas_list[2][4])),
        GreenhouseGasData(str(gas_list[3][0]), int(gas_list[3][1]), str(gas_list[3][2]), str(gas_list[3][3]), str(gas_list[3][4]))
        ]
    print()
    collection = GreenhouseGasCollection(data)
    # print("Data:", collection)

    print()
    collection.sort_by("Recent")
    # print("Data sorted by Recent:", collection)

    print()
    result = collection.search(str(gas_list[0][0]))
    # print("Data for Carbon dioxide:", result)

    return data
    dataframe = pd.DataFrame(collection.data, columns=GreenhouseGasData._fields)
    return dataframe

if __name__ == "__main__":
    data = main()
    



    
print(val)
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

print("NOAA Mean Sea Level Rise:\n\nYear:   Average:")
for item in lod:
    print(f"{item[0]}:   {item[1]}")

db.table(db.query_builder("CO2", "TABLE", colandType))
insertQ = db.query_builder("CO2", "INSERT", colandType)
db.insert(insertQ, htmlDf)

cursor.execute("SELECT * FROM CO2")
lod = cursor.fetchall()
print("\n\n")
print("Total Carbon Emissions:\n\nYear:   Average:")

for item in lod:
    print(f"{item[0]}:   {item[1]}")

sqliteConnection.close()

try:
    os.remove(database)
except:
    raise FileNotFoundError(f"Could not find path: {database}")