import re


class Song:

    def __init__(self, info: dict):
        self.title = stripTitle(info["title"][0]) \
                if info["title"] is not None else None
        self.album = info["album"][0] if info["album"] is not None else None
        self.artist = info["artist"][0] if info["artist"] is not None else None
        self.path = info["path"]


    def getInfo(self) -> dict:
        return {"title": self.title, \
                "artist": self.artist, \
                "album": self.album}


    def getTitle(self) -> str:
        return self.title


    def getArtist(self) -> str:
        return self.artist


    def getAlbum(self) -> str:
        return self.album


    def getPath(self) -> str:
        return self.path


def stripTitle(title: str) -> str:
    title = re.sub(r"[\[\(].*[\]\)]", "", title)
    title = re.sub(r"[´`]", "'", title)
    title = re.sub(r"\s{2,}", " ", title)

    title = title.rstrip()
    return title
