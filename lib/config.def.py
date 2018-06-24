# See LICENSE file for copyright and license details.

"""
amprolla configuration file
"""

# from hashlib import md5, sha1, sha256
from hashlib import sha256

cpunm = 2  # number of cpus you want to use for multiprocessing
logdir = '/home/amprolla/amprolla/log'
spooldir = '/home/amprolla/amprolla/spool'
gpgdir = '/home/amprolla/amprolla/gnupg'
signingkey = 'E032601B7CA10BC3EA53FA81BB23C00C61FC752C'
signrelease = True
mergedir = '/home/amprolla/amprolla/merged-volatile'
mergesubdir = 'dists'
lockpath = '/run/lock/amprolla.lock'
banpkgs = {'systemd', 'systemd-sysv', 'file-rc'}
checksums = [
    # {'name': 'MD5Sum', 'f': md5},
    # {'name': 'SHA1', 'f': sha1},
    {'name': 'SHA256', 'f': sha256},
]

distrolabel = 'Devuan'
repo_order = ['devuan', 'debian-security', 'debian']

# used for a hacky way to skip certain suites when crawling Debian
skips = ['jessie-security', 'ascii-security', 'beowulf-security']

repos = {
    'devuan': {
        'name': 'DEVUAN',
        'host': 'http://pkgmaster.devuan.org',
        'dists': 'devuan/dists',
        'pool': 'devuan/pool',
        'aliases': False,
        'skipmissing': False,
    },
    'debian-security': {
        'name': 'DEBIAN-SECURITY',
        'host': 'http://security.debian.org',
        'dists': 'dists',
        'pool': 'pool',
        'aliases': True,
        'skipmissing': True,
    },
    'debian': {
        'name': 'DEBIAN',
        'host': 'http://deb.debian.org',
        'dists': 'debian/dists',
        'pool': 'debian/pool',
        'aliases': True,
        'skipmissing': False,
    },
}

suites = {
    'jessie': [
        'jessie',
        'jessie-backports',
        'jessie-proposed-updates',
        'jessie-security',
        'jessie-updates',
    ],
    'ascii': [
        'ascii',
        'ascii-backports',
        'ascii-proposed-updates',
        'ascii-security',
        'ascii-updates',
    ],
    'beowulf': [
        'beowulf',
        # 'beowulf-backports',
        'beowulf-proposed-updates',
        'beowulf-security',
        'beowulf-updates',
    ],
    'unstable': [
        'unstable',
    ],
}

aliases = {
    'DEBIAN-SECURITY': {
        'beowulf-security': 'buster/updates',
        'ascii-security': 'stretch/updates',
        'jessie-security': 'jessie/updates',
    },
    'DEBIAN': {
        'beowulf': 'buster',
        'beowulf-backports': 'buster-backports',
        'beowulf-proposed-updates': 'buster-proposed-updates',
        'beowulf-updates': 'buster-updates',

        'ascii': 'stretch',
        'ascii-backports': 'stretch-backports',
        'ascii-proposed-updates': 'stretch-proposed-updates',
        'ascii-updates': 'stretch-updates',
    },
}

release_aliases = {
    'beowulf': {
        'Suite': 'testing',
        'Codename': 'beowulf',
        'Version': '3.0',
        'Origin': 'Devuan',
    },
    'beowulf-backports': {
        'Suite': 'testing-backports',
        'Codename': 'beowulf-backports',
        'Origin': 'Devuan Backports',
        'Label': 'Devuan Backports',
    },
    'beowulf-proposed-updates': {
        'Suite': 'testing-proposed-updates',
        'Codename': 'beowulf-proposed-updates',
    },
    'beowulf-security': {
        'Suite': 'testing-security',
        'Codename': 'beowulf-security',
        'Label': 'Devuan-Security',
        'Origin': 'Devuan',
    },
    'beowulf-updates': {
        'Suite': 'testing-updates',
        'Codename': 'beowulf-updates',
        'Origin': 'Devuan',
    },

    'ascii': {
        'Suite': 'stable',
        'Codename': 'ascii',
        'Version': '2.0',
        'Origin': 'Devuan',
    },
    'ascii-backports': {
        'Suite': 'stable-backports',
        'Codename': 'ascii-backports',
        'Origin': 'Devuan Backports',
        'Label': 'Devuan Backports',
    },
    'ascii-proposed-updates': {
        'Suite': 'stable-proposed-updates',
        'Codename': 'ascii-proposed-updates',
    },
    'ascii-security': {
        'Suite': 'stable-security',
        'Codename': 'ascii-security',
        'Label': 'Devuan-Security',
        'Origin': 'Devuan',
    },
    'ascii-updates': {
        'Suite': 'stable-updates',
        'Codename': 'ascii-updates',
        'Origin': 'Devuan',
    },

    'jessie': {
        'Suite': 'oldstable',
        'Codename': 'jessie',
        'Version': '1.0',
        'Origin': 'Devuan',
    },
    'jessie-backports': {
        'Suite': 'oldstable-backports',
        'Codename': 'jessie-backports',
        'Origin': 'Devuan Backports',
    },
    'jessie-proposed-updates': {
        'Suite': 'oldstable-proposed-updates',
        'Codename': 'jessie-proposed-updates',
    },
    'jessie-security': {
        'Suite': 'oldstable-security',
        'Codename': 'jessie-security',
        'Label': 'Devuan-Security',
        'Origin': 'Devuan',
    },
    'jessie-updates': {
        'Suite': 'oldstable-updates',
        'Codename': 'jessie-updates',
        'Origin': 'Devuan',
    },
}

