import os
import re
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

def getM3uMusic(m3u_file_path):
    """ Creates a list of Song objects
    Songs files are parsed from the m3u file
    """
    songs = []
    with open(m3u_file_path) as m3u_file:
        for line in m3u_file:
            if lineIsMusic(line.rstrip()):
                print("\t%s" % line)
                songs.append(Song(getFileInfo(line.rstrip())))
    return songs


def lineIsMusic(m3u_line) -> bool:
    """ Test is an m3u entry is a local file

    Filters out URLs and comments from an m3u file

    :param m3u_line: A string containing the m3u entry line

    :return: True if line is a local file, False otherwise
    """
    return m3u_line[0] == "/" and \
            not re.search("://", m3u_line) and \
            m3u_line.lower().endswith((".mp3", ".flac", ".m4a"))
