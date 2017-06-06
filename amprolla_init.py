#!/usr/bin/env python3
# see LICENSE file for copyright and license details

"""
This module will download the initial Release files used to populate
the spooldir, along with all the files hashed inside the Release files
"""

from os.path import join
from multiprocessing import Pool

from lib.config import repos, suites, aliases, spooldir, mainrepofiles
from lib.net import download
from lib.parse import parse_release


def pop_dirs(repo):
    """
    Crawls through the directories to come up with complete needed
    directory structure.
    Returns a list of tuples holding the remote and local locations
    of the files
    Example:
        (http://auto.mirror.devuan.org/devuan/dists/jessie/main/binary-armhf/Packages.gz,
         ./spool/devuan/dists/unstable/contrib/binary-armhf/Packages.gz)
    """
    repodata = repos[repo]

    urls = []

    for i in suites:
        for j in suites[i]:
            baseurl = join(repodata['host'], repodata['dists'])
            suite = j
            if repodata['aliases'] is True:
                if j in aliases[repodata['name']]:
                    suite = aliases[repodata['name']][j]
                elif repodata['skipmissing'] is True:
                    continue
                skips = ['jessie-security', 'ascii-security']  # hack
                if repo == 'debian' and j in skips:
                    continue
            pair = (join(baseurl, suite),
                    join(baseurl.replace(repodata['host'],
                                         spooldir), suite))
            urls.append(pair)

    return urls


def main():
    """
    Loops through all repositories, and downloads their *Release* files, along
    with all the files listed within those Release files.
    """
    for dist in repos:
        print('Downloading %s directory structure' % dist)
        dlurls = pop_dirs(dist)
        for url in dlurls:
            tpl = []
            for file in mainrepofiles:
                urls = (join(url[0], file), join(url[1], file))
                tpl.append(urls)
            dlpool = Pool(4)
            dlpool.map(download, tpl)
            dlpool.close()

            release_contents = open(join(url[1], 'Release')).read()
            release_contents = parse_release(release_contents)
            tpl = []
            for k in release_contents:
                # if k.endswith('/binary-armhf/Packages.gz'):
                urls = (join(url[0], k), join(url[1], k))
                tpl.append(urls)
            dlpool = Pool(4)
            dlpool.map(download, tpl)
            dlpool.close()


if __name__ == '__main__':
    main()
