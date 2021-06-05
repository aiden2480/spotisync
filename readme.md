# Spotisync
<div id="badges" align="center">
    <img  src="https://img.shields.io/github/last-commit/aiden2480/spotisync?color=1db954&logoColor=191414&style=flat-square"  alt="GitHub last commit">
    <img  src="https://img.shields.io/github/commit-activity/m/aiden2480/spotisync?color=1db954&logoColor=191414&style=flat-square"  alt="GitHub commits per month">
    <img  src="https://img.shields.io/github/repo-size/aiden2480/spotisync?color=1db954&logoColor=191414&style=flat-square"  alt="GitHub repo size">
    <img  src="https://img.shields.io/badge/Python-3.9.1-1db954?style=flat-square"  alt="Python 3.9.1">
</div>

## What is spotisync?
A small program making use of [spotDL](https://github.com/spotDL/spotify-downloader/) to download songs from a Spotify playlist and keep them in sync with a local folder.
It will download new songs and delete old songs as necessary. Through spotDL, it will also 

## Setup
1. Run `pip install -r requirements.txt` to install dependencies. Note that spotDL must be at least version [`3.6.0`](https://github.com/spotDL/spotify-downloader/issues/1251) due to changes in that version that allow the specification of the `--ffmpeg` flag so that the binaries don't have to be on PATH.
2. Run `python spotisync.py` and enter in your folder filepath and playlist URL when prompted. In future I'll update it to read from a JSON file or something to keep multiple locations up to date. 
