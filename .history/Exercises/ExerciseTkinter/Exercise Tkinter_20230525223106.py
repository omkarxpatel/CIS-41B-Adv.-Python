import tkinter as tk
from Spotify import main



window = tk.Tk()
window.title("Playlist Generator")
window.geometry("1000x500")

playlist_link = tk.StringVar()


label = tk.Label(window, text="Enter Playlist Link:")
label.pack()

entry = tk.Entry(window, textvariable=playlist_link)
entry.pack()

def main():
    val = playlist_link.get()
    if val:
    start_gen()

button = tk.Button(window, text="Generate Playlist", command=main(playlist_link.get()))
button.pack()

# Start the Tkinter event loop
window.mainloop()