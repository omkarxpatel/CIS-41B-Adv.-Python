import socket
import pandas as pd
import tkinter as tk
from io import StringIO

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.json_string = ""

    def send_query(self, query):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        client_socket.send(query.encode())

        result = client_socket.recv(15890).decode()

        client_socket.close()

        df = pd.read_csv(StringIO(result), sep=",")
        self.json_string = df.to_json(orient="records", sort_keys=True)

    def __call__(self):
        root = tk.Tk()
        text = tk.Text(root)
        text.insert(tk.END, self.json_string)
        text.pack()
        root.mainloop()

if __name__ == "__main__":
    client = Client('localhost', 6000)
    query = "SELECT * FROM CO2_Data"
    client.send_query(query)
    client()