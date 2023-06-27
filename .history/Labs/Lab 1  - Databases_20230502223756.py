import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import os

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