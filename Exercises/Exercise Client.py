
import socket
import pandas as pd
from io import StringIO

class Client:
   def __init__(self, host, port):
       self.host = host
       self.port = port

   def send_query(self, query):
       client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       client_socket.connect((self.host, self.port))

       client_socket.send(query.encode())

       result = client_socket.recv(15890).decode()

       client_socket.close()

       df = pd.read_csv(StringIO(result), sep=",")
       return df

if __name__ == "__main__":
   client = Client('localhost', 6000)
   query = "SELECT * FROM CO2_Data"
   result_df = client.send_query(query)
   print(result_df)

