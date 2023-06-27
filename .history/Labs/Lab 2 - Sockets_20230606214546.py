import tkinter as tk
import csv
import matplotlib.pyplot as plt
import sqlite3

DATABASE_NAME = 'your_database.db'  # Replace with your actual database name

def business_layer(statename):
    query = f"SELECT Year, CO2_Emissions FROM tablename WHERE State = '{statename}'"
    data = execute_query(query)
    graphics(data)

def execute_query(query):
    conn = sqlite3.connect(DATABASE_NAME)  # Connect to your database
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def graphics(data):
    x = [row[0] for row in data]
    y = [row[1] for row in data]

    plt.plot(x, y)
    plt.xlabel('Year')
    plt.ylabel('CO2 Emissions')
    plt.title('CO2 Emissions Over Time')
    plt.show()

def generate_graph():
    statename = variable.get()
    business_layer(statename)

states = []
with open('Labs/USAStatesCO2.csv', 'r', encoding='latin-1') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        states.append(row[0])

window = tk.Tk()
window.title('CO2 Emissions')
variable = tk.StringVar(window)
variable.set(states[0])

state_dropdown = tk.OptionMenu(window, variable, *states)
state_dropdown.pack()

generate_button = tk.Button(window, text='Generate Graph', command=generate_graph)
generate_button.pack()

window.mainloop()
