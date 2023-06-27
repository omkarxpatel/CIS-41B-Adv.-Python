import socket
import pandas as pd
from io import StringIO

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dataframe = None

    def send_query(self, query):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

        client.send(query.encode())

        result = client.recv(15890).decode()

        client.close()

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

        data = self.dataframe.to_json(orient="records", sort_keys=True)
        return data

    def __repr__(self):
        return f"Client(host='{self.host}', port={self.port})"

    def __len__(self):
        if self.dataframe is None:
            return 0

        return len(self.dataframe)

    def __getitem__(self, key):
        if self.dataframe is None:
            raise ValueError("No DataFrame available. Please acquire the DataFrame first.")

        return self.dataframe[key]

    def __iter__(self):
        if self.dataframe is None:
            raise ValueError("No DataFrame available. Please acquire the DataFrame first.")

        return iter(self.dataframe)

if __name__ == "__main__":
    client = Client('localhost', 6000)
    query = "SELECT * FROM CO2_Data"
    client.send_query(query)

    print(client)  # Convert DataFrame to JSON string and print
    print(len(client))  # Get the number of rows in the DataFrame
    print(client['column_name'])  # Access a column in the DataFrame
    for row in client:  # Iterate over the DataFrame rows
        print(row)
