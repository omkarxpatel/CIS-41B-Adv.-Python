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
       # Create a socket
       server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

       try:
           # Bind the socket to the specified host and port
           server_socket.bind((self.host, self.port))

           # Listen for incoming connections
           server_socket.listen(1)
           print(f"Server started and listening on {self.host}:{self.port}")

           while True:
               # Accept a client connection
               client_socket, address = server_socket.accept()
               print(f"Accepted connection from {address[0]}:{address[1]}")

               # Handle the client request
               self.handle_client(client_socket)

       finally:
           server_socket.close()

   def handle_client(self, client_socket):
       # Receive the query from the client
       query = client_socket.recv(4096).decode()
       print("Received query:", query)

       # Execute the query and send the result back to the client
       result = self.database.execute_query(query)
       result_str = "\n".join([",".join(map(str, row)) for row in result])
       client_socket.send(result_str.encode())

       # Close the client socket
       client_socket.close()

   def process_data(self, filename):
       try:
           # Read the CSV file
           df = pd.read_csv(filename, skiprows=2, nrows=52)
           df = df.iloc[:, :56]
           print(df)

           # Create the table in the database
           table_name = "CO2_Data"  # Updated table name
           columns = df.shape[1]  # Get the number of columns from the DataFrame
           self.database.create_table(table_name, columns)  # Pass the integer value for columns

           # Insert the data into the table
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

# Example usage
server = Server("localhost", 6000, "Lab1.db")
server.database.connect()
server.process_data("USAStatesCO2.csv")
server.start()
server.close()

Exercise Client:
import socket
import pandas as pd
from io import StringIO

class Client:
   def __init__(self, host, port):
       self.host = host
       self.port = port

   def send_query(self, query):
       # Create a socket connection to the server
       client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       client_socket.connect((self.host, self.port))

       # Send the query to the server
       client_socket.send(query.encode())

       # Receive the result from the server
       result = client_socket.recv(15890).decode()

       # Close the client socket
       client_socket.close()

       # Convert the received string to a DataFrame
       df = pd.read_csv(StringIO(result), sep=",")
       return df

if __name__ == "__main__":
   client = Client('localhost', 6000)
   query = "SELECT * FROM CO2_Data"
   result_df = client.send_query(query)
   print(result_df)

