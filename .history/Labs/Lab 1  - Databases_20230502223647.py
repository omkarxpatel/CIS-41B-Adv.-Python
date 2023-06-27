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