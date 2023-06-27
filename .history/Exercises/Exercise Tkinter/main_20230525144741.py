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







#########################
#   GENERATE PLAYLIST   #
#########################


def generate_similar_playlist(spotifyObject, playlist_url):
    tasktime = time.time()

    checklist(0, task=tasktime)
    checklist(1, True)
    onetime = time.time()

    playlist_id = playlist_url.split("/")[-1]
    playlist = spotifyObject.playlist(playlist_id)

    song_names = []
    tracks = playlist["tracks"]

    for z in range(len(tracks["items"])):
        item = tracks["items"][z]
        song_names.append(item["track"]["name"])

        checklist(1, True, task=tasktime)

    checklist(1, task=onetime)
    checklist(2, True)
    twotime = time.time()

    song_ids = []
    total_songs = []

    for z in range(len(song_names)):
        item = song_names[z]
        result = spotifyObject.search(q=item, type="track")
        song_id = result["tracks"]["items"][0]["id"]

        song_ids.append(song_id)
        checklist(2, True, task=twotime)

    checklist(2, task=twotime)
    checklist(3, True)
    threetime = time.time()

    for _ in range(int(roundPlaylistLen(len(song_ids)) / 4)):
        recommendations = spotifyObject.recommendations(
            limit=20, seed_tracks=random.sample(song_ids, 5)
        )

        for y in range(len(recommendations["tracks"])):
            song = recommendations["tracks"][y]["name"]
            song_uri = recommendations["tracks"][y]["uri"]

            value = f"{song}:{song_uri}"
            total_songs.append(value)
            checklist(3, True, task=threetime)

    scope = "playlist-modify-public playlist-modify-private"
    token = util.prompt_for_user_token(
        username,
        scope,
        client_id=clientID,
        client_secret=clientSecret,
        redirect_uri=redirectURI,
    )
    sp = spotipy.Spotify(auth=token)

    generated_name = "".join(random.choices(string.ascii_letters, k=10))
    gen_playlist = sp.user_playlist_create(username, name=generated_name)
    gen_playlist_id = gen_playlist["id"]

    checklist(3, task=threetime)
    checklist(4, True)
    fourtime = time.time()

    for item in total_songs:
        item = item.split(":")

        sp.user_playlist_add_tracks(username, gen_playlist_id, [item[-1]])
        checklist(4, True, task=fourtime)

    checklist(4, task=fourtime)
    checklist(5, True)

    time.sleep(1)
    checklist(5, task=tasktime)

    print(f"Generated playlist: {generated_name}")
    print(f"Playlist URL: {gen_playlist['external_urls']['spotify']}")
