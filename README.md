# local-to-spotify
## start.py
This program searches for mp3, flac, and m4a files in a given directory. The songs found are matched with Spotify songs which are then added to the user's library.

## start_playlist.py
This program matches song files from an M3U file and adds them to a Spotify playlist.

Requirements
============

- [Mutagen](https://mutagen.readthedocs.io/en/latest/)
- [Spotipy](https://spotipy.readthedocs.io/en/latest/)
- [Spotify developer credentials for Spotipy](https://developer.spotify.com/dashboard)
- Python 3.8

Usage
=====

1. Create a file "config.cfg" in the project directory
2. Add your information to config.cfg. Follow "config_example.cfg" for format
3. Run start.py or start_playlist.py
