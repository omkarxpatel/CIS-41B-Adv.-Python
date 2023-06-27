import tkinter as tk
from tkinter import messagebox

import os
import time
import random
import string
import spotipy
import spotipy.util as util
from colorama import Fore as fore


username = "9mjw6j7712eqyhu54vu5dsag6"
clientID = "fbe9c56baeb24b4e83331867cb867e34"
clientSecret = "20d4c1e7719641ccb02559bedcdbd7b2"
redirectURI = "https://open.spotify.com" 
    
    
window = tk.Tk()
window.title("Playlist Generator")
window.geometry("1000x150")

playlist_link = tk.StringVar()



not_completed = "❌"
completed = "✅"
working = "⏳"

topbot = "--------------------------------------------"
step1 = f"| {not_completed} | Extracting songs         |          |"
step2 = f"| {not_completed} | Extracting song-ids      |          |"
step3 = f"| {not_completed} | Generating songs         |          |"
step4 = f"| {not_completed} | Adding songs             |          |"
step5 = f"| {not_completed} | Playlist finished        |          |"


def checklist_helper(task):
    task = int(task)
    taskTime = round(time.time() - task, 2)
    spacing = " " * (6 - len(str(taskTime)))

    return [taskTime, spacing]


def checklist(step, working_bool=None, task=None):
    clear(0)
    global step1, step2, step3, step4, step5

    value = completed
    if working_bool == True:
        value = working

    if step == 1:
        if task:
            val = checklist_helper(task)
            step1 = f"| {value} | Extracting songs         | ({val[0]}s){val[1]}|"

    elif step == 2:
        if task:
            val = checklist_helper(task)
            step2 = f"| {value} | Extracting song-ids      | ({val[0]}s){val[1]}|"

    elif step == 3:
        if task:
            val = checklist_helper(task)
            step3 = f"| {value} | Generating songs         | ({val[0]}s){val[1]}|"

    elif step == 4:
        if task:
            val = checklist_helper(task)
            step4 = f"| {value} | Adding songs             | ({val[0]}s){val[1]}|"

    elif step == 5:
        if task:
            val = checklist_helper(task)
            step5 = f"| {value} | Playlist finished        | ({val[0]}s){val[1]}|"

    msgbox = f"{topbot}\n{step1}\n{step2}\n{step3}\n{step4}\n{step5}\n{topbot}"
    messagebox.showinfo(msgbox)


def roundPlaylistLen(val):
    return (val + (20 - val % 20)) / 4


def isvalid(option, min, max):
    return min <= option <= max


def raiseError(error):
    print(f"{fore.RED}Error: {fore.RESET}{error}")


def clear(val):
    if val != 0:
        time.sleep(val)
    os.system("clear")
    
#########################
#   GENERATE PLAYLIST   #
#########################


def convert_code():
    try:
        auth = spotipy.SpotifyOAuth(clientID, clientSecret, redirectURI)
        token_info = auth.get_cached_token()
        if not token_info:
            auth_url = auth.get_authorize_url()
            messagebox.showinfo("Authentication Required", "Please authorize the application to access your Spotify account.")
            
            auth_token = input("Enter the authorization token: ")  # Prompt the user to enter the authorization token
            token_info = auth.get_access_token(auth_token)

        spotifyObject = spotipy.Spotify(auth=token_info["access_token"])

        playlist_url = playlist_link.get()

        if playlist_url.strip() != "":
            playlist_generator(spotifyObject, playlist_url)
    except spotipy.SpotifyException as e:
        messagebox.showerror("Spotify API Error", str(e))

def playlist_generator(spotifyObject, playlist_url):
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


    # Replace print statements with messagebox
    messagebox.showinfo("Playlist Generated", f"Generated playlist: {generated_name}\nPlaylist URL: {gen_playlist['external_urls']['spotify']}")

def main():
    vals = convert_code()
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