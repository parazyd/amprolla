# See LICENSE file for copyright and license details.

"""
Logging functions
"""

from time import strftime
from os import makedirs
from os.path import join
import sys

from lib.config import logdir


def timestamp():
    """
    Return current time in a certain format.
    """
    return strftime("%Y/%m/%d %H:%M:%S")


def die(msg, tofile=True):
    """
    Log error and exit with exitcode 1
    """
    msg = "%s [ERR] %s" % (timestamp(), msg)
    print(msg)
    if tofile:
        logtofile('amprolla.txt', msg+'\n')
    sys.exit(1)


def warn(msg, tofile=True):
    """
    Log warning and continue
    """
    msg = "%s [WARN] %s" % (timestamp(), msg)
    print(msg)
    if tofile:
        logtofile('amprolla.txt', msg+'\n')


def info(msg, tofile=True):
    """
    Log informational message and continue
    """
    msg = "%s [INFO] %s" % (timestamp(), msg)
    print(msg)
    if tofile:
        logtofile('amprolla.txt', msg+'\n')


def logtofile(filename, text, redo=False):
    """
    Log given text to a given file.
    If redo is True, rewrites the file
    """
    makedirs(logdir, exist_ok=True)
    wrt = 'a'
    if redo:
        wrt = 'w'
    lfile = open(join(logdir, filename), wrt)
    lfile.write(text)
    lfile.close()
