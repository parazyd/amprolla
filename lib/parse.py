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


def compare_epochs(epo1, epo2):
    """
    Compares two given epochs and returns their difference.
    """
    return int(epo1) - int(epo2)


def get_epoch(ver):
    """
    Parses and returns the epoch, and the rest, split of a version string.
    """
    if ':' in ver:
        return ver.split(':', 1)
    return "0", ver


def get_upstream(rest):
    """
    Separate upstream_version from debian-version. The latter is whatever is
    found after the last "-" (hyphen)
    """
    split_s = rest.rsplit('-', 1)
    if len(split_s) < 2:
        return split_s[0], ""
    return split_s


def get_non_digit(s):
    """
    Get a string and return the longest leading substring consisting exclusively
    of non-digits (or an empty string), and the remaining substring.
    """
    if not s:
        return "", ""
    head = ""
    tail = s
    N = len(s)
    i = 0
    while i < N and not s[i].isdigit():
        head += s[i]
        tail = tail[1:]
        i += 1
    return head, tail


def get_digit(s):
    """
    Get a string and return the integer value of the longest leading substring
    consisting exclusively of digit characters (or zero otherwise), and the
    remaining substring.
    """
    if not s:
        return 0, ""
    head = ""
    tail = s
    N = len(s)
    i = 0
    while i < N and s[i].isdigit():
        head += s[i]
        tail = tail[1:]
        i += 1
    return int(head), tail


def char_val(c):
    """
    Returns an integer value of a given unicode character. Returns 0 on ~ (since
    this is in Debian's policy)
    """
    if c == '~':
        return 0
    elif not c.isalpha():
        return 256 + ord(c)
    return ord(c)


def compare_deb_str(a1, a2):
    while len(a1) > 0 and len(a2) > 0:
        char_diff = char_val(a1[0]) - char_val(a2[0])
        if char_diff != 0:
            return char_diff
        a1 = a1[1:]
        a2 = a2[1:]
    if len(a1) == 0:
        if len(a2) == 0:
            return 0
        else:
            if a2[0] == '~':
                return 512
            else:
                return -ord(a2[0])
    else:
        if a1[0] == '~':
            return -512
        else:
            return ord(a1[0])


def compare_non_epoch(s1, s2):
    cont = True
    while cont:
        alpha1, tail1 = get_non_digit(s1)
        alpha2, tail2 = get_non_digit(s2)
        if alpha1 == alpha2:
            if not tail1 and not tail2:
                diff = 0
                break
            num1, s1 = get_digit(tail1)
            num2, s2 = get_digit(tail2)
            if num1 == num2:
                cont = True
            else:
                diff = num1 - num2
                cont = False
        else:
            cont = False
            diff = compare_deb_str(alpha1, alpha2)

    return diff


def cmppkgver(ver1, ver2):
    """
    Main function to compare two package versions. Wraps around other functions
    to provide a result. It returns an integer < 0 if ver1 is earlier than ver2,
    0 if ver1 is the same as ver2, and an integer > 0 if ver2 is earlier than
    ver2.

    WARNING: The function does not induce a total order (i.e., return values
    MUST NOT be added or subtracted)

    https://www.debian.org/doc/debian-policy/#version
    """
    epoch1, rest1 = get_epoch(ver1)
    epoch2, rest2 = get_epoch(ver2)

    ec = compare_epochs(epoch1, epoch2)
    if ec != 0:
        # The two versions differ on epoch
        return ec

    upst1, rev1 = get_upstream(rest1)
    upst2, rev2 = get_upstream(rest2)

    up_diff = compare_non_epoch(upst1, upst2)
    if up_diff == 0:
        return compare_non_epoch(rev1, rev2)
    return up_diff


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
