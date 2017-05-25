#!/usr/bin/env python
# copyright (c) 2017 - Ivan J. <parazyd@dyne.org>
# see LICENSE file for copyright and license details

import ast
import gzip
import re
#import requests
import time

from . import config
from .log import notice


def get_time(date):
    return time.mktime(time.strptime(date, "%a, %d %b %Y %H:%M:%S %Z"))


def get_date(relfile):
    match = re.search('Date: .+', relfile)
    if match:
        line = relfile[match.start():match.end()]
        relfile = line.split(': ')[1]
    return relfile


def parse_release(reltext):
    _hash = {}
    match = re.search('SHA256:+', reltext)
    if match:
        line = reltext[match.start():-1]
        for i in line.split('\n'):
            if i == 'SHA256:' or i == '\n':  # XXX: hack
                continue
            _hash[(i.split()[2])] = i.split()[0]
        return _hash


def parse_package(entry):
    """ Parses a single Packages entry """
    pkgs = {}

    contents = entry.split('\n')

    key = ''
    value = ''
    for line in contents:
        if line.startswith(' '):
            value += '\n' + line
        else:
            pkgs[key] = value

            v = line.split(':', 1)
            key = v[0]
            value = v[1][1:]

    if key:
        pkgs[key] = value

    return pkgs


PACKAGES_REGEX = re.compile('([A-Za-z0-9\-]+): ')
def parse_package_re(entry):
    """ Parses a single Packages entry """
    contents = PACKAGES_REGEX.split(entry)[1:]  # Throw away the first ''

    keys = contents[::2]
    vals = map(lambda x: x.strip(), contents[1::2])

    return dict(zip(keys, vals))


def parse_packages(pkgtext):
    # this parses our package file into a hashmap
    # key: package name, value: entire package paragraph as a hashmap
    map = {}

    pkgs = pkgtext.split("\n\n")
    for pkg in pkgs:
        m = re.match('Package: .+', pkg)
        if m:
            line = pkg[m.start():m.end()]
            key = line.split(': ')[1]
            map[key] = parse_package(pkg)

    return map

def parse_dependencies(dependencies):
    """
    Parses a dependency line from a debian Packages file.

    Example line::

        'lib6 (>= 2.4), libdbus-1-3 (>= 1.0.2), foo'

    Output::

        {'lib6': '(>= 2.4)', 'libdbus-1-3': '(>= 1.0.2)', 'foo': None}
    """
    r = {}

    for pkg_plus_version in dependencies.split(', '):
        v = pkg_plus_version.split(' ', 1)
        name = v[0]

        # If we get passed an empty string, the name is '', and we just outright
        # stop
        if not name:
            return {}

        if len(v) == 2:
            version = v[1]
            r[name] = version
        else:
            r[name] = None

    return r


def print_package(map, pkgname):
    try:
        pkg = ast.literal_eval(map[pkgname])
        sin = []
        for i in config.pkgfmt:
            if config.pkgfmt[i] in pkg.keys():
                sin.append(config.pkgfmt[i] + pkg[config.pkgfmt[i]])
        return sin
    except:
        log.die("nonexistent package")


def compare_dict(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    return modified


def compare_release(oldrel, newrel):
    r = requests.get(newrel)
    new = r.text
    with open(oldrel, "rb") as f:
        old = f.read()

    oldtime = get_time(get_date(old))
    newtime = get_time(get_date(new))
    if newtime > oldtime:
        notice("Update available")
        newhashes = parse_release(new)
        oldhashes = parse_release(old)
        changes = compare_dict(newhashes, oldhashes)
        # k = pkg name, v = sha256
        return changes


# relmap = compare_release("../spool/dists/jessie/updates/Release", "http://security.debian.org/dists/jessie/updates/Release")
# print relmap
# for k,v in relmap.iteritems():
#    print(k)
