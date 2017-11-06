# See LICENSE file for copyright and license details.

"""
Package merging functions and helpers
"""

from os import makedirs
from os.path import dirname, isfile, join
from gzip import open as gzip_open
# from lzma import open as lzma_open
from shutil import copyfile

import lib.globalvars as globalvars
from lib.config import mergedir, packages_keys, sources_keys, spooldir
from lib.log import logtofile
from lib.parse import parse_dependencies, parse_packages


def write_packages(packages, filename, sort=True, sources=False):
    """
    Writes `packages` to a file (per debian Packages format)
    If sort=True, the packages are sorted by name.
    """
    makedirs(dirname(filename), exist_ok=True)

    # Copy the arch-specific Release file from devuan if it's not there
    bsnm = 'Packages.gz'
    if sources:
        bsnm = 'Sources.gz'
    rl = filename.replace(bsnm, 'Release')
    sprl = rl.replace(mergedir, join(spooldir, 'devuan'))
    if not isfile(rl) and isfile(sprl):
        copyfile(sprl, rl)

    gzf = gzip_open(filename, 'w')
    # xzf = lzma_open(filename.replace('.gz', '.xz'), 'w')
    # f = open(filename.replace('.gz', ''), 'wb')

    pkg_items = packages.items()
    if sort:
        pkg_items = sorted(pkg_items, key=lambda x: x[0])

    if sources:
        keylist = sources_keys
    else:
        keylist = packages_keys

    for pkg_name, pkg_contents in pkg_items:
        for key in keylist:
            if key in pkg_contents:
                s = '%s: %s\n' % (key, pkg_contents[key])
                gzf.write(s.encode('utf-8'))
                # xzf.write(s.encode('utf-8'))
                # f.write(s.encode('utf-8'))
        gzf.write(b'\n')
        # xzf.write(b'\n')
        # f.write(b'\n')

    gzf.close()
    # xzf.close()
    # f.close()


def load_packages_file(filename):
    """
    Load a gzip'd packages file.
    Returns a dictionary of package name and package key-values.
    """
    # TODO: should we skip files like this if they don't exist?
    if filename is not None and isfile(filename):
        packages_contents = gzip_open(filename).read()
        packages_contents = packages_contents.decode('utf-8')
        return parse_packages(packages_contents)

    return None


def package_banned(pkg, banned_pkgs):
    """
    Returns True is the package contains a banned dependency.
    Currently checks and parses both the 'Depends:' and the 'Pre-Depends'
    fields of the package.
    """
    if pkg.get('Package') in banned_pkgs:
        logtofile('bannedpackages.txt', '%s,%s\n' % (globalvars.suite,
                                                     pkg.get('Package')))
        return True

    depends = parse_dependencies(pkg.get('Depends', ''))
    pre_depends = parse_dependencies(pkg.get('Pre-Depends', ''))

    depends = [v for v in depends]
    pre_depends = [v for v in pre_depends]

    deps = set(depends).union(set(pre_depends))

    if 'libsystemd0' in deps:
        logtofile('libsystemd.txt', '%s,%s\n' % (globalvars.suite,
                                                 pkg.get('Package')))

    if bool(deps.intersection(banned_pkgs)):
        logtofile('bannedpackages.txt', '%s,%s\n' % (globalvars.suite,
                                                     pkg.get('Package')))
    return bool(deps.intersection(banned_pkgs))


def package_newer(pkg1, pkg2):
    """
    Checks whether the package of a lower priority is newer than the package
    of the higher priority and returns True if so.
    """
    higher_prio = pkg1.get('Version').split('+')
    lower_prio = pkg2.get('Version').split('+')

    if lower_prio[0] > higher_prio[0]:
        return True

    return False


def merge_packages(pkg1, pkg2, name1, name2, banned_packages=set(),
                   rewriter=None):
    """
    Merges two previously loaded/parsed (using load_packages_file) packages
    dictionaries, preferring `pkg1` over `pkg2`, and optionally discarding any
    banned packages.
    """
    new_pkgs = {}
    package_names = set(pkg1.keys()).union(set(pkg2.keys()))
    obsoletepkgs = []

    for pkg in package_names:
        pkg1_pkg = pkg1.get(pkg)
        pkg2_pkg = pkg2.get(pkg)

        if pkg1_pkg and pkg2_pkg:
            if rewriter:
                pkg1_pkg = rewriter(pkg1_pkg, name1)
            new_pkgs[pkg] = pkg1_pkg
            if package_newer(pkg1_pkg, pkg2_pkg):
                obsoletepkgs.append('%s,%s,%s,%s' % (globalvars.suite,
                                                     pkg1_pkg.get('Package'),
                                                     pkg1_pkg.get('Version'),
                                                     pkg2_pkg.get('Version')))
        elif pkg1_pkg:
            if not package_banned(pkg1_pkg, banned_packages):
                if rewriter:
                    pkg1_pkg = rewriter(pkg1_pkg, name1)
                new_pkgs[pkg] = pkg1_pkg
        elif pkg2_pkg:
            if not package_banned(pkg2_pkg, banned_packages):
                if rewriter:
                    pkg2_pkg = rewriter(pkg2_pkg, name2)
                new_pkgs[pkg] = pkg2_pkg
        else:
            assert False, 'Impossibru'

    if obsoletepkgs:
        obsoletepkgs = '\n'.join(obsoletepkgs)
        logtofile('%s-oldpackages.txt' % globalvars.suite, obsoletepkgs,
                  redo=True)

    return new_pkgs


def merge_packages_many(packages, banned_packages=set(), rewriter=None):
    """
    Merges two (or more) previously loaded/parsed (using load_packages_file)
    packages dictionaries, priority is defined by the order of the `packages`
    list, optionally discarding any banned packages.
    """
    if not len(packages) > 1:
        while not len(packages) > 1:
            packages.append({'name': '', 'packages': {}})

    new_pkgs = {}

    pkg1 = packages[0]
    pkg2 = packages[1]

    new_pkgs = merge_packages(pkg1['packages'], pkg2['packages'],
                              pkg1['name'], pkg2['name'],
                              banned_packages=banned_packages,
                              rewriter=rewriter)

    for pkg in packages[2:]:
        new_pkgs = merge_packages(new_pkgs, pkg['packages'], '', pkg['name'],
                                  banned_packages=banned_packages)

    return new_pkgs
