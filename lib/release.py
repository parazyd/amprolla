# See LICENSE file for copyright and license details.

"""
Release file functions and helpers
"""

from datetime import datetime, timedelta
from gzip import decompress as gzip_decomp
from lzma import compress as lzma_comp
from os.path import getsize, isfile
from subprocess import Popen

import lib.globalvars as globalvars
from lib.config import (checksums, distrolabel, gpgdir, release_aliases,
                        release_keys, signingkey)
from lib.log import info
from lib.parse import parse_release_head, parse_release


def rewrite_release_head(headers):
    """
    Rewrites the necessary headers in a Release file
    Used to override needed values defined in config.release_aliases
    """
    if headers['Suite'] in release_aliases:
        headers['Label'] = distrolabel
        suitename = headers['Suite']
        for var in release_aliases[suitename]:
            headers[var] = release_aliases[suitename][var]

    return headers


def write_release(oldrel, newrel, filelist, r, sign=True, rewrite=True):
    """
    Generates a valid Release file
    if sign=False: do not use gnupg to sign the file
    if rewrite=True: rewrite the Release headers as defined in the config

    Arguments taken: oldrel, newrel, filelist, r
        * location of the old Release file (used to take metadata)
        * location where to write the new Release file
        * list of files to make checksums
        * string to remove from the path of the hashed file
    """
    t1 = datetime.utcnow()
    # t2 = datetime.utcnow() + timedelta(days=7)

    prettyt1 = t1.strftime('%a, %d %b %Y %H:%M:%S UTC')
    # prettyt2 = t2.strftime('%a, %d %b %Y %H:%M:%S UTC')

    # this holds our local data in case we don't want to rehash files
    local_rel = open(newrel).read()
    local_rel = parse_release(local_rel)

    old = open(oldrel).read()
    new = open(newrel, 'w')

    rel_cont = parse_release_head(old)

    rel_cont['Date'] = prettyt1
    # rel_cont['Valid-Until'] = prettyt2

    if rewrite:
        rel_cont = rewrite_release_head(rel_cont)

    for k in release_keys:
        if k in rel_cont:
            new.write('%s: %s\n' % (k, rel_cont[k]))

    if globalvars.rehash:
        rehash_release(filelist, new, r)
    else:
        info('Reusing old checksums')
        for csum in checksums:
            new.write('%s:\n' % csum['name'])
            for i, j in local_rel.items():
                new.write(' %s %8s %s\n' % (j[0], j[1], i))

    new.close()

    if sign:
        sign_release(newrel)


def rehash_release(_filelist, fd, r):
    """
    Calculates checksums of a given filelist and writes them to the given
    file descriptor. Takes r as the third argument, which is a string to
    remove from the path of the hashed file when writing it to a file.
    """
    info('Hashing checksums')
    for csum in checksums:
        fd.write('%s:\n' % csum['name'])
        for f in _filelist:
            if isfile(f):
                cont = open(f, 'rb').read()
                fd.write(' %s %8s %s\n' % (csum['f'](cont).hexdigest(),
                                           getsize(f), f.replace(r+'/', '')))
            elif f.endswith('.xz') and isfile(f.replace('.xz', '.gz')):
                xzstr = lzma_comp(open(f.replace('.xz', '.gz'), 'rb').read())
                fd.write(' %s %8s %s\n' % (csum['f'](xzstr).hexdigest(),
                                           len(xzstr), f.replace(r+'/', '')))
            elif not f.endswith('.gz') and isfile(f+'.gz'):
                uncomp = gzip_decomp(open(f+'.gz', 'rb').read())
                fd.write(' %s %8s %s\n' % (csum['f'](uncomp).hexdigest(),
                                           len(uncomp), f.replace(r+'/', '')))
    return


def sign_release(infile):
    """
    Signs both the clearsign and the detached signature of a Release file.

    Takes a valid path to a release file as an argument.
    """
    args = ['gpg', '-q', '--default-key', signingkey, '--batch', '--yes',
            '--homedir', gpgdir]

    clearargs = args + ['--clearsign', '-a', '-o',
                        infile.replace('Release', 'InRelease'), infile]
    detachargs = args + ['-sb', '-o', infile+'.gpg', infile]

    info('Signing Release (clearsign)')
    cleargpg = Popen(clearargs)
    cleargpg.wait(timeout=5)

    info('Signing Release (detached sign)')
    detachgpg = Popen(detachargs)
    detachgpg.wait(timeout=5)
