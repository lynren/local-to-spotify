import os
from mutagen.easyid3 import EasyID3
import mutagen.flac
import mutagen.id3
import mutagen.mp4
from classes.song import Song

def getMusic(music_folder: str) -> list:
    """ Gets music files

    Searches the given directory for mp3, flac, and m4a files

    :param music_folder: A string containing the music directory path

    :return: A list of songs found. If no songs found, None is returned
    """
    songs = []
    for root, dirs, files in os.walk(music_folder):
        for f in files:
            path = root + '/' + f
            if f.endswith(".mp3"):
                fileFound(path)
                new_song = Song(getMp3Info(path))
                songs.append(new_song)
            elif f.endswith(".flac"):
                fileFound(path)
                songs.append(Song(getFlacInfo(path)))
            elif f.endswith(".m4a"):
                fileFound(path)
                songs.append(Song(getM4aInfo(path)))
    return songs if len(songs) > 0 else None


def fileFound(f: str):
    """ Prints a file path with a tab preppended
    """
    print("\t%s" % f)


def getMp3Info(music_file_path: str) -> dict:
    """ Returns dict containing music file info
    """
    try:
        audio = EasyID3(music_file_path)
    except mutagen.id3.ID3NoHeaderError:
        return {'title': None, 'artist': None, 'album': None, 'path': music_file_path}
    return {'title': audio['title'], 'artist': audio['artist'], 'album': audio['album'], \
            'path': music_file_path}


def getFlacInfo(music_file_path: str) -> dict:
    try:
        audio = mutagen.flac.FLAC(music_file_path)
    except mutagen.flac.error:
        return {'title': None, 'artist': None, 'album': None, 'path': music_file_path}
    return {'title': audio['title'], 'artist': audio['artist'], 'album': audio['album'], \
            'path': music_file_path}


def getM4aInfo(music_file_path: str) -> dict:
    try:
        audio = mutagen.mp4.MP4(music_file_path)
    except mutagen.mp4.MP4StreamInfoError:
        return {'title': None, 'artist': None, 'album': None, 'path': music_file_path}
    return {'title': audio['\xa9nam'], 'artist': audio['\xa9ART'], \
            'album': audio['\xa9alb'], 'path': music_file_path}
