import os
from configparser import ConfigParser
from random import shuffle

import spotipy
from mutagen.easyid3 import EasyID3
from spotipy.oauth2 import SpotifyClientCredentials


# Config
config = ConfigParser()
config.read("./config.ini")
loc = config["PLAYLIST"]["playlistlocation"]
m3u8loc = config["PLAYLIST"]["m3u8location"]

# Set up spotipy client
creds = SpotifyClientCredentials(
    config["SPOTIFY CREDENTIALS"]["clientid"],
    config["SPOTIFY CREDENTIALS"]["clientsecret"]
)
spotify = spotipy.Spotify(client_credentials_manager=creds)
pdata = spotify.playlist(config["PLAYLIST"]["playlisturi"])
name = pdata["name"]

quarantine = f"#EXTM3U\n#PLAYLIST:{name}"
local_filenames = [f for f in os.listdir(loc) if f.endswith(".mp3")]
shuffle(local_filenames)

# Format song data
for fp in local_filenames:
    audio = EasyID3(f"{loc}\\{fp}")
    title = audio["title"][0]
    quarantine += f"\n\n#EXTINF: -1, {title}\n{loc}\\{fp}"
    print(" * Wrote", title)

# Write to file
with open(m3u8loc, "w") as fp:
    fp.write(quarantine)
print(f"Wrote {name} ({len(local_filenames)} songs) to {m3u8loc}")