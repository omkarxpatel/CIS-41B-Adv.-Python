import socket
import pickle
from tkinter import Tk, Label

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dataframe = None

    def receive_dataframe(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        df_bytes = b""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            df_bytes += chunk

        self.dataframe = pickle.loads(df_bytes)

        client_socket.close()

    def search_by_key(self, key):
        if self.dataframe is None:
            raise ValueError("No DataFrame available. Please acquire the DataFrame first.")

        if key not in self.dataframe:
            raise KeyError(f"Key '{key}' not found in the DataFrame.")

        return self.dataframe[key]

    def __repr__(self):
        if self.dataframe is None:
            return "No DataFrame available."

        json_data = self.dataframe.to_json(orient="records", sort_keys=True)

        # Use Tkinter to display the JSON string
        root = Tk()
        root.title("DataFrame JSON")
        label = Label(root, text=json_data, justify="left", font=("Arial", 12))
        label.pack(padx=10, pady=10)
        root.mainloop()

        return ""

if __name__ == "__main__":
    client = Client('localhost', 6000)
    client.receive_dataframe()
    print(client)
