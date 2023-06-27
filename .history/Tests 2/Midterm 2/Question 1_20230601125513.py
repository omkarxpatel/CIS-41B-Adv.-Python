# LAB 0 - DATA ACQUISITION.PY
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re

class WebScraper:
    def __init__(self, htmlfile=None, htmlsite=None):
        self.htmlfile = htmlfile
        self.htmlsite = htmlsite
        

    def __str__(self):
        return f"WebScraper: htmlfile={self.htmlfile}, htmlsite={self.htmlsite}"
    

    def openHtmlFile(self):
        with open(self.htmlfile, "r") as f:
            contents = f.read()
            
        return BeautifulSoup(contents, 'html.parser')


    def openHtmlSite(self):    
        html = urlopen(self.htmlsite)
        return BeautifulSoup(html, 'html.parser')    


    def soupf(self):
        soupf = self.openHtmlFile()
        print(soupf.prettify()); print(soupf.h2); print(soupf.head); print(soupf.li); print("HTML: {0}, name: {1}, text: {2}".format(soupf.h2, soupf.h2.name, soupf.h2.text)); print(25*'=-')
        return soupf


    def souph(self):
        souph = self.openHtmlSite()
        print(souph.prettify()); print(souph.h2); print(souph.head); print(souph.li); print("HTML: {0}, name: {1}, text: {2}".format(souph.h2, souph.h2.name, souph.h2.text)); print(25*'=-')
        return souph


    def children(self, html):
        [print(child.name) for child in html.recursiveChildGenerator() if child.name is not None]           


    def findAll(self, html, tags):
        dict = {}

        for tag in html.find_all(tags):
            print("{0}: {1}".format(tag.name, tag.text))
            r = re.compile(r'\s')
            s = r.split(tag.text)
            dict[s[0]] = s[1]

        for k,v in dict.items():
            print('key= ',k,'\tvalue= ',v)    


    def appendTag(self, html, tag, nustr):
        newtag = html.new_tag(tag)
        newtag.string=nustr
        ultag = html.ul  
        ultag.append(newtag)  

        print(ultag.prettify()) 

    def insertAt(self, html, tag, nustr, index):
        newtag = html.new_tag(tag)
        newtag.string = nustr
        ultag = html.ul   
        ultag.insert(index, newtag)   

        print(ultag.prettify()) 


    def selectIndex(self, html, index):
        soup = BeautifulSoup(html, 'html.parser')
        sel = soup.select(f'li:nth-of-type({index})')
        print(sel)


    def selectParagraph(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        p_elems = soup.find_all('p')
        print(p_elems)

        for elem in p_elems:
            print(str(elem))

            
    def selectSpan(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        spanElem = soup.select('span')
        print(spanElem)

        for i in spanElem:
            print(i.getText())


# scraper = WebScraper()

# response = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capitaLinks to an external site.')
# span_elems = scraper.selectSpan(response.text)
# print(span_elems)





# LAB 1 DATABASES.PY
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

# path to my files is Files/... (in a files folder)   
    
# html_data = pd.read_html("Files/Co2.html", header=2)
# htmlDf = html_data[0].groupby('year')['average'].mean().round(2)
# htmlDf = pd.DataFrame(htmlDf)

# csvDF = pd.read_csv("Files/SeaLevel.csv", skiprows=3)
# csvDF['year'] = csvDF['year'].astype(int)

# csvDf = csvDF.groupby("year")['TOPEX/Poseidon'].mean().round(2)
# csvDf = pd.DataFrame(csvDf)

# database = "Lab1_.db"
# db = Database(database)
# colandType = {'year': 'INTEGER', 'average': "REAL"}

# db.table(db.query_builder("SeaLevel", "TABLE", colandType))
# db.insert(db.query_builder("SeaLevel", "INSERT", colandType), csvDf)
# cursor = sqliteConnection.cursor()

# cursor.execute("SELECT * FROM SeaLevel")
# lod = cursor.fetchall()

# print("NOAA Mean Sea Level Rise:\n\nYear:   Average:")
# for item in lod:
#     print(f"{item[0]}:   {item[1]}")

# db.table(db.query_builder("CO2", "TABLE", colandType))
# insertQ = db.query_builder("CO2", "INSERT", colandType)
# db.insert(insertQ, htmlDf)

# cursor.execute("SELECT * FROM CO2")
# lod = cursor.fetchall()
# print("\n\n")
# print("Total Carbon Emissions:\n\nYear:   Average:")

# for item in lod:
#     print(f"{item[0]}:   {item[1]}")

# sqliteConnection.close()

# try:
#     os.remove(database)
# except:
#     raise FileNotFoundError(f"Could not find path: {database}")



# EXERCISE CLIENT

import socket
import pandas as pd
from io import StringIO

class Client:
   def __init__(self, host, port):
       self.host = host
       self.port = port

   def send_query(self, query):
       client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       client_socket.connect((self.host, self.port))

       client_socket.send(query.encode())

       result = client_socket.recv(15890).decode()

       client_socket.close()

       df = pd.read_csv(StringIO(result), sep=",")
       return df

if __name__ == "__main__":
   client = Client('localhost', 6000)
   query = "SELECT * FROM CO2_Data"
   result_df = client.send_query(query)
   print(result_df)




# EXERCISE SERVER

import socket
import sqlite3
import pandas as pd

class Database:
   def __init__(self, db):
       self.db = db
       self.cursor = None
       self.sqliteConnection = None

   def connect(self):
       try:
           self.sqliteConnection = sqlite3.connect(self.db)
           self.cursor = self.sqliteConnection.cursor()
           print("Database created and successfully connected to SQLite")
       except sqlite3.Error as error:
           print("Error while connecting to SQLite:", error)

   def create_table(self, table_name, columns):
       try:
           column_definitions = ', '.join([f'column_{i} TEXT' for i in range(columns)])
           create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
           self.cursor.execute(create_table_query)
           self.sqliteConnection.commit()
           print(f"Table '{table_name}' created successfully")
       except sqlite3.Error as error:
           print("Error while creating table:", error)

   def insert_data(self, table_name, data):
       try:
           insert_query = f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(data))})"
           self.cursor.execute(insert_query, data)
           self.sqliteConnection.commit()
           print("Data inserted successfully")
       except sqlite3.Error as error:
           print("Error while inserting data:", error)

   def execute_query(self, query):
       self.cursor.execute(query)
       result = self.cursor.fetchall()
       return result

   def close(self):
       if self.cursor:
           self.cursor.close()
       if self.sqliteConnection:
           self.sqliteConnection.close()
       print("Database connection closed")

