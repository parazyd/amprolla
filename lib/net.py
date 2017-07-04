# see LICENSE file for copyright and license details

"""
Network functions/helpers
"""

from os import makedirs
from os.path import dirname
import requests

from lib.log import die, info, warn


def download(uris):
    """
    Downloads a file by providing it an url and a write path in a tuple
    """
    url = uris[0]
    path = uris[1]
    info("dl: %s" % url)

    try:
        r = requests.get(url, stream=True, timeout=20)
    except requests.exceptions.ConnectionError:
        warn("Caught exception: Connection reset. Retrying.")
        return download(uris)

    if r.status_code == 404:
        warn("failed: 404 not found!")
        return
    elif r.status_code != 200:
        die("failed: %d" % r.status_code)

    makedirs(dirname(path), exist_ok=True)
    f = open(path, 'wb')
    # chunk_size {sh,c}ould be more on gbit servers
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
            # f.flush()
    f.close()
