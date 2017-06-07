#!/usr/bin/env python3
# see LICENSE file for copyright and license details

"""
Perform incremental updates
"""

from os.path import join
import requests
from multiprocessing import Pool

from amprolla_init import pop_dirs
from amprolla_merge import prepare_merge_dict
from lib.config import repos, spooldir, repo_order
from lib.parse import parse_release, get_time, get_date, compare_dict
from lib.net import download

from pprint import pprint


def remote_is_newer(remote, local):
    rem_date = get_date(remote)
    loc_date = get_date(local)

    print('Remote date: %s' % rem_date)
    print('Local  date: %s' % loc_date)

    if get_time(rem_date) > get_time(loc_date):
        print('Remote Release is newer!')
        return True

    return False


def perform_update(suite, paths):
    print('==================================================')
    print('Checking for updates in %s' % suite)
    print(paths)

    needsmerge = {}
    needsmerge['downloads'] = []  # all files that have to be downloaded
    c = 0
    for i in repo_order:
        # i = repository name
        needsmerge[i] = {}
        needsmerge[i]['mergelist'] = []

        if paths[c]:
            print('Working on %s repo' % i)
            remote_path = paths[c].replace(spooldir, repos[i]['host'])
            remote_rel = requests.get(join(remote_path, 'Release'))
            remote_rel_text = remote_rel.text
            tup = (remote_rel, join(paths[c], 'Release'))
            download(tup)

            local_rel_text = open(join(paths[c], 'Release')).read()

            if remote_is_newer(remote_rel_text, local_rel_text):
                remote_parsed = parse_release(remote_rel_text)
                local_parsed = parse_release(local_rel_text)
                diffs = compare_dict(remote_parsed, local_parsed)
                if diffs:
                    for k in diffs:
                        if k.endswith('Packages.gz') or k.endswith('Sources.gz'):
                            needsmerge[i]['mergelist'].append(k)
                        rmt = join(paths[c].replace(spooldir, repos[i]['host']), k)
                        loc = join(paths[c], k)
                        dlf = (rmt, loc)
                        needsmerge['downloads'].append(dlf)

        c += 1
        # break

    # download what needs to be downloaded
    print('Downloading updates...')
    dlpool = Pool(4)
    dlpool.map(download, needsmerge['downloads'])
    dlpool.close

    # create union of our Packages.gz and Sources.gz files we will merge
    uni = []
    for i in repo_order:
        uni.append(needsmerge[i]['mergelist'])
    updpkg_list = set().union(*uni)

    # perform the actual merge
    if updpkg_list:
        print('Merging files...')
        mrgpool = Pool(4)
        mrgpool.map(merge, updpkg_list)
        mrgpool.close()

    print('Generating Release...')
    gen_release(suite)

    print('==================================================')


def main():
    """
    Do the update for all repos
    """
    roots = prepare_merge_dict()
    for suite, paths in roots.items():
        perform_update(suite, paths)
        break


if __name__ == '__main__':
    main()
