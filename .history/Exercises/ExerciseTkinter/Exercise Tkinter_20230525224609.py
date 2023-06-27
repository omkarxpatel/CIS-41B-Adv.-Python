"""
Note TO POFESSOR

I have a few user tokens/secrets which I have to use to run this program as it collborates with the spotify api. I dont feel comfortable
sharing these. But, if you do happen to be needing a video for grading/showing the class (hopefully), I am happy to provide that for you.
Thank you
"""

import tkinter as tk
from Spotify import start_gen



window = tk.Tk()
window.title("Playlist Generator")
window.geometry("1000x500")

playlist_link = tk.StringVar()


label = tk.Label(window, text="Enter Playlist Link:")
label.pack()

entry = tk.Entry(window, textvariable=playlist_link)
entry.pack()

def main():
    global label, button
    
    val = playlist_link.get()
    if val:
        
        button["state"] = "disabled"
        label["text"] = "generating playlist, check console for info..."
        
        window.update()
        
        start_gen(val)
        label["text"] = "playlist complete, rerun the program to try again"
        
        window.update()
        
button = tk.Button(window, text="Generate Playlist", command=main)
button.pack()

# Start the Tkinter event loop
window.mainloop()