import os
import configparser
from difflib import SequenceMatcher
import spotipy
import spotipy.util as util
from scraper import getM3uMusic
from matcher import getMatch
from log import printSearch, matchFound
from classes.song import Song
from classes.tcolors import Tcolors


def getConfig() -> dict:
    """ Parses config.cfg in program folder
        Returns a dictionary containing config settings
    """
    config = configparser.ConfigParser()
    config.read("config.cfg")
    return {"CLIENT_ID": config.get("SPOTIFY", "CLIENT_ID"), "CLIENT_SECRET": config.get("SPOTIFY", "CLIENT_SECRET"), "REDIRECT_URI": "http://localhost", "USERNAME": config.get("SPOTIFY", "USERNAME")}


def setEnviron(config: dict):
    """ Sets OS environment variables for spotipy
    """
    os.environ["SPOTIPY_CLIENT_ID"] = config["CLIENT_ID"]
    os.environ["SPOTIPY_CLIENT_SECRET"] = config["CLIENT_SECRET"]
    os.environ["SPOTIPY_REDIRECT_URI"] = config["REDIRECT_URI"]


def getM3uPath():
    m3u_path = input("Enter m3u file path: ")
    return m3u_path if m3u_path != "" else None

def getPlaylistName():
    playlist_name = input("Enter playlist name: ")
    return None if playlist_name == "" else playlist_name


def main():
    config = getConfig()
    setEnviron(config)
    username = config["USERNAME"]

    while (m3u_path := getM3uPath()) is None or (playlist_name := getPlaylistName()) is None:
        print(Tcolors.FAIL + "m3u file or playlist name not provided. Exiting program."
                + Tcolors.ENDC)

    print(Tcolors.HEADER + "Extracting music file paths..." + Tcolors.ENDC)
    songs = getM3uMusic(m3u_path)

    if songs is None:
        print(Tcolors.FAIL + "M3U file contains no music. Exiting program." + Tcolors.ENDC)
        raise SystemExit

    scope = "user-read-private playlist-modify-public playlist-modify-private"
    token = util.prompt_for_user_token(username, scope)

    if not token:
        raise SystemExit

    spotify_client = spotipy.Spotify(auth=token)
    unmatched_songs = []
    matched_song_uris = []

    print(Tcolors.HEADER + "Starting song matching..."  + Tcolors.ENDC)

    while len(songs) > 0:
        track = songs.pop()
        printSearch(track)
        song_match = getMatch(spotify_client, track)
        if song_match is not None:
            matchFound(song_match)
            matched_song_uris.append(song_match["uri"])
        else:
            print(Tcolors.FAIL + "No match found!" + Tcolors.ENDC)
            unmatched_songs.append(track)

    if len(matched_song_uris) > 0:
        playlist = spotify_client.user_playlist_create(username, playlist_name,
                public=True)
        spotify_client.user_playlist_add_tracks(username, playlist["id"], matched_song_uris)
    else:
        print(Tcolors.FAIL + "No matches for any tracks were found" + Tcolors.ENDC)

    print("\nMatching finished. All matched tracks have been added to \"%s\" playlist"
            % playlist_name)

    print("\n------------------------------------\n")

    if len(unmatched_songs) > 0:
        print(Tcolors.WARNING + "Unmatched files:" + Tcolors.ENDC)
        for f in unmatched_songs:
            print("\t%s" % f.getPath())


if __name__ == "__main__":
    main()
