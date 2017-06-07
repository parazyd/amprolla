#!/usr/bin/env python3
# see LICENSE file for copyright and license details

"""
Amprolla main module
"""

from os.path import basename, join
from multiprocessing import Pool
from time import time
# from pprint import pprint

from lib.package import (write_packages, load_packages_file,
                         merge_packages_many)
from lib.config import (aliases, banpkgs, repo_order, repos, spooldir, suites,
                        mergedir, mergesubdir, pkgfiles, srcfiles, categories,
                        arches)
from lib.release import write_release


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

    for suite in merge_dict:
        for repo in repo_order:
            tmpsuite = suite
            if repos[repo]['aliases'] is True:
                if tmpsuite in aliases[repos[repo]['name']]:
                    tmpsuite = aliases[repos[repo]['name']][suite]
                elif repos[repo]['skipmissing'] is True:
                    tmpsuite = None
                skips = ['jessie-security', 'ascii-security']
                if repo == 'debian' and suite in skips:
                    tmpsuite = None
            if tmpsuite:  # make it a proper path
                tmpsuite = join(spooldir, repos[repo]['dists'], tmpsuite)
            merge_dict[suite].append(tmpsuite)

    return merge_dict


def devuan_rewrite(pkg, repo_name):
    """
    Function to be called when including a certain package. Allows for changing
    any attributes. Currently only changes the filename if we include a package
    when repo_name == 'devuan'.
    """
    # if repo_name == 'devuan':
    pkg['Filename'] = pkg['Filename'].replace('pool/', 'pool/%s/' %
                                              repos[repo_name]['name'])

    return pkg


def merge(packages_list):
    """
    Merges the Packages/Sources files given in the package list
    """
    all_repos = []
    print('Loading packages: %s' % packages_list)

    devuan = load_packages_file(packages_list[0])
    if devuan:
        all_repos.append({'name': 'devuan', 'packages': devuan})

    debian_sec = load_packages_file(packages_list[1])
    if debian_sec:
        all_repos.append({'name': 'debian-sec', 'packages': debian_sec})

    debian = load_packages_file(packages_list[2])
    if debian:
        all_repos.append({'name': 'debian', 'packages': debian})

    if basename(packages_list[0]) == 'Packages.gz':
        print('Merging packages')
        src = False
        new_pkgs = merge_packages_many(all_repos, banned_packages=banpkgs,
                                       rewriter=devuan_rewrite)
    elif basename(packages_list[0]) == 'Sources.gz':
        print('Merging sources')
        src = True
        new_pkgs = merge_packages_many(all_repos)

    print('Writing packages')
    # replace the devuan subdir with our mergedir that we plan to fill
    # FIXME: do not assume Devuan always exists
    new_out = packages_list[0].replace(join(spooldir,
                                            repos['devuan']['dists']),
                                       join(mergedir, mergesubdir))
    if src:
        write_packages(new_pkgs, new_out, sources=True)
    else:
        write_packages(new_pkgs, new_out)


def gen_release(suite):
    """
    Generates a Release file for a given suite (jessie/ascii/unstable)
    """

    filelist = []
    print('Crawling %s' % suite)
    rootdir = join(mergedir, mergesubdir, suite)
    for cat in categories:
        for arch in arches:
            if arch == 'source':
                flist = srcfiles
            else:
                flist = pkgfiles

            for i in flist:
                filelist.append(join(rootdir, cat, arch, i))
                if arch != 'source':
                    filelist.append(join(rootdir, cat,
                                         'debian-installer', arch, i))

    newrfl = join(rootdir, 'Release')
    oldrfl = newrfl.replace(join(mergedir, mergesubdir),
                            join(spooldir, repos['devuan']['dists']))

    print('Writing Release')
    write_release(oldrfl, newrfl, filelist, rootdir)


def main_merge(packages_file):
    """
    Main function that calls the actual merge
    """
    to_merge = prepare_merge_dict()

    for suite in to_merge:
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

    # pprint(pkg)
    mrgpool = Pool(4)  # Set it to the number of CPUs you want to use
    mrgpool.map(main_merge, pkg)
    mrgpool.close()

    rel_list = []
    for i in suites:
        for j in suites[i]:
            rel_list.append(j)
            # gen_release(j)

    relpool = Pool(4)  # Set it to the number of CPUs you want to use
    relpool.map(gen_release, rel_list)
    relpool.close()


if __name__ == '__main__':
    t1 = time()
    main()
    t2 = time()
    print('total time: %s' % (t2 - t1))
