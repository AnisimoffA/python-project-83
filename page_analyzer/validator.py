from validators import url
from urllib.parse import urlparse


def url_validator(URL):
    if not url(URL) or url(URL) and len(URL) > 255:
        return False
    return True


def url_normalize(URL):
    return urlparse(URL)
