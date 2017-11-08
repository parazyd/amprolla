# See LICENSE file for copyright and license details.

"""
amprolla configuration file
"""

# from hashlib import md5, sha1, sha256
from hashlib import sha256

cpunm = 4  # number of cpus you want to use for multiprocessing
logdir = './log'
spooldir = './spool'
gpgdir = './gnupg'
signingkey = 'CA608125'
signrelease = True
mergedir = './merged-volatile'
mergesubdir = 'dists'
banpkgs = {'systemd', 'systemd-sysv'}
checksums = [
    # {'name': 'MD5Sum', 'f': md5},
    # {'name': 'SHA1', 'f': sha1},
    {'name': 'SHA256', 'f': sha256},
]

distrolabel = 'Devuan'
repo_order = ['devuan', 'debian-security', 'debian']

repos = {
    'devuan': {
        'name': 'DEVUAN',
        'host': 'http://auto.mirror.devuan.org',
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
    'unstable': [
        'unstable',
    ]
}

aliases = {
    'DEBIAN-SECURITY': {
        'ascii-security': 'stretch/updates',
        'jessie-security': 'jessie/updates',
    },
    'DEBIAN': {
        'ascii': 'stretch',
        'ascii-backports': 'stretch-backports',
        'ascii-proposed-updates': 'stretch-proposed-updates',
        'ascii-updates': 'stretch-updates',
    }
}

release_aliases = {
    'ascii': {
        'Suite': 'testing',
        'Codename': 'ascii',
        'Version': '2.0',
    },
    # backports always has:
    # Origin/Label: DISTRO Backports
    # Suite/Codename: CODENAME-backports
    'ascii-backports': {
        'Origin': 'Devuan Backports',
        'Label': 'Devuan Backports',
        'Suite': 'ascii-backports',
        'Codename': 'ascii-backports',
    },
    # proposed-updates has:
    # Suite: STABILITY-proposed-updates
    # Codename: CODENAME-proposed-updates
    # Except in stable where:
    # Suite: proposed-updates
    # Codename: CODENAME-proposed-updates
    'ascii-proposed-updates': {
        'Suite': 'testing-proposed-updates',
        'Codename': 'ascii-proposed-updates',
    },
    # security always has:
    # Label: DISTRO-Security
    # Suite: STABILITY
    # Codename: CODENAME
    'ascii-security': {
        'Label': 'Devuan-Security',
        'Suite': 'testing',
        'Codename': 'ascii',
    },
    # updates has:
    # Suite: STABILITY-updates
    # Codename: CODENAME-updates
    'ascii-updates': {
        'Suite': 'testing-updates',
        'Codename': 'ascii-updates',
    },

    'jessie': {
        'Suite': 'stable',
        'Codename': 'jessie',
        'Version': '1.0',
    },
    'jessie-backports': {
        'Origin': 'Devuan Backports',
        'Label': 'Devuan Backports',
        'Suite': 'jessie-backports',
        'Codename': 'jessie-backports',
    },
    'jessie-proposed-updates': {
        'Suite': 'proposed-updates',
        'Codename': 'jessie-proposed-updates'
    },
    'jessie-security': {
        'Label': 'Devuan-Security',
        'Suite': 'stable',
        'Codename': 'jessie',
    },
    'jessie-updates': {
        'Suite': 'stable-updates',
        'Codename': 'jessie-updates',
    }
}

categories = ['main', 'contrib', 'non-free']

arches = [
    'source',
    'binary-all',
    'binary-alpha',
    'binary-amd64',
    'binary-arm64',
    'binary-armel',
    'binary-armhf',
    'binary-hppa',
    'binary-hurd-i386',
    'binary-i386',
    'binary-ia64',
    'binary-kfreebsd-amd64',
    'binary-kfreebsd-i386',
    'binary-mips',
    'binary-mips64el',
    'binary-mipsel',
    'binary-powerpc',
    'binary-ppc64el',
    'binary-s390x',
    'binary-sparc'
]

mainrepofiles = [
    'InRelease',
    'Release',
    'Release.gpg'
]

pkgfiles = [
    'Packages',
    'Packages.gz',
    'Packages.xz',
    'Release'
]

srcfiles = [
    'Sources',
    'Sources.gz',
    'Sources.xz',
    'Release'
]

release_keys = [
    # 'Origin',
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
    'SHA256'
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
    'Python3-Version'
]
