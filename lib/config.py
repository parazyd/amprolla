#!/usr/bin/env python
# copyright (c) 2017 - Ivan J. <parazyd@dyne.org>
# see LICENSE file for copyright and license details

spooldir = './spool'
sign_key = 'fa1b0274'
mergedir = './merged'
mergedsubdirs = ['dists', 'pool']
banpkgs = {'systemd', 'systemd-sysv'}
#checksums = [ 'md5sum', 'sha1', 'sha256', 'sha512' ]

repos = {
    'devuan': {
        'name': 'DEVUAN',
        'host': 'http://auto.mirror.devuan.org',
        'dists': 'devuan/dists',
        'pool': 'devuan/pool',
        'aliases': False,
        'skipmissing': False,
        'priority': 0,
    },
    'debian-sec': {
        'name': 'DEBIAN-SECURITY',
        'host': 'http://security.debian.org',
        'dists': 'dists',
        'pool': 'pool',
        'aliases': True,
        'skipmissing': True,
        'priority': 1,
    },
    'debian': {
        'name': 'DEBIAN',
        #'host': 'httpredir.debian.org',
        'host': 'http://ftp.debian.org',
        'dists': 'debian/dists',
        'pool': 'debian/pool',
        'aliases': True,
        'skipmissing': False,
        'priority': 2,
    }
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
        'ascii-security': 'testing/updates',
        'jessie-security': 'jessie/updates',
    },
    'DEBIAN': {
        'ascii': 'testing',
        'ascii-backports': 'testing-backports',
        'ascii-proposed-updates': 'testing-proposed-updates',
        'ascii-updates': 'testing-updates',
    }
}

categories = ['main', 'contrib', 'non-free']

mainrepofiles = [
    'InRelease',
    'Release',
    'Release.gpg'
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
    'Origin',
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
