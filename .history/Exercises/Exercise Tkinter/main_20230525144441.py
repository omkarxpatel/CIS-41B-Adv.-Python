import tkinter as tk
from tkinter import messagebox
import os
import time
import random
import string
import spotipy
import spotipy.util as util
from colorama import Fore as fore

window = tk.Tk()
window.title("Playlist Generator")
window.geometry("300x150")

playlist_link = tk.StringVar()


def convert_code():
    # Place your converted code here

    def playlist_generator():
        # Convert the playlist generation logic
        playlist_url = playlist_link.get()
        # Rest of the code...

        # Replace print statements with messagebox
        messagebox.showinfo("Playlist Generated", f"Generated playlist: {generated_name}\nPlaylist URL: {gen_playlist['external_urls']['spotify']}")


def raise_error(error):
    messagebox.showerror("Error", error)


# Tkinter GUI elements
label = tk.Label(window, text="Enter Playlist Link:")
label.pack()

entry = tk.Entry(window, textvariable=playlist_link)
entry.pack()

button = tk.Button(window, text="Generate Playlist", command=convert_code)
button.pack()

# Start the Tkinter event loop
window.mainloop()
