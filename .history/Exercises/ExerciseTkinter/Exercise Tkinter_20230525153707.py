import tkinter as tk
from tkinter import messagebox
import ExerciseTkinter.Spotify.generate_similar_playlist

username = "9mjw6j7712eqyhu54vu5dsag6"
clientID = "fbe9c56baeb24b4e83331867cb867e34"
clientSecret = "20d4c1e7719641ccb02559bedcdbd7b2"
redirectURI = "https://open.spotify.com" 


window = tk.Tk()
window.title("Playlist Generator")
window.geometry("1000x500")

playlist_link = tk.StringVar()


label = tk.Label(window, text="Enter Playlist Link:")
label.pack()

entry = tk.Entry(window, textvariable=playlist_link)
entry.pack()

button = tk.Button(window, text="Generate Playlist", command=generate_similar_playlist)
button.pack()

# Start the Tkinter event loop
window.mainloop()