#!/usr/bin/env python
# copyright (c) 2017 - Ivan J. <parazyd@dyne.org>
# see LICENSE file for copyright and license details

import ast
import gzip
import re
import requests
import time

import config
from log import notice


def get_time(date):
    return time.mktime(time.strptime(date, "%a, %d %b %Y %H:%M:%S %Z"))


def get_date(relfile):
    match = re.search('Date: .+', relfile)
    if match:
        line = relfile[match.start():match.end()]
        relfile = line.split(': ')[1]
    return relfile


def parse_release(reltext):
    hash = {}
    match = re.search('SHA256:+', reltext)
    if match:
        line = reltext[match.start():-1]
        for i in line.split('\n'):
            if i == 'SHA256:' or i == '\n':  # XXX: hack
                continue
            hash[(i.split()[2])] = i.split()[0]
        return hash


def parse_package(entry):
    # for parsing a single package
    values = re.split('\\n[A-Z].+?:', entry)[0:]
    values[0] = values[0].split(':')[1]
    keys = re.findall('\\n[A-Z].+?:', '\n' + entry)
    both = zip(keys, values)
    return {key.lstrip(): value for key, value in both}


def parse_packages(pkgtext):
    # this parses our package file into a hashmap
    # key: package name, value: entire package paragraph as a hashmap
    map = {}

    # TODO: consider also this approach
    # def parse_packages(pkgfilepath):
    # with gzip.open(pkgfilepath, "rb") as f:
    #    pkgs = f.read().split("\n\n")

    pkgs = pkgtext.split("\n\n")
    for pkg in pkgs:
        m = re.match('Package: .+', pkg)
        if m:
            line = pkg[m.start():m.end()]
            key = line.split(': ')[1]
            map[key] = parse_package(pkg)
    return map


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
