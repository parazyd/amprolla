#!/usr/bin/env python3
# see LICENSE file for copyright and license details

"""
Perform incremental updates
"""

from os.path import join
import requests

from amprolla_init import pop_dirs
from amprolla_merge import prepare_merge_dict
from lib.config import repos, spooldir
from lib.parse import parse_release, get_time, get_date, compare_dict

from pprint import pprint


roots = prepare_merge_dict()

needsmerge = []

for suite, paths in roots.items():
    print(suite)
    print(paths)
    devuan_loc = paths[0]
    debian_sec_loc = paths[1]
    debian_loc = paths[2]

    if devuan_loc:
        devuan_rem = devuan_loc.replace(spooldir, repos['devuan']['host'])
        print(devuan_rem)
        remoterel = join(devuan_rem, 'Release')
        localrel = join(devuan_loc, 'Release')

        if remote_is_newer(remoterel, localrel):
            print('Do something')
            # probably add suite to needsmerge

    if debian_sec_loc:
        print('Do the same')

    if debian_loc:
        print('Do the same')


    break

def remote_is_newer(remote, local):
    rem = requests.get(remote)
    rem_contents = rem.text
    rem_date = get_date(rem_contents)

    loc_contents = open(localrel).read()
    loc_date = get_date(loc_contents)

    print('Remote date: %s' % rem_date)
    print('Local date: %s' % loc_date)

    if get_time(rem_date) > get_time(loc_date):
        print('Remote Release is newer!')
        return True

    return False
