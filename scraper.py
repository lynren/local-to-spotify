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
        for file_ in files:
            if file_.lower().endswith((".mp3", ".flac", ".m4a")):
                print("\t%s" % path)
                path = root + '/' + file_
                songs.append(Song(getFileInfo(path)))

    return songs if len(songs) > 0 else None


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


def getFileInfo(music_file_path) -> dict:
    if music_file_path.endswith(".mp3"):
        return getMp3Info(music_file_path)
    if music_file_path.endswith(".flac"):
        return getFlacInfo(music_file_path)
    # ends with .m4a or .mp4
    return getM4aInfo(music_file_path)
