import tkinter as tk
from tkinter import ttk
import sqlite3
import json
import matplotlib.pyplot as plt

# Data Layer
class DataLayer:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        return json.dumps(data)

# Business Layer
class BusinessLayer:
    def __init__(self, data_layer):
        self.data_layer = data_layer

    def get_country_data(self, country):
        query = f"SELECT * FROM emissions WHERE State = '{country}'"
        data = self.data_layer.execute_query(query)
        return data

# Graphic Layer
class GraphicLayer:
    def plot_data(self, data):
        years = [str(year) for year in range(1970, 2021)]
        emissions = [float(data[year]) for year in years]

        plt.plot(years, emissions)
        plt.xlabel('Year')
        plt.ylabel('CO2 Emissions (million metric tons)')
        plt.title('CO2 Emissions Over Time')
        plt.show()

# User Layer
class UserInterface:
    def __init__(self, business_layer):
        self.business_layer = business_layer

        self.window = tk.Tk()
        self.window.title("CO2 Emissions")
        self.combo_box = ttk.Combobox(self.window)
        self.combo_box.bind("<<ComboboxSelected>>", self.get_country_data)
        self.combo_box.pack()

    def run(self):
        countries = self.get_country_list()
        self.combo_box['values'] = countries
        self.window.mainloop()

    def get_country_list(self):
        query = "SELECT DISTINCT State FROM emissions"
        data = self.business_layer.data_layer.execute_query(query)
        countries = [row['State'] for row in json.loads(data)]
        return countries

    def get_country_data(self, event):
        country = self.combo_box.get()
        data = self.business_layer.get_country_data(country)
        self.plot_data(data)

    def plot_data(self, data):
        graphic_layer = GraphicLayer()
        graphic_layer.plot_data(json.loads(data))

# Server Layer (Dummy implementation using SQLite database)
class ServerLayer:
    def __init__(self, data_layer):
        self.data_layer = data_layer

    def start(self):
        self.data_layer.conn.close()

# Create and populate SQLite database
def create_database(filename):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS emissions")
    cursor.execute("CREATE TABLE emissions (State TEXT, " +
                   ", ".join([f"_{year} REAL" for year in range(1970, 2021)]) +
                   ")")

    with open("USAStatesCO2.csv") as file:
        lines = file.readlines()

    for i, line in enumerate(lines[3:]):
        values = line.strip().split(",")
        state = values[0].strip()
        emissions = [float(value.strip()) if value.strip() != '' else None for value in values[1:]]
        cursor.execute(f"INSERT INTO emissions VALUES ('{state}', " +
                       ", ".join([str(emission) if emission is not None else 'NULL', because the response exceeded the maximum length.
