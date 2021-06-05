import inspect
import io
import logging
import os
import re
import requests
import spotipy
import tempfile
import zipfile

from mutagen.easyid3 import EasyID3
from spotdl import console_entry_point
from spotdl.download.downloader import DownloadManager
from spotdl.search import songGatherer
from spotdl.search.spotifyClient import SpotifyClient
from spotipy.oauth2 import SpotifyClientCredentials


# Get client ID and secret from spotdl source files
def get_client_secrets():
    errormsg = "Couldn't grab credentials from spotdl, try reinstalling/upgrading it"
    pattern = re.compile("client_(?:id|secret) ?= ?(?:'|\")(\\w*)(?:'|\")")
    sauce = inspect.getsource(console_entry_point)
    matches = re.findall(pattern, sauce)

    assert len(matches) == 2, errormsg
    return dict(zip(["client_id", "client_secret"], matches))

# Looks for ffmpeg in the temp dir and downloads it if it can't find it
def get_ffmpeg():
    logging.debug("[FFMPEG] Locating driver")
    for r, d, f in os.walk(tempfile.gettempdir()):
        for fil in f:
            if fil.startswith("ffmpeg_") and fil.endswith(".exe"):
                logging.debug(f"[FFMPEG] Driver found at {os.path.join(r, fil)}")
                return os.path.join(r, fil)
    logging.debug("[FFMPEG] Driver not found, downloading")

    # TODO: Don't download from my website lol it'll likely break
    with requests.get("https://ffmpeg-downloads.chocolatejade42.repl.co/ffmpeg.zip") as resp:
        driver = resp.content
    logging.debug("[FFMPEG] Driver downloaded, writing to disk")

    with zipfile.NamedTemporaryFile(prefix="ffmpeg_", suffix=".exe", delete=False) as temp:
        zf = zipfile.ZipFile(io.BytesIO(driver))
        temp.write(zf.open("ffmpeg.exe").read())
        logging.debug(f"[FFMPEG] Finished write: {temp.name}")
    return temp.name

# Download remaining songs in a playlist
def download_playlist(url: str, loc: str):
    data = get_playlist_data(url)
    songs = data["tracks"]["items"]
    loc = loc.strip("\\").strip("/")

    # Online vs local songs
    online = dict() # Format: song name: URL
    local = dict() # Format: song name: location

    for elem in songs:
        title = elem["track"]["name"]
        artists = [o["name"] for o in elem["track"]["artists"]]
        online[f"{', '.join(artists)} - {title}"] = elem["track"]["external_urls"]["spotify"]
    
    for elem in [f for f in os.listdir(loc) if f.endswith(".mp3")]:
        id3 = EasyID3(f"{loc}\\{elem}")
        artist = ", ".join(id3["artist"][0].split("/"))
        local[f"{artist} - {id3['title'][0]}"] = elem
    
    not_downloaded = [i for i in online.keys() if i not in local.keys()]
    left_over = [i for i in local.keys() if i not in online.keys()]

    # Download new songs
    if not_downloaded:
        for song in not_downloaded:
            logging.info(f"Downloading song {song!r}")
        download_songs([online[i] for i in not_downloaded], loc)

    # Delete old songs
    if left_over:
        for song in left_over:
            logging.info(f"Removing deleted song {song!r}")
            os.remove(f"{loc}\\{local[song]}")
    
    # Regenerate M3U8 playlist file
    if not_downloaded or left_over:
        generate_m3u8(data["name"].lower(), loc, local)

    # Playlist should be up to date
    logging.info("Playlist up to date")

# Get playlist data of the current playlist from spotify
def get_playlist_data(url: str):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        **get_client_secrets()
    ))
    return spotify.playlist(url)

# Download a list of songs
def download_songs(query: list, loc: str):
    init_spotdl(loc.strip("\\").strip("/"))
    songs = list()
        
    with DownloadManager({"ffmpeg_path": get_ffmpeg()}) as dm:
        for song in query:
            songs.extend(songGatherer.from_query(song))
        
        if len(songs):
            dm.download_multiple_songs(songs)
    
    if os.path.exists("./Temp"):
        os.rmdir("./Temp")

# Generate new M3U8 file
def generate_m3u8(title: str, loc: str, songdata: dict):
    m3u8 = f"#EXTM3U\n#PLAYLIST:{title}"

    for name, path in songdata.items():
        m3u8 += f"\n\n#EXTINF: -1, {name}\n{loc}\\{path}"
    
    with open(f"{loc}\\{title}.m3u8", "w") as fp:
        fp.write(m3u8)

# Initialise spotdl
def init_spotdl(loc: str):
    os.chdir(loc.strip("\\").strip("/"))
    SpotifyClient.init(user_auth=False, **get_client_secrets())


if __name__ == "__main__":
    LOCATION = input("Enter the folder path of the local playlist: ")
    PLAYLIST = input("Enter the spotify playlist URL: ")

    # Enable logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )
    
    # Download/update playlist
    download_playlist(PLAYLIST, LOCATION)
