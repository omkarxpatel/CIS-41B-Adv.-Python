import socket  # Import socket module
from tkinter import *
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import sqlite3
import json
import os


class tKinter:
    def __init__(self, countries):
        self.countries = countries
        self.country = self.display()
        
    def display(self):
        master = Tk()
        master.geometry("715x250")
        menu = StringVar()
        menu.set("No Country Selected")
        
        drop = OptionMenu(master, menu, *self.countries)
        drop.pack()
        
        def ok():
            print ("value is: " + menu.get())
            return menu.get()
        
        button = Button(master, text="Submit", command=master.destroy)
        button.pack()
        
        master.mainloop()     
        
        return ok()
    
class graphic():
    def __init__(self, tup, years):
        self.data = tup
        self.years = reversed(years)
        self.xyPlot()

    def xyPlot(self):
        data = []
        years = []
        for i in reversed(self.data):
            if i != self.data[0]:
                data.append(i)
        for j in self.years:
            years.append(j[2:])

        plt.figure(figsize=(12, 6))
        plt.plot(years, data)
        plt.xlabel("Years (1990-2017)")
        plt.ylabel("Values")
        plt.title(self.data[0])
        plt.show()
        

class client:
    def __init__(self, portnumber):
        self.sktClient = socket.socket()             # Create a socket object
        self.host = socket.gethostname()  #Ip address that the TCPServer is there
        print("Printing hostname:", self.host)
        self.port = portnumber   
        self.sktClient.connect((self.host, self.port))   # Reserve a port 
        print("IP address:", self.sktClient.getsockname())

    def GetData(self):
        JSONstring = ""
        
        while True:
            print('receiving data...')
            data = self.sktClient.recv(1024)
            print('data=', (data)) 
            if not data:
                break
            JSONstring += data.decode("utf-8")
            break
        
        string = json.loads(JSONstring)
        return string
    
    def SendData(self, json):
        while True:
            
            message = json.encode('UTF-8')  #send data
            print('sending {!r}'.format(json))
            
            self.sktClient.send(message)
            print('Done sending')
            break

    
if __name__ == "__main__":
    cli = client(3262)
    countries = cli.GetData()
    country = tKinter(countries).country
    cli.SendData(json.dumps(country))
    country_data = cli.GetData()
    years = cli.GetData()
    graphic(country_data, years)