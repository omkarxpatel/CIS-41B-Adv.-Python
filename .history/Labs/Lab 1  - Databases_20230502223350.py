import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import os

sqliteConnection = None

class FileParser:
    def __init__(self, csv, html):
        self.csvFile = csv
        self.htmlFile = html        
        
    def parseHTML(self):
        data = pd.read_html(self.htmlFile, header = 2)
        df = data[0].groupby('year')['average'].mean().round(2)
        df = pd.DataFrame(df)    
        return df
        
    def parseCSV(self):
        df = pd.read_csv(self.csvFile,skiprows=3)
        df['year'] = df['year'].astype(int) #getting rid of the decimal
        df = df.groupby("year")['TOPEX/Poseidon'].mean().round(2)   
        df = pd.DataFrame(df)
        return df
        
class Database:
    def __init__(self, dbName):
        self.dbName = dbName
        
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
   
    
    def query_builder(self, name, qType, colandType, dataType=[]): 
        col = list(colandType)
        types = list(colandType.values())
        if qType == ("TABLE" or "table" or "Table"):
            query = f"CREATE TABLE IF NOT EXISTS {name} "
            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += f"{col[i]} {types[i]})"
                else:
                    query += f"({col[i]} {types[i]}, "
            
        elif qType == ("INSERT" or "insert" or "Insert"):
            query = f"INSERT INTO {name} "
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
            
            
        elif qType == ("SELECT" or "select" or "Select"):
            query = f"SELECT {dataType[1]} FROM {name} WHERE {dataType[0]} == " + "'{}'"
            
        elif qType == ("DELETE" or "delete" or "Delete"):
            query = f"DELETE from {name} WHERE {dataType} = "
        
        return query

    
        
if __name__ == '__main__':         
    csv = "SeaLevel.csv"
    html = "Co2.html"
    parse = FileParser(csv, html)
    htmlDf = parse.parseHTML()
    csvDf = parse.parseCSV()
    database = "Lab1_.db"        
    db = Database(database)
    db.connect()
    
    
    c = "CO2"
    s = "SeaLevel"
    colandType = {'year': 'INTEGER', 'average': "REAL"}
    #CO2
    tableQ = db.query_builder(c, "TABLE", colandType)
    db.table(tableQ)
    insertQ = db.query_builder(c, "INSERT", colandType)
    db.insert(insertQ, csvDf)
    #SeaLevel
    tableQ = db.query_builder(s, "TABLE", colandType)
    db.table(tableQ)  
    insertQ = db.query_builder(s, "INSERT", colandType)
    db.insert(insertQ, htmlDf)
    
    
    #CO2
    searchQ = db.query_builder(c, "SELECT", colandType, ["year", "average"])
    record = db.search(searchQ, 2001)
    print(record)  
    searchQ = db.query_builder(c, "SELECT", colandType, ["average", "year"])
    record = db.search(searchQ, 11.93)
    print(record)
    #SeaLevel
    searchQ = db.query_builder(s, "SELECT", colandType, ["year", "average"])
    record = db.search(searchQ, 1965)
    print(record)  
    searchQ = db.query_builder(s, "SELECT", colandType, ["average", "year"])
    record = db.search(searchQ, 327.45)
    print(record) 
    
    
    print(OutputStream(c))
    print(OutputStream(s))    
    
    
    #CO2
    deleteQ = db.query_builder(c, "DELETE", colandType, "year")
    record = db.delete(deleteQ, 2000)
    deleteQ = db.query_builder(c, "DELETE", colandType, "average")
    record = db.delete(deleteQ, -5.27)
    #SeaLevel
    deleteQ = db.query_builder(c, "DELETE", colandType, "year")
    record = db.delete(deleteQ, 1970) 
    deleteQ = db.query_builder(c, "DELETE", colandType, "average")
    record = db.delete(deleteQ, 326.32)

    
    print(OutputStream(c))
    print(OutputStream(s))
    
    sqliteConnection.close()
    os.remove(database)    