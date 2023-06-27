import tkinter as tk
from tkinter import messagebox


username = "9mjw6j7712eqyhu54vu5dsag6"
clientID = "fbe9c56baeb24b4e83331867cb867e34"
clientSecret = "20d4c1e7719641ccb02559bedcdbd7b2"
redirectURI = "https://open.spotify.com" 

label = tk.Label(window, text="Enter Playlist Link:")
label.pack()

entry = tk.Entry(window, textvariable=playlist_link)
entry.pack()

button = tk.Button(window, text="Generate Playlist", command=main)
button.pack()

# Start the Tkinter event loop
window.mainloop()