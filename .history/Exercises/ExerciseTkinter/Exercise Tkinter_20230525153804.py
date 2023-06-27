import tkinter as tk
from ExerciseTkinter.Spotify import generate_similar_playlist



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