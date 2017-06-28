# see LICENSE file for copyright and license details

"""
Release file functions and helpers
"""

from datetime import datetime, timedelta
from os.path import getsize, isfile
import gnupg

from lib.config import checksums, release_keys, signingkey
from lib.parse import parse_release_head


def write_release(oldrel, newrel, filelist, r, sign=True):
    """
    Generates a valid Release file
    if sign=False: do not use gnupg to sign the file

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
    gpg = gnupg.GPG()

    stream = open(infile, 'rb')

    # Clearsign
    gpg.sign_file(stream, keyid=signingkey, clearsign=True, detach=False,
                  output=infile.replace('Release', 'InRelease'))

    # Detached signature (somewhat broken?)
    # gpg.sign_file(stream, keyid=signingkey, clearsign=False, detach=True,
    #              output=infile + '.gpg')
