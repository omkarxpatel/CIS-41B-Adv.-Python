import tkinter as tk
import matplotlib.pyplot as plt
import socket
import json
import csv

# User Layer
class UserInterface:
    def __init__(self):
        self.root = tk.Tk() #initaite thkineter
        self.root.title("Data Visualization") 
        
        self.country_label = tk.Label(self.root, text="Select a country:") # text to prompt the user
        self.country_label.pack()
        
        self.country_entry = tk.Entry(self.root) # text box to allow user to enter state
        self.country_entry.pack()
        
        self.plot_button = tk.Button(self.root, text="Plot", command=self.plot_data) #
        self.plot_button.pack()
        
    def plot_data(self):
        country = self.country_entry.get()
        BusinessLayer().process_request(country)
        
    def run(self):
        self.root.mainloop()

# Business Layer
class BusinessLayer:
    def process_request(self, country):
        query = f"SELECT * FROM data WHERE country = '{country}' AND year BETWEEN 1970 AND 2020"
        data = DataLayer().execute_query(query)
        GraphicLayer().plot_data(data)


class DataLayer:
    def execute_query(self, query):
        data = {
            "year": [],
            "co2_level": []
        }
        
        country = query.split("'")[1]  # Extract the country name from the query
        
        with open("Labs/USAStatesCo2.csv", "r", encoding="iso-8859-1") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the descriptive line
            next(csv_reader)  # Skip the header row
            for line in csv_reader:
                year = int(line[0])
                co2_level = float(line[1])
                if line[2] == country and 1970 <= year <= 2020:  # Filter by country and year range
                    data["year"].append(year)
                    data["co2_level"].append(co2_level)
        
        return data


# Graphic Layer
class GraphicLayer:
    def plot_data(self, data):
        plt.plot(data["year"], data["co2_level"])
        plt.xlabel("Year")
        plt.ylabel("CO2 Level")
        plt.title("CO2 Emissions Over Time")
        plt.show()

# Server Layer (Exercise server)
class Server:
    def __init__(self):
        self.host = "localhost"
        self.port = 1234
        
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print("Server listening on {}:{}".format(self.host, self.port))
            
            while True:
                client_socket, address = server_socket.accept()
                print("Connection from:", address)
                
                query = client_socket.recv(1024).decode()
                data = DataLayer().execute_query(query)
                response = json.dumps(data)
                
                client_socket.sendall(response.encode())
                client_socket.close()

# Client Socket (Exercise client)
class Client:
    def __init__(self):
        self.host = "localhost"
        self.port = 1234
        
    def request_data(self, query):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(query.encode())
            
            response = client_socket.recv(1024).decode()
            data = json.loads(response)
            
            return data

# Start the application
if __name__ == "__main__":
    server = Server()
    user_interface = UserInterface()
    user_interface.run()
