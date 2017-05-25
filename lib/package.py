from gzip import open as gzip_open

from lib.parse import (parse_packages, parse_dependencies)
from lib.config import packages_keys

def write_packages(packages, filename, sort=False):
    """
    Writes `packages` to a file (per debian Packages format)
    If sort=True, the packages are sorted by name.
    """
    f = open(filename, 'w+')

    pkg_items = packages.items()
    if sort:
        pkg_items = sorted(pkg_items, key=lambda x: x[0])

    for pkg_name, pkg_contents in pkg_items:
        for key in packages_keys:
            if key in pkg_contents:
                f.write('%s: %s\n' % (key, pkg_contents[key]))
        f.write('\n')

    f.close()

def load_packages_file(filename):
    """ Load a gzip'd packages file.
    Returns a dictionary of package name and package key-values.
    """
    packages_contents = gzip_open(filename).read()
    packages_contents = packages_contents.decode('utf-8')
    return parse_packages(packages_contents)


def package_banned(pkg, banned_pkgs):
    """
    Returns True is the package contains a banned dependency.
    Currently checks and parses both the 'Depends:' and the 'Pre-Depends' fields
    of the package.
    """
    if pkg.get('Package') in banned_pkgs:
        return True

    depends = parse_dependencies(pkg.get('Depends', ''))
    pre_depends = parse_dependencies(pkg.get('Pre-Depends', ''))

    depends = [v[0] for v in depends]
    pre_depends = [v[0] for v in pre_depends]

    deps = set(depends).union(set(pre_depends))

    return bool(deps.intersection(banned_pkgs))


def merge_packages(pkg1, pkg2, banned_packages=set()):
    """
    Merges two previously loaded/parsed (using load_packages_file) packages
    dictionaries, preferring `pkg1` over `pkg2`, and optionally discarding any
    banned packages.
    """
    new_pkgs = {}
    package_names = set(pkg1.keys()).union(set(pkg2.keys()))

    for pkg in package_names:
        pkg1_pkg = pkg1.get(pkg)
        pkg2_pkg = pkg2.get(pkg)

        if pkg1_pkg and pkg2_pkg:
            new_pkgs[pkg] = pkg1_pkg
        elif pkg1_pkg:
            if not package_banned(pkg1_pkg, banned_packages):
                new_pkgs[pkg] = pkg1_pkg
        elif pkg2_pkg:
            if not package_banned(pkg2_pkg, banned_packages):
                new_pkgs[pkg] = pkg2_pkg
        else:
            assert False, 'Impossibru'

    return new_pkgs

def merge_packages_many(packages, banned_packages=set()): # TODO: Make generic
    """
    Merges two (or more) previously loaded/parsed (using load_packages_file)
    packages dictionaries, priority is defined by the order of the `packages`
    list, optionally discarding any banned packages.
    """
    assert len(packages) > 1

    new_pkgs = {}

    pkg1 = packages[0]
    pkg2 = packages[1]

    new_pkgs = merge_packages(pkg1, pkg2, banned_packages=banned_packages)

    for pkg in packages[2:]:
        new_pkgs = merge_packages(new_pkgs, pkg, banned_packages=banned_packages)

    return new_pkgs
