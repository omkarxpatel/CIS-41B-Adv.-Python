import pickle
import sqlite3
import pandas as pd

# Define a class to store greenhouse gas data.
class GreenhouseGasData:
    def __init__(self, country, year, emissions):
        self.country = country
        self.year = year
        self.emissions = emissions

    def __repr__(self):
        return f"GreenhouseGasData(country={self.country}, year={self.year}, emissions={self.emissions})"

# Define a class to interact with a SQLite database.
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        column_defs = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
        query = f"CREATE TABLE {table_name} ({column_defs})"
        self.cursor.execute(query)

    def insert(self, table_name, values):
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def close(self):
        self.conn.close()

# Define a class to build SQL queries.
class QueryBuilder:
    @staticmethod
    def build_insert_query(table_name, byte_stream):
        return f"INSERT INTO {table_name} (data) VALUES (?)", (byte_stream,)

# Create some GreenhouseGasData objects and store them in a collection.
collection = [
    GreenhouseGasData("China", 2020, 10000),
    GreenhouseGasData("United States", 2020, 5000),
    GreenhouseGasData("India", 2020, 3000)
]

# Create a pandas DataFrame from the data.
df = pd.DataFrame.from_records(collection, columns=GreenhouseGasData.__dict__.keys())

# Convert the DataFrame to bytes.
byte_stream = pickle.dumps(df)

# Create a Database object and insert the byte stream into it.
db = Database("example.db")
db.create_table("greenhouse_gas_data", {"data": "BLOB"})
db.insert("greenhouse_gas_data", (byte_stream,))
db.close()

# Build the SQL query for the byte stream insertion using the QueryBuilder.
insert_query, insert_values = QueryBuilder.build_insert_query("greenhouse_gas_data", byte_stream)

# Print the SQL query and values for debugging.
print(insert_query)
print(insert_values)