categories = ['main', 'contrib', 'non-free']

arches = [
    'source',
    'binary-all',
    # 'binary-alpha',
    'binary-amd64',
    'binary-arm64',
    'binary-armel',
    'binary-armhf',
    # 'binary-hppa',
    # 'binary-hurd-i386',
    'binary-i386',
    # 'binary-ia64',
    # 'binary-kfreebsd-amd64',
    # 'binary-kfreebsd-i386',
    # 'binary-mips',
    # 'binary-mips64el',
    # 'binary-mipsel',
    # 'binary-powerpc',
    'binary-ppc64el',
    # 'binary-s390x',
    # 'binary-sparc',
]

mainrepofiles = [
    'InRelease',
    'Release',
    'Release.gpg',
]

pkgfiles = [
    'Packages',
    'Packages.gz',
    'Packages.xz',
    'Release',
]

srcfiles = [
    'Sources',
    'Sources.gz',
    'Sources.xz',
    'Release',
]

release_keys = [
    'Origin',
    'Label',
    'Suite',
    'Version',
    'Codename',
    'Date',
    'Valid-Until',
    'Architectures',
    'Components',
    'Description',
    'NotAutomatic',
    'ButAutomaticUpgrades',
]

packages_keys = [
    'Package',
    'Version',
    'Kernel-Version',
    'Installer-Menu-Item',
    'Essential',
    'Installed-Size',
    'Maintainer',
    'Architecture',
    'Replaces',
    'Provides',
    'Depends',
    'Conflicts',
    'Pre-Depends',
    'Breaks',
    'Homepage',
    'Apport',
    'Auto-Built-Package',
    'Build-Ids',
    'Origin',
    'Bugs',
    'Built-Using',
    'Enhances',
    'Recommends',
    'Description',
    'Description-md5',
    'Ghc-Package',
    'Gstreamer-Decoders',
    'Gstreamer-Elements',
    'Gstreamer-Encoders',
    'Gstreamer-Uri-Sinks',
    'Gstreamer-Uri-Sources',
    'Gstreamer-Version',
    'Lua-Versions',
    'Modaliases',
    'Npp-Applications',
    'Npp-Description',
    'Npp-File',
    'Npp-Mimetype',
    'Npp-Name',
    'Original-Maintainer',
    'Original-Source-Maintainer',
    'Package-Type',
    'Postgresql-Version',
    'Python-Version',
    'Python-Versions',
    'Ruby-Versions',
    'Source',
    'Suggests',
    'Xul-Appid',
    'Multi-Arch',
    'Build-Essential',
    'Tag',
    'Section',
    'Priority',
    'Filename',
    'Size',
    'MD5sum',
    'SHA1',
    'SHA256',
]

sources_keys = [
    'Package',
    'Binary',
    'Version',
    'Maintainer',
    'Uploaders',
    'Build-Depends',
    'Architecture',
    'Standards-Version',
    'Format',
    'Files',
    'Vcs-Browser',
    'Vcs-Svn',
    'Checksums-Sha1',
    'Checksums-Sha256',
    'Homepage',
    'Package-List',
    'Directory',
    'Priority',
    'Section',
    'Vcs-Git',
    'Dm-Upload-Allowed',
    'Build-Conflicts',
    'Testsuite',
    'Build-Depends-Indep',
    'Vcs-Bzr',
    'Vcs-Mtn',
    'Vcs-Hg',
    'Ruby-Versions',
    'Dgit',
    'Vcs-Darcs',
    'Extra-Source-Only',
    'Python-Version',
    'Testsuite-Triggers',
    'Autobuild',
    'Build-Conflicts-Indep',
    'Vcs-Cvs',
    'Comment',
    'Origin',
    'Vcs-Arch',
    'Original-Maintainer',
    'Python3-Version',
]
