from classes.song import Song
from classes.tcolors import Tcolors


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
