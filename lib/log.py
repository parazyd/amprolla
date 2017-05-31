# see LICENSE file for copyright and license details

"""
Logging functions
"""

# TODO: Replace with logging

import sys


def die(msg):
    print("\033[1;31m[E] %s\033[0m" % msg)
    sys.exit(1)


def notice(msg):
    print("\033[1;32m(*) %s\033[0m" % msg)
    return


def warn(msg):
    print("\033[1;33m[W] %s\033[0m" % msg)
    return


def cleanexit():
    notice("exiting cleanly...")
    sys.exit(0)
