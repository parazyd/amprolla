#!/usr/bin/env python3
# see LICENSE file for copyright and license details

"""
Perform incremental updates
"""

from os.path import join
from multiprocessing import Pool
from time import time
import requests

from amprolla_merge import prepare_merge_dict, gen_release, merge
from lib.config import repos, spooldir, repo_order, aliases
from lib.parse import parse_release, get_time, get_date, compare_dict
from lib.net import download


def remote_is_newer(remote, local):
    """
    Checks if a remote Release file holds a newer date, and returns True if so
    """
    rem_date = get_date(remote)
    loc_date = get_date(local)

    print('Remote date: %s' % rem_date)
    print('Local  date: %s' % loc_date)

    if get_time(rem_date) > get_time(loc_date):
        print('Remote Release is newer!')
        return True

    return False


def perform_update(suite, paths):
    """
    Performs an incremental update and merge of a given suite
    """
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

            local_rel_text = open(join(paths[c], 'Release')).read()

            diffs = {}
            if remote_is_newer(remote_rel.text, local_rel_text):
                download((join(remote_path, 'Release'),
                          join(paths[c], 'Release')))

                diffs = compare_dict(parse_release(remote_rel.text),
                                     parse_release(local_rel_text))
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
    if needsmerge['downloads']:
        print('Downloading updates...')
        dlpool = Pool(4)
        dlpool.map(download, needsmerge['downloads'])

    # create union of our Packages.gz and Sources.gz files we will merge
    uni = []
    for i in repo_order:
        uni.append(needsmerge[i]['mergelist'])
    updpkg_list = set().union(*uni)

    # make a list of package lists to feed into merge()
    merge_list = []
    for i in updpkg_list:
        pkgs = []
        for j in repo_order:
            sui = suite
            # append valid aliases
            if repos[j]['aliases']:
                if suite in aliases[repos[j]['name']]:
                    sui = aliases[repos[j]['name']][suite]
                elif repos[j]['skipmissing']:
                    sui = None
                skips = ['jessie-security', 'ascii-security']  # hack
                if j == 'debian' and suite in skips:
                    sui = None

            if sui:
                pkgs.append(join(spooldir, repos[j]['dists'], sui, i))
            else:
                pkgs.append(None)

        merge_list.append(pkgs)

    # perform the actual merge
    if merge_list:
        print('Merging files...')
        mrgpool = Pool(4)
        mrgpool.map(merge, merge_list)

    # generate Release files if we got any new files
    if needsmerge['downloads']:
        print('Generating Release...')
        gen_release(suite)


def main():
    """
    Do the update for all repos
    """
    roots = prepare_merge_dict()
    for suite, paths in roots.items():
        perform_update(suite, paths)
        # break


if __name__ == '__main__':
    t1 = time()
    main()
    t2 = time()
    print('total time: %s' % (t2 - t1))
