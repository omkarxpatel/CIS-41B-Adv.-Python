import socket
import pandas as pd
from io import StringIO

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dataframe = None

    def send_query(self, query):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        client.send(query.encode())

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
    client = Client('localhost', 6000)
    query = "SELECT * FROM CO2_Data"
    client.send_query(query)
    print(client)  # Convert DataFrame to JSON string and print