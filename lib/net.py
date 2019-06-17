# See LICENSE file for copyright and license details.

"""
Network functions/helpers
"""

from os import makedirs
from os.path import dirname
import requests

from lib.log import info, warn


def download(uris):
    """
    Downloads a file by providing it an url and a write path in a tuple
    """
    url = uris[0]
    path = uris[1]
    info("dl: %s" % url)

    try:
        rfile = requests.get(url, stream=True, timeout=20)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            ConnectionResetError) as err:
        warn('Caught exception: "%s". Retrying...' % err)
        return download(uris)

    if rfile.status_code != 200:
        warn('%s failed: %d' % (url, rfile.status_code))
        return

    makedirs(dirname(path), exist_ok=True)
    lfile = open(path, 'wb')
    # chunk_size {sh,c}ould be more on gbit servers
    for chunk in rfile.iter_content(chunk_size=1024):
        if chunk:
            lfile.write(chunk)
            # f.flush()
    lfile.close()
