# See LICENSE file for copyright and license details.

"""
Lockfile functions
"""

from time import time
from os import remove
from os.path import isfile
import sys

from lib.log import info

def check_lock():
    """
    Checks if a lockfile is active, and creates one if not.
    """
    if isfile('/tmp/amprolla.lock'):
        info('Lockfile found. Defering operation.')
        sys.exit(1)

    with open('/tmp/amprolla.lock', 'w') as lock:
        lock.write(int(time()))


def free_lock():
    """
    Frees an active lockfile.
    """
    remove('/tmp/amprolla.lock')
