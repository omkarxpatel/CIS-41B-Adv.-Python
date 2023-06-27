import tkinter as tk
import matplotlib.pyplot as plt
import csv

class Server:
    def __init__(self, data_file):
        self.data = self.load_data(data_file)
    
    def load_data(self, data_file):
        with open(data_file, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        return data

class Client:
    def __init__(self, server):
        self.server = server
        self.selected_state = None
    
    def select_state(self, state):
        self.selected_state = state
    
    def request_data(self):
        if self.selected_state:
            data = self.server.data
            header = data[0]
            state_index = header.index('State')
            year_indices = [i for i, item in enumerate(header) if item.isdigit()]
            
            years = []
            datapoints = []
            for row in data:
                if row[state_index] == self.selected_state:
                    years = [int(row[i]) for i in year_indices]
                    datapoints = [float(row[i]) for i in year_indices]
                    break
            
            return years, datapoints
        
        return [], []

class GraphicLayer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
    
    def plot_data(self, years, datapoints):
        self.ax.plot(years, datapoints)
        plt.show()

class BusinessLayer:
    def __init__(self, client, graphic_layer):
        self.client = client
        self.graphic_layer = graphic_layer
    
    def process_request(self):
        years, datapoints = self.client.request_data()
        self.graphic_layer.plot_data(years, datapoints)

class UserLayer:
    def __init__(self, business_layer):
        self.business_layer = business_layer
        
        self.root = tk.Tk()
        self.root.title('CO2 Data')
        
        self.state_var = tk.StringVar()
        
        self.state_label = tk.Label(self.root, text='Select a state:')
        self.state_label.pack()
        
        self.state_entry = tk.Entry(self.root, textvariable=self.state_var)
        self.state_entry.pack()
        
        self.submit_button = tk.Button(self.root, text='Submit', command=self.submit_state)
        self.submit_button.pack()
        
        self.root.mainloop()
    
    def submit_state(self):
        state = self.state_var.get()
        self.business_layer.client.select_state(state)
        self.business_layer.process_request()

# Main script
server = Server('USAStatesCo2.csv')
client = Client(server)
graphic_layer = GraphicLayer()
business_layer = BusinessLayer(client, graphic_layer)
user_layer = UserLayer(business_layer)
