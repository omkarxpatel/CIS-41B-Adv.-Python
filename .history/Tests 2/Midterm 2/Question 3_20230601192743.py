import socket
import pandas as pd
import json
from io import StringIO

class DataFrameProcessor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dataframe = None

    def acquire_dataframe(self, query):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        client_socket.send(query.encode())

        result = client_socket.recv(15890).decode()

        client_socket.close()

        self.dataframe = pd.read_csv(StringIO(result), sep=",")

    def search_by_key(self, key):
        if self.dataframe is None:
            raise ValueError("No DataFrame available. Please acquire the DataFrame first.")

        if key not in self.dataframe:
            raise KeyError(f"Key '{key}' not found in the DataFrame.")

        return self.dataframe[key]

    def __str__(self):
        if self.dataframe is None:
            return "No DataFrame available."

        json_data = self.dataframe.to_json(orient="records", sort_keys=True)
        return json_data

if __name__ == "__main__":
    client = DataFrameProcessor('localhost', 6000)
    query = "SELECT * FROM CO2_Data"
    client.acquire_dataframe(query)
    print(client.dataframe)  # DataFrame object
    print(client.search_by_key('column_name'))  # Replace 'column_name' with the actual key
    print(str(client))  # JSON string representation
