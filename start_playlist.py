import os
import configparser
from difflib import SequenceMatcher
import spotipy
import spotipy.util as util
from scraper import getM3uMusic
from classes.song import Song
from classes.tcolors import Tcolors


def strCompare(string1, string2) -> float:
    """ String comparison

        Computes the distance between two strings and returns the
        distance
    """
    print("Testing \"%s\" against \"%s\"" % (string1, string2))
    return SequenceMatcher(None, string1.lower(), string2.lower()).ratio()


def getMatch(spotify_client, local_song):
    """ Find Spotify match

    Takes a song's track name and artist name then searches for a matching song
    on Spotify. The matching song is returned. If no match is found, None is returned

    :param local_song: A Song object containing the track info
    :return: A dictionary containing Spotify track info
    """
    results = spotify_client.search(q="track:%s" %
        local_song.getTitle(), limit=30, type='track')
    spotify_matches = results["tracks"]["items"]
    matched_song = None

    #if no matches found
    if not spotify_matches:
        print(Tcolors.FAIL + "No Spotify results found for \"%s\"" % \
                local_song.getTitle() + Tcolors.ENDC)
        return None

    # if local song has Artist data, try to match with spotify artist
    if local_song.getArtist():
        for spotify_song in spotify_matches:
            if matched_song is not None:
                break

            # try matching with list of spotify artists
            for spotify_song_artist in spotify_song["artists"]:
                artist_match_ratio = strCompare(local_song.getArtist(), \
                        spotify_song_artist["name"])

                # if artist names are a somewhat close match
                if 0.45 < artist_match_ratio < 0.6:
                    # check if track names closely match
                    if strCompare(local_song.getTitle(), spotify_song["name"]) > 0.6:
                        matched_song = spotify_song
                        break

                elif artist_match_ratio >= 0.6:
                    matched_song = spotify_song
                    break

    # if local song has no artist, match with title only
    else:
        for spotify_song in spotify_matches:
            if strCompare(local_song.getTitle(), spotify_song["name"]) > 0.7:
                matched_song = spotify_song
                break
    return matched_song


def printSearch(song: Song):
    """ Prints search query information
    """
    if song.getTitle() is not None and song.getArtist() is not None:
        print("\nSearching for %s - %s" % (song.getArtist(), song.getTitle()))
    elif song.getTitle() is not None:
        print("Searching for %s" % song.getTitle())


def matchFound(song_match):
    """ Prints Spotify match information
    """
    print(Tcolors.OKGREEN + "Match found:" + Tcolors.ENDC + \
        "\n\tArtist: %s\n\tTitle: %s\n\tAlbum: %s" % \
        (song_match["artists"][0]["name"], song_match["name"], \
        song_match["album"]["name"]))


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


def main():
    config = getConfig()
    setEnviron(config)
    username = config["USERNAME"]

    m3u_path = input("Enter m3u file path: ")
    playlist_name = input("Enter playlist name: ")
    if m3u_path == "" or playlist_name == "":
        print("m3u file or playlist name not provided. Exiting program.")
        raise SystemExit

    print(Tcolors.HEADER + "Extracting music file paths..." + Tcolors.ENDC)
    songs = getM3uMusic(m3u_path)

    if songs is None:
        print("M3U file contains no music. Exiting program.")
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
        print("No matches for any tracks were found")

    print("\nMatching finished. All matched tracks have been added to \"%s\" playlist"
            % playlist_name)

    print("\n------------------------------------\n")

    if len(unmatched_songs) > 0:
        print(Tcolors.WARNING + "Unmatched files:" + Tcolors.ENDC)
        for f in unmatched_songs:
            print("\t%s" % f.getPath())


if __name__ == "__main__":
    main()
