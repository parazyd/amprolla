# see LICENSE file for copyright and license details

"""
Network functions/helpers
"""

import os
import requests

from .log import die, warn


def download(url, path):
    """
    Downloads a file by providing it an url and a write path
    """
    print("downloading: %s\nto: %s" % (url, path))
    r = requests.get(url, stream=True)
    if r.status_code == 404:
        warn("download of %s failed: not found!" % url)
        return
    elif r.status_code != 200:
        die("download of %s failed" % url)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        # chunk_size {sh,c}ould be more on gbit servers
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                # f.flush()
    print("\033[1;32m .  done\033[0m")
    return
