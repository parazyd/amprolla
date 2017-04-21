#!/usr/bin/env python
# copyright (c) 2017 - Ivan J. <parazyd@dyne.org>
# see LICENSE file for copyright and license details

import requests

import config
from log import die, notice, warn, cleanexit


def download(url, path):
    print("\tdownloading: %s\n\tto: %s" % (url, path))
    r = requests.get(url, stream=True)
    if r.status_code == 404:
        warn("not found!")
        return
    elif r.status_code != 200:
        die("fail!")

    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024): # XXX: should be more on gbit servers
            if chunk:
                f.write(chunk)
                #f.flush()
    print("\033[1;32m .  done\033[0m")
    return
