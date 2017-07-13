#!/usr/bin/env python3
"""
Amprolla module for merging Contents files
"""

from gzip import open as gzip_open
from multiprocessing import Pool
from os import makedirs
from os.path import dirname, join, isfile
from time import time

from amprolla_merge import prepare_merge_dict
from lib.config import (arches, categories, cpunm, mergedir, mergesubdir,
                        repos, spooldir)
import lib.globalvars as globalvars


def merge_contents(filelist):
    """
    Merges a list of Contents files and returns a dict of the merged files
    """
    pkgs = {}
    for i in filelist:
        if i and isfile(i):
            cfile = gzip_open(i).read()
            cfile = cfile.decode('utf-8')
            contents = cfile.split('\n')

            for line in contents:
                if line.startswith('This file maps each file'):
                    while not line.startswith('FILE'):
                        continue
                if line != '' and not line.startswith('FILE'):
                    sin = line.split()
                    if sin[-1] not in pkgs.keys():
                        pkgs[sin[-1]] = []
                    pkgs[sin[-1]].append(' '.join(sin[:-1]))
    return pkgs


def write_contents(pkgs, filename):
    """
    Writes a merged Contents dict to the given filename in gzip format
    """
    makedirs(dirname(filename), exist_ok=True)
    gzf = gzip_open(filename, 'w')

    for pkg, files in sorted(pkgs.items()):
        for f in files:
            ln = "%s %s\n" % (f, pkg)
            gzf.write(ln.encode('utf-8'))

    gzf.write(b'\n')
    gzf.close()


def main_merge(contents_file):
    """
    Main merge logic. First parses the files into dictionaries, and
    writes them to the mergedir afterwards
    """
    to_merge = prepare_merge_dict()

    for suite in to_merge:
        globalvars.suite = suite
        cont_list = []
        for rep in to_merge[suite]:
            if rep:
                cont_list.append(join(rep, contents_file))
            else:
                cont_list.append(None)

        print("Merging contents: %s" % cont_list)
        contents_dict = merge_contents(cont_list)

        outfile = cont_list[0].replace(join(spooldir,
                                            repos['devuan']['dists']),
                                       join(mergedir, mergesubdir))
        print("Writing contents: %s" % outfile)
        write_contents(contents_dict, outfile)


def main():
    """
    Main function to allow multiprocessing.
    """
    cont = []
    for i in arches:
        for j in categories:
            if i != 'source':
                cont.append(join(j, i.replace('binary', 'Contents')+'.gz'))
            else:
                cont.append(join(j, 'Contents-'+i+'.gz'))

    mrgpool = Pool(cpunm)
    mrgpool.map(main_merge, cont)
    mrgpool.close()


if __name__ == '__main__':
    t1 = time()
    main()
    t2 = time()
    print('total time: %s' % (t2 - t1))
