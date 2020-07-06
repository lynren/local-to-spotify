from difflib import SequenceMatcher
import spotipy
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
                if 0.45 < artist_match_ratio < 0.65:
                    # check if track names closely match
                    if strCompare(local_song.getTitle(), spotify_song["name"]) > 0.75:
                        matched_song = spotify_song
                        break

                elif artist_match_ratio >= 0.65:
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
