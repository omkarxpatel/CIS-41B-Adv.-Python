import tkinter as tk
import csv
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATABASE_NAME = "emissions.db"

def business_layer(statename):
    query = f"SELECT Year, CO2_Emissions FROM tablename WHERE State = ?"
    data = execute_query(query, (statename,))
    graphics(data)

def execute_query(query, params):
    conn = sqlite3.connect(DATABASE_NAME)  # Connect to your database
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

def graphics(data):
    # Plot the graph using matplotlib
    # Replace this code with your actual graph plotting logic
    x = [int(row[0]) for row in data]  # Assuming the first column contains x-values as integers
    y = [float(row[1]) for row in data]  # Assuming the second column contains y-values as floats

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('Year')
    ax.set_ylabel('CO2 Emissions')
    ax.set_title('CO2 Emissions Over Time')

    # Create a Tkinter frame
    frame = tk.Frame(window)
    frame.pack(side=tk.BOTTOM, padx=10, pady=10)

    # Embed the matplotlib figure into the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def generate_graph():
    statename = variable.get()
    business_layer(statename)

# Read the CSV file and extract the states
states = []
with open('Labs/USAStatesCO2.csv', 'r', encoding='latin-1') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        states.append(row[0])  # Assuming the state names are in the first column

# UI using tkinter
window = tk.Tk()
window.title('CO2 Emissions')
variable = tk.StringVar(window)
variable.set(states[0])  # Set the default selected state

# Dropdown menu for state selection
state_dropdown = tk.OptionMenu(window, variable, *states)
state_dropdown.pack()

# Button to generate the graph
generate_button = tk.Button(window, text='Generate Graph', command=generate_graph)
generate_button.pack()

window.mainloop()

