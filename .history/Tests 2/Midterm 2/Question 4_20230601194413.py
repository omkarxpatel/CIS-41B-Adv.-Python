import socket
import pandas as pd
import pickle

# Load the DataFrame from question1
# Replace this code with your DataFrame retrieval logic
import pandas as pd
import requests

response = requests.get("https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt")

if response.status_code == 200:
    data = response.text

    rows = data.split('\n')[51:]
    valid = []

    for row in rows:
        try:
            data = row.split()

            if len(data) == 8:
                valid.append(data)
        except:
            pass

    col = len(valid[0])

    df = pd.DataFrame(valid,columns=["column_" + str(x) for x in range(1, col+1)])

# Start the server
HOST = 'localhost'
PORT = 6000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server listening on {}:{}".format(HOST, PORT))

while True:
    client_socket, addr = server_socket.accept()
    print("Client connected from:", addr)

    df_bytes = pickle.dumps(df)

    # Send the DataFrame bytes to the clientx
    client_socket.sendall(df_bytes)

    # Close the connection
    client_socket.close()
