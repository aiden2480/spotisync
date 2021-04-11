# Spotisync
<div  id="badges" align="center">
    <img  src="https://img.shields.io/github/last-commit/aiden2480/spotisync?color=1db954&logoColor=191414&style=flat-square"  alt="GitHub last commit">
    <img  src="https://img.shields.io/github/commit-activity/m/aiden2480/spotisync?color=1db954&logoColor=191414&style=flat-square"  alt="GitHub commits per month">
    <img  src="https://img.shields.io/github/repo-size/aiden2480/spotisync?color=1db954&logoColor=191414&style=flat-square"  alt="GitHub repo size">
    <img  src="https://img.shields.io/badge/Python-3.9.1-1db954?style=flat-square"  alt="Python 3.9.1">
</div>

## What is `spotisync`?
A small program making use of [spotDL](https://github.com/spotDL/spotify-downloader/) to download songs from a Spotify playlist and keep them in sync with a local folder. 

## Setup
1. Set up Ffmpeg and install it to path. Binaries can be found [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z) and an installation guide can be found [here](https://windowsloop.com/install-ffmpeg-windows-10/).
	* Note: In a future version of `spotDL`, you'll be able to specify the Ffmpeg filepath rather than installing it to PATH ([See: 1252](https://github.com/spotDL/spotify-downloader/pull/1252)). Once that happens,  this script will be updated.
	* Winrar or another file archiver utility software is required to open the binary files at the moment. (Again, will be updated when #1252 is merged)
2. Rename the `config.ini.example` file to remove the trailing extension, and fill in the configuration.
3. Run `python sync_playlist.py`
