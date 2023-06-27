import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import NamedTuple
import pickle
import sqlite3


class GreenhouseGasData(NamedTuple):
   Gas: str
   Pre_1750: float
   Recent: str
   Absolute_increase_since_1750: str
   Percentage_increase_since_1750: str


class GreenhouseGasCollection:
   def __init__(self):
       self.data = []

   def __repr__(self):
       return str(self.data)

   def add_data(self, gas_data):
       self.data.append(gas_data)

   def sort_by(self, column):
       if column not in GreenhouseGasData._fields:
           raise ValueError(f"{column} not found in {GreenhouseGasData._fields}")
       self.data = sorted(self.data, key=lambda x: getattr(x, column))

   def search(self, gas):
       for gas_data in self.data:
           if gas_data.Gas == gas:
               return gas_data
       return None


class WebScraping:
   def __init__(self, url):
       self.url = url
       self.response = requests.get(self.url)
       self.soup = BeautifulSoup(self.response.text, 'html.parser')

   def extract_data(self):
       data = defaultdict(list)
       tables = self.soup.find_all('table', {'class': 'wikitable'})
       table = tables[2]
       rows = table.find_all('tr')[1:]
       for row in rows:
           cols = row.find_all('td')
           cols = [col.text.strip().replace("ppm", "").replace("ppb", "") for col in cols]
           cols = [col.split('[')[0].split('\xa0')[0] if '[' in col else col.split('\xa0')[0] for col in cols]
           data['Gas'].append(cols[0])
           data['Pre-1750'].append(float(cols[1]))
           data['Recent'].append(float(cols[2]))
           data['Absolute increase since 1750'].append(float(cols[3]))
           data['Percentage increase since 1750'].append((cols[4].rstrip('%')))
       return data

class Database:
   def __init__(self, dbName):
       self.dbName = dbName
       cursor = dbName.cursor()

   def connect(self):
       global sqliteConnection
       try:
           sqliteConnection = sqlite3.connect(self.dbName)
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

   def insert(self, query, df_bytes):
       global sqliteConnection
       try:
           cursor = sqliteConnection.cursor()
           df = pickle.loads(df_bytes)
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

   def query_builder(self, Data_Base, Query_Type, Query_Tuple):
       if Query_Type.lower() == "table":
           columns, types = zip(*Query_Tuple)
           query = f"CREATE TABLE IF NOT EXISTS {Data_Base} ("
           query += ", ".join(f"{col} {typ}" for col, typ in zip(columns, types))
           query += ")"
       elif Query_Type.lower() == "insert":
           columns, values = zip(*Query_Tuple)
           query = f"INSERT INTO {Data_Base} ({', '.join(columns)})"
           query += " VALUES (" + ", ".join(["'{}'"] * len(columns)).format(*values) + ")"
       elif Query_Type.lower() == "select":
           column, value = Query_Tuple
           query = f"SELECT {column} FROM {Data_Base} WHERE {column} = '{value}'"
       elif Query_Type.lower() == "delete":
           column, value = Query_Tuple
           query = f"DELETE from {Data_Base} WHERE {column} = '{value}'"
       else:
           query = ""

       return query

def main():
   ws = WebScraping('https://en.wikipedia.org/wiki/Greenhouse_gas')
   data = ws.extract_data()
   collection = GreenhouseGasCollection()

   for i in range(len(data['Gas'])):
       gas_data = GreenhouseGasData(data['Gas'][i], data['Pre-1750'][i], data['Recent'][i],
                                    data['Absolute increase since 1750'][i], data['Percentage increase since 1750'][i])
       collection.add_data(gas_data)

   df = pd.DataFrame(collection.data, columns=GreenhouseGasData._fields)

   # Connect to the database and build the insert query
   conn = sqlite3.connect('test.db')
   db = Database(conn)
   columns = GreenhouseGasData._fields
   query_tuple = list(zip(columns, ['text', 'real', 'real', 'real', 'real']))
   table_query = db.query_builder('greenhouse_gas', 'table', query_tuple)
   insert_query = f"INSERT INTO greenhouse_gas ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?)"

   # Serialize the DataFrame to bytes and insert into the database
   df_bytes = pickle.dumps(df)
   db.insert(insert_query, df_bytes)
   cursor = db.cursor()
   select_all = "SELECT * FROM greenhouse_gas"
   cursor.execute(select_all)
   list_of_data = cursor.fetchall()
   for data in list_of_data:
       print(data)


