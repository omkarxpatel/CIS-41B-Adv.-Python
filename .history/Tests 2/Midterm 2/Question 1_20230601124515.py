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



#E