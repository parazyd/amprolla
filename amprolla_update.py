#!/usr/bin/env python3
# see LICENSE file for copyright and license details

"""
Perform incremental updates
"""

from os.path import join
from multiprocessing import Pool
from time import time
import requests

import lib.globalvars as globalvars
from lib.config import aliases, cpunm, repos, repo_order, spooldir, skips
from lib.lock import check_lock, free_lock
from lib.log import info, warn, die
from lib.parse import compare_dict, get_date, get_time, parse_release
from lib.net import download
from amprolla_merge import gen_release, merge, prepare_merge_dict


def remote_is_newer(remote, local):
    """
    Checks if a remote Release file holds a newer date, and returns True if so
    """
    rem_date = get_date(remote)
    loc_date = get_date(local)

    # print('Remote date: %s' % rem_date)
    # print('Local  date: %s' % loc_date)

    if get_time(rem_date) > get_time(loc_date):
        info('Remote Release is newer!')
        return True

    return False


def perform_update(suite, paths):
    """
    Performs an incremental update and merge of a given suite
    """
    info('Checking for updates in %s' % suite)
    # print(paths)
    globalvars.suite = suite
    globalvars.rehash = False

    needsmerge = {}
    needsmerge['downloads'] = []  # all files that have to be downloaded
    regenrelease = False
    cnt = 0
    for i in repo_order:
        # i = repository name
        needsmerge[i] = {}
        needsmerge[i]['mergelist'] = []

        if paths[cnt]:
            info('Working on %s repo' % i)
            remote_path = paths[cnt].replace(spooldir, repos[i]['host'])
            try:
                remote_rel = requests.get(join(remote_path, 'Release'))
            except requests.exceptions.ConnectionError as err:
                warn('Caught exception: "%s". Retrying...' % err)
                return perform_update(suite, paths)

            local_rel_text = open(join(paths[cnt], 'Release')).read()

            diffs = {}
            if remote_is_newer(remote_rel.text, local_rel_text):
                download((join(remote_path, 'Release'),
                          join(paths[cnt], 'Release')))
                regenrelease = True

                diffs = compare_dict(parse_release(remote_rel.text),
                                     parse_release(local_rel_text))
            if diffs:
                globalvars.rehash = True
                for k in diffs:
                    if k.endswith('Packages.gz') or k.endswith('Sources.gz'):
                        needsmerge[i]['mergelist'].append(k)
                    rmt = join(paths[cnt].replace(spooldir, repos[i]['host']), k)
                    loc = join(paths[cnt], k)
                    dlf = (rmt, loc)
                    needsmerge['downloads'].append(dlf)

        cnt += 1
        # break

    # download what needs to be downloaded
    if needsmerge['downloads']:
        info('Downloading updates...')
        dlpool = Pool(cpunm)
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
                if j == 'debian' and suite in skips:
                    sui = None

            if sui:
                pkgs.append(join(spooldir, repos[j]['dists'], sui, i))
            else:
                pkgs.append(None)

        merge_list.append(pkgs)

    # perform the actual merge
    if merge_list:
        info('Merging files...')
        mrgpool = Pool(cpunm)
        mrgpool.map(merge, merge_list)

    # generate Release files if we got any new files
    if needsmerge['downloads'] or regenrelease:
        info('Generating Release...')
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
    try:
        t1 = time()
        check_lock()
        main()
        free_lock()
        t2 = time()
        info('Total incremental update time: %s' % (t2 - t1), tofile=True)
    except Exception as e:
        die(e)
