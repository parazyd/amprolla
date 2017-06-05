#!/usr/bin/env python3
# see LICENSE file for copyright and license details

from os.path import join
from lib.config import arches, categories
from multiprocessing import Pool


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
