#!/usr/bin/env python3
# see LICENSE file for copyright and license details

from os.path import join
from lib.config import arches, categories
from multiprocessing import Pool


pkg = []
for i in arches:
    for j in categories:
        pkg.append(join(j, i, 'Packages.gz'))
        pkg.append(join(j, 'debian-installer', i, 'Packages.gz'))


#print(pkg)
am = __import__('amprolla_merge')

p = Pool(4)
p.map(am.main, pkg)
