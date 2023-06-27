import tkinter as tk
from tkinter import messagebox

import os
import time
import random
import string
import spotipy
import spotipy.util as util
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