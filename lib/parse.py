# See LICENSE file for copyright and license details.

"""
Parsing functions/helpers
"""

from time import mktime, strptime


def get_time(date):
    """
    Gets epoch time
    """
    if not date:
        # hardcode if something's amiss
        date = 'Sun, 29 Oct 2017 10:00:00 UTC'
    return mktime(strptime(date, '%a, %d %b %Y %H:%M:%S %Z'))


def get_date(relfile):
    """
    Gets the date from the contents of a Release file
    """
    date = None
    contents = relfile.split('\n')
    for line in contents:
        if line.startswith('Date: '):
            date = line.split(': ')[1]
            break
    return date


def parse_release(reltext):
    """
    Parses a Release file and returns a dict of the files we need
    key = filename, value = tuple of sha256sum and file size
    """
    hashes = {}

    contents = reltext.split('\n')

    sha256 = False
    for line in contents:
        if sha256 is True and line != '':
            filename = line.split()[2]
            filesize = line.split()[1]
            checksum = line.split()[0]
            hashes[filename] = (checksum, filesize)
        elif line.startswith('SHA256:'):
            sha256 = True

    return hashes


def parse_release_head(reltext):
    """
    Parses the header of the release file to grab needed metadata
    """
    metadata = {}

    contents = reltext.split('\n')

    splitter = 'MD5Sum:'

    md5sum = False
    for line in contents:
        if md5sum is True:
            break
        elif line.startswith(splitter):
            md5sum = True
        else:
            k = line.split(': ')[0]
            v = line.split(': ')[1]
            metadata[k] = v

    return metadata


def parse_package(entry):
    """
    Parses a single Packages entry
    """
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


def parse_packages(pkgtext):
    """
    Parses our package file contents into a hashmap
    key: package name, value: entire package paragraph as a hashmap
    """
    _map = {}

    pkgs = pkgtext.split('\n\n')
    for pkg in pkgs:
        single = pkg.split('\n')
        for line in single:
            if line.startswith('Package: '):
                key = line.split(': ')[1]
                _map[key] = parse_package(pkg)
                break

    return _map


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

        # If we get passed an empty string, the name is '', and we just
        # outright stop
        if not name:
            return {}

        if len(v) == 2:
            version = v[1]
            r[name] = version
        else:
            r[name] = None

    return r


def compare_dict(d1, d2):
    """
    Compares two dicts
    Takes two dicts and returns a dict of tuples with the differences.

    Example input:

        d1={'foo': 'bar'}, 22={'foo': 'baz'}

    Example output:

        {'foo': ('bar', 'baz')}
    """
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    return modified
