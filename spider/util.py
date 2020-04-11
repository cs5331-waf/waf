import os.path
from urllib.parse import urlparse


def construct_full_url(link, parsed_url):
    parsed_link = urlparse(link)
    path_tokens = os.path.split(parsed_url.path)
    # Action attribute is relative to current path based on URL
    if path_tokens[0] not in parsed_link.path:
        link = path_tokens[0] + '/' + link
    if not parsed_link.netloc:
        link = parsed_url.netloc + link
    if not parsed_link.scheme:
        link = parsed_url.scheme + "://" + link
    return link

