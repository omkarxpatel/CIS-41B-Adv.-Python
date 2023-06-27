import tkinter as tk
from tkinter import messagebox
from colorama import Fore as fore



    
#########################
#   GENERATE PLAYLIST   #
#########################
def main():
    vals = get_info()
    playlist_generator(vals[0],vals[1])

# Tkinter GUI elements
label = tk.Label(window, text="Enter Playlist Link:")
label.pack()

entry = tk.Entry(window, textvariable=playlist_link)
entry.pack()

button = tk.Button(window, text="Generate Playlist", command=main)
button.pack()

# Start the Tkinter event loop
window.mainloop()