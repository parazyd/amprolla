#!/usr/bin/env python
# copyright (c) 2017 - Ivan J. <parazyd@dyne.org>
# see LICENSE file for copyright and license details

amprolla = {
    "spooldir": "./spool",
    "sign_key": "fa1b0274",
    "mergedir": "./merged",
    "mergedsubdirs": ["dists", "pool"],
    "banpkgs": ['systemd', 'systemd-sysv']
    #"checksums": [ 'md5sum', 'sha1', 'sha256', 'sha512' ]
}

repos = {
    # key name is priority, first is 0
    0: {
        "name": "DEVUAN",
        "host": "packages.devuan.org",
        "dists": "devuan/dists",
        "pool": "devuan/pool",
        "aliases": False,
        "skipmissing": False
    },
    1: {
        "name": "DEBIAN-SECURITY",
        "host": "security.debian.org",
        "dists": "dists",
        "pool": "pool",
        "aliases": True,
        "skipmissing": True
    },
    2: {
        "name": "DEBIAN",
        #"host": "httpredir.debian.org",
        "host": "ftp.debian.org",
        "dists": "debian/dists",
        "pool": "debian/pool",
        "aliases": True,
        "skipmissing": False
    }
}

suites = {
    'jessie': [
        'jessie',
        'jessie-backports',
        'jessie-proposed-updates',
        'jessie-security',
        'jessie-updates'
    ],
    'ascii': [
        'ascii',
        'ascii-backports',
        'ascii-proposed-updates',
        'ascii-security',
        'ascii-updates'
    ],
    'unstable': [
        'unstable'
    ]
}

aliases = {
    "DEBIAN-SECURITY": {
        'ascii-security': 'testing/updates',
        'jessie-security': 'jessie/updates'
    },
    "DEBIAN": {
        'ascii': 'testing',
        'ascii-backports': 'testing-backports',
        'ascii-proposed-updates': 'testing-proposed-updates',
        'ascii-updates': 'testing-updates'
    }
}

categories = ['main', 'contrib', 'non-free']


releases = {
    "Release-jessie": {
        "Suite": "stable",
        "Codename": "jessie",
        "Label": "Devuan",
        "Version": "1.0",
        "Description": "Devuan 1.0 Jessie (stable release)"
    },
    "Release-ascii": {
        "Suite": "testing",
        "Codename": "ascii",
        "Label": "Devuan",
        "Version": "2.0",
        "Description": "Devuan 2.0 Ascii (testing release)"
    },
    "Release-unstable": {
        "Suite": "unstable",
        "Codename": "ceres",
        "Label": "Devuan",
        "Version": "x.x",
        "Description": "Devuan x.x Ceres (unstable release)"
    }
}


binaryarches = [
    'all',
    'alpha',
    'amd64',
    'arm64',
    'armel',
    'armhf',
    'hppa',
    'hurd-i386',
    'i386',
    'ia64',
    'kfreebsd-amd64',
    'kfreebsd-i386',
    'mips',
    'mips64el',
    'mipsel',
    'powerpc',
    'ppc64el',
    's390x',
    'sparc'
]

installerarches = [
    'amd64',
    'arm64',
    'armel',
    'i386'
]

mainrepofiles = [
    "InRelease",
    "Release",
    "Release.gpg"
]

pkgfmt = [
    'Package:',
    'Version:',
    'Essential:',
    'Installed-Size:',
    'Maintainer:',
    'Architecture:',
    'Replaces:',
    'Provides:',
    'Depends:',
    'Conflicts:',
    'Pre-Depends:',
    'Breaks:',
    'Homepage:',
    'Apport:',
    'Auto-Built-Package:',
    'Build-Ids',
    'Origin:',
    'Bugs:',
    'Built-Using:',
    'Enhances:',
    'Recommends:',
    'Description:',
    'Description-md5:',
    'Ghc-Package:',
    'Gstreamer-Decoders:',
    'Gstreamer-Elements:',
    'Gstreamer-Encoders:',
    'Gstreamer-Uri-Sinks:',
    'Gstreamer-Uri-Sources:',
    'Gstreamer-Version:',
    'Lua-Versions:',
    'Modaliases:',
    'Npp-Applications:',
    'Npp-Description:',
    'Npp-File:',
    'Npp-Mimetype:',
    'Npp-Name:',
    'Origin:',
    'Original-Maintainer:',
    'Original-Source-Maintainer:',
    'Package-Type:',
    'Postgresql-Version:',
    'Python-Version:',
    'Python-Versions:',
    'Ruby-Versions:',
    'Source:',
    'Suggests:',
    'Xul-Appid:',
    'Multi-Arch:',
    'Build-Essential:',
    'Tag:',
    'Section:',
    'Priority:',
    'Filename:',
    'Size:',
    'MD5sum:',
    'SHA1:',
    'SHA256:'
]
