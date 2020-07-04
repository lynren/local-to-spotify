import re


def stripTitle(title: str) -> str:
    title = re.sub(r"[\[\(].*[\]\)]", "", title)
    title = re.sub(r"[´`]", "'", title)
    title = re.sub(r"\s{2,}", " ", title)

    title = title.rstrip()
    return title
