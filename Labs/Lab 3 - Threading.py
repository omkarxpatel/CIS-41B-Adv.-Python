from urllib.request import urlopen
from bs4 import BeautifulSoup
import threading
import sqlite3
import matplotlib.pyplot as plt

sqliteConnection = None
threadLock = threading.Lock()
data = []


class FileStream():
    def __init__(self, url):
        self.htmlsite = url

    def openHtmlSite(self):
        html = urlopen(self.htmlsite)
        
        soup = BeautifulSoup(html, 'html.parser')
        return soup


class databaseService:
    def __init__(self, dbName, tableName):
        self.dbName = dbName  # make into parameters
        
        self.tableN = tableName  # make into parameters

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global sqliteConnection
        
        if sqliteConnection:
            sqliteConnection.close()
            print("Disconnected from SQLite")

    def construct(self, soup):
        with self:
            # parse data
            table = soup.find("table", {"class": self.tableN})
            rows = []
            
            for row in table.findAll("tr"):
                rows.append(row)
                
            title = []
            for tag in rows[0].findAll("th"):
                title.append(tag.text)
                
            rows.pop(0)
            tableTitle = title[0]
            columnNames = []
            count = 0
            
            for tag in rows[0].findAll("th"):
                if count <= 7:
                    count += 1
                    columnNames.append(tag.text)
            rows.pop(0)
            allData = []
            for row in rows:
                rowData = []
                
                for tag in row.findAll("td")[0:8]:
                    rowData.append(tag.text)
                allData.append(rowData)

            # create SQL queries and insert data
            string = ""
            for i in columnNames:
                if i == columnNames[0]:
                    string += "('{}' INT,".format(i)
                    
                elif i == columnNames[-1]:
                    string += "'{}' DECIMAL)".format(i)
                    
                else:
                    string += "'{}' DECIMAL, ".format(i)
                    
            query = "CREATE TABLE '{}' {}".format(tableTitle, string)
            self.table(query)
            for row in allData:
                query = "INSERT INTO '{}' (".format(tableTitle)
                
                for name in columnNames:
                    
                    if name == columnNames[-1]:
                        query += f"'{name}') VALUES ("
                        
                    else:
                        query += f"'{name}', "
                        
                for cell in row:
                    if cell == row[-1]:
                        
                        query += f"{cell})"
                    else:
                        
                        query += f"{cell}, "
                self.insert(query)
            columnNames.pop(0)
            columnNames.pop(-1)
            return tableTitle, columnNames

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

    def insert(self, query):
        global sqliteConnection
        try:
            cursor = sqliteConnection.cursor()
            cursor.execute(query)
            sqliteConnection.commit()
            
            print("Inserted successfully into table")
            
        except sqlite3.Error as error:
            print("Failed to insert: ", error)

    def search(self, sqliteConnection, query):
        try:
            print(query)
            cursor = sqliteConnection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        
        except sqlite3.Error as error:
            print("Year not found: ", error)


class threads(threading.Thread):
    def __init__(self, dbName, table, colN, rang=[]):
        threading.Thread.__init__(self)
        self.dbName = dbName
        self.table = table
        self.colN = colN
        self.rang = rang
        self._return = None

    def run(self):
        global data
        print("Starting " + self.name)
        threadLock.acquire()
        
        sqliteConnection = sqlite3.connect(self.dbName)  # can't reuse the global connection so create new connection
        dataCol = agent(self.dbName, self.table).getData(sqliteConnection, self.colN, rang=[1990, 2019])
        data.append(dataCol)
        sqliteConnection.close()
        threadLock.release()
        
        print("Exiting " + self.name)


class agent():
    def __init__(self, dbName, table):
        self.dbName = dbName
        self.table = table

    def getData(self, sqliteConnection, column, rang=[]):
        query = self.queryBuilder(column, rang)
        data = databaseService(self.dbName, self.table).search(sqliteConnection, query)
        return data

    def queryBuilder(self, column, rang=[]):
        try:
            if column[-1] == "*":
                column = "[" + column + "]"
                
            if len(rang) == 0:
                query = f"SELECT {column} FROM '{self.table}'"
                
            elif len(rang) == 2:
                rangbeg = rang[0] - 1979
                rangend = rang[1] - 1979
                
                query = f"SELECT Year, {column} FROM '{self.table}' WHERE Year BETWEEN {rang[0]} AND {rang[1]}"
            return query
        except:
            print("There's an error with the range entered.")


class plot():
    def __init__(self, columnNames, data):
        self.colNs = columnNames
        self.data = data
        self.linearRegress()

    def linearRegress(self):
        # Initialise the subplot function using number of rows and columns
        figure, axis = plt.subplots(len(self.data)//3, len(self.data)//2, figsize=(12, 8))

        for ind in range(len(self.data)//2):
            x_val = [x[0] for x in self.data[ind]]
            y_val = [x[1] for x in self.data[ind]]
            axis[0, ind].plot(x_val, y_val)
            axis[0, ind].set_title(self.colNs[ind])
            
        for ind in range(len(self.data)//2):
            x_val = [x[0] for x in self.data[ind+3]]
            y_val = [x[1] for x in self.data[ind+3]]
            axis[1, ind].plot(x_val, y_val)
            axis[1, ind].set_title(self.colNs[ind+3])

        # Combine all the operations and display
        plt.show()


if __name__ == "__main__":
    url = "https://gml.noaa.gov/aggi/aggi.html"
    databaseName = "Lab3.db"
    tableClass = "table table-bordered table-condensed table-striped table-header"
    soup = FileStream(url).openHtmlSite()
    
    with databaseService(databaseName, tableClass) as db_service:
        tableTitle, columnNames = db_service.construct(soup)
        threadLock = threading.Lock()
        threadlist = []
        
        for index in range(len(columnNames)):
            threadlist.insert(index, threads(databaseName, tableTitle, columnNames[index], rang=[1990, 2019]))
        
        for index in range(len(columnNames)):
            threadlist[index].start()
            
        for index in range(len(columnNames)):
            threadlist[index].join()
            
        plot(columnNames, data)