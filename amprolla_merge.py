#!/usr/bin/env python3
# See LICENSE file for copyright and license details.

"""
Amprolla main module
"""

from os.path import basename, join
from multiprocessing import Pool
from time import time


import lib.globalvars as globalvars
from lib.config import (aliases, arches, banpkgs, categories, cpunm, mergedir,
                        mergesubdir, pkgfiles, repos, repo_order, spooldir,
                        srcfiles, suites, skips)
from lib.lock import check_lock, free_lock
from lib.package import (load_packages_file, merge_packages_many,
                         write_packages)
from lib.release import write_release
from lib.log import info, die


def prepare_merge_dict():
    """
    This function will prepare a dict of lists that contain the repos
    that need to be merged in an ordered fashion. Orders them using the
    repo_order list found in lib.config
    Example output:
        {'ascii': ['ascii', None, 'stretch']},
    """
    merge_dict = {}

    for suite in suites:
        for i in suites[suite]:
            merge_dict[i] = []

    from pprint import pprint
    pprint(merge_dict)

    for suite in merge_dict:
        print(suite)
        for repo in repo_order:
            print(repo)
            tmpsuite = suite
            if repos[repo]['aliases'] is True:
                if tmpsuite in aliases[repos[repo]['name']]:
                    tmpsuite = aliases[repos[repo]['name']][suite]
                elif repos[repo]['skipmissing'] is True:
                    tmpsuite = None
                if repo == 'debian' and suite in skips:
                    tmpsuite = None
            if tmpsuite:  # make it a proper path
                rep = repos[repo]['host'].replace('http://', '')
                rep = rep.replace('https://', '')
                tmpsuite = join(spooldir, rep, repos[repo]['dists'], tmpsuite)
            merge_dict[suite].append(tmpsuite)

    return merge_dict


def devuan_rewrite(pkg, repo_name):
    """
    Function to be called when including a certain package. Allows for changing
    any attributes.
    """

    if 'Filename' in pkg and repos[repo_name]['name'] not in pkg['Filename']:
        pkg['Filename'] = pkg['Filename'].replace('pool/', 'pool/%s/' %
                                                  repos[repo_name]['name'], 1)
    if 'Directory' in pkg and repos[repo_name]['name'] not in pkg['Directory']:
        pkg['Directory'] = pkg['Directory'].replace('pool/', 'pool/%s/' %
                                                    repos[repo_name]['name'], 1)

    return pkg


def merge(packages_list):
    """
    Merges the Packages/Sources files given in the package list

    ['path/to/devuan/Packages.gz', None, 'path/to/debian/Packages.gz']
    """
    all_repos = []
    src = False
    print('Loading packages: %s' % packages_list)

    for i in range(len(repo_order)):
        pkgs = load_packages_file(packages_list[i])
        if pkgs:
            all_repos.append({'name': repo_order[i], 'packages': pkgs})

    for i in range(len(repo_order)):
        if packages_list[i]:
            if basename(packages_list[i]) == 'Packages.gz':
                print('Merging packages')
                src = False
                new_pkgs = merge_packages_many(all_repos,
                                               banned_packages=banpkgs,
                                               rewriter=devuan_rewrite)
            elif basename(packages_list[i]) == 'Sources.gz':
                print('Merging sources')
                src = True
                new_pkgs = merge_packages_many(all_repos,
                                               rewriter=devuan_rewrite)
            break

    print('Writing packages')
    for i in range(len(repo_order)):
        if packages_list[i]:
            rep = repos[repo_order[i]]['host'].replace('http://', '')
            rep = rep.replace('https://', '')
            new_out = packages_list[i].replace(join(spooldir, rep,
                                                    repos[repo_order[i]]['dists']),
                                               join(mergedir, mergesubdir))
            break

    write_packages(new_pkgs, new_out, sources=src)


def gen_release(suite):
    """
    Generates a Release file for a given suite (jessie/ascii/unstable)
    """

    filelist = []
    print('\nCrawling %s' % suite)
    rootdir = join(mergedir, mergesubdir, suite)
    for cat in categories:
        for arch in arches:
            if arch == 'source':
                flist = srcfiles
            else:
                flist = pkgfiles
                cont = arch.replace('binary', 'Contents')
                cont_udeb = arch.replace('binary', 'Contents-udeb')
                filelist.append(join(rootdir, cat, cont+'.gz'))
                filelist.append(join(rootdir, cat, cont))
                filelist.append(join(rootdir, cat, cont_udeb+'.gz'))
                filelist.append(join(rootdir, cat, cont_udeb))

            for i in flist:
                filelist.append(join(rootdir, cat, arch, i))
                if arch != 'source':
                    filelist.append(join(rootdir, cat,
                                         'debian-installer', arch, i))

    newrfl = join(rootdir, 'Release')
    rep = repos['devuan']['host'].replace('http://', '')
    rep = rep.replace('https://', '')
    oldrfl = newrfl.replace(join(mergedir, mergesubdir),
                            join(spooldir, rep, repos['devuan']['dists']))

    print('Writing Release')
    write_release(oldrfl, newrfl, filelist, rootdir)


def main_merge(packages_file):
    """
    Main function that calls the actual merge
    """
    to_merge = prepare_merge_dict()

    for suite in to_merge:
        globalvars.suite = suite
        pkg_list = []
        for rep in to_merge[suite]:
            if rep:
                pkg_list.append(join(rep, packages_file))
            else:
                pkg_list.append(None)

        merge(pkg_list)


def main():
    """
    Crawls the entire directory structure and orchestrates the merge
    in a queue using multiprocessing
    """
    pkg = []
    for i in arches:
        for j in categories:
            if i == 'source':
                mrgfile = 'Sources.gz'
            else:
                mrgfile = 'Packages.gz'
                pkg.append(join(j, 'debian-installer', i, mrgfile))

            pkg.append(join(j, i, mrgfile))

    mrgpool = Pool(cpunm)
    mrgpool.map(main_merge, pkg)
    mrgpool.close()

    rel_list = []
    for i in suites:
        for j in suites[i]:
            rel_list.append(j)

    relpool = Pool(cpunm)
    relpool.map(gen_release, rel_list)
    relpool.close()


if __name__ == '__main__':
    try:
        t1 = time()
        check_lock()
        main()
        free_lock()
        t2 = time()
        info('Total full merge time: %s' % (t2 - t1), tofile=True)
    except Exception as e:
        die(e)
