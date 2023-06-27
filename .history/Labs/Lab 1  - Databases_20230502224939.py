import sqlite3
import pandas as pd

class Database:
    def __init__(self, dbName):
        self.dbName = dbName
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dbName)
            print("Database created and Successfully Connected to SQLite")
            select_Query = "select sqlite_version();"
            self.conn.execute(select_Query)
            self.conn.commit()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def table(self, query):
        try:
            self.conn.execute(query)
            self.conn.commit()
            print("SQLite table created")

        except sqlite3.Error as error:
            print("Table exists: ", error)

    def insert(self, query, df):
        try:
            for row in df.itertuples(index=False):
                self.conn.execute(query, tuple(row))
            self.conn.commit()
            print("Inserted successfully into table")

        except sqlite3.Error as error:
            print("Failed to insert: ", error)

    def search(self, query, value):
        cursor = self.conn.cursor()
        sel = query.format(value)
        cursor.execute(sel)
        result = cursor.fetchall()
        return result[0][0] if result else None

    def delete(self, query, id):
        try:
            delete_query = query + str(id)
            self.conn.execute(delete_query)
            self.conn.commit()
            print("Record deleted successfully")

        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)

    def query_builder(self, Data_Base, Query_Type, colandType, dataType=[]):
        col = list(colandType)
        types = list(colandType.values())
        if Query_Type == "TABLE":
            query = f"CREATE TABLE IF NOT EXISTS {Data_Base} ("
            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += f"{col[i]} {types[i]})"
                else:
                    query += f"{col[i]} {types[i]}, "

        elif Query_Type == "INSERT":
            query = f"INSERT INTO {Data_Base} ("
            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += f"{col[i]}) VALUES ("
                else:
                    query += f"{col[i]}, "

            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += "?)"
                else:
                    query += "?, "

        elif Query_Type == "SELECT":
            if dataType:
                query = f"SELECT {dataType[1]} FROM {Data_Base} WHERE {dataType[0]} = ?"
            else:
                query = f"SELECT * FROM {Data_Base}"

        elif Query_Type == "DELETE":
            query = f"DELETE from {Data_Base} WHERE {dataType} = "

        return query

# Parsing Co2.html
html_data = pd.read_html("Co2.html", header=2)
htmlDf = html_data[0].groupby('year')['average'].mean().round(2)
htmlDf = pd.DataFrame(htmlDf)

# Parsing SeaLevel.csv
csvDF = pd.read_csv("Files/SeaLevel.csv", skiprows=3)
csvDF['year'] = csvDF['year'].astype(int)  # Convert year column to integer
csvDf = csvDF.groupby("year")['TOPEX/Poseidon'].mean().round(2)
csvDf = pd.DataFrame(csvDf)

database = "Lab1_.db"
db = Database(database)
db.connect()
c = "CO2"
s = "SeaLevel"
colandType = {'year': 'INTEGER', 'average': "REAL"}

db.table(db.query_builder("SeaLevel", "TABLE", colandType))
db.insert(db.query_builder("SeaLevel", "INSERT", colandType), csvDf)
cursor = sqliteConnection.cursor()

select_all = "SELECT * FROM SeaLevel"
cursor.execute(select_all)
list_of_data = cursor.fetchall()
print("NOAA Mean Sea Level Rise:\nyear    average")
for data in list_of_data:
    print(f"{data[0]}:   {data[1]}")

db.table(db.query_builder("CO2", "TABLE", colandType))
insertQ = db.query_builder("CO2", "INSERT", colandType)
db.insert(insertQ, htmlDf)

select_all = "SELECT * FROM CO2"
cursor.execute(select_all)
list_of_data = cursor.fetchall()
print("Total Carbon Emissions:\nyear    average")
for data in list_of_data:
    print(f"{data[0]}:   {data[1]}")

sqliteConnection.close()
os.remove(database)