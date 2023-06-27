import pickle
import pandas as pd
import os
import sqlite3




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
    
html_data = pd.read_html("Files/Co2.html", header=2)
htmlDf = html_data[0].groupby('year')['average'].mean().round(2)
htmlDf = pd.DataFrame(htmlDf)

csvDF = pd.read_csv("Files/SeaLevel.csv", skiprows=3)
csvDF['year'] = csvDF['year'].astype(int)

csvDf = csvDF.groupby("year")['TOPEX/Poseidon'].mean().round(2)
csvDf = pd.DataFrame(csvDf)

database = "Lab1_.db"
db = Database(database)
colandType = {'year': 'INTEGER', 'average': "REAL"}

db.table(db.query_builder("SeaLevel", "TABLE", colandType))
db.insert(db.query_builder("SeaLevel", "INSERT", colandType), csvDf)
cursor = sqliteConnection.cursor()

cursor.execute("SELECT * FROM SeaLevel")
lod = cursor.fetchall()

print("NOAA Mean Sea Level Rise:\n\nYear:   Average:")
for item in lod:
    print(f"{item[0]}:   {item[1]}")

db.table(db.query_builder("CO2", "TABLE", colandType))
insertQ = db.query_builder("CO2", "INSERT", colandType)
db.insert(insertQ, htmlDf)

cursor.execute("SELECT * FROM CO2")
lod = cursor.fetchall()
print("\n\n")
print("Total Carbon Emissions:\n\nYear:   Average:")

for item in lod:
    print(f"{item[0]}:   {item[1]}")

sqliteConnection.close()

try:
    os.remove(database)
except:
    raise FileNotFoundError(f"Could not find path: {database}")


# Create a database object
db = Database(database='midterm1')

# Create a QueryBuilder object
qb = QueryBuilder()

# Create a collection of GreenhouseGasData objects
collection = [
    GreenhouseGasData('USA', 'CA', '2010', 1000, 500, 200),
    GreenhouseGasData('USA', 'CA', '2011', 1100, 550, 250),
    GreenhouseGasData('USA', 'CA', '2012', 1200, 600, 300),
    GreenhouseGasData('USA', 'NY', '2010', 900, 450, 150),
    GreenhouseGasData('USA', 'NY', '2011', 950, 500, 175),
    GreenhouseGasData('USA', 'NY', '2012', 1000, 550, 200),
]

# Create a pandas DataFrame from the data.
df = pd.DataFrame.from_records(collection, columns=GreenhouseGasData.__dict__.keys())

# Convert the DataFrame to bytes.
byte_stream = pickle.dumps(df)

# Insert the byte stream into the database.
table_name = 'GreenhouseGasData'
columns = ['data']
query = qb.build_insert_query(table_name, columns)
db.execute(query, (byte_stream,))

# Select the data from the database.
query = qb.build_select_query(table_name, columns)
result = db.execute(query)

# Convert the byte stream back to a DataFrame.
result_df = pickle.loads(result[0][0])

# Print the data.
print(result_df)
