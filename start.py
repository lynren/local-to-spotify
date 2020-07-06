import os
import configparser
from difflib import SequenceMatcher
import spotipy
import spotipy.util as util
from scraper import getMusic
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


def getInput():
    music_dir = input("Enter music directory absolute path: ")
    if music_dir == "" or music_dir.rstrip()[0] != "/":
        return None
    return music_dir


def main():
    config = getConfig()
    setEnviron(config)
    username = config["USERNAME"]

    while (music_dir := getInput()) is None:
        print(Tcolors.FAIL + "An absolute path must be provided." + Tcolors.ENDC)

    print("Searching for music files...")
    songs = getMusic(music_dir)

    if songs is None:
        print(Tcolors.FAIL + "Music directory is empty. Exiting program." + Tcolors.ENDC)
        raise SystemExit

    scope = "user-read-private user-library-modify"
    token = util.prompt_for_user_token(username, scope)

    if not token:
        raise SystemExit

    spotify_client = spotipy.Spotify(auth=token)
    unmatched_songs = []
    matched_song_uris = []

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
        spotify_client.current_user_saved_tracks_add(tracks=matched_song_uris)
    else:
        print("Matches for any tracks were not found")

    print("\nMatching finished. All matched tracks have been added to %s's Spotify library"
            % username)

    print("\n------------------------------------\n")

    if len(unmatched_songs) > 0:
        print(Tcolors.WARNING + "Unmatched files:" + Tcolors.ENDC)
        for f in unmatched_songs:
            print("\t%s" % f.getPath())


if __name__ == "__main__":
    main()
