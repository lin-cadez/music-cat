import csv
import os
import re
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# load credentials from .env file
load_dotenv()

CLIENT_ID = 'aaaf9c6454bf40ab96f2a3314eb60856'
CLIENT_SECRET = '22c83fc9bf1748078a3b07bce05ad4cc'
OUTPUT_FILE_NAME = "anthems.csv"
OUTPUT_FILE_NAME="src/"+OUTPUT_FILE_NAME

# change for your target playlist
PLAYLIST_LINK = "https://open.spotify.com/playlist/4lhWxULgawAPOEgAkClW0b?si=2c6b8123bffc49cf"

# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get uri from https link
if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# get list of tracks in a given playlist (note: max playlist length 100)
tracks = session.playlist_tracks(playlist_uri)["items"]

with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
	pass
file.close()

# create csv file
with open(OUTPUT_FILE_NAME, "a", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # write header column names
    writer.writerow(["track", "artist"])

    # extract name and artist
    for track in tracks:
        name = track["track"]["name"]
        artists = ", ".join(
            [artist["name"] for artist in track["track"]["artists"]]
        )

        # write to csv
        writer.writerow([name, artists])


data = []

with open(OUTPUT_FILE_NAME, 'r', encoding="utf-8") as file:
  csvreader = csv.reader(file, delimiter=',')

  for row in csvreader:
    if row!=[]:
      title=row[0]
      try:
        author=row[1]
      except:
        row=str(row).replace("[", "").replace("]", "").strip().replace('"', "").lstrip("'")
        title=row.split(",")[0]
        author=row.split(",")[1]
      data.append(f"{title},{author}")


print(data)


with open(OUTPUT_FILE_NAME, 'w', encoding="utf-8") as file:
  # Create a CSV writer
  csvwriter = csv.writer(file)

  # Write each element in data as a new line in the file
  for row in data:
    csvwriter.writerow([row])
