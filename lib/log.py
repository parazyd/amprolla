# See LICENSE file for copyright and license details.

"""
Logging functions
"""

from time import time
from os import makedirs, remove
from os.path import join
import sys

from lib.config import logdir


def die(msg, tofile=True):
    """
    Log error and exit with exitcode 1
    """
    msg = "%d [ERR] %s\n" % (int(time()), msg)
    print(msg)
    if tofile:
        logtofile('amprolla.txt', msg)
    sys.exit(1)


def warn(msg, tofile=True):
    """
    Log warning and continue
    """
    msg = "%d [WARN] %s\n" % (int(time()), msg)
    print(msg)
    if tofile:
        logtofile('amprolla.txt', msg)


def info(msg, tofile=True):
    """
    Log informational message and continue
    """
    msg = "%d [INFO] %s\n" % (int(time()), msg)
    print(msg)
    if tofile:
        logtofile('amprolla.txt', msg)


def logtofile(filename, text, redo=False):
    """
    Log given text to a given file.
    If redo is True, rewrites the file
    """
    makedirs(logdir, exist_ok=True)
    if redo:
        remove(join(logdir, filename))
    lfile = open(join(logdir, filename), 'a')
    lfile.write(text)
    lfile.close()
