#!/usr/bin/env python3
# see LICENSE file for copyright and license details

"""
Module used to orchestrace the entire amprolla merge
"""

from os.path import join
from multiprocessing import Pool

from lib.config import (arches, categories, suites, mergedir, mergesubdir,
                        pkgfiles, srcfiles, spooldir, repos)
from lib.release import write_release

# from pprint import pprint


def do_merge():
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

    am = __import__('amprolla_merge')

    p = Pool(4)
    p.map(am.main, pkg)


def gen_release(s):
    """
    Generates a Release file for a given main suite (jessie/ascii/unstable)
    """

    for suite in suites[s]:
        filelist = []
        print('Crawling %s' % suite)
        rootdir = join(mergedir, mergesubdir, suite)
        for cat in categories:
            for arch in arches:
                if arch == 'source':
                    flist = srcfiles
                else:
                    flist = pkgfiles

                for fl in flist:
                    filelist.append(join(rootdir, cat, arch, fl))
                    if arch != 'source':
                        filelist.append(join(rootdir, cat,
                                             'debian-installer', arch, fl))

        newrfl = join(rootdir, 'Release')
        oldrfl = newrfl.replace(join(mergedir, mergesubdir),
                                join(spooldir, repos['devuan']['dists']))

        print('Writing Release')
        write_release(oldrfl, newrfl, filelist, rootdir)
        # break


do_merge()

for st in suites:
    gen_release(st)
