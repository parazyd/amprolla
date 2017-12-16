# See LICENSE file for copyright and license details.

"""
Lockfile functions
"""

from time import time
from os import remove
from os.path import isfile
import sys

from lib.config import lockpath
from lib.log import info


def check_lock():
    """
    Checks if a lockfile is active, and creates one if not.
    """
    if isfile(lockpath):
        info('Lockfile found. Defering operation.')
        sys.exit(1)

    with open(lockpath, 'w') as lock:
        lock.write(str(int(time())))


def free_lock():
    """
    Frees an active lockfile.
    """
    if isfile(lockpath):
        remove(lockpath)
