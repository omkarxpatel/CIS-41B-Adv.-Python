import pickle
import pandas as pd
import os

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
