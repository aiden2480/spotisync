import os
import spotipy
from mutagen.easyid3 import EasyID3
from spotipy.oauth2 import SpotifyClientCredentials


URI = input("Enter playlist URI: ")
LOCATION = input("Enter parent folder path: ")

# Set up spotipy client
creds = SpotifyClientCredentials(
    "5f573c9620494bae87890c0f08a60293",
    "212476d9b0f3472eaa762d90b19b0ba8",
)
spotify = spotipy.Spotify(client_credentials_manager=creds)

# Grab playlist data
pdata = spotify.playlist(URI)
tracks = pdata["tracks"]["items"]
splist = list()
for i in tracks:
    title = i["track"]["name"]
    artists = [o["name"] for o in i["track"]["artists"]]
    splist.append(f"{title} - {'/'.join(artists)}")

# Determine which files have already been downloaded locally
lplist = list()
local_filenames = [f for f in os.listdir(LOCATION) if f.endswith(".mp3")]

for file in local_filenames:
    audio = EasyID3(f"{LOCATION}\\{file}")
    lplist.append(f"{audio['title'][0]} - {audio['artist'][0]}")

# Compare spotify playlist with local one
not_downloaded = [p for p in splist if p not in lplist]
deleted = [p for p in lplist if p not in splist]

print("Not downloaded from spotify")
for p in not_downloaded:
    print(f" - {p}")
if not not_downloaded:
    print(" - None")
print()

print("Deleted but still on local machine")
for p in deleted:
    print(f" - {p}")
if not deleted:
    print(" - None")

# Gather the download URLs
urls = list()
for p in not_downloaded:
    for i in tracks:
        title = i["track"]["name"]
        artists = [o["name"] for o in i["track"]["artists"]]
        code = f"{title} - {'/'.join(artists)}"

        if p == code:
            urls.append(i["track"]["external_urls"]["spotify"])
            break

if not_downloaded:
    os.system(f"cd {LOCATION} && spotdl {' '.join(urls)}")

# Remove Temp folder because spotdl doesn't do that for some reason
try:
    os.rmdir(f"{LOCATION}\\Temp")
except FileNotFoundError:
    pass

# TODO: Delete songs deleted from Spotify playlist