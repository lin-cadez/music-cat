import os
import csv
import pytube
from youtubesearchpython import Search
import re
import spotipy
import json
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


def song_dl(title):

    #print(title)
    song=title+".mp3"
    song_out=title+".wav"
    cwd=os.getcwd()
    cwd_song=cwd+"\\"+song
    cwd_song_new=cwd+"\\"+song_out
    if os.path.exists(cwd_song_new):
        return cwd_song_new
    else:
        try:
            url = Search(title, limit = 1)
            url=url.result()["result"][0]["link"]
            
            yt = pytube.YouTube(url).streams.filter(only_audio=True)[0]
          
            a=yt.download(filename=cwd_song)
        except:
            print("track: ", title, "wasnt downloaded because of reasons")

        return cwd_song_new


with open('creds.json') as f:
    creds = json.load(f)


CLIENT_ID = creds["CLIENT_ID"]
CLIENT_SECRET = creds["CLIENT_SECRET"]

print(CLIENT_ID)
print(CLIENT_SECRET)

data = []

print("dobrodošel v spotify prenosniku  :-)")
PLAYLIST_LINK = input("ime playlist: ")
#PLAYLIST_LINK="https://open.spotify.com/playlist/5ITggBAGBS8x745G8aVzgH?si=c0d636672236467d"

# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get uri from https link
if PLAYLIST_LINK.startswith("https://open.spotify.com/playlist/"):
    playlist_uri = PLAYLIST_LINK.split("playlist/")[1]
    playlist_uri = playlist_uri.split("?")[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# get list of tracks in a given playlist (note: max playlist length 100)
tracks = session.playlist_tracks(playlist_uri)["items"]



for index, track in enumerate(tracks):
  name = track["track"]["name"] +" "+ track["track"]["artists"][0]["name"]
  print(name)
  song_dl(name)

  print("-------------------")
  print("sam še", len(tracks)-(index+1), "trackov")
  
  

  
print("-------------------")
print("naloženo")     





