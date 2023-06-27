import tkinter as tk
import csv
import matplotlib.pyplot as plt

def business_layer(statename):
    # Construct your SQL query here and retrieve data from the database
    # Replace this code with your actual implementation
    query = f"SELECT * FROM tablename WHERE State = '{statename}'"
    # Execute the query and retrieve the data
    data = execute_query(query)
    # Pass the data to the graphics layer for plotting
    graphics(data)

def execute_query(query):
    # Execute your SQL query and retrieve the data
    # Replace this code with your actual implementation
    # You can use libraries like sqlite3 or SQLAlchemy for database operations
    data = []  # Placeholder for retrieved data
    return data

def graphics(data):
    # Plot the graph using matplotlib
    # Replace this code with your actual graph plotting logic
    x = [row[0] for row in data]  # Assuming the first column contains x-values
    y = [row[1] for row in data]  # Assuming the second column contains y-values

    plt.plot(x, y)
    plt.xlabel('Year')
    plt.ylabel('CO2 Emissions')
    plt.title('CO2 Emissions Over Time')
    plt.show()

def generate_graph():
    statename = variable.get()
    business_layer(statename)

# Read the CSV file and extract the states
states = []
with open('file.csv', 'r', encoding='latin-1') as csv_file:
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
