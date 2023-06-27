import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import os
import matplotlib.pyplot as plt


class Database:
   def __init__(self, db):
       self.db = db

   def connect(self):
       global sqliteConnection
       try:
           sqliteConnection = sqlite3.connect(self.db)
           cursor = sqliteConnection.cursor()
           print("Database created and Successfully Connected to SQLite")
           select_Query = "select sqlite_version();"
           cursor.execute(select_Query)
           record = cursor.fetchall()
       except sqlite3.Error as error:
           print("Error while connecting to sqlite", error)

   def table(self, query):
       global sqliteConnection
       try:
           cursor = sqliteConnection.cursor()
           cursor.execute(query)
           sqliteConnection.commit()
           print("SQLite table created")
       except sqlite3.Error as error:
           print("Table exists: ", error)

   def insert(self, query, df):
       global sqliteConnection
       try:
           cursor = sqliteConnection.cursor()
           for row in df.itertuples():
               insert_sql = query.format(row[0], row[1])
               cursor.execute(insert_sql)
           sqliteConnection.commit()
           print("Inserted successfully into table")
       except sqlite3.Error as error:
           print("Failed to insert: ", error)

   def search(self, query, value):
       global sqliteConnection
       cursor = sqliteConnection.cursor()
       sel = query.format(value)
       cursor.execute(sel)
       result = cursor.fetchall()
       return result[0][0]

   def delete(self, query, id):
       global sqliteConnection
       try:
           cursor = sqliteConnection.cursor()
           delete_query = query + str(id)
           cursor.execute(delete_query)
           sqliteConnection.commit()
           print("Record deleted successfully ")
       except sqlite3.Error as error:
           print("Failed to delete record from sqlite table", error)

   def query_builder(self, Data_Base, Query_Type, column, Query_Tuple=[]):
       col = list(column)
       types = list(column.values())
       if Query_Type == "TABLE":
           string = f"CREATE TABLE IF NOT EXISTS {Data_Base} "
           for i in range(len(col)):
               if col[i] == col[-1]:
                   string += f"{col[i]} {types[i]})"
               else:
                   string += f"({col[i]} {types[i]}, "
       elif Query_Type == "INSERT":
           string = f"INSERT INTO {Data_Base} "
           for i in range(len(col)):
               if col[i] == col[-1]:
                   string += f"{col[i]}) VALUES "
               else:
                   string += f"({col[i]}, "
           for i in range(len(col)):
               if col[i] == col[-1]:
                   string += "{})"
               else:
                   string += "({}, "
       elif Query_Type == "SELECT":
           string = f"SELECT {Query_Tuple[1]} FROM {Data_Base} WHERE {Query_Tuple[0]} == " + "'{}'"
       elif Query_Type == "DELETE":
           string = f"DELETE from {Data_Base} WHERE {Query_Tuple} = "
       return string


# Parsing Co2.html
html_data = pd.read_html("Files/Co2.html", header=2)
htmlDf = html_data[0].groupby('year')['average'].mean().round(2)

# Parsing SeaLevel.csv
csvDF = pd.read_csv("Files/SeaLevel.csv", skiprows=3)
csvDF['year'] = csvDF['year'].astype(int)
csvDf = csvDF.groupby("year")['TOPEX/Poseidon'].mean().round(2)

# Combine the data into a single DataFrame
df = pd.concat([htmlDf, csvDf], axis=1)

# Create a new figure and axis object
fig, ax = plt.subplots()

ax.plot(df.index, df['average'], label='CO2')
ax.plot(df.index, df['TOPEX/Poseidon'], label='SeaLevel')

ax.set_xlabel('Year')
ax.set_ylabel('Level')
ax.set_title('CO2 and SeaLevel over Time')

ax.legend()

plt.show()


