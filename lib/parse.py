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
            key = line.split(': ')[0]
            val = line.split(': ')[1]
            metadata[key] = val

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

            val = line.split(':', 1)
            key = val[0]
            value = val[1][1:]

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
    ret = {}

    for pkg_plus_version in dependencies.split(', '):
        ver = pkg_plus_version.split(' ', 1)
        name = ver[0]

        # If we get passed an empty string, the name is '', and we just
        # outright stop
        if not name:
            return {}

        if len(ver) == 2:
            version = ver[1]
            ret[name] = version
        else:
            ret[name] = None

    return ret


def compare_dict(dic1, dic2):
    """
    Compares two dicts
    Takes two dicts and returns a dict of tuples with the differences.

    Example input:

        dic1={'foo': 'bar'}, dic2={'foo': 'baz'}

    Example output:

        {'foo': ('bar', 'baz')}
    """
    d1_keys = set(dic1.keys())
    d2_keys = set(dic2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    mod = {o: (dic1[o], dic2[o]) for o in intersect_keys if dic1[o] != dic2[o]}
    return mod
