import socket
import pandas as pd
import pickle
from tkinter import Tk, Label
import matplotlib.pyplot as plt

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dataframe = None

    def receive_dataframe(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

        df_bytes = b""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            df_bytes += chunk

        self.dataframe = pickle.loads(df_bytes)

        client.close()

    def convert_to_annual_average(self):
        if self.dataframe is None:
            raise ValueError("No DataFrame available. Please acquire the DataFrame first.")

        self.dataframe['column_2'] = pd.to_numeric(self.dataframe['column_2'], errors='coerce')
        self.dataframe['column_1'] = pd.to_datetime(self.dataframe['column_1'])

        annual_average = self.dataframe.groupby(self.dataframe['column_1'].dt.year)['column_2'].mean()

        return annual_average

    def plot_annual_data(self):
        avg = self.convert_to_annual_average()

        # Extract the decades and corresponding values
        decades = [str(year)[:3] + '0' for year in annual_average.index]
        values = annual_average.values

        # Plot the annual data
        plt.plot(decades, values)
        plt.xlabel('Decades')
        plt.ylabel('Annual Average')
        plt.title('Annual Average CO2 Levels')
        plt.show()

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
    client.plot_annual_data()