class Server:
   def __init__(self, host, port, db):
       self.host = host
       self.port = port
       self.database = Database(db)

   def start(self):
       server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

       try:
           server_socket.bind((self.host, self.port))

           server_socket.listen(1)
           print(f"Server started and listening on {self.host}:{self.port}")

           while True:
               client_socket, address = server_socket.accept()
               print(f"Accepted connection from {address[0]}:{address[1]}")

               self.handle_client(client_socket)

       finally:
           server_socket.close()

   def handle_client(self, client_socket):
       query = client_socket.recv(4096).decode()
       print("Received query:", query)

       # Execute the query and send the result back to the client
       result = self.database.execute_query(query)
       result_str = "\n".join([",".join(map(str, row)) for row in result])
       client_socket.send(result_str.encode())

       client_socket.close()

   def process_data(self, filename):
       try:
           df = pd.read_csv(filename, skiprows=2, nrows=52)
           df = df.iloc[:, :56]
           print(df)

           table_name = "CO2_Data"  
           columns = df.shape[1]  
           self.database.create_table(table_name, columns)  

           for _, row in df.iterrows():
               data = tuple(row)
               self.database.insert_data(table_name, data)

           print("Data processing completed")
       except FileNotFoundError:
           print("File not found")
       except Exception as e:
           print("Error occurred during data processing:", e)

   def close(self):
       self.database.close()

# server = Server("localhost", 6000, "Lab1.db")
# server.database.connect()
# server.process_data("Files/USAStatesCO2.csv")
# server.start()
# server.close()
