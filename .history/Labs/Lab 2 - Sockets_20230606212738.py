from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import sqlite3
import os

sqliteConnection = None

class FileStream():

    def __init__(self, url):
        self.htmlsite = url
    
    def openHtmlSite(self):
        html = urlopen(self.htmlsite)
        return html
    
class Parser():

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
    
    
    def findData(self, tableClass=""):
        #finding correct table and splitting soup into content and headers
        tables = self.soup.find_all('table') 
        if len(tables) == 1:
            tableContent = tables[0].tbody
            tableHead = tables[0].thead.text
        else:
            tableContent = self.soup.find('table', class_=tableClass).tbody
            tableHead = self.soup.find('table', class_=tableClass).thead
        rows = tableContent.find_all('tr')
        tableHead = tableHead.split("  ")
        for i in tableHead:
            if i == '':
                tableHead.remove(i)
                
        
        #getting data from content
        data = []
        for tag in rows:
            data.append(tag.text)
        countries = []
        newData = []
        country = ""
        totalEmiss = ""
        perCapEmiss = ""
        for string in data:
            for char in string:
                if char.isalpha() == True or char == " ":
                    country += char
            string = re.sub(",", "", string)
            countries.append(country)
            country = ""
            nums = [float(v) for v in re.findall(r"[\d]+\.\d{1,2}", string)]
            newData.append(nums)

        #return a list of country and corresponding data
        retList = [tableHead]
        for i in range(len(countries)):
            retList.append([countries[i], *newData[i]])
        return retList
            
    
    
class Database():
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
        
    def insert(self, query, listV):
        global sqliteConnection
        try:
            cursor = sqliteConnection.cursor()
            for i in range(len(listV)):
                if type(listV[i]) == str:
                    listV[i] = f'"{listV[i]}"'
            insert_sql = query.format(*listV)
            print(insert_sql)
            cursor.execute(insert_sql)
            sqliteConnection.commit()
            print("Inserted successfully into table")
        except sqlite3.Error as error:
            print("Failed to insert: ", error)        
        
    def search(self, query, value=-1):
        global sqliteConnection
        cursor = sqliteConnection.cursor()
        if value != -1:
            sel = query.format(value)
            cursor.execute(sel)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        if value != -1:
            return result[0][0]  
        else:
            return result
        
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
   
    
    def query_builder(self, name, qType, header, Exampledata=[]):
        col = header
        types = []
        if len(Exampledata) != 0:
            for i in Exampledata:
                if type(i) == str:
                    types.append("STRING")
                elif type(i) == float:
                    types.append("REAL")
                elif type(i) == int:
                    types.append("INTEGER")
                elif type(i) == bool:
                    types.append("BOOL")
                else:
                    types.append("NOT NULL")
        
        if qType == ("TABLE" or "table" or "Table"):
            query = f'CREATE TABLE IF NOT EXISTS "{name}" ('
            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += f'"{col[i]}" {types[i]})'
                else:
                    query += f'"{col[i]}" {types[i]}, '
            
        elif qType == ("INSERT" or "insert" or "Insert"):
            query = f'INSERT INTO "{name}" ('
            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += f'"{col[i]}") VALUES ('
                else:
                    query += f'"{col[i]}", ' 
            for i in range(len(col)):
                if col[i] == col[-1]:
                    query += "{})"
                else:
                    query += "{}, "   
            
        elif qType == ("SELECT" or "select" or "Select"):
            query = f'SELECT {header[1]} FROM "{name}" WHERE {header[0]} == ' + "'{}'"
            
        elif qType == ("DELETE" or "delete" or "Delete"):
            query = f"DELETE from {name} WHERE {header[0]} = "
        return query
    
class OutputStream():
    def __init__(self, TableName):
        self.tname = TableName
        
    def PieGraph(self, label, dataPoints):
        global sqliteConnection         
        query = f'SELECT "{label}", "{dataPoints}" FROM "{self.tname}"'
        data = db.search(query)
        labels = []
        values = []
        for i in range(len(data)):
            labels.append(data[i][0])
            values.append(data[i][1])
        fig1, ax1 = plt.subplots()
        wedges, texts, autotexts = ax1.pie(values, 
                                           labels = labels,
                                           autopct='%1.1f%%', 
                                           shadow=True,
                                           startangle=30)     
        ax1.set_title(dataPoints + " per " + label)
        ax1.axis('equal')
        plt.show()        
        
        
if __name__ == "__main__":
    url = "https://worldpopulationreview.com/country-rankings/pollution-by-country"
    html = FileStream(url).openHtmlSite()
    data = Parser(html).findData()    
    headers = data[0]
    data = data[1:]    
    
    database = "Lab2.db"        
    db = Database(database)
    db.connect()    
    tableN = "Pollution by Country 2022"
    
    tableQ = db.query_builder(tableN, "TABLE", headers, data[0])
    db.table(tableQ)
    insertQ = db.query_builder(tableN, "INSERT", headers)
    for i in data:
        db.insert(insertQ, i)
    output = OutputStream(tableN)
    output.PieGraph(headers[0], headers[1])