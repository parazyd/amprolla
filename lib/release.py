# see LICENSE file for copyright and license details

"""
Release file functions and helpers
"""

from datetime import datetime, timedelta
from os.path import getsize, isfile
import gnupg

from lib.config import (checksums, distrolabel, gpgdir, release_aliases,
                        release_keys, signingkey)
from lib.parse import parse_release_head


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

    for csum in checksums:
        new.write('%s:\n' % csum['name'])
        for f in filelist:
            if isfile(f):
                cont = open(f, 'rb').read()
                new.write(' %s %8s %s\n' % (csum['f'](cont).hexdigest(),
                                            getsize(f), f.replace(r+'/', '')))

    new.close()

    if sign:
        sign_release(newrel)


def sign_release(infile):
    """
    Signs both the clearsign and the detached signature of a Release file
    """
    gpg = gnupg.GPG(gnupghome=gpgdir)

    stream = open(infile, 'rb')

    # Clearsign
    signed_data = gpg.sign_file(stream, keyid=signingkey, clearsign=True,
                                detach=False)
    inrel = open(infile.replace('Release', 'InRelease'), 'wb')
    inrel.write(signed_data.data)
    inrel.close()

    # Detached signature (somewhat broken?)
    # gpg.sign_file(stream, keyid=signingkey, clearsign=False, detach=True,
    #              output=infile + '.gpg')
